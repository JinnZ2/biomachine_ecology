"""Boot-time self-test routines for BioMachine nodes.

Each check returns a dict with status ("pass", "warn", "fail"), a message,
and optional detail fields.  Running as a script prints a JSON diagnostic
report to stdout — suitable for piping into telemetry or logging.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path
from typing import Any

GLYPH = "🔧🩺"

ROOT = Path(__file__).resolve().parent.parent


# ---------------------------------------------------------------------------
# Individual checks
# ---------------------------------------------------------------------------

def check_json_syntax(path: Path) -> dict[str, Any]:
    """Verify a JSON file can be parsed."""
    try:
        with open(path) as f:
            json.load(f)
        return {"check": "json_syntax", "file": str(path.name), "status": "pass"}
    except json.JSONDecodeError as exc:
        return {
            "check": "json_syntax",
            "file": str(path.name),
            "status": "fail",
            "detail": str(exc),
        }
    except FileNotFoundError:
        return {
            "check": "json_syntax",
            "file": str(path.name),
            "status": "fail",
            "detail": "file not found",
        }


def check_schema_ref(path: Path) -> dict[str, Any]:
    """Verify a JSON data file contains a $schema reference."""
    try:
        with open(path) as f:
            data = json.load(f)
        ref = data.get("$schema", "")
        if ref:
            return {"check": "schema_ref", "file": str(path.name), "status": "pass"}
        return {
            "check": "schema_ref",
            "file": str(path.name),
            "status": "warn",
            "detail": "missing $schema field",
        }
    except Exception as exc:
        return {
            "check": "schema_ref",
            "file": str(path.name),
            "status": "fail",
            "detail": str(exc),
        }


def check_genome(genome_path: Path | None = None) -> dict[str, Any]:
    """Validate seal genome template exists and has required fields."""
    if genome_path is None:
        genome_path = ROOT / "seal_core" / "SEAL_GENOME_TEMPLATE.json"
    try:
        with open(genome_path) as f:
            data = json.load(f)
        missing = []
        for key in ("geometry", "material", "tolerances"):
            if key not in data:
                missing.append(key)
        if missing:
            return {
                "check": "genome",
                "status": "fail",
                "detail": f"missing keys: {missing}",
            }
        return {"check": "genome", "status": "pass"}
    except FileNotFoundError:
        return {
            "check": "genome",
            "status": "fail",
            "detail": "genome file not found",
        }
    except Exception as exc:
        return {"check": "genome", "status": "fail", "detail": str(exc)}


def check_telemetry_dir(telemetry_dir: Path | None = None) -> dict[str, Any]:
    """Verify the telemetry directory exists and contains at least one JSON."""
    if telemetry_dir is None:
        telemetry_dir = ROOT / "seal_core" / "telemetry"
    if not telemetry_dir.is_dir():
        return {
            "check": "telemetry_dir",
            "status": "fail",
            "detail": "directory not found",
        }
    json_files = list(telemetry_dir.glob("*.json"))
    if not json_files:
        return {
            "check": "telemetry_dir",
            "status": "warn",
            "detail": "no telemetry files present",
        }
    return {
        "check": "telemetry_dir",
        "status": "pass",
        "detail": f"{len(json_files)} file(s) found",
    }


def check_stl_generator() -> dict[str, Any]:
    """Verify the STL generator module can be imported."""
    gen_path = ROOT / "regenerator" / "STL_generator.py"
    if not gen_path.exists():
        return {
            "check": "stl_generator",
            "status": "fail",
            "detail": "STL_generator.py not found",
        }
    try:
        import py_compile
        py_compile.compile(str(gen_path), doraise=True)
        return {"check": "stl_generator", "status": "pass"}
    except py_compile.PyCompileError as exc:
        return {
            "check": "stl_generator",
            "status": "fail",
            "detail": str(exc),
        }


def check_harvester_config(
    config_path: Path | None = None,
) -> dict[str, Any]:
    """Verify energy harvester config exists and has a power bus."""
    if config_path is None:
        config_path = ROOT / "energy_harvester" / "harvester_config_example.json"
    try:
        with open(config_path) as f:
            data = json.load(f)
        if "power_bus" not in data:
            return {
                "check": "harvester_config",
                "status": "warn",
                "detail": "no power_bus defined",
            }
        bus = data["power_bus"]
        lockout = bus.get("undervoltage_lockout_v", 0)
        if lockout <= 0:
            return {
                "check": "harvester_config",
                "status": "warn",
                "detail": "undervoltage lockout not set",
            }
        return {"check": "harvester_config", "status": "pass"}
    except FileNotFoundError:
        return {
            "check": "harvester_config",
            "status": "warn",
            "detail": "config file not found",
        }
    except Exception as exc:
        return {"check": "harvester_config", "status": "fail", "detail": str(exc)}


def check_glyph_index() -> dict[str, Any]:
    """Verify the glyph index CSV is readable and non-empty."""
    csv_path = ROOT / "materials_glyph_bank" / "glyph-index.csv"
    if not csv_path.exists():
        return {
            "check": "glyph_index",
            "status": "fail",
            "detail": "glyph-index.csv not found",
        }
    import csv

    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    required = {"glyph", "name", "category"}
    if not reader.fieldnames or required - set(reader.fieldnames):
        return {
            "check": "glyph_index",
            "status": "fail",
            "detail": f"missing columns: {required - set(reader.fieldnames or [])}",
        }
    return {
        "check": "glyph_index",
        "status": "pass",
        "detail": f"{len(rows)} glyphs registered",
    }


def check_offline_queue(queue_dir: Path | None = None) -> dict[str, Any]:
    """Check offline telemetry queue for pending items."""
    if queue_dir is None:
        queue_dir = ROOT / "diagnostics" / "queue"
    if not queue_dir.is_dir():
        return {
            "check": "offline_queue",
            "status": "pass",
            "detail": "no queue directory (clean state)",
        }
    pending = list(queue_dir.glob("*.json"))
    if pending:
        return {
            "check": "offline_queue",
            "status": "warn",
            "detail": f"{len(pending)} unsent packet(s) queued",
        }
    return {"check": "offline_queue", "status": "pass", "detail": "queue empty"}


# ---------------------------------------------------------------------------
# Full diagnostic suite
# ---------------------------------------------------------------------------

ALL_CHECKS = [
    check_genome,
    check_telemetry_dir,
    check_stl_generator,
    check_harvester_config,
    check_glyph_index,
    check_offline_queue,
]


def run_diagnostics() -> dict[str, Any]:
    """Run all self-test checks and return a diagnostic report."""
    results = []
    overall = "pass"
    for fn in ALL_CHECKS:
        result = fn()
        results.append(result)
        if result["status"] == "fail":
            overall = "fail"
        elif result["status"] == "warn" and overall != "fail":
            overall = "warn"

    return {
        "$schema": "../schemas/diagnostic_report.schema.json",
        "glyph": GLYPH,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "overall": overall,
        "checks": results,
    }


def main() -> None:
    report = run_diagnostics()
    json.dump(report, sys.stdout, indent=4)
    sys.stdout.write("\n")
    if report["overall"] == "fail":
        sys.exit(1)


if __name__ == "__main__":
    main()
