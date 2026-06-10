"""
Render Graphviz DOT diagrams under wiki/diagrams/ to SVG under wiki/assets/.

Usage:
    uv run python scripts/render_dot.py wiki/diagrams/<slug>-diagram-N.dot [...]
    uv run python scripts/render_dot.py --all
"""

import sys
from pathlib import Path

import graphviz

ROOT = Path(__file__).resolve().parent.parent
DIAGRAMS_DIR = ROOT / "wiki" / "diagrams"
ASSETS_DIR = ROOT / "wiki" / "assets"


def render(dot_path: Path) -> Path:
    dot_source = dot_path.read_text(encoding="utf-8")
    svg_data = graphviz.Source(dot_source).pipe(format="svg").decode("utf-8")
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    svg_path = ASSETS_DIR / f"{dot_path.stem}.svg"
    svg_path.write_text(svg_data, encoding="utf-8")
    return svg_path


def main():
    if len(sys.argv) < 2:
        print("Usage: render_dot.py <file.dot> [<file.dot> ...] | --all")
        sys.exit(1)

    if sys.argv[1] == "--all":
        dot_paths = sorted(DIAGRAMS_DIR.glob("*.dot"))
    else:
        dot_paths = [Path(p) for p in sys.argv[1:]]

    errors = 0
    for dot_path in dot_paths:
        if not dot_path.exists():
            print(f"  ERROR {dot_path}: not found")
            errors += 1
            continue
        try:
            svg_path = render(dot_path)
        except Exception as e:
            print(f"  ERROR {dot_path}: {e}")
            errors += 1
            continue
        print(f"  OK    {svg_path.relative_to(ROOT)}")

    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
