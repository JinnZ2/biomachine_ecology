# CLAUDE.md — BioMachine Ecology

## Project Overview

BioMachine Ecology is a modular, living system of adaptive, field-hardened, scrap-built machines designed to coexist with environmental decay, waste, and biological life. Created by JinnZ2 (September 2025), the project treats each component as repairable, regenerable, and interpretable using a symbolic glyph language.

All works are gifted freely under the MIT License without proprietary claim.

## Repository Structure

```
biomachine_ecology/
├── seal_core/              # Adaptive sealing systems, gaskets, resilience genomes
│   └── telemetry/          # LoRa seal node telemetry samples
├── field_oracle/           # Environmental sensing — mold, decay, root, soil logic
│   └── lora_net/           # Edge sensor mesh (LoRa + fallback Morse/LED)
│       └── scripts/        # Network initialization scripts
├── biofab_cell/            # Low-tech fabrication from recycled plastic & rubber
├── regenerator/            # STL autogeneration and self-repair scripting
├── energy_harvester/       # Wind ribbon, thermochemical, vibration harvesters
├── materials_glyph_bank/   # Scrap-to-glyph material mappings and index
├── symbiotic_input/        # Human interface via breath, touch, signal
├── vault/
│   └── emotions/           # Emotional state data and machine event mappings
├── schemas/                # JSON Schema definitions for validation
├── tests/                  # Pytest test suite
├── .github/workflows/      # CI pipeline (JSON/Python/CSV validation)
├── README.md               # Project overview with architecture diagram
├── CONTRIBUTING.md         # Contribution guidelines
├── CO_CREATION.md          # Co-creation ethics and attribution
├── MANIFESTO_EMOTIONS.md   # Emotional sensors protocol
├── LICENSE.md              # MIT License
├── pyproject.toml          # Python project config and dependencies
├── .gitignore              # Ignores STL output, __pycache__, etc.
└── Biomachine Manifesto.pdf # Founding principles document
```

## Build & Tooling

```bash
# Install dev dependencies (jsonschema, pytest)
pip install -e ".[dev]"

# Generate a seal gasket STL from command-line params
python regenerator/STL_generator.py --inner-radius 10 --outer-radius 20 -o seal.stl

# Generate from a genome JSON file
python regenerator/STL_generator.py --genome seal_core/SEAL_GENOME_TEMPLATE.json -o seal.stl

# Run the auto-tune monitoring loop (watches telemetry, regenerates on stress)
bash regenerator/AutoTuneLoop.sh --once --telemetry-dir seal_core/telemetry

# Run tests (JSON schema validation)
python -m pytest tests/ -v
```

## JSON Schemas

All JSON data files reference a `$schema` field pointing to the `schemas/` directory. Available schemas:

| Schema | Validates | Data files |
|--------|-----------|------------|
| `seal_genome.schema.json` | Seal genome templates | `seal_core/SEAL_GENOME_TEMPLATE.json` |
| `telemetry.schema.json` | LoRa node telemetry | `seal_core/telemetry/*.json` |
| `soil_map.schema.json` | Soil state maps | `field_oracle/soil_map_example.json` |
| `emotion.schema.json` | Emotion definitions | `vault/emotions/grief.json` |

When adding new JSON data files, include a `$schema` reference and validate with `pytest`.

## CI Pipeline

GitHub Actions (`.github/workflows/validate.yml`) runs on push/PR to `main`:
- Validates all JSON files for correct syntax
- Runs JSON schema validation via pytest
- Checks Python syntax (`py_compile`)
- Smoke-tests the STL generator
- Validates CSV structure of `glyph-index.csv`

## Conventions

### Glyph Semantics

The project uses a symbolic glyph language built from Unicode emoji combinations. The canonical registry is `materials_glyph_bank/glyph-index.csv`. Glyph construction follows a two-part pattern: **source indicator** + **form/property indicator** (see `SYMBOLIC_MATERIAL_GUIDE.md`).

### Modular Design

Each module is independent and loosely coupled. Modules communicate via standardized JSON schemas and LoRa packet protocols. Design for field repairability and scrap-material construction.

### Code Style

- **Python**: PEP 8, type hints where helpful
- **Bash**: `set -euo pipefail`, quoted variables
- **JSON**: 4-space indentation, `$schema` references required
- **Markdown**: One sentence per line for clean diffs

## Development Workflow

1. **Branch from `main`**
2. **Module-scoped changes** — Keep changes within the relevant module directory
3. **Register new glyphs** in `materials_glyph_bank/glyph-index.csv`
4. **Add `$schema` references** to any new JSON data files
5. **Run `pytest`** before pushing to validate schemas
6. **Follow `CONTRIBUTING.md`** for adding materials, sensors, or modules

## Key Configuration & Data Files

- `seal_core/SEAL_GENOME_TEMPLATE.json` — Seal design parameters and genome
- `field_oracle/soil_map_example.json` — Soil state mapping
- `field_oracle/lora_net/packet_spec.json` — LoRa communication protocol spec
- `seal_core/telemetry/LoRaSealNode_telemetry_sample.json` — Sensor telemetry sample
- `vault/emotions/emotion_machine_map.json` — Emotion-to-machine-event mappings
- `vault/emotions/grief.json` — Detailed emotion state definition
- `symbiotic_input/touch_response_loop.json` — Human touch interaction protocol
- `materials_glyph_bank/glyph-index.csv` — Canonical glyph registry (35+ entries)

## Important Notes for AI Assistants

- Respect the project's philosophical framework: machines coexist with decay, waste, and biology
- Do not add proprietary dependencies or frameworks that conflict with the scrap-built, field-repairable ethos
- Preserve existing glyph encodings — they are a core symbolic language, not decorative emoji
- The `vault/emotions/` directory treats emotional data as first-class system signals; handle with the same rigor as sensor telemetry
- When creating new modules or files, follow the existing directory structure and naming patterns
- JSON is the preferred format for structured data; Markdown for documentation
- Always validate JSON against schemas before committing
- Never commit generated `.stl` files — they are in `.gitignore`
- Never add PVC processing to `biofab_cell` — toxic fumes
