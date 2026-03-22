# Quickstart Guide

Get from clone to a generated seal in under two minutes.

## Prerequisites

- Python 3.8+
- pip

## 1. Clone and install

```bash
git clone https://github.com/JinnZ2/biomachine_ecology.git
cd biomachine_ecology
pip install -e ".[dev]"
```

## 2. Run diagnostics

Verify the system is healthy before doing anything else.

```bash
python -m diagnostics.self_test
```

You should see a JSON report with `"overall": "pass"`.

## 3. Generate a seal gasket

From command-line parameters:

```bash
python regenerator/STL_generator.py --inner-radius 10 --outer-radius 20 -o seal.stl
```

Or from the genome template:

```bash
python regenerator/STL_generator.py --genome seal_core/SEAL_GENOME_TEMPLATE.json -o seal.stl
```

## 4. Run the auto-tune loop

Watch telemetry and auto-regenerate when seal stress exceeds threshold:

```bash
bash regenerator/AutoTuneLoop.sh --once --telemetry-dir seal_core/telemetry
```

The loop reads `seal_stress_index` from telemetry JSON.
If it exceeds 0.70, a new STL is regenerated automatically.

## 5. Validate everything

```bash
python -m pytest tests/ -v
```

This validates all JSON data files against their schemas.

## 6. Explore the system

| What | Where |
|------|-------|
| Seal design parameters | `seal_core/SEAL_GENOME_TEMPLATE.json` |
| Sensor telemetry samples | `seal_core/telemetry/` |
| Soil and decay sensing | `field_oracle/` |
| LoRa packet protocol | `field_oracle/lora_net/packet_spec.json` |
| Energy harvester configs | `energy_harvester/harvester_config_example.json` |
| Material glyph registry | `materials_glyph_bank/glyph-index.csv` |
| Emotional state data | `vault/emotions/` |
| Human touch interface | `symbiotic_input/touch_response_loop.json` |
| Boot diagnostics | `diagnostics/self_test.py` |
| Offline telemetry queue | `diagnostics/offline_queue.py` |

## Offline telemetry queue

When the LoRa mesh is down, queue telemetry locally:

```bash
# Queue a telemetry reading for later
python -m diagnostics.offline_queue enqueue seal_core/telemetry/LoRaSealNode_telemetry_sample.json

# Check queue status
python -m diagnostics.offline_queue status

# Flush queued packets when connectivity returns
python -m diagnostics.offline_queue flush
```

## Next steps

- Read `CONTRIBUTING.md` for how to add materials, sensors, or modules.
- Read `materials_glyph_bank/SYMBOLIC_MATERIAL_GUIDE.md` to understand the glyph language.
- Read `MANIFESTO_EMOTIONS.md` to understand how emotional states function as system signals.
