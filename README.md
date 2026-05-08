<div align="center">

# Creativity Engine MCP

**MCP server for creativity engine mcp operations**

[![PyPI](https://img.shields.io/pypi/v/meok-creativity-engine-mcp)](https://pypi.org/project/meok-creativity-engine-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![MEOK AI Labs](https://img.shields.io/badge/MEOK_AI_Labs-MCP_Server-purple)](https://meok.ai)

</div>

## Overview

Creativity Engine MCP provides AI-powered tools via the Model Context Protocol (MCP).

## Tools

| Tool | Description |
|------|-------------|
| `find_bisociations` | Find creative bisociations between two concepts (Koestler's theory). Discovers h |
| `assess_creativity` | Score an idea across 5 creativity dimensions: novelty, utility, surprise, elegan |
| `compute_novelty` | Compute novelty score by comparing against known solutions in the QD archive. |
| `suggest_exploration` | Suggest unexplored conceptual territories for creative exploration. |
| `get_qd_archive_stats` | Get Quality-Diversity archive statistics. |

## Installation

```bash
pip install meok-creativity-engine-mcp
```

## Usage with Claude Desktop

Add to your Claude Desktop MCP config (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "creativity-engine": {
      "command": "python",
      "args": ["-m", "meok_creativity_engine_mcp.server"]
    }
  }
}
```

## Usage with FastMCP

```python
from mcp.server.fastmcp import FastMCP

# This server exposes 5 tool(s) via MCP
# See server.py for full implementation
```

## License

MIT © [MEOK AI Labs](https://meok.ai)
