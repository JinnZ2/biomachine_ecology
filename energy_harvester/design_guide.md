# Energy Harvester Module

**Glyph:** `⚡🌀`
**Module:** `energy_harvester`

## Overview

The energy harvester module captures ambient energy from wind, thermal gradients, and mechanical vibration to power BioMachine sensor nodes and LoRa radios. All harvesters are built from scrap and salvaged components.

## Harvester Types

### Wind Ribbon Harvester

**Glyph:** `🌬️⚡`

A flexible strip of piezoelectric material (salvaged buzzer elements) mounted on a fluttering ribbon. Wind causes the ribbon to oscillate, generating small AC voltages rectified and stored in a capacitor bank.

| Parameter | Value |
|-----------|-------|
| Ribbon length | 300-600 mm |
| Ribbon material | Mylar / PETG strip |
| Piezo element | Salvaged buzzer disc, 27mm |
| Output voltage | 2-8V AC (rectified to 3.3V DC) |
| Power output | 0.5-5 mW (depends on wind speed) |
| Min wind speed | 2 m/s |

**Construction:**
1. Mount piezo disc at the base of a flexible strip clamped to a post
2. Ribbon flutters in wind, flexing the piezo element
3. Bridge rectifier (4x 1N4148 diodes) converts AC to DC
4. 1000uF capacitor smooths output
5. LDO regulator (MCP1700) steps down to 3.3V

### Thermoelectric (Peltier) Scavenger

**Glyph:** `🔥⚡`

Salvaged Peltier modules (from CPU coolers or portable fridges) used in reverse as thermoelectric generators (TEG). Placed between a heat source (sun-heated metal, compost, warm pipe) and a heat sink (soil, shade, water).

| Parameter | Value |
|-----------|-------|
| Module size | 40x40mm TEC1-12706 or similar |
| Temperature delta needed | > 10 C |
| Output voltage | 0.5-2V per module |
| Power output | 1-20 mW per module |
| Boost converter | MT3608 module to 3.3V |

**Construction:**
1. Clean salvaged Peltier module, test with multimeter for continuity
2. Mount hot side on dark metal plate (sun-heated) or compost pile surface
3. Mount cold side on aluminum fin heat sink buried in soil
4. Connect to MT3608 boost converter, set output to 3.3V
5. Add 470uF capacitor on output

### Vibration Harvester

**Glyph:** `📳⚡`

Captures mechanical vibration from machinery, footfalls, or wind-induced structure resonance using a cantilever beam with a piezo element.

| Parameter | Value |
|-----------|-------|
| Cantilever material | Spring steel strip, 80mm x 10mm |
| Tip mass | 5-10g (bolt + nuts) |
| Piezo element | PZT disc bonded to cantilever root |
| Resonant frequency | 10-50 Hz (adjustable via tip mass) |
| Power output | 0.1-2 mW |

**Construction:**
1. Clamp spring steel strip at one end to rigid mount
2. Bond piezo disc near the clamped root with epoxy
3. Add adjustable tip mass (threaded bolt allows tuning)
4. Rectify and smooth output as with wind ribbon

## Power Management

All harvesters feed into a shared power bus with the following architecture:

```
[Wind Ribbon] --+--> [Schottky OR] --> [SuperCap 10F] --> [LDO 3.3V] --> Node
[Peltier TEG] --+                          |
[Vibration]   --+                     [Undervoltage lockout]
```

- **Schottky OR** — Prevents backfeed between harvesters (BAT54S)
- **SuperCap** — 10F/5.5V supercapacitor for energy buffering
- **Undervoltage lockout** — Node enters deep sleep below 2.8V, wakes above 3.0V

## Integration with LoRa Nodes

The harvester connects to the sensor node power input. The node's firmware monitors `battery_v` in telemetry and adjusts transmit interval to conserve energy when supply is low:

| Battery Voltage | Transmit Interval | Power Mode |
|----------------|-------------------|------------|
| > 3.5V | 60s | Normal |
| 3.2-3.5V | 300s | Power save |
| 2.8-3.2V | 900s | Low power |
| < 2.8V | — | Deep sleep |
