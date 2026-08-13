#!/usr/bin/env python3
"""LoRa network node initialization script.

Configures a new BioMachine LoRa sensor node by writing a node
configuration JSON file with the assigned node ID, radio parameters
from the packet spec, and default telemetry settings.

Usage:
    python field_oracle/lora_net/scripts/init_node.py --node-id 12
    python field_oracle/lora_net/scripts/init_node.py --node-id 12 --seal-id seal_core_gasket_01
    python field_oracle/lora_net/scripts/init_node.py --node-id 12 -o node_12_config.json

Prerequisites:
    - Python 3.8+
    - packet_spec.json in the parent directory
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PACKET_SPEC = SCRIPT_DIR.parent / "packet_spec.json"


def load_packet_spec(path: Path = PACKET_SPEC) -> dict:
    with open(path) as f:
        return json.load(f)


def generate_node_config(
    node_id: int,
    seal_id: str | None = None,
    telemetry_interval_s: int = 60,
    packet_spec_path: Path = PACKET_SPEC,
) -> dict:
    """Generate a node configuration from the packet spec."""
    spec = load_packet_spec(packet_spec_path)

    config = {
        "node_id": node_id,
        "glyph": "📡📊",
        "created": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "radio": {
            "frequency_mhz": spec["frequency_mhz"],
            "spreading_factor": spec["spreading_factor"],
            "bandwidth_khz": spec["bandwidth_khz"],
            "coding_rate": spec["coding_rate"],
        },
        "telemetry": {
            "interval_s": telemetry_interval_s,
            "enabled_readings": [
                "temperature_c",
                "humidity_pct",
                "pressure_kpa",
                "vibration_g",
                "uv_index",
                "salt_conductivity_ms",
            ],
        },
        "fallback_modes": list(spec.get("fallback_modes", {}).keys()),
    }

    if seal_id:
        config["seal_id"] = seal_id

    return config


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Initialize a new BioMachine LoRa sensor node"
    )
    parser.add_argument(
        "--node-id", type=int, required=True,
        help="Unique node ID (0-255)",
    )
    parser.add_argument(
        "--seal-id", type=str, default=None,
        help="Optional seal identifier to monitor",
    )
    parser.add_argument(
        "--interval", type=int, default=60,
        help="Telemetry reporting interval in seconds (default: 60)",
    )
    parser.add_argument(
        "-o", "--output", type=str, default=None,
        help="Output file path (default: stdout)",
    )
    parser.add_argument(
        "--packet-spec", type=str, default=str(PACKET_SPEC),
        help="Path to packet_spec.json",
    )

    args = parser.parse_args()

    if not 0 <= args.node_id <= 255:
        print("Error: node-id must be 0-255", file=sys.stderr)
        sys.exit(1)

    config = generate_node_config(
        node_id=args.node_id,
        seal_id=args.seal_id,
        telemetry_interval_s=args.interval,
        packet_spec_path=Path(args.packet_spec),
    )

    output = json.dumps(config, indent=4) + "\n"

    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
        print(f"Node config written to {args.output}")
    else:
        sys.stdout.write(output)


if __name__ == "__main__":
    main()
