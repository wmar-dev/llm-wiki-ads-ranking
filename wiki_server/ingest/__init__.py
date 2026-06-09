import sys


USAGE = """Usage: python -m wiki_server.ingest <subcommand> [args]

Subcommands:
  webpage  <url>                       Ingest a webpage via Playwright
  pdf      <file_path>                 Ingest a PDF (auto-sectioned at 50 pages)
  image    <file_path>                 Ingest an image via multimodal description
  podcast  <file_path>                 Ingest a podcast transcript (.txt/.srt) or audio
  youtube  <url>                       Ingest a YouTube video transcript via yt-dlp
  dot      <dot_file> [--page <path>]  Render a Graphviz dot diagram to SVG
"""


def main() -> None:
    if len(sys.argv) < 2:
        print(USAGE)
        sys.exit(1)

    subcommand = sys.argv[1]

    if subcommand == "webpage":
        from wiki_server.ingest.webpage import ingest_webpage
        if len(sys.argv) < 3:
            print("Usage: ingest webpage <url>")
            sys.exit(1)
        ingest_webpage(sys.argv[2])

    elif subcommand == "pdf":
        from wiki_server.ingest.pdf import ingest_pdf
        if len(sys.argv) < 3:
            print("Usage: ingest pdf <file_path>")
            sys.exit(1)
        ingest_pdf(sys.argv[2])

    elif subcommand == "image":
        from wiki_server.ingest.image import ingest_image
        if len(sys.argv) < 3:
            print("Usage: ingest image <file_path>")
            sys.exit(1)
        ingest_image(sys.argv[2])

    elif subcommand == "podcast":
        from wiki_server.ingest.podcast import ingest_podcast
        if len(sys.argv) < 3:
            print("Usage: ingest podcast <file_path>")
            sys.exit(1)
        ingest_podcast(sys.argv[2])

    elif subcommand == "youtube":
        from wiki_server.ingest.youtube import ingest_youtube
        if len(sys.argv) < 3:
            print("Usage: ingest youtube <url>")
            sys.exit(1)
        ingest_youtube(sys.argv[2])

    elif subcommand == "dot":
        from wiki_server.ingest.dot import ingest_dot
        dot_file = sys.argv[2] if len(sys.argv) > 2 else None
        if not dot_file:
            print("Usage: ingest dot <dot_file> [--page <wiki_page>]")
            sys.exit(1)
        page_arg = None
        if "--page" in sys.argv:
            idx = sys.argv.index("--page")
            page_arg = sys.argv[idx + 1] if idx + 1 < len(sys.argv) else None
        ingest_dot(dot_file, page_arg)

    else:
        print(f"Unknown subcommand: {subcommand}\n")
        print(USAGE)
        sys.exit(1)


if __name__ == "__main__":
    main()
