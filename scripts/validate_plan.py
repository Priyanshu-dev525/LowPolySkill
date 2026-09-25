#!/usr/bin/env python3
"""Structural checker for Universal Low-Poly Model Plans.

Usage:
    python scripts/validate_plan.py path/to/plan.md
    python scripts/validate_plan.py path/to/plan.md --lenient
    python scripts/validate_plan.py assets/examples/*.md
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REQUIRED_HEADINGS = [
    ("# LOW-POLY MODEL PLAN", re.compile(r"^#\s+LOW-POLY MODEL PLAN", re.I | re.M)),
    ("## 1. Model Overview", re.compile(r"^##\s+1\.\s+Model Overview", re.I | re.M)),
    ("## 2. Target Style", re.compile(r"^##\s+2\.\s+Target Style", re.I | re.M)),
    ("## 3. Coordinate System", re.compile(r"^##\s+3\.\s+Coordinate System", re.I | re.M)),
    ("## 4. Component Breakdown", re.compile(r"^##\s+4\.\s+Component Breakdown", re.I | re.M)),
    ("## 5. Step-by-Step Construction", re.compile(r"^##\s+5\.\s+Step-by-Step Construction", re.I | re.M)),
    ("## 6. Assembly", re.compile(r"^##\s+6\.\s+Assembly", re.I | re.M)),
    ("## 7. Materials", re.compile(r"^##\s+7\.\s+Materials", re.I | re.M)),
    ("## 8. Low-Poly Optimization", re.compile(r"^##\s+8\.\s+Low-Poly Optimization", re.I | re.M)),
    ("## 9. Final Validation", re.compile(r"^##\s+9\.\s+Final Validation", re.I | re.M)),
    ("## 10. Optional Software Implementation", re.compile(r"^##\s+10\.\s+Optional Software Implementation", re.I | re.M)),
]

COMPONENT_HEADER = re.compile(
    r"\|\s*Part\s*\|\s*Base Shape\s*\|\s*Dimensions\s*\|\s*Position\s*\|\s*Rotation\s*\|\s*Polygon Level\s*\|",
    re.I,
)
MATERIAL_HEADER = re.compile(
    r"\|\s*Material\s*\|\s*Color\s*\|\s*Roughness\s*\|\s*Metallic\s*\|\s*Shading\s*\|",
    re.I,
)
HEX_COLOR = re.compile(r"#[0-9A-Fa-f]{6}")
TABLE_ROW = re.compile(r"^\|([^|]+(?:\|[^|]+){4,})\|", re.M)
SEPARATOR_ROW = re.compile(r"^\|\s*:?-{3,}", re.M)

PRIMITIVES = (
    "cube",
    "plane",
    "cylinder",
    "cone",
    "sphere",
    "icosphere",
    "capsule",
    "torus",
    "pyramid",
    "prism",
    "polygon",
    "box",
)
OPERATIONS = (
    "create",
    "scale",
    "rotate",
    "move",
    "translate",
    "extrude",
    "inset",
    "bevel",
    "loop cut",
    "merge",
    "bridge",
    "duplicate",
    "mirror",
    "array",
    "boolean",
    "subdivide",
    "delete",
    "dissolve",
    "weld",
    "flip",
    "assign",
)

COORD_KEYS = ("up axis", "forward", "origin", "overall dimension", "base unit")


def section_body(text: str, heading_re: re.Pattern, next_re: re.Pattern | None) -> str:
    m = heading_re.search(text)
    if not m:
        return ""
    start = m.end()
    end = len(text)
    if next_re:
        n = next_re.search(text, start)
        if n:
            end = n.start()
    return text[start:end]


def count_table_data_rows(block: str, header_re: re.Pattern) -> int:
    m = header_re.search(block)
    if not m:
        return 0
    rest = block[m.end() :]
    count = 0
    for line in rest.splitlines():
        if not line.strip().startswith("|"):
            if count:
                break
            continue
        if re.match(r"^\|\s*:?-{2,}", line.strip()):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if not any(cells):
            continue
        # skip placeholder / empty guidance rows
        joined = " ".join(cells).strip()
        if not joined or joined.startswith("<!--") or all(c in ("", "—", "-", "n/a") for c in cells):
            continue
        count += 1
    return count


def check_file(path: Path, lenient: bool) -> list[str]:
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []

    for label, rx in REQUIRED_HEADINGS:
        if not rx.search(text):
            errors.append(f"missing heading: {label}")

    if not COMPONENT_HEADER.search(text):
        errors.append("missing component table header (Part | Base Shape | Dimensions | Position | Rotation | Polygon Level)")
    else:
        n = count_table_data_rows(text, COMPONENT_HEADER)
        if n < 1 and not lenient:
            errors.append("component table has no data rows")

    if not MATERIAL_HEADER.search(text):
        errors.append("missing material table header (Material | Color | Roughness | Metallic | Shading)")
    else:
        n = count_table_data_rows(text, MATERIAL_HEADER)
        if n < 1 and not lenient:
            errors.append("material table has no data rows")

    hexes = HEX_COLOR.findall(text)
    if len(hexes) < 2 and not lenient:
        errors.append(f"expected at least 2 hex colors, found {len(hexes)}")

    lower = text.lower()
    missing_coord = [k for k in COORD_KEYS if k not in lower]
    if missing_coord and not lenient:
        errors.append("coordinate system missing: " + ", ".join(missing_coord))

    if not lenient:
        # construction should mention primitives and operations
        s5 = section_body(text, REQUIRED_HEADINGS[5][1], REQUIRED_HEADINGS[6][1])
        body = s5.lower()
        if body.strip():
            prim_hits = [p for p in PRIMITIVES if p in body]
            op_hits = [o for o in OPERATIONS if o in body]
            if len(prim_hits) < 1:
                errors.append("section 5 does not name any primitive (cube, cylinder, cone, …)")
            if len(op_hits) < 3:
                errors.append("section 5 has too few modeling operations (create/scale/extrude/…)")
            if not re.search(r"\d", s5):
                errors.append("section 5 has no numeric dimensions or amounts")

        s10 = section_body(text, REQUIRED_HEADINGS[10][1], None)
        if not s10.strip():
            errors.append("section 10 is empty (write 'No target software specified' if none)")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a LOW-POLY MODEL PLAN markdown file.")
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--lenient", action="store_true", help="only require headings (for blank templates)")
    args = parser.parse_args()

    failed = 0
    for path in args.paths:
        if not path.is_file():
            print(f"FAIL  {path}: not a file")
            failed += 1
            continue
        errors = check_file(path, args.lenient)
        if errors:
            failed += 1
            print(f"FAIL  {path}")
            for e in errors:
                print(f"      - {e}")
        else:
            print(f"OK    {path}")
    if failed:
        print(f"\n{failed} file(s) failed.")
        return 1
    print(f"\n{len(args.paths)} file(s) passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
