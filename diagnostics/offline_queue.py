"""Offline-first telemetry queue.

When the LoRa mesh is unreachable, telemetry packets are written to a local
JSON queue directory.  When connectivity returns, queued packets are flushed
in order.

Queue directory: diagnostics/queue/
Each file is named with a monotonic timestamp: <epoch_ns>.json

Usage as a library:
    from diagnostics.offline_queue import enqueue, flush_queue

Usage from CLI:
    # Enqueue a telemetry file
    python -m diagnostics.offline_queue enqueue seal_core/telemetry/sample.json

    # Flush all queued packets (dry-run)
    python -m diagnostics.offline_queue flush --dry-run

    # Flush (actually send — prints to stdout as stand-in for LoRa TX)
    python -m diagnostics.offline_queue flush
"""

from __future__ import annotations

import json
import shutil
import sys
import time
from pathlib import Path
from typing import Any

GLYPH = "📡💾"

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_QUEUE_DIR = Path(__file__).resolve().parent / "queue"


def enqueue(
    telemetry: dict[str, Any] | Path | str,
    queue_dir: Path | None = None,
) -> Path:
    """Add a telemetry packet to the offline queue.

    Parameters
    ----------
    telemetry:
        Either a dict (packet data) or a path to a JSON file.
    queue_dir:
        Override the default queue directory.

    Returns
    -------
    Path to the queued file.
    """
    if queue_dir is None:
        queue_dir = DEFAULT_QUEUE_DIR
    queue_dir.mkdir(parents=True, exist_ok=True)

    if isinstance(telemetry, (str, Path)):
        path = Path(telemetry)
        with open(path) as f:
            data = json.load(f)
    else:
        data = telemetry

    ts = time.time_ns()
    dest = queue_dir / f"{ts}.json"
    with open(dest, "w") as f:
        json.dump(data, f, indent=4)
        f.write("\n")

    return dest


def peek_queue(queue_dir: Path | None = None) -> list[Path]:
    """Return queued files sorted oldest-first."""
    if queue_dir is None:
        queue_dir = DEFAULT_QUEUE_DIR
    if not queue_dir.is_dir():
        return []
    return sorted(queue_dir.glob("*.json"))


def flush_queue(
    queue_dir: Path | None = None,
    dry_run: bool = False,
    tx_callback: Any = None,
) -> list[dict[str, Any]]:
    """Send all queued packets and remove them from the queue.

    Parameters
    ----------
    queue_dir:
        Override the default queue directory.
    dry_run:
        If True, print packets but do not remove from queue.
    tx_callback:
        Optional callable(data: dict) invoked for each packet.
        If None, packets are printed to stdout as a default sink.

    Returns
    -------
    List of packet dicts that were flushed.
    """
    if queue_dir is None:
        queue_dir = DEFAULT_QUEUE_DIR

    queued = peek_queue(queue_dir)
    flushed: list[dict[str, Any]] = []

    for path in queued:
        with open(path) as f:
            data = json.load(f)

        if tx_callback is not None:
            tx_callback(data)
        else:
            print(json.dumps(data, indent=2))

        flushed.append(data)

        if not dry_run:
            path.unlink()

    if not dry_run and queue_dir.is_dir() and not list(queue_dir.iterdir()):
        queue_dir.rmdir()

    return flushed


def queue_status(queue_dir: Path | None = None) -> dict[str, Any]:
    """Return a summary of the current queue state."""
    if queue_dir is None:
        queue_dir = DEFAULT_QUEUE_DIR
    pending = peek_queue(queue_dir)
    return {
        "glyph": GLYPH,
        "queue_dir": str(queue_dir),
        "pending_count": len(pending),
        "oldest": str(pending[0].name) if pending else None,
        "newest": str(pending[-1].name) if pending else None,
    }


def main() -> None:
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print("Usage: python -m diagnostics.offline_queue <enqueue FILE | flush [--dry-run] | status>")
        sys.exit(0)

    cmd = args[0]
    if cmd == "enqueue":
        if len(args) < 2:
            print("Error: enqueue requires a JSON file path", file=sys.stderr)
            sys.exit(1)
        dest = enqueue(args[1])
        print(f"Queued: {dest}")

    elif cmd == "flush":
        dry_run = "--dry-run" in args
        flushed = flush_queue(dry_run=dry_run)
        if dry_run:
            print(f"\n--- Dry run: {len(flushed)} packet(s) would be flushed ---")
        else:
            print(f"\n--- Flushed {len(flushed)} packet(s) ---")

    elif cmd == "status":
        status = queue_status()
        print(json.dumps(status, indent=4))

    else:
        print(f"Unknown command: {cmd}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
