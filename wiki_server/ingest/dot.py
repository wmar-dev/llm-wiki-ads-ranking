import shutil
import sys
from pathlib import Path

from wiki_server import config


def ingest_dot(dot_file: str, page: str | None = None) -> None:
    import graphviz

    src = Path(dot_file)
    if not src.exists():
        print(f"File not found: {dot_file}")
        sys.exit(1)

    dot_text = src.read_text(encoding="utf-8")
    name = src.stem

    assets_dir = config.WIKI_DIR / "assets"
    diagrams_dir = config.WIKI_DIR / "diagrams"
    assets_dir.mkdir(parents=True, exist_ok=True)
    diagrams_dir.mkdir(parents=True, exist_ok=True)

    svg_dest = assets_dir / f"{name}.svg"
    dot_dest = diagrams_dir / f"{name}.dot"

    try:
        src_obj = graphviz.Source(dot_text)
        svg_data = src_obj.pipe(format="svg").decode("utf-8")
    except graphviz.backend.execute.CalledProcessError as e:
        print(f"Dot syntax error in {dot_file}: {e}. No SVG written.")
        sys.exit(1)
    except Exception as e:
        print(f"Graphviz error: {e}. No SVG written.")
        sys.exit(1)

    svg_dest.write_text(svg_data, encoding="utf-8")
    shutil.copy2(src, dot_dest)
    print(f"SVG written: {svg_dest}")
    print(f"Dot source preserved: {dot_dest}")

    if page:
        page_path = Path(page)
        if not page_path.exists():
            print(f"Warning: wiki page not found for embedding: {page}")
        else:
            svg_ref = f"\n![{name}](/assets/{name}.svg)\n"
            with open(page_path, "a", encoding="utf-8") as f:
                f.write(svg_ref)
            print(f"SVG reference added to: {page}")
