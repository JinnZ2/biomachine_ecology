"""Validate all JSON data files against their schemas."""

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SCHEMAS_DIR = ROOT / "schemas"


def load_json(path):
    with open(path) as f:
        return json.load(f)


def find_json_files():
    """Find all non-schema JSON files in the repository."""
    for p in ROOT.rglob("*.json"):
        if ".git" in p.parts or "schemas" in p.parts or "node_modules" in p.parts:
            continue
        yield p


@pytest.mark.parametrize("json_file", list(find_json_files()), ids=lambda p: str(p.relative_to(ROOT)))
def test_json_syntax(json_file):
    """Every JSON file must be valid JSON."""
    load_json(json_file)


SCHEMA_MAP = {
    "seal_genome": "seal_genome.schema.json",
    "telemetry": "telemetry.schema.json",
    "soil_map": "soil_map.schema.json",
    "emotion": "emotion.schema.json",
    "emotion_machine_map": "emotion_machine_map.schema.json",
    "touch_response": "touch_response.schema.json",
    "packet_spec": "packet_spec.schema.json",
    "harvester_config": "harvester_config.schema.json",
    "diagnostic_report": "diagnostic_report.schema.json",
}


def resolve_schema(data):
    """Try to find matching schema from $schema reference."""
    ref = data.get("$schema", "")
    for key, filename in SCHEMA_MAP.items():
        if filename in ref:
            schema_path = SCHEMAS_DIR / filename
            if schema_path.exists():
                return load_json(schema_path)
    return None


@pytest.mark.parametrize("json_file", list(find_json_files()), ids=lambda p: str(p.relative_to(ROOT)))
def test_json_schema_validation(json_file):
    """Validate JSON files that reference a schema."""
    try:
        import jsonschema
    except ImportError:
        pytest.skip("jsonschema not installed")

    data = load_json(json_file)
    schema = resolve_schema(data)
    if schema is None:
        pytest.skip(f"No schema found for {json_file.name}")

    jsonschema.validate(instance=data, schema=schema)
