"""
Convert all Mermaid diagrams in wiki markdown files to DOT + SVG.

Reads every ```mermaid code fence from wiki/*.md, converts to Graphviz
DOT, renders SVG, and replaces the fence with an image reference.
"""

import re
from pathlib import Path

import graphviz

WIKI_DIR = Path(__file__).resolve().parent.parent / "wiki"
ASSETS_DIR = WIKI_DIR / "assets"
DIAGRAMS_DIR = WIKI_DIR / "diagrams"
MERMAID_PATTERN = re.compile(
    r"^```mermaid\n(.+?)\n```", re.MULTILINE | re.DOTALL
)

ALLOWED_DIRECTIONS = {"LR", "RL", "TB", "BT", "TD"}


def slugify(text: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")
    return re.sub(r"_+", "_", s)


def node_id(raw: str) -> str:
    nid = re.sub(r"[^a-zA-Z0-9_]", "_", raw.strip())
    nid = re.sub(r"_+", "_", nid)
    nid = nid.strip("_")
    if not nid or nid[0].isdigit():
        nid = "n" + nid
    return nid


def escape_dot_label(text: str) -> str:
    text = text.replace("\\", "\\\\")
    text = text.replace('"', '\\"')
    text = text.replace("\n", "\\n")
    text = text.replace("<br/>", "\\n")
    text = text.replace("<br />", "\\n")
    return text


def find_matching_bracket(s: str, start: int, open_ch: str, close_ch: str) -> int:
    depth = 1
    for i in range(start, len(s)):
        if s[i] == open_ch:
            depth += 1
        elif s[i] == close_ch:
            depth -= 1
            if depth == 0:
                return i
    return -1


def parse_node_spec(spec: str):
    spec = spec.strip()
    if not spec:
        return None

    patterns = [
        ("]", "[", "box", None),
        ("}", "{", "diamond", None),
        (")", "(", "box", "rounded"),
    ]

    for close_ch, open_ch, shape, style in patterns:
        idx = spec.find(open_ch)
        if idx != -1:
            close_idx = find_matching_bracket(spec, idx + 1, open_ch, close_ch)
            if close_idx != -1:
                nid = spec[:idx].strip()
                label = spec[idx + 1 : close_idx].strip()
                return nid, label, shape, style

    return None


def parse_edge_line(stripped: str):
    stripped = stripped.strip()
    if not stripped:
        return None

    arrow_patterns = ["-->|", "---|", "-->", "---", "-.->", "==>"]

    for arrow_sym in arrow_patterns:
        idx = stripped.find(arrow_sym)
        if idx == -1:
            continue

        lhs = stripped[:idx].strip()
        rest = stripped[idx + len(arrow_sym) :].strip()

        elabel = ""
        rhs = rest

        if arrow_sym.endswith("|"):
            if "|" in rest:
                pipe_idx = rest.index("|")
                elabel = rest[:pipe_idx].strip()
                rhs = rest[pipe_idx + 1 :].strip()
        elif rest.startswith("|"):
            pipe_close = rest.find("|", 1)
            if pipe_close != -1:
                elabel = rest[1:pipe_close].strip()
                rhs = rest[pipe_close + 1 :].strip()

        return lhs, arrow_sym.rstrip("|"), elabel, rhs

    return None


def convert_mermaid_to_dot(mermaid_source: str) -> str | None:
    lines = mermaid_source.split("\n")
    if not lines:
        return None

    header = lines[0].strip()
    is_sequence = header == "sequenceDiagram"
    is_graph = header.startswith("graph ") or header.startswith("flowchart ")

    if not is_graph and not is_sequence:
        return None

    rankdir = "LR"
    if is_graph:
        parts = header.split()
        if len(parts) >= 2:
            direction = parts[1].upper()
            if direction in ALLOWED_DIRECTIONS:
                if direction == "TD":
                    rankdir = "TB"
                else:
                    rankdir = direction

    dot_lines = []
    declared_nodes = set()

    if is_sequence:
        dot_lines.append("digraph G {")
        dot_lines.append("    rankdir=LR;")
        dot_lines.append("    node [shape=box, style=rounded];")
        dot_lines.append("    edge [fontsize=10];")
        participants = {}
        for line in lines[1:]:
            stripped = line.strip()
            if stripped.startswith("participant "):
                rest = stripped[len("participant "):].strip()
                if " as " in rest:
                    p_parts = rest.split(" as ", 1)
                    pid = p_parts[0].strip()
                    pname = p_parts[1].strip()
                else:
                    pid = rest
                    pname = rest
                pnode = node_id(pid)
                participants[pid] = pnode
                dot_lines.append(f'    {pnode} [label="{escape_dot_label(pname)}"];')
                declared_nodes.add(pnode)
        for line in lines[1:]:
            stripped = line.strip()
            if "->>" in stripped:
                parts = re.split(r"->>+", stripped)
                if len(parts) >= 2:
                    src = parts[0].strip().strip(":")
                    rest = parts[1].strip()
                    label = ""
                    if ":" in rest:
                        idx = rest.index(":")
                        dst = rest[:idx].strip()
                        label = rest[idx + 1:].strip()
                    else:
                        dst = rest
                    snode = node_id(src)
                    dnode = node_id(dst)
                    elabel = f' [label="{escape_dot_label(label)}"]' if label else ""
                    dot_lines.append(f"    {snode} -> {dnode}{elabel};")
        dot_lines.append("}")
        return "\n".join(dot_lines)

    dot_lines.append("digraph G {")
    dot_lines.append(f"    rankdir={rankdir};")
    dot_lines.append("    node [fontsize=11];")
    dot_lines.append('    edge [fontsize=10, arrowhead=normal];')

    subgraph_stack = 0

    def indent():
        return "    " * (1 + subgraph_stack)

    def decl_node(nid, label, shape, style):
        nonlocal dot_lines
        normalized = node_id(nid)
        if normalized in declared_nodes:
            return
        declared_nodes.add(normalized)
        attr = f'label="{escape_dot_label(label)}"'
        if shape == "diamond":
            attr += ", shape=diamond"
        elif style == "rounded":
            attr += ', shape=box, style="rounded"'
        else:
            attr += ", shape=box"
        dot_lines.append(f'{indent()}{normalized} [{attr}];')

    for line in lines[1:]:
        stripped = line.strip()
        if not stripped or stripped.startswith("%%") or stripped.startswith("#"):
            continue

        if stripped.startswith("subgraph "):
            sname = stripped[len("subgraph "):].strip()
            cname = f"cluster_{slugify(sname)}" if sname else "cluster_unknown"
            dot_lines.append(f'{indent()}subgraph {cname} {{')
            dot_lines.append(f'{indent()}    label="{escape_dot_label(sname)}";')
            dot_lines.append(f'{indent()}    style="rounded";')
            subgraph_stack += 1
            continue

        if stripped == "end" and subgraph_stack > 0:
            subgraph_stack -= 1
            dot_lines.append(f"{indent()}}}")
            continue

        parsed = parse_edge_line(stripped)
        if parsed is not None:
            lhs, arrow, elabel, rhs = parsed

            lhs_node = parse_node_spec(lhs)
            if lhs_node:
                lid, llab, lsh, lst = lhs_node
                decl_node(lid, llab, lsh, lst)
            else:
                lid = node_id(lhs)
                if lid not in declared_nodes:
                    decl_node(lid, lhs, "box", None)

            rhs_node = parse_node_spec(rhs)
            if rhs_node:
                rid, rlab, rsh, rst = rhs_node
                decl_node(rid, rlab, rsh, rst)
            else:
                rid = node_id(rhs)
                if rid not in declared_nodes:
                    decl_node(rid, rhs, "box", None)

            dir_none = ""
            if arrow == "---":
                dir_none = ", dir=none"
            elif arrow == "-.->":
                dir_none = ", style=dashed"
            elif arrow == "==>":
                dir_none = ", style=bold"

            lid_norm = node_id(lid)
            rid_norm = node_id(rid)

            if elabel:
                eattr = f'label="{escape_dot_label(elabel)}"{dir_none}'
                dot_lines.append(f'{indent()}{lid_norm} -> {rid_norm} [{eattr}];')
            elif dir_none:
                dot_lines.append(f'{indent()}{lid_norm} -> {rid_norm}[{dir_none.lstrip(", ")}];')
            else:
                dot_lines.append(f'{indent()}{lid_norm} -> {rid_norm};')
            continue

        node_parsed = parse_node_spec(stripped)
        if node_parsed:
            nid, label, shape, style = node_parsed
            decl_node(nid, label, shape, style)

    dot_lines.append("}")
    return "\n".join(dot_lines)


def main():
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    DIAGRAMS_DIR.mkdir(parents=True, exist_ok=True)

    md_files = sorted(WIKI_DIR.rglob("*.md"))
    total_converted = 0
    total_errors = 0

    for md_file in md_files:
        content = md_file.read_text(encoding="utf-8")
        matches = list(MERMAID_PATTERN.finditer(content))
        if not matches:
            continue

        rel_path = md_file.relative_to(WIKI_DIR)
        base = rel_path.with_suffix("").as_posix().replace("/", "-")
        replaced_content = content
        offset = 0

        for idx, match in enumerate(matches, 1):
            mermaid_src = match.group(1)
            slug = f"{base}-diagram-{idx}"

            dot_source = convert_mermaid_to_dot(mermaid_src)
            if dot_source is None:
                print(f"  SKIP {rel_path} diagram {idx}: unsupported type")
                continue

            dot_path = DIAGRAMS_DIR / f"{slug}.dot"
            svg_path = ASSETS_DIR / f"{slug}.svg"

            dot_path.write_text(dot_source, encoding="utf-8")

            try:
                src_obj = graphviz.Source(dot_source)
                svg_data = src_obj.pipe(format="svg").decode("utf-8")
            except Exception as e:
                print(f"  ERROR {rel_path} diagram {idx}: {e}")
                total_errors += 1
                continue

            svg_path.write_text(svg_data, encoding="utf-8")
            print(f"  OK   {slug}")

            new_fence = f'![{slug}](/assets/{slug}.svg)'
            start = match.start() + offset
            end = match.end() + offset
            replaced_content = (
                replaced_content[:start]
                + new_fence
                + replaced_content[end:]
            )
            offset += len(new_fence) - (match.end() - match.start())
            total_converted += 1

        md_file.write_text(replaced_content, encoding="utf-8")
        print(f"{rel_path}: {len(matches)} diagram(s) converted")

    print(f"\nDone: {total_converted} diagrams converted, {total_errors} errors")


if __name__ == "__main__":
    main()
