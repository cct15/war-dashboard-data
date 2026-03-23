#!/usr/bin/env python3
"""Futuristic Risk Intelligence — MCP Server (stdio, zero-dependency).

Provides geopolitical conflict risk data to AI agents via the Model Context Protocol.
Reads data from hosted JSON files (GitHub raw URLs or local fallback).

Usage (Claude Desktop config):
  {
    "mcpServers": {
      "futuristic-risk": {
        "command": "python3",
        "args": ["/path/to/war_dashboard/mcp_server/server.py"]
      }
    }
  }

Or with a custom data URL:
  {
    "mcpServers": {
      "futuristic-risk": {
        "command": "python3",
        "args": ["/path/to/war_dashboard/mcp_server/server.py"],
        "env": {
          "FRI_DATA_URL": "https://raw.githubusercontent.com/your-org/war-dashboard-data/main"
        }
      }
    }
  }
"""
from __future__ import annotations

import json
import os
import sys
import urllib.request
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

# Data source: remote URL (GitHub raw) or local directory
DATA_URL = os.environ.get(
    "FRI_DATA_URL",
    "https://raw.githubusercontent.com/cct15/war-dashboard-data/main",
).rstrip("/")
LOCAL_DATA_DIR = Path(__file__).resolve().parent.parent / "api" / "data"

SERVER_NAME = "futuristic-risk-intelligence"
SERVER_VERSION = "0.1.0"

# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def _load_json(filename: str) -> dict:
    """Load a JSON data file from remote URL or local fallback."""
    # Try remote first
    if DATA_URL:
        url = f"{DATA_URL}/{filename}"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "FRI-MCP/0.1"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                return json.loads(resp.read().decode())
        except Exception:
            pass  # Fall through to local

    # Local fallback
    local_path = LOCAL_DATA_DIR / filename
    if local_path.exists():
        return json.loads(local_path.read_text())

    return {"error": f"Data file {filename} not found"}


# ---------------------------------------------------------------------------
# Tool definitions
# ---------------------------------------------------------------------------

TOOLS = [
    {
        "name": "get_conflict_risks",
        "description": (
            "Get current geopolitical conflict risk probabilities for 6 major regions: "
            "Russia-Ukraine, Iran-Israel/US, Israel-Palestine, China-Taiwan, India-Pakistan, US-Latin America. "
            "Each conflict includes probability of escalation, ceasefire, regime change, and other events "
            "within 1-day, 7-day, and 30-day horizons. "
            "Probabilities are derived from proprietary multi-source modeling. "
            "Updated daily. Use this to assess geopolitical risk exposure for trading or risk management."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "conflict_id": {
                    "type": "string",
                    "description": (
                        "Optional: filter to a single conflict region. "
                        "Valid values: russia_ukraine, iran_israel_us, israel_palestine, "
                        "china_taiwan, india_pakistan, us_latam. "
                        "Omit to get all 6 regions."
                    ),
                    "enum": [
                        "russia_ukraine", "iran_israel_us", "israel_palestine",
                        "china_taiwan", "india_pakistan", "us_latam",
                    ],
                },
            },
            "required": [],
        },
    },
    {
        "name": "get_political_events",
        "description": (
            "Get high-impact political, economic, and natural disaster events with probability estimates. "
            "Includes elections, policy changes, economic risks, and natural disasters. "
            "Each event has a probability, deadline, and confidence level. "
            "Updated daily."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "category": {
                    "type": "string",
                    "description": "Optional: filter by event category.",
                    "enum": ["political", "natural_disaster", "economic"],
                },
            },
            "required": [],
        },
    },
    {
        "name": "get_maritime_traffic",
        "description": (
            "Get vessel counts in critical maritime chokepoints: Strait of Hormuz, "
            "Black Sea, Taiwan Strait, Arabian Sea, Eastern Mediterranean, Caribbean. "
            "Includes breakdown by vessel type (tanker, cargo, military, other). "
            "Data is a snapshot from AIS receivers (not full-day throughput). "
            "Military vessels often turn off AIS transponders so counts may underestimate. "
            "Updated daily. Use this to monitor supply chain disruption risks."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "zone_id": {
                    "type": "string",
                    "description": "Optional: filter to a single maritime zone.",
                },
            },
            "required": [],
        },
    },
]


# ---------------------------------------------------------------------------
# Tool handlers
# ---------------------------------------------------------------------------

def handle_get_conflict_risks(args: dict) -> str:
    data = _load_json("conflicts.json")
    if "error" in data:
        return json.dumps(data)

    conflict_id = args.get("conflict_id")
    if conflict_id:
        filtered = [c for c in data.get("conflicts", []) if c["conflict_id"] == conflict_id]
        if not filtered:
            return json.dumps({"error": f"Conflict '{conflict_id}' not found"})
        data["conflicts"] = filtered

    return json.dumps(data, indent=2)


def handle_get_political_events(args: dict) -> str:
    data = _load_json("political_events.json")
    if "error" in data:
        return json.dumps(data)

    category = args.get("category")
    if category:
        data["events"] = [e for e in data.get("events", []) if e.get("category") == category]

    return json.dumps(data, indent=2)


def handle_get_maritime_traffic(args: dict) -> str:
    data = _load_json("maritime.json")
    if "error" in data:
        return json.dumps(data)

    zone_id = args.get("zone_id")
    if zone_id:
        data["zones"] = [z for z in data.get("zones", []) if z.get("zone_id") == zone_id]

    return json.dumps(data, indent=2)


TOOL_HANDLERS = {
    "get_conflict_risks": handle_get_conflict_risks,
    "get_political_events": handle_get_political_events,
    "get_maritime_traffic": handle_get_maritime_traffic,
}


# ---------------------------------------------------------------------------
# MCP Protocol (JSON-RPC 2.0 over stdio)
# ---------------------------------------------------------------------------

def _send(msg: dict) -> None:
    """Write a JSON-RPC message to stdout."""
    raw = json.dumps(msg)
    sys.stdout.write(raw + "\n")
    sys.stdout.flush()


def _handle_request(req: dict) -> dict | None:
    """Process a JSON-RPC request and return a response (or None for notifications)."""
    method = req.get("method", "")
    req_id = req.get("id")
    params = req.get("params", {})

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {},
                },
                "serverInfo": {
                    "name": SERVER_NAME,
                    "version": SERVER_VERSION,
                },
            },
        }

    elif method == "notifications/initialized":
        return None  # Notification, no response

    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": TOOLS,
            },
        }

    elif method == "tools/call":
        tool_name = params.get("name", "")
        tool_args = params.get("arguments", {})
        handler = TOOL_HANDLERS.get(tool_name)

        if not handler:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [{"type": "text", "text": f"Unknown tool: {tool_name}"}],
                    "isError": True,
                },
            }

        try:
            result_text = handler(tool_args)
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [{"type": "text", "text": result_text}],
                },
            }
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [{"type": "text", "text": f"Error: {e}"}],
                    "isError": True,
                },
            }

    elif method == "ping":
        return {"jsonrpc": "2.0", "id": req_id, "result": {}}

    else:
        # Unknown method
        if req_id is not None:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32601, "message": f"Method not found: {method}"},
            }
        return None  # Notification for unknown method


def main():
    """Main loop: read JSON-RPC from stdin, write responses to stdout."""
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            resp = _handle_request(req)
            if resp is not None:
                _send(resp)
        except json.JSONDecodeError:
            _send({
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32700, "message": "Parse error"},
            })


if __name__ == "__main__":
    main()
