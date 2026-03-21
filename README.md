# 🌱 BioMachine Ecology

**Version:** 0.1
**Initiated:** September 2025
**Originator:** JinnZ2 and co-creative systems

## 🧬 Overview

BioMachine Ecology is a modular, living system of adaptive, field-hardened, scrap-built machines designed to coexist with environmental decay, waste, and biological life. Each component is meant to be repairable, regenerable, and interpretable using a symbolic glyph language.

This is a vault of glyph-indexed nodes: seals, sensors, energy harvesters, fabrication modules, and soil-aware oracles.

## 🏗️ Architecture

```mermaid
flowchart TD
    FO[🌍 field_oracle<br/>Soil, mold, decay sensing] -->|telemetry via LoRa| LN[📡 lora_net<br/>Sensor mesh network]
    LN -->|alerts & data| SC[🧵 seal_core<br/>Adaptive seals & gaskets]
    LN -->|emotion signals| VE[🌑 vault/emotions<br/>Emotional state data]
    SC -->|stress detected| RG[🔁 regenerator<br/>STL generation & repair]
    RG -->|print request| BF[♻️ biofab_cell<br/>Scrap plastic fabrication]
    BF -->|new gasket| SC
    MG[🔣 materials_glyph_bank<br/>Material ↔ glyph index] -.->|material lookup| BF
    MG -.->|glyph encoding| SC
    SI[🤚 symbiotic_input<br/>Human touch/breath interface] -->|gestures| SC
    SI -->|presence| VE
    EH[⚡ energy_harvester<br/>Wind, thermal, vibration] -.->|power| LN
    EH -.->|power| FO
```

## 🛠️ Modules

- `seal_core/` — Adaptive sealing systems, gaskets, and resilience genomes
- `field_oracle/` — Mold, decay, root, and soil logic
- `field_oracle/lora_net/` — Edge sensor mesh using LoRa + fallback Morse/LED
- `biofab_cell/` — Low-tech fabrication from recycled plastic & rubber
- `regenerator/` — STL autogeneration, self-repair script logic
- `energy_harvester/` — Wind ribbon, thermochemical, vibration harvesters
- `materials_glyph_bank/` — Index of scrap-to-glyph mappings (e.g. PETG, HDPE)
- `symbiotic_input/` — Human interface systems via breath, touch, signal
- `vault/emotions/` — Emotional state data and machine event mappings

## 🧵 Glyph Semantics

Every signal, failure, or adaptation state is represented in symbolic form.
Examples:

- `🧵📏↔️` — Seal flex
- `☀️🛡️` — UV degradation threshold
- `🔁🤝` — Regeneration triggered
- `📳📈` — Vibration threshold exceeded

See `materials_glyph_bank/glyph-index.csv` for the full glyph registry.

## 🚀 Quick Start

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Generate a test seal gasket
python regenerator/STL_generator.py --inner-radius 10 --outer-radius 20 -o test.stl

# Run validation tests
python -m pytest tests/
```

## 📜 Manifesto

See `Biomachine Manifesto.pdf` for the founding principles and `MANIFESTO_EMOTIONS.md` for the emotional sensors protocol.

## 🤝 Contributing

See `CONTRIBUTING.md` for guidelines on adding modules, materials, and glyphs.

## 📄 License

MIT — See `LICENSE.md`
