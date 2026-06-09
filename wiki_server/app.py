import json
import mimetypes
import os
import re
import time
from pathlib import Path

from flask import Flask, abort, render_template, request, send_file
from markdown_it import MarkdownIt
from mdit_py_plugins.dollarmath import dollarmath_plugin

from wiki_server import config

_md = (
    MarkdownIt("commonmark")
    .enable("linkify")
    .enable("table")
    .use(dollarmath_plugin, allow_digits=False)
)

_WIKI_LINK_RE = re.compile(r"\[\[wiki/([^\]]+)\]\]")


def _wiki_link(m: re.Match) -> str:
    page = m.group(1)
    label = page.replace(".md", "").replace("/", " › ").replace("-", " ").title()
    return f'<a href="/wiki/{page}">{label}</a>'


def render_page(md_path: Path) -> str:
    text = md_path.read_text(encoding="utf-8")
    text = _WIKI_LINK_RE.sub(_wiki_link, text)
    return _md.render(text)


def _log_access(path: str, status: int) -> None:
    entry = json.dumps({"ts": int(time.time()), "path": path, "status": status}) + "\n"
    log = config.ACCESS_LOG
    with open(log, "a", encoding="utf-8") as f:
        f.write(entry)
    # Rotate if over threshold
    if os.path.getsize(log) > config.ACCESS_LOG_MAX_BYTES:
        _rotate_log()


def _rotate_log() -> None:
    log = config.ACCESS_LOG
    base = str(log)
    segment = 1
    while Path(f"{base}.{segment:03d}").exists():
        segment += 1
    os.rename(base, f"{base}.{segment:03d}")


def create_app() -> Flask:
    app = Flask(__name__, template_folder="templates", static_folder="static")

    @app.route("/")
    def index():
        index_path = config.WIKI_DIR / "index.md"
        if not index_path.exists():
            html = "<p>No pages yet. Use <code>make ingest</code> to add content.</p>"
        else:
            html = render_page(index_path)
        _log_access("/", 200)
        return render_template("page.html", content=html, title="Wiki Index")

    _section_dirs = {
        "synthesis": config.WIKI_DIR / "synthesis",
        "concepts": config.WIKI_DIR / "concepts",
        "entities": config.WIKI_DIR / "entities",
        "sources": config.WIKI_DIR / "sources",
    }

    @app.route("/wiki/<section>/")
    def wiki_section(section):
        dir_path = _section_dirs.get(section)
        if not dir_path or not dir_path.exists():
            return render_template("page.html", content="<p>Section not found.</p>", title=section.title()), 404
        entries = sorted(dir_path.iterdir())
        links = "".join(
            f'<li><a href="/wiki/{section}/{f.name}">{f.stem.replace("-", " ").title()}</a></li>\n'
            for f in entries if f.suffix == ".md"
        )
        count = sum(1 for f in entries if f.suffix == ".md")
        html = f"<h1>{section.title()}</h1>\n<p>{count} page(s)</p>\n<ul>\n{links}</ul>"
        _log_access(f"/wiki/{section}/", 200)
        return render_template("page.html", content=html, title=f"{section.title()} — LLM Wiki")

    @app.route("/wiki/<path:page>")
    def wiki_page(page):
        slug = page[:-3] if page.endswith(".md") else page
        md_path = config.WIKI_DIR / f"{slug}.md"
        if not md_path.exists():
            _log_access(request.path, 404)
            return render_template("404.html"), 404
        html = render_page(md_path)
        _log_access(request.path, 200)
        return render_template("page.html", content=html, title=slug.replace("-", " ").title())

    @app.route("/search")
    def search():
        from wiki_server.search.query import search as bm25_search
        q = request.args.get("q", "").strip()
        results = bm25_search(q) if q else []
        return render_template("search.html", query=q, results=results)

    @app.route("/metrics")
    def metrics():
        from wiki_server.metrics.report import generate_report
        report = generate_report()
        return render_template("metrics.html", report=report)

    @app.route("/assets/<path:filename>")
    def assets(filename):
        asset_path = config.WIKI_DIR / "assets" / filename
        if not asset_path.exists():
            abort(404)
        return send_file(asset_path, mimetype="image/svg+xml")

    @app.route("/raw/images/<path:filename>")
    def raw_images(filename):
        img_path = config.RAW_DIR / "images" / filename
        if not img_path.exists():
            abort(404)
        mime, _ = mimetypes.guess_type(filename)
        return send_file(img_path, mimetype=mime or "application/octet-stream")

    return app
