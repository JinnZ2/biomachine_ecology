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
├── README.md               # Project overview and module listing
├── CO_CREATION.md          # Co-creation ethics and attribution
├── MANIFESTO_EMOTIONS.md   # Emotional sensors protocol
├── LICENSE.md              # MIT License
└── Biomachine Manifesto.pdf # Founding principles document
```

## Language & File Types

| Type | Usage |
|------|-------|
| **Markdown** | Primary documentation format |
| **JSON** | Configuration, data schemas, telemetry, emotional states |
| **Python** | Generative/parametric design (e.g., STL generation) |
| **Bash** | System automation scripts |
| **CSV** | Tabular data (glyph indexing) |
| **SVG** | Wiring and network topology diagrams |
| **PDF** | Design documentation and process guides |

## Key Configuration & Data Files

- `seal_core/SEAL_GENOME_TEMPLATE.json` — Seal design parameters and genome
- `field_oracle/soil_map_example.json` — Soil state mapping schema
- `field_oracle/lora_net/packet_spec.json` — LoRa communication protocol spec
- `seal_core/telemetry/LoRaSealNode_telemetry_sample.json` — Sensor telemetry format
- `vault/emotions/emotion_machine_map.json` — Emotion-to-machine-event mappings
- `vault/emotions/grief.json` — Detailed emotion state definition
- `symbiotic_input/touch_response_loop.json` — Human interaction protocol
- `materials_glyph_bank/glyph-index.csv` — Material glyph index

## Conventions

### Glyph Semantics

The project uses a symbolic glyph language built from Unicode emoji combinations to represent signals, states, and adaptations:

- `🧵📏↔️` — seal flex
- `☀️🛡️` — UV degradation
- `🔁🤝` — regeneration
- Materials, emotions, and machine states all have glyph representations

### Modular Design

Each module (seal_core, field_oracle, etc.) is independent and loosely coupled. Modules communicate via standardized JSON schemas and LoRa packet protocols. Design for field repairability and scrap-material construction.

### Documentation

- Each module contains its own markdown documentation
- JSON files serve as both config and living documentation of schemas
- The `CO_CREATION.md` file governs attribution and ethics

## Build & Tooling

**No formal build system, test suite, or linting configuration exists.** The project is primarily documentation and design schemas at this stage. Key automation stubs:

- `regenerator/AutoTuneLoop.sh` — Auto-tuning automation (placeholder)
- `regenerator/STL_generator.py` — Parametric STL generation (placeholder)
- `field_oracle/lora_net/scripts/` — Network init scripts (placeholder)

## Development Workflow

1. **Branch from `main`** — The primary remote branch is `main`
2. **Module-scoped changes** — Keep changes within the relevant module directory
3. **JSON schema consistency** — When modifying JSON data schemas, ensure backward compatibility with existing telemetry and config files
4. **Glyph integrity** — Preserve the symbolic glyph language; new glyphs should follow the emoji-combination pattern documented in `materials_glyph_bank/SYMBOLIC_MATERIAL_GUIDE.md`
5. **Ethics** — Follow the co-creation principles in `CO_CREATION.md`; emotions and ecological states are treated as transmittable, modular signals

## Project Status

The repository is in early-stage development. Most files are structural placeholders (1 byte stubs) defining the intended architecture. The foundational design — module layout, JSON schemas, glyph language, and documentation — is established but implementation is minimal.

## Important Notes for AI Assistants

- Respect the project's philosophical framework: machines coexist with decay, waste, and biology
- Do not add proprietary dependencies or frameworks that conflict with the scrap-built, field-repairable ethos
- Preserve existing glyph encodings — they are a core symbolic language, not decorative emoji
- The `vault/emotions/` directory treats emotional data as first-class system signals; handle with the same rigor as sensor telemetry
- When creating new modules or files, follow the existing directory structure and naming patterns
- JSON is the preferred format for structured data; Markdown for documentation
