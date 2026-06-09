import re
import time
from pathlib import Path
from wiki_server import config


def slug_from_title(title: str) -> str:
    slug = title.lower().strip()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"[\s_]+", "-", slug)
    slug = re.sub(r"-+", "-", slug).strip("-")
    # Ensure uniqueness by appending -2, -3 if slug already exists
    candidate = slug
    counter = 2
    while (config.WIKI_DIR / f"{candidate}.md").exists():
        candidate = f"{slug}-{counter}"
        counter += 1
    return candidate


def write_wiki_page(slug: str, frontmatter: dict, body: str) -> Path:
    config.WIKI_DIR.mkdir(parents=True, exist_ok=True)
    page_path = config.WIKI_DIR / f"{slug}.md"
    fm_lines = ["---"]
    for key, value in frontmatter.items():
        if isinstance(value, list):
            fm_lines.append(f"{key}:")
            for item in value:
                fm_lines.append(f"  - {item}")
        else:
            fm_lines.append(f'{key}: "{value}"')
    fm_lines.append("---")
    fm_lines.append("")
    page_path.write_text("\n".join(fm_lines) + body, encoding="utf-8")
    return page_path


def append_log_entry(title: str, source_type: str, source_path: str) -> None:
    log_path = config.WIKI_DIR / "log.md"
    timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    entry = f"\n- **{timestamp}** | `{source_type}` | [{title}]({source_path})"
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(entry)
