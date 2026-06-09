import sys


USAGE = """Usage: python -m wiki_server.search <subcommand> [args]

Subcommands:
  rebuild              Drop and rebuild full index from wiki/*.md
  update <page_path>   Incrementally update index for one wiki page
"""


def main() -> None:
    if len(sys.argv) < 2:
        print(USAGE)
        sys.exit(1)

    subcommand = sys.argv[1]

    if subcommand == "rebuild":
        from wiki_server.search.index import rebuild_index
        rebuild_index()

    elif subcommand == "update":
        if len(sys.argv) < 3:
            print("Usage: python -m wiki_server.search update <page_path>")
            sys.exit(1)
        from wiki_server.search.index import index_page
        page_path = sys.argv[2]
        index_page(page_path)
        print(f"Updated index for: {page_path}")

    else:
        print(f"Unknown subcommand: {subcommand}\n")
        print(USAGE)
        sys.exit(1)


if __name__ == "__main__":
    main()
