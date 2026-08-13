#!/usr/bin/env bash
# AutoTuneLoop — Continuous seal parameter tuning for BioMachine Ecology
#
# Monitors telemetry JSON from LoRa seal nodes, detects drift in seal
# performance, and regenerates STL files with adjusted parameters.
#
# Usage: ./AutoTuneLoop.sh [--interval SECONDS] [--telemetry-dir DIR] [--genome FILE]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

# Defaults resolve against the repo, not the current directory, so the loop
# runs the same from anywhere.
INTERVAL=60
TELEMETRY_DIR="$REPO_ROOT/seal_core/telemetry"
GENOME_FILE="$REPO_ROOT/seal_core/SEAL_GENOME_TEMPLATE.json"
OUTPUT_DIR="./output"

usage() {
    echo "Usage: $0 [--interval SECONDS] [--telemetry-dir DIR] [--genome FILE]"
    echo ""
    echo "Options:"
    echo "  --interval      Polling interval in seconds (default: 60)"
    echo "  --telemetry-dir Directory containing telemetry JSON files"
    echo "  --genome        Path to seal genome template JSON"
    echo "  --output-dir    Directory for generated STL files (default: ./output)"
    echo "  --once          Run one iteration and exit"
    exit 1
}

RUN_ONCE=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --interval)    INTERVAL="$2"; shift 2 ;;
        --telemetry-dir) TELEMETRY_DIR="$2"; shift 2 ;;
        --genome)      GENOME_FILE="$2"; shift 2 ;;
        --output-dir)  OUTPUT_DIR="$2"; shift 2 ;;
        --once)        RUN_ONCE=true; shift ;;
        -h|--help)     usage ;;
        *)             echo "Unknown option: $1"; usage ;;
    esac
done

mkdir -p "$OUTPUT_DIR"

check_telemetry() {
    local latest
    latest=$(find "$TELEMETRY_DIR" -name "*.json" -type f -printf '%T@ %p\n' 2>/dev/null \
        | sort -rn | head -1 | cut -d' ' -f2-)

    if [[ -z "$latest" ]]; then
        echo "[$(date -Iseconds)] No telemetry files found in $TELEMETRY_DIR"
        return 1
    fi

    echo "[$(date -Iseconds)] Latest telemetry: $latest"

    # Check for seal stress indicators
    if command -v python3 &>/dev/null; then
        python3 -c "
import json, sys
with open('$latest') as f:
    data = json.load(f)
# Nested under seal_metrics in the telemetry schema; tolerate flat files too.
metrics = data.get('seal_metrics', {})
stress = metrics.get('seal_stress_index', data.get('seal_stress_index', 0))
if stress > 0.7:
    print(f'ALERT: Seal stress index {stress:.2f} exceeds threshold 0.70')
    sys.exit(2)
else:
    print(f'OK: Seal stress index {stress:.2f} within normal range')
"
        return $?
    else
        echo "Warning: python3 not available, skipping telemetry analysis"
        return 0
    fi
}

regenerate_stl() {
    echo "[$(date -Iseconds)] Regenerating STL from genome: $GENOME_FILE"
    local timestamp
    timestamp=$(date +%Y%m%d_%H%M%S)
    python3 "$SCRIPT_DIR/STL_generator.py" \
        --genome "$GENOME_FILE" \
        -o "$OUTPUT_DIR/seal_gasket_${timestamp}.stl"
}

echo "=== BioMachine AutoTuneLoop ==="
echo "Interval: ${INTERVAL}s | Telemetry: $TELEMETRY_DIR | Genome: $GENOME_FILE"
echo ""

while true; do
    if check_telemetry; then
        echo "[$(date -Iseconds)] System nominal."
    else
        exit_code=$?
        if [[ $exit_code -eq 2 ]]; then
            echo "[$(date -Iseconds)] Stress detected — triggering regeneration."
            regenerate_stl
        fi
    fi

    if [[ "$RUN_ONCE" == "true" ]]; then
        echo "[$(date -Iseconds)] Single iteration complete."
        exit 0
    fi

    sleep "$INTERVAL"
done
