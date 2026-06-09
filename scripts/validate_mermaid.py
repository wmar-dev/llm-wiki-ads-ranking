import sys, json, asyncio
from pathlib import Path
from playwright.async_api import async_playwright


async def validate(text: str) -> dict:
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        result = await page.evaluate(
            """
            async (diagram) => {
                const m = await import(
                    'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs'
                );
                const mmd = m.default || m;
                try {
                    await mmd.parse(diagram);
                    return { valid: true };
                } catch (e) {
                    return {
                        valid: false,
                        error: e.message || String(e),
                        line: e.line || e.loc?.first_line || null,
                    };
                }
            }
            """,
            text,
        )
        await browser.close()
        return result


def extract_blocks(wiki_dir: Path):
    for f in sorted(wiki_dir.rglob("*.md")):
        content = f.read_text(encoding="utf-8")
        lines = content.split("\n")
        i = 0
        while i < len(lines):
            if lines[i].strip() == "```mermaid":
                start = i
                i += 1
                block_lines = []
                while i < len(lines) and not lines[i].strip().startswith("```"):
                    block_lines.append(lines[i])
                    i += 1
                yield f, start + 1, "\n".join(block_lines)
            i += 1


async def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--all":
        wiki_dir = Path("wiki")
        errors = []
        for filepath, lineno, block in extract_blocks(wiki_dir):
            result = await validate(block)
            if not result["valid"]:
                rel = filepath.relative_to(wiki_dir)
                errors.append(
                    {
                        "file": str(rel),
                        "line": lineno,
                        "error": result["error"],
                    }
                )
                print(
                    f"FAIL  {rel}:{lineno}  {result['error'][:80]}"
                )
            else:
                rel = filepath.relative_to(wiki_dir)
                print(f"OK    {rel}:{lineno}")
        if errors:
            print(f"\n{len(errors)} diagram(s) failed validation")
            sys.exit(1)
        else:
            print("\nAll diagrams valid")
    else:
        text = sys.stdin.read()
        result = await validate(text)
        print(json.dumps(result))


if __name__ == "__main__":
    asyncio.run(main())
