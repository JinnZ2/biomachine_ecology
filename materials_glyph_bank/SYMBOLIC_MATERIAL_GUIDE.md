# Symbolic Material Guide — Materials Glyph Bank

**Glyph:** `🔣♻️`
**Module:** `materials_glyph_bank`

## Overview

Every material in the BioMachine Ecology is assigned a symbolic glyph for quick identification in the field, in telemetry data, and in regeneration logs. This guide defines the encoding system.

## Glyph Construction Rules

Material glyphs follow a two-part pattern:

1. **Source indicator** — Where the material came from
2. **Form/property indicator** — What it is or how it behaves

Example: `♻️🛢️` = recycled (`♻️`) + container/drum (`🛢️`) = recycled HDPE from containers

## Material Registry

| Material | Glyph | Source | Properties |
|----------|-------|--------|------------|
| HDPE (recycled) | `♻️🛢️` | Bottles, drums, containers | Tough, chemical resistant, easy to melt |
| PETG (recycled) | `♻️🧴` | Bottles, packaging | Clear, impact resistant, moderate temp |
| PP (recycled) | `♻️📦` | Containers, caps | Flexible, fatigue resistant |
| PLA (bio-source) | `🌿🧵` | Corn starch filament | Biodegradable, low temp, brittle |
| Steel (salvaged) | `🔩🏗️` | Structural scrap | Strong, heavy, rust-prone |
| Copper (salvaged) | `🔩⚡` | Wire, motors | Conductive, soft, recyclable |
| Aluminum (salvaged) | `🔩🪶` | Cans, frames | Light, corrosion resistant |
| Rubber (salvaged) | `♻️🫧` | Tires, gaskets, hoses | Elastic, weather resistant |
| Glass fiber | `🪟🧵` | Insulation scrap | Stiff reinforcement |
| Mycelium | `🍄🧱` | Grown from substrate | Biodegradable structural fill |
| Beeswax | `🐝🫗` | Local apiary waste | Sealant, waterproofing |
| Clay | `🟤🏺` | Local soil | Thermal mass, insulation |

## Environmental Resistance Glyphs

These modifiers are appended to material glyphs in telemetry and genome files:

| Condition | Glyph | Meaning |
|-----------|-------|---------|
| UV resistant | `☀️🛡️` | Material withstands prolonged sun exposure |
| UV vulnerable | `☀️⚠️` | Degrades under UV — needs shielding |
| Salt tolerant | `🧂🛡️` | Survives marine/coastal environments |
| Waterproof | `💧🛡️` | Impermeable to water |
| Heat tolerant | `🔥🛡️` | Stable above 100 C |
| Biodegradable | `🌱💀` | Will decompose in soil over time |

## How to Register a New Material

1. Add an entry to `glyph-index.csv` with: glyph, material name, category, source, and key properties
2. Update this guide with the new entry in the appropriate table
3. If the material will be used in seal genomes, add it to `SEAL_GENOME_TEMPLATE.json` as a valid material type
