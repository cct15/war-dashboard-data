# Futuristic Risk Intelligence — Data Feed

Geopolitical conflict risk data for AI agents. Updated daily.

## Data Files

| File | Description |
|------|-------------|
| `conflicts.json` | Risk probabilities for 6 major geopolitical conflicts (escalation, ceasefire, regime change, etc.) |
| `political_events.json` | High-impact political, economic, and natural disaster events with probability estimates |
| `maritime.json` | Vessel counts in critical maritime chokepoints (Hormuz, Taiwan Strait, etc.) |

## Usage

### Raw URL (REST API)
```
https://raw.githubusercontent.com/cct15/war-dashboard-data/main/conflicts.json
https://raw.githubusercontent.com/cct15/war-dashboard-data/main/political_events.json
https://raw.githubusercontent.com/cct15/war-dashboard-data/main/maritime.json
```

### MCP Server (for Claude, GPT, and other LLM agents)

See [war_dashboard/mcp_server](https://github.com/cct15/war-dashboard-data) for the MCP server that wraps this data.

## Data Schema

### conflicts.json

Each conflict includes:
- **probability_30d / 7d / 1d**: P(event occurs within time horizon)
- **risk_events**: Breakdown by event type (escalation, ceasefire, etc.)
- **direction**: `risk_increase` (higher probability = more danger) or `risk_decrease` (higher probability = less danger)
- **change_vs_yesterday / change_vs_7d_ago**: Probability deltas

### Coverage

6 conflict regions: Russia-Ukraine, Iran-Israel/US, Israel-Palestine, China-Taiwan, India-Pakistan, US-Latin America.

5 event types: escalation, ceasefire, ceasefire_cancel, regime_change, diplomatic.

## Source

Probabilities derived from prediction market data and statistical modeling. Updated daily by [Futuristic Risk Intelligence](https://github.com/cct15).

## License

Data is free for non-commercial use. Contact for commercial licensing.
