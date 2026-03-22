"""Unit and integration tests for the diagnostics module."""

import json
import tempfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent


# ---------------------------------------------------------------------------
# self_test unit tests
# ---------------------------------------------------------------------------

class TestCheckJsonSyntax:
    def test_valid_json(self, tmp_path):
        from diagnostics.self_test import check_json_syntax

        f = tmp_path / "good.json"
        f.write_text('{"a": 1}')
        result = check_json_syntax(f)
        assert result["status"] == "pass"

    def test_invalid_json(self, tmp_path):
        from diagnostics.self_test import check_json_syntax

        f = tmp_path / "bad.json"
        f.write_text("{broken")
        result = check_json_syntax(f)
        assert result["status"] == "fail"

    def test_missing_file(self, tmp_path):
        from diagnostics.self_test import check_json_syntax

        result = check_json_syntax(tmp_path / "nope.json")
        assert result["status"] == "fail"


class TestCheckSchemaRef:
    def test_has_schema(self, tmp_path):
        from diagnostics.self_test import check_schema_ref

        f = tmp_path / "data.json"
        f.write_text(json.dumps({"$schema": "../schemas/test.schema.json"}))
        result = check_schema_ref(f)
        assert result["status"] == "pass"

    def test_missing_schema(self, tmp_path):
        from diagnostics.self_test import check_schema_ref

        f = tmp_path / "data.json"
        f.write_text(json.dumps({"key": "value"}))
        result = check_schema_ref(f)
        assert result["status"] == "warn"


class TestCheckGenome:
    def test_real_genome(self):
        from diagnostics.self_test import check_genome

        result = check_genome()
        assert result["status"] == "pass"

    def test_missing_genome(self, tmp_path):
        from diagnostics.self_test import check_genome

        result = check_genome(tmp_path / "nope.json")
        assert result["status"] == "fail"

    def test_incomplete_genome(self, tmp_path):
        from diagnostics.self_test import check_genome

        f = tmp_path / "incomplete.json"
        f.write_text(json.dumps({"geometry": {}}))
        result = check_genome(f)
        assert result["status"] == "fail"
        assert "missing keys" in result["detail"]


class TestCheckTelemetryDir:
    def test_real_telemetry_dir(self):
        from diagnostics.self_test import check_telemetry_dir

        result = check_telemetry_dir()
        assert result["status"] == "pass"

    def test_missing_dir(self, tmp_path):
        from diagnostics.self_test import check_telemetry_dir

        result = check_telemetry_dir(tmp_path / "nonexistent")
        assert result["status"] == "fail"

    def test_empty_dir(self, tmp_path):
        from diagnostics.self_test import check_telemetry_dir

        empty = tmp_path / "empty"
        empty.mkdir()
        result = check_telemetry_dir(empty)
        assert result["status"] == "warn"


class TestCheckStlGenerator:
    def test_generator_exists(self):
        from diagnostics.self_test import check_stl_generator

        result = check_stl_generator()
        assert result["status"] == "pass"


class TestCheckGlyphIndex:
    def test_glyph_index(self):
        from diagnostics.self_test import check_glyph_index

        result = check_glyph_index()
        assert result["status"] == "pass"
        assert "glyphs registered" in result["detail"]


class TestCheckOfflineQueue:
    def test_no_queue(self, tmp_path):
        from diagnostics.self_test import check_offline_queue

        result = check_offline_queue(tmp_path / "noqueue")
        assert result["status"] == "pass"

    def test_empty_queue(self, tmp_path):
        from diagnostics.self_test import check_offline_queue

        q = tmp_path / "queue"
        q.mkdir()
        result = check_offline_queue(q)
        assert result["status"] == "pass"

    def test_pending_queue(self, tmp_path):
        from diagnostics.self_test import check_offline_queue

        q = tmp_path / "queue"
        q.mkdir()
        (q / "1234.json").write_text("{}")
        result = check_offline_queue(q)
        assert result["status"] == "warn"
        assert "1 unsent" in result["detail"]


class TestRunDiagnostics:
    def test_full_diagnostic_run(self):
        from diagnostics.self_test import run_diagnostics

        report = run_diagnostics()
        assert report["overall"] in ("pass", "warn", "fail")
        assert report["glyph"] == "🔧🩺"
        assert len(report["checks"]) > 0
        assert "$schema" in report

    def test_report_validates_against_schema(self):
        try:
            import jsonschema
        except ImportError:
            pytest.skip("jsonschema not installed")

        from diagnostics.self_test import run_diagnostics

        report = run_diagnostics()
        schema_path = ROOT / "schemas" / "diagnostic_report.schema.json"
        with open(schema_path) as f:
            schema = json.load(f)
        jsonschema.validate(instance=report, schema=schema)


# ---------------------------------------------------------------------------
# offline_queue unit tests
# ---------------------------------------------------------------------------

class TestOfflineQueue:
    def test_enqueue_from_dict(self, tmp_path):
        from diagnostics.offline_queue import enqueue, peek_queue

        data = {"node_id": 1, "timestamp": "2025-01-01T00:00:00Z"}
        dest = enqueue(data, queue_dir=tmp_path)
        assert dest.exists()
        assert json.loads(dest.read_text()) == data
        assert len(peek_queue(tmp_path)) == 1

    def test_enqueue_from_file(self, tmp_path):
        from diagnostics.offline_queue import enqueue

        src = ROOT / "seal_core" / "telemetry" / "LoRaSealNode_telemetry_sample.json"
        dest = enqueue(src, queue_dir=tmp_path)
        assert dest.exists()
        with open(src) as f:
            expected = json.load(f)
        assert json.loads(dest.read_text()) == expected

    def test_flush_removes_files(self, tmp_path):
        from diagnostics.offline_queue import enqueue, flush_queue, peek_queue

        enqueue({"a": 1}, queue_dir=tmp_path)
        enqueue({"b": 2}, queue_dir=tmp_path)
        assert len(peek_queue(tmp_path)) == 2

        collected = []
        flushed = flush_queue(queue_dir=tmp_path, tx_callback=collected.append)
        assert len(flushed) == 2
        assert len(collected) == 2
        assert len(peek_queue(tmp_path)) == 0

    def test_flush_dry_run_keeps_files(self, tmp_path):
        from diagnostics.offline_queue import enqueue, flush_queue, peek_queue

        enqueue({"x": 1}, queue_dir=tmp_path)
        flush_queue(queue_dir=tmp_path, dry_run=True, tx_callback=lambda d: None)
        assert len(peek_queue(tmp_path)) == 1

    def test_flush_empty_queue(self, tmp_path):
        from diagnostics.offline_queue import flush_queue

        flushed = flush_queue(queue_dir=tmp_path)
        assert flushed == []

    def test_queue_status(self, tmp_path):
        from diagnostics.offline_queue import enqueue, queue_status

        status = queue_status(queue_dir=tmp_path)
        assert status["pending_count"] == 0

        enqueue({"z": 1}, queue_dir=tmp_path)
        status = queue_status(queue_dir=tmp_path)
        assert status["pending_count"] == 1
        assert status["glyph"] == "📡💾"

    def test_fifo_order(self, tmp_path):
        """Queue should flush in FIFO order (oldest first)."""
        import time
        from diagnostics.offline_queue import enqueue, flush_queue

        enqueue({"seq": 1}, queue_dir=tmp_path)
        time.sleep(0.001)
        enqueue({"seq": 2}, queue_dir=tmp_path)
        time.sleep(0.001)
        enqueue({"seq": 3}, queue_dir=tmp_path)

        collected = []
        flush_queue(queue_dir=tmp_path, tx_callback=collected.append)
        assert [d["seq"] for d in collected] == [1, 2, 3]


# ---------------------------------------------------------------------------
# Integration: cross-module workflow tests
# ---------------------------------------------------------------------------

class TestIntegration:
    def test_stressed_telemetry_triggers_alert_check(self):
        """Verify stressed telemetry has seal_stress_index above threshold."""
        stressed = ROOT / "seal_core" / "telemetry" / "LoRaSealNode_stressed_sample.json"
        genome = ROOT / "seal_core" / "SEAL_GENOME_TEMPLATE.json"

        with open(stressed) as f:
            telemetry = json.load(f)
        with open(genome) as f:
            genome_data = json.load(f)

        stress = telemetry["seal_metrics"]["seal_stress_index"]
        threshold = genome_data["tolerances"]["seal_stress_threshold"]
        assert stress > threshold, (
            f"Stressed sample stress={stress} should exceed genome threshold={threshold}"
        )

    def test_normal_telemetry_below_threshold(self):
        """Normal telemetry should not trigger regeneration."""
        normal = ROOT / "seal_core" / "telemetry" / "LoRaSealNode_telemetry_sample.json"
        genome = ROOT / "seal_core" / "SEAL_GENOME_TEMPLATE.json"

        with open(normal) as f:
            telemetry = json.load(f)
        with open(genome) as f:
            genome_data = json.load(f)

        stress = telemetry["seal_metrics"]["seal_stress_index"]
        threshold = genome_data["tolerances"]["seal_stress_threshold"]
        assert stress < threshold

    def test_packet_types_have_valid_glyphs(self):
        """All packet type glyphs should be registered in glyph-index.csv."""
        import csv

        packet_spec = ROOT / "field_oracle" / "lora_net" / "packet_spec.json"
        glyph_csv = ROOT / "materials_glyph_bank" / "glyph-index.csv"

        with open(packet_spec) as f:
            spec = json.load(f)
        with open(glyph_csv, newline="") as f:
            registered = {row["glyph"] for row in csv.DictReader(f)}

        for code, ptype in spec["packet_types"].items():
            assert ptype["glyph"] in registered, (
                f"Packet type {code} ({ptype['name']}) glyph {ptype['glyph']!r} "
                f"not in glyph-index.csv"
            )

    def test_emotion_machine_map_structure(self):
        """Emotion machine map entries should have required fields."""
        emap = ROOT / "vault" / "emotions" / "emotion_machine_map.json"

        with open(emap) as f:
            data = json.load(f)

        for key, mapping in data.items():
            if key.startswith("$"):
                continue
            assert "machine_event" in mapping, f"'{key}' missing machine_event"
            assert "signal" in mapping, f"'{key}' missing signal"
            assert "response" in mapping, f"'{key}' missing response"

    def test_genome_material_glyph_registered(self):
        """Seal genome material glyph should be in the glyph registry."""
        import csv

        genome = ROOT / "seal_core" / "SEAL_GENOME_TEMPLATE.json"
        glyph_csv = ROOT / "materials_glyph_bank" / "glyph-index.csv"

        with open(genome) as f:
            data = json.load(f)
        with open(glyph_csv, newline="") as f:
            registered = {row["glyph"] for row in csv.DictReader(f)}

        mat_glyph = data["material"]["glyph"]
        assert mat_glyph in registered, (
            f"Genome material glyph {mat_glyph!r} not in glyph-index.csv"
        )

    def test_enqueue_telemetry_and_diagnose(self, tmp_path):
        """End-to-end: enqueue telemetry, run diagnostics, check queue warning."""
        from diagnostics.offline_queue import enqueue
        from diagnostics.self_test import check_offline_queue

        src = ROOT / "seal_core" / "telemetry" / "LoRaSealNode_telemetry_sample.json"
        enqueue(src, queue_dir=tmp_path)

        result = check_offline_queue(tmp_path)
        assert result["status"] == "warn"
        assert "1 unsent" in result["detail"]

    def test_stl_generator_from_genome(self, tmp_path):
        """Verify STL generator produces output from genome template."""
        import subprocess

        genome = ROOT / "seal_core" / "SEAL_GENOME_TEMPLATE.json"
        out = tmp_path / "test_seal.stl"
        result = subprocess.run(
            ["python", str(ROOT / "regenerator" / "STL_generator.py"),
             "--genome", str(genome), "-o", str(out)],
            capture_output=True, text=True,
        )
        assert result.returncode == 0, f"STL generator failed: {result.stderr}"
        assert out.exists()
        assert out.stat().st_size > 0
