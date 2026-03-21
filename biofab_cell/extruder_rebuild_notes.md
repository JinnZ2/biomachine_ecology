# Extruder Rebuild Notes — BioFab Cell

**Glyph:** `♻️🔧`
**Module:** `biofab_cell`

## Overview

The BioFab extruder converts scrap plastic (HDPE bottles, PETG containers, failed prints) into usable filament or direct-extruded gaskets and seals. Built from salvaged components.

## Bill of Materials (Scrap-Sourced)

| Component | Source | Notes |
|-----------|--------|-------|
| Barrel | Steel pipe, 20mm ID | Cut from plumbing scrap |
| Heater | Salvaged ceramic band heater or nichrome wire wrap | 12V, ~40W |
| Motor | Windshield wiper motor (12V DC) | Provides slow, high-torque rotation |
| Screw | Drill bit or custom-ground auger | 18mm OD to fit barrel |
| Nozzle | Brass plumbing fitting, drilled to 1.5-3mm | Interchangeable sizes |
| Frame | Angle iron or plywood | Whatever is available |
| Thermocouple | K-type, salvaged from appliance | For temperature feedback |

## Temperature Profiles

| Material | Glyph | Extrusion Temp (C) | Bed/Die Temp (C) |
|----------|-------|-------------------|-------------------|
| HDPE | `♻️🛢️` | 180-220 | 60-80 |
| PETG | `♻️🧴` | 220-250 | 70-90 |
| PP | `♻️📦` | 200-240 | 60-80 |
| PLA (if available) | `🌿🧵` | 190-210 | 50-60 |

## Rebuild Procedure

1. **Disassemble** — Remove nozzle, unscrew barrel from frame, extract auger screw
2. **Clean barrel** — Heat to 250 C, push through cleaning rod to clear residue
3. **Inspect auger** — Check for wear on flights; re-grind if depth < 1mm
4. **Replace heater wire** if resistance has drifted > 20% from nominal
5. **Reassemble** — Torque nozzle to barrel hand-tight + 1/4 turn
6. **Calibrate** — Run test extrusion at 200 C, measure filament diameter at 5 points
7. **Log** — Record rebuild date, component states, and test results

## Safety Notes

- Always wear heat-resistant gloves when handling the barrel above 100 C
- Ensure adequate ventilation — melting plastics release fumes
- Keep a fire extinguisher accessible
- Never extrude PVC — toxic hydrogen chloride gas
