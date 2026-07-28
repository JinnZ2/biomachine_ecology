# Contributing to BioMachine Ecology

## Ethics First

Read `CO_CREATION.md` before contributing. This project is co-created freely — no proprietary claims, no gatekeeping.

## Repository Structure

Each module is self-contained in its own directory. Keep changes scoped to the relevant module unless you're adding cross-module infrastructure.

## How to Contribute

### Adding a New Material

1. Add an entry to `materials_glyph_bank/glyph-index.csv`
2. Update `materials_glyph_bank/SYMBOLIC_MATERIAL_GUIDE.md` with the new entry
3. If usable in seals, add it as a valid material in `seal_core/SEAL_GENOME_TEMPLATE.json`

### Adding a New Glyph

Follow the two-part pattern: **source indicator** + **form/property indicator**. Register it in `glyph-index.csv`. See `SYMBOLIC_MATERIAL_GUIDE.md` for the full encoding rules.

### Adding a New Sensor or Module

1. Create a directory under the appropriate parent module
2. Add a markdown file documenting the sensor/module purpose, inputs, outputs, and glyphs
3. Add any JSON configuration with a `$schema` reference
4. Update `README.md` with the new module entry
5. Register any new glyphs in `glyph-index.csv`

### Modifying JSON Schemas

- Keep backward compatibility — add new fields as optional
- Always include a `$schema` reference in data files
- Run `python -m pytest tests/` to validate schemas if you have the dev dependencies installed

## Development Setup

See `QUICKSTART.md`.

## Branching

- Branch from `main`
- Use descriptive branch names: `add-pressure-sensor`, `fix-genome-schema`, etc.
- Keep commits focused — one logical change per commit

## File Formats

| Format | Use for |
|--------|---------|
| Markdown | Documentation |
| JSON | Configuration, schemas, telemetry data |
| CSV | Tabular indexes (glyphs, materials) |
| Python | Generative/parametric code |
| Bash | Automation scripts |
| SVG | Diagrams |

## Code Style

- Python: Follow PEP 8, use type hints where helpful
- Bash: Use `set -euo pipefail`, quote variables
- JSON: 4-space indentation, include `$schema` references
- Markdown: One sentence per line for readable diffs

## What Not to Do

- Don't add PVC processing — toxic fumes (see `biofab_cell/extruder_rebuild_notes.md`)
- Don't add proprietary dependencies
- Don't remove or alter existing glyph definitions without discussion
- Don't commit generated STL files (add them to `.gitignore`)
