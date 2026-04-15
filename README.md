# Creativity Engine

> By [MEOK AI Labs](https://meok.ai) — MEOK AI Labs — Creativity engine. Bisociation (Koestler), novelty scoring, quality-diversity archive, conceptual exploration.

Creativity Engine MCP — MEOK AI Labs. Bisociation, novelty scoring, QD archive, exploration.

## Installation

```bash
pip install creativity-engine-mcp
```

## Usage

```bash
# Run standalone
python server.py

# Or via MCP
mcp install creativity-engine-mcp
```

## Tools

### `find_bisociations`
Find creative bisociations between two concepts (Koestler's theory). Discovers hidden connections across domains.

**Parameters:**
- `concept_a` (str)
- `concept_b` (str)
- `depth` (int)

### `assess_creativity`
Score an idea across 5 creativity dimensions: novelty, utility, surprise, elegance, feasibility.

**Parameters:**
- `idea` (str)

### `compute_novelty`
Compute novelty score by comparing against known solutions in the QD archive.

**Parameters:**
- `description` (str)
- `domain` (str)

### `suggest_exploration`
Suggest unexplored conceptual territories for creative exploration.

**Parameters:**
- `current_domain` (str)
- `goal` (str)

### `get_qd_archive_stats`
Get Quality-Diversity archive statistics.


## Authentication

Free tier: 15 calls/day. Upgrade at [meok.ai/pricing](https://meok.ai/pricing) for unlimited access.

## Links

- **Website**: [meok.ai](https://meok.ai)
- **GitHub**: [CSOAI-ORG/creativity-engine-mcp](https://github.com/CSOAI-ORG/creativity-engine-mcp)
- **PyPI**: [pypi.org/project/creativity-engine-mcp](https://pypi.org/project/creativity-engine-mcp/)

## License

MIT — MEOK AI Labs
