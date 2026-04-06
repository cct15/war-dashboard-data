# Futuristic Risk Intelligence — MCP Server & Data Feed

<!-- mcp-name: io.github.cct15/war-dashboard-data -->

Geopolitical conflict risk data for AI agents via [Model Context Protocol (MCP)](https://modelcontextprotocol.io/). Updated daily.

[![PyPI](https://img.shields.io/pypi/v/war-dashboard-data)](https://pypi.org/project/war-dashboard-data/)
[![war-dashboard-data MCP server](https://glama.ai/mcp/servers/cct15/war-dashboard-data/badges/card.svg)](https://glama.ai/mcp/servers/cct15/war-dashboard-data)

## MCP Tools

| Tool | Description |
|------|-------------|
| `get_conflict_risks` | Risk probabilities for 6 major geopolitical conflicts (escalation, ceasefire, regime change) with 1d/7d/30d horizons |
| `get_political_events` | High-impact political, economic, and natural disaster events with probability estimates |
| `get_maritime_traffic` | ⚠️ **Suspended** — AIS snapshot data does not meet reliability standards. Returns `status: unavailable`. |

## Install

```bash
pip install war-dashboard-data
```

## Quick Start

### Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "futuristic-risk": {
      "command": "war-dashboard-data"
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

⚠️ **Suspended**: Maritime chokepoint monitoring is temporarily unavailable. Free AIS data (45-second WebSocket snapshots) produces sporadic zero-vessel readings in busy straits, which could mislead agents into inferring blockades. Returns `{"status": "unavailable", "zones": []}`. Maritime data is still collected internally for the daily HTML report's narrative context.

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

## Website & Research

**[futuristicrisks.com](https://futuristicrisks.com)** — Live risk dashboard, cascade impact analysis, daily verified intelligence, and API documentation.

**Research articles**:
- [2026年全球地缘政治风险全景分析](https://futuristicrisks.com/blog/geopolitical-risk-2026.html)
- [伊朗局势对油价和供应链的影响分析](https://futuristicrisks.com/blog/iran-oil-impact.html)
- [台海冲突对全球半导体供应链的风险评估](https://futuristicrisks.com/blog/taiwan-semiconductor-risk.html)

Built by [Futuristic Risk Intelligence](https://futuristicrisks.com).
