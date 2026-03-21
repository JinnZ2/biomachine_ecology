# Rot & Residue Sensor — Field Oracle Module

**Glyph:** `🍂🔬`
**Module:** `field_oracle`

## Purpose

Detects organic decay, mold presence, and residue accumulation in the field environment. Feeds data into the soil map and triggers alerts when decay indices exceed thresholds.

## Sensor Inputs

| Sensor | Type | Glyph | Range |
|--------|------|-------|-------|
| VOC gas sensor | MQ-135 or equivalent | `💨🔬` | 10-1000 ppm |
| Humidity probe | Capacitive | `💧📏` | 0-100% RH |
| Temperature | Thermistor NTC 10K | `🌡️` | -20 to 80 C |
| Light/UV | Photodiode + UV sensor | `☀️🔬` | 0-15 UV index |
| Conductivity | Two-electrode probe | `⚡📏` | 0-20 mS/cm |

## Decay Index Calculation

The decay index (0.0 to 1.0) is computed from weighted sensor inputs:

```
decay_index = (0.3 * voc_normalized)
            + (0.25 * humidity_factor)
            + (0.2 * temperature_factor)
            + (0.15 * conductivity_factor)
            + (0.1 * uv_inverse_factor)
```

Where each factor is normalized to [0, 1] based on the sensor range.

## Thresholds & Alerts

| Level | Decay Index | Glyph | Action |
|-------|------------|-------|--------|
| Normal | 0.0 - 0.3 | `🟢🍂` | Log only |
| Elevated | 0.3 - 0.6 | `🟡🍂` | Increase monitoring frequency |
| High | 0.6 - 0.8 | `🟠🍂` | Alert via LoRa, flag for inspection |
| Critical | 0.8 - 1.0 | `🔴🍂` | Immediate alert, trigger seal check |

## Mold Detection

Mold presence is flagged when:
- VOC > 200 ppm **AND** humidity > 70% **AND** temperature 20-35 C

Mold glyph: `🦠🍂`

## Wiring

Connect to the LoRa node as specified in `lora_net/node_wiring.svg`. Power from the shared 3.3V rail. Data lines to the I2C bus (SDA/SCL) or analog inputs as appropriate for each sensor type.
