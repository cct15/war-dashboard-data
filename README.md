# Futuristic Risk Intelligence — MCP Server & Data Feed

Geopolitical conflict risk data for AI agents via [Model Context Protocol (MCP)](https://modelcontextprotocol.io/). Updated daily.

## MCP Tools

| Tool | Description |
|------|-------------|
| `get_conflict_risks` | Risk probabilities for 6 major geopolitical conflicts (escalation, ceasefire, regime change) with 1d/7d/30d horizons |
| `get_political_events` | High-impact political, economic, and natural disaster events with probability estimates |
| `get_maritime_traffic` | Vessel counts in critical maritime chokepoints (Strait of Hormuz, Taiwan Strait, etc.) |

## Quick Start

### Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "futuristic-risk": {
      "command": "python3",
      "args": ["path/to/mcp_server/server.py"]
    }
  }
}
```

Then ask Claude: *"What's the current escalation risk for Russia-Ukraine?"*

### Direct API (REST)

```bash
curl https://raw.githubusercontent.com/cct15/war-dashboard-data/main/conflicts.json
```

## Coverage

**6 conflict regions**: Russia-Ukraine, Iran-Israel/US, Israel-Palestine, China-Taiwan, India-Pakistan, US-Latin America

**5 event types** with clear risk direction:

| Event Type | Meaning | Direction |
|-----------|---------|-----------|
| `escalation` | Military escalation (strikes, invasion, nuclear test) | risk_increase |
| `ceasefire` | Ceasefire or peace agreement reached | risk_decrease |
| `ceasefire_cancel` | Existing ceasefire breaks down | risk_increase |
| `regime_change` | Government falls or changes | risk_increase |
| `diplomatic` | Major diplomatic event (nuclear deal, treaty) | neutral |

## Data Schema

### conflicts.json

Each conflict includes:
- **probability_30d / 7d / 1d**: P(event occurs within time horizon)
- **risk_events**: Breakdown by event type
- **direction**: `risk_increase` (higher probability = more danger) or `risk_decrease` (higher probability = less danger)
- **change_vs_yesterday / change_vs_7d_ago**: Probability deltas
- **risk_level**: `high` / `medium` / `low`
- **anomaly_detected**: Whether probability diverges from news intensity

### maritime.json

Vessel counts in 6 critical chokepoints, broken down by type (tanker, cargo, military, other). Snapshot-based from AIS data.

### political_events.json

High-impact events with probability, deadline, category, and data confidence level.

## Use Cases

- **Trading agents**: Adjust crypto/commodity positions based on geopolitical risk changes
- **Risk management**: Monitor conflict escalation probabilities for portfolio hedging
- **DeFi protocols**: Dynamic collateral ratios based on geopolitical risk
- **Research agents**: Track probability trends across 6 conflict regions
- **News agents**: Get structured risk data instead of parsing headlines

## Technical Details

- **Zero dependencies**: MCP server uses only Python stdlib (works with Python 3.9+)
- **Data source**: Proprietary multi-source modeling
- **Update frequency**: Daily
- **Latency**: Public data has ~24h delay

## License

Data is free for non-commercial use. Contact for commercial licensing.

Built by [Futuristic Risk Intelligence](https://github.com/cct15).
