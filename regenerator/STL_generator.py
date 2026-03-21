#!/usr/bin/env python3
"""STL generator for BioMachine Ecology seal gaskets and repair parts.

Generates parametric STL meshes from seal genome JSON definitions.
Designed for low-resolution 3D printing from recycled filament.
"""

import argparse
import json
import math
import struct
from pathlib import Path


def make_triangle(normal, v1, v2, v3):
    """Return a 50-byte STL binary triangle record."""
    return struct.pack("<12fH", *normal, *v1, *v2, *v3, 0)


def generate_annular_seal(inner_radius, outer_radius, thickness, segments=36):
    """Generate triangles for a flat annular seal (gasket ring).

    Args:
        inner_radius: Inner hole radius in mm.
        outer_radius: Outer edge radius in mm.
        thickness: Seal thickness in mm.
        segments: Number of radial segments for smoothness.

    Returns:
        List of triangle byte records.
    """
    triangles = []

    def ring_points(radius, z):
        return [
            (radius * math.cos(2 * math.pi * i / segments),
             radius * math.sin(2 * math.pi * i / segments),
             z)
            for i in range(segments)
        ]

    top_inner = ring_points(inner_radius, thickness)
    top_outer = ring_points(outer_radius, thickness)
    bot_inner = ring_points(inner_radius, 0.0)
    bot_outer = ring_points(outer_radius, 0.0)

    for i in range(segments):
        j = (i + 1) % segments
        angle = 2 * math.pi * i / segments
        cos_a, sin_a = math.cos(angle), math.sin(angle)

        # Top face
        triangles.append(make_triangle(
            (0, 0, 1), top_inner[i], top_outer[i], top_outer[j]))
        triangles.append(make_triangle(
            (0, 0, 1), top_inner[i], top_outer[j], top_inner[j]))

        # Bottom face
        triangles.append(make_triangle(
            (0, 0, -1), bot_inner[i], bot_outer[j], bot_outer[i]))
        triangles.append(make_triangle(
            (0, 0, -1), bot_inner[i], bot_inner[j], bot_outer[j]))

        # Outer wall
        triangles.append(make_triangle(
            (cos_a, sin_a, 0),
            top_outer[i], bot_outer[i], bot_outer[j]))
        triangles.append(make_triangle(
            (cos_a, sin_a, 0),
            top_outer[i], bot_outer[j], top_outer[j]))

        # Inner wall
        triangles.append(make_triangle(
            (-cos_a, -sin_a, 0),
            top_inner[i], bot_inner[j], bot_inner[i]))
        triangles.append(make_triangle(
            (-cos_a, -sin_a, 0),
            top_inner[i], top_inner[j], bot_inner[j]))

    return triangles


def write_stl(filepath, triangles):
    """Write triangles to a binary STL file."""
    header = b"\x00" * 80
    with open(filepath, "wb") as f:
        f.write(header)
        f.write(struct.pack("<I", len(triangles)))
        for tri in triangles:
            f.write(tri)
    print(f"Wrote {len(triangles)} triangles to {filepath}")


def load_genome(genome_path):
    """Load seal parameters from a genome JSON file."""
    with open(genome_path) as f:
        genome = json.load(f)
    return {
        "inner_radius": genome.get("inner_radius_mm", 10.0),
        "outer_radius": genome.get("outer_radius_mm", 20.0),
        "thickness": genome.get("thickness_mm", 2.0),
        "segments": genome.get("segments", 36),
    }


def main():
    parser = argparse.ArgumentParser(
        description="Generate STL seal gaskets from genome definitions")
    parser.add_argument(
        "--genome", type=Path,
        help="Path to seal genome JSON file")
    parser.add_argument(
        "--inner-radius", type=float, default=10.0,
        help="Inner radius in mm (default: 10)")
    parser.add_argument(
        "--outer-radius", type=float, default=20.0,
        help="Outer radius in mm (default: 20)")
    parser.add_argument(
        "--thickness", type=float, default=2.0,
        help="Thickness in mm (default: 2)")
    parser.add_argument(
        "--segments", type=int, default=36,
        help="Number of radial segments (default: 36)")
    parser.add_argument(
        "-o", "--output", type=Path, default=Path("seal_gasket.stl"),
        help="Output STL file path")

    args = parser.parse_args()

    if args.genome:
        params = load_genome(args.genome)
    else:
        params = {
            "inner_radius": args.inner_radius,
            "outer_radius": args.outer_radius,
            "thickness": args.thickness,
            "segments": args.segments,
        }

    triangles = generate_annular_seal(**params)
    write_stl(args.output, triangles)


if __name__ == "__main__":
    main()
