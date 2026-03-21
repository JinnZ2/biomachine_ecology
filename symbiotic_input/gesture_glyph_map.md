# Gesture-to-Glyph Map — Symbiotic Input

**Glyph:** `🤚🔣`
**Module:** `symbiotic_input`

## Overview

Maps physical human gestures to system glyphs and actions. The BioMachine reads gestures through capacitive touch, pressure pads, and proximity sensors, translating them into the glyph language.

## Gesture Registry

| Gesture | Glyph | Sensor | Action | Response |
|---------|-------|--------|--------|----------|
| Single tap | `👆` | Capacitive | Status query | LED pattern: current state |
| Double tap | `👆👆` | Capacitive | Trigger regeneration | Blink confirm + regen |
| Long press (2-5s) | `🤚⏳` | Pressure pad | Diagnostic mode | Slow pulse + telemetry dump |
| Breath proximity | `🌬️` | Thermistor | Presence acknowledge | Warm LED glow |
| Palm cover (>3s) | `🤚🌑` | Light sensor | Sleep/low-power mode | Fade to dark |
| Rapid triple tap | `👆👆👆` | Capacitive | Emergency alert | Red flash + LoRa alert |
| Slide left-right | `👉👈` | Capacitive array | Cycle display mode | Next info page on LED |
| Sustained pressure | `🤚💪` | Pressure pad | Force calibration | Haptic feedback pulse |

## Feedback Channels

| Channel | Glyph | Hardware | Use |
|---------|-------|----------|-----|
| LED strip | `💡🔣` | WS2812B x4 | Visual status, alerts, acknowledgment |
| Haptic motor | `📳🤚` | ERM vibration motor | Touch confirmation, warnings |
| Piezo buzzer | `🔊🔣` | Piezo disc | Audio alerts, Morse fallback |

## Design Principles

- Gestures must be **unambiguous** — no two gestures should require the same motion
- Response latency must be **< 200ms** for tap gestures to feel responsive
- All gestures must be **performable with one hand** (field conditions)
- Feedback must use **at least two channels** (e.g., LED + haptic) for accessibility
