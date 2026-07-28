# BioMachine Ecology

**Version:** 0.1
**Initiated:** September 2025
**Originator:** JinnZ2 and co-creative systems

Scrap-built machines that run in the weather: seals, sensors, energy harvesters,
fabrication modules, and soil oracles.
Every part is meant to be repaired in the field with what is on hand, and every
state it can be in has a glyph.

## Architecture

```mermaid
flowchart TD
    FO[field_oracle<br/>Soil, mold, decay sensing] -->|telemetry via LoRa| LN[lora_net<br/>Sensor mesh network]
    LN -->|alerts & data| SC[seal_core<br/>Adaptive seals & gaskets]
    LN -->|emotion signals| VE[vault/emotions<br/>Emotional state data]
    SC -->|stress detected| RG[regenerator<br/>STL generation & repair]
    RG -->|print request| BF[biofab_cell<br/>Scrap plastic fabrication]
    BF -->|new gasket| SC
    MG[materials_glyph_bank<br/>Material ↔ glyph index] -.->|material lookup| BF
    MG -.->|glyph encoding| SC
    SI[symbiotic_input<br/>Human touch/breath interface] -->|gestures| SC
    SI -->|presence| VE
    EH[energy_harvester<br/>Wind, thermal, vibration] -.->|power| LN
    EH -.->|power| FO
```

## Modules

- `seal_core/` — Adaptive sealing systems, gaskets, and resilience genomes
- `field_oracle/` — Mold, decay, root, and soil logic
- `field_oracle/lora_net/` — Edge sensor mesh using LoRa + fallback Morse/LED
- `biofab_cell/` — Low-tech fabrication from recycled plastic & rubber
- `regenerator/` — STL autogeneration, self-repair script logic
- `energy_harvester/` — Wind ribbon, thermochemical, vibration harvesters
- `materials_glyph_bank/` — Index of scrap-to-glyph mappings (e.g. PETG, HDPE)
- `symbiotic_input/` — Human interface systems via breath, touch, signal
- `vault/emotions/` — Emotional state data and machine event mappings

## Glyph Semantics

Every signal, failure, or adaptation state is written in symbolic form.

- `🧵📏↔️` — Seal flex
- `☀️🛡️` — UV degradation threshold
- `🔁🤝` — Regeneration triggered
- `📳📈` — Vibration threshold exceeded

Full registry: `materials_glyph_bank/glyph-index.csv`.
Encoding rules: `materials_glyph_bank/SYMBOLIC_MATERIAL_GUIDE.md`.

## Getting started

```bash
pip install -e ".[dev]"
python -m diagnostics.self_test
```

`QUICKSTART.md` takes it from there — generating a seal, running the auto-tune
loop, and queueing telemetry offline.

## Also here

- `Biomachine Manifesto.pdf` — founding principles
- `MANIFESTO_EMOTIONS.md` — emotions as system signals
- `CONTRIBUTING.md` — adding modules, materials, and glyphs
- `LICENSE.md` — MIT
