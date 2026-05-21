from __future__ import annotations

import html
import re
import shutil
from pathlib import Path
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[1]
SITE_DIR = ROOT / "site"
OUT_DIR = ROOT / "_site"
TEMPLATE = (SITE_DIR / "template.html").read_text(encoding="utf-8")

LANGS = {
    "en": {
        "root": ROOT,
        "label": "English",
        "switch": "Tiếng Việt",
        "home": "Home",
        "guide": "Study guide",
        "search": "Search lessons",
        "placeholder": "Filter by title",
        "description": "Static reading site for the AI Agents for Beginners course.",
    },
    "vi": {
        "root": ROOT / "translations" / "vi",
        "label": "Tiếng Việt",
        "switch": "English",
        "home": "Trang chủ",
        "guide": "Hướng dẫn học",
        "search": "Tìm bài học",
        "placeholder": "Lọc theo tiêu đề",
        "description": "Website tài liệu tĩnh cho khóa học AI Agents for Beginners.",
    },
}

PUBLIC_ROOT_FILES = {"README.md", "STUDY_GUIDE.md", "SUPPORT.md"}
RUNNABLE_EXTENSIONS = {".ipynb", ".py", ".cs", ".dll", ".exe", ".env"}
ASSET_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg", ".ico"}
EXCLUDED_DIRS = {
    ".agents",
    ".devcontainer",
    ".git",
    ".github",
    "_site",
    "site",
    "tools",
    "venv",
    "__pycache__",
}

SOURCE_TO_OUTPUT: dict[tuple[str, Path], Path] = {}
LESSON_SLUGS: list[str] = []


def is_external(href: str) -> bool:
    parsed = urlsplit(href)
    return parsed.scheme in {"http", "https", "mailto", "tel"}


def split_fragment(href: str) -> tuple[str, str]:
    if "#" not in href:
        return href, ""
    base, fragment = href.split("#", 1)
    return base, "#" + fragment


def should_skip_markdown(path: Path, lang_root: Path) -> bool:
    rel = path.relative_to(lang_root)
    parts = set(rel.parts)
    if "code_samples" in parts or "code-samples" in parts:
        return True
    if rel.parts and rel.parts[0] == "translations":
        return True
    if len(rel.parts) == 1:
        return rel.name not in PUBLIC_ROOT_FILES
    return False


def output_path_for(lang: str, src: Path) -> Path:
    lang_root = LANGS[lang]["root"]
    rel = src.relative_to(lang_root)
    if rel == Path("README.md"):
        return OUT_DIR / lang / "index.html"
    if rel.name.lower() == "readme.md":
        return OUT_DIR / lang / rel.parent / "index.html"
    return OUT_DIR / lang / rel.with_suffix("") / "index.html"


def collect_sources() -> None:
    global LESSON_SLUGS
    LESSON_SLUGS = sorted(
        path.name
        for path in ROOT.iterdir()
        if path.is_dir() and re.match(r"^\d{2}-", path.name) and (path / "README.md").exists()
    )

    for lang, meta in LANGS.items():
        lang_root = meta["root"]
        for src in lang_root.rglob("*.md"):
            if any(part in EXCLUDED_DIRS for part in src.relative_to(lang_root).parts):
                continue
            if should_skip_markdown(src, lang_root):
                continue
            SOURCE_TO_OUTPUT[(lang, src.resolve())] = output_path_for(lang, src)


def first_heading(markdown: str, fallback: str) -> str:
    for line in markdown.splitlines():
        line = line.lstrip("\ufeff")
        match = re.match(r"^#\s+(.+?)\s*$", line)
        if match:
            return strip_markdown(match.group(1))
    return fallback


def strip_markdown(text: str) -> str:
    text = re.sub(r"!\[([^\]]*)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"[*_`#>]+", "", text)
    return html.unescape(text).strip()


def relative_href(from_html: Path, to_html: Path) -> str:
    rel = Path(shutil.os.path.relpath(to_html, from_html.parent)).as_posix()
    return rel.replace("index.html", "") or "./"


def lang_counterpart(lang: str, src: Path, current_out: Path) -> str:
    other = "vi" if lang == "en" else "en"
    lang_root = LANGS[lang]["root"]
    other_root = LANGS[other]["root"]
    try:
        rel = src.relative_to(lang_root)
    except ValueError:
        rel = Path("README.md")
    counterpart = other_root / rel
    target = SOURCE_TO_OUTPUT.get((other, counterpart.resolve()), OUT_DIR / other / "index.html")
    return relative_href(current_out, target)


def rewrite_local_href(lang: str, current_src: Path, current_out: Path, href: str) -> str | None:
    href = href.strip()
    if not href:
        return href
    if href.startswith("#") or is_external(href):
        return href

    base, fragment = split_fragment(href)
    target = (current_src.parent / base).resolve()

    if Path(base).suffix.lower() in RUNNABLE_EXTENSIONS:
        return None

    candidates = [target]
    if target.is_dir():
        candidates.insert(0, target / "README.md")
    elif target.suffix == "":
        candidates.insert(0, target / "README.md")

    for candidate in candidates:
        mapped = SOURCE_TO_OUTPUT.get((lang, candidate.resolve()))
        if mapped:
            return relative_href(current_out, mapped) + fragment

    if target.suffix.lower() in RUNNABLE_EXTENSIONS:
        return None

    if target.exists() and target.is_file():
        try:
            rel_to_root = target.relative_to(ROOT)
        except ValueError:
            return href
        asset_out = OUT_DIR / rel_to_root
        return Path(shutil.os.path.relpath(asset_out, current_out.parent)).as_posix() + fragment

    return href


def rewrite_image_src(current_src: Path, current_out: Path, src: str) -> str:
    src = src.strip()
    if not src or is_external(src):
        return src
    base, fragment = split_fragment(src)
    target = (current_src.parent / base).resolve()
    if not target.exists():
        return src
    try:
        rel_to_root = target.relative_to(ROOT)
    except ValueError:
        return src
    asset_out = OUT_DIR / rel_to_root
    return Path(shutil.os.path.relpath(asset_out, current_out.parent)).as_posix() + fragment


def inline_format(text: str, lang: str, current_src: Path, current_out: Path) -> str:
    placeholders: list[str] = []

    def save(value: str) -> str:
        placeholders.append(value)
        return f"\u0000{len(placeholders) - 1}\u0000"

    def code_repl(match: re.Match[str]) -> str:
        return save(f"<code>{html.escape(match.group(1))}</code>")

    text = re.sub(r"`([^`]+)`", code_repl, text)
    escaped = html.escape(text)

    def image_repl(match: re.Match[str]) -> str:
        alt = html.escape(match.group(1))
        src = html.escape(rewrite_image_src(current_src, current_out, match.group(2)))
        return save(f'<img src="{src}" alt="{alt}" loading="lazy">')

    escaped = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", image_repl, escaped)

    def link_repl(match: re.Match[str]) -> str:
        label = match.group(1)
        href = html.unescape(match.group(2))
        rewritten = rewrite_local_href(lang, current_src, current_out, href)
        if rewritten is None:
            return html.escape(strip_markdown(label))
        return save(f'<a href="{html.escape(rewritten)}">{label}</a>')

    escaped = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link_repl, escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", escaped)

    for index in range(len(placeholders) - 1, -1, -1):
        value = placeholders[index]
        escaped = escaped.replace(f"\u0000{index}\u0000", value)
    return escaped


def parse_table(lines: list[str], index: int, lang: str, src: Path, out: Path) -> tuple[str, int] | None:
    if index + 1 >= len(lines) or "|" not in lines[index] or "|" not in lines[index + 1]:
        return None
    separator = lines[index + 1].strip()
    if not re.match(r"^\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?$", separator):
        return None

    def cells(line: str) -> list[str]:
        return [cell.strip() for cell in line.strip().strip("|").split("|")]

    header = cells(lines[index])
    rows: list[list[str]] = []
    cursor = index + 2
    while cursor < len(lines) and "|" in lines[cursor] and lines[cursor].strip():
        rows.append(cells(lines[cursor]))
        cursor += 1

    parts = ["<table><thead><tr>"]
    parts.extend(f"<th>{inline_format(cell, lang, src, out)}</th>" for cell in header)
    parts.append("</tr></thead><tbody>")
    for row in rows:
        parts.append("<tr>")
        parts.extend(f"<td>{inline_format(cell, lang, src, out)}</td>" for cell in row)
        parts.append("</tr>")
    parts.append("</tbody></table>")
    return "".join(parts), cursor


def markdown_to_html(markdown: str, lang: str, src: Path, out: Path) -> str:
    lines = markdown.lstrip("\ufeff").splitlines()
    blocks: list[str] = []
    index = 0

    while index < len(lines):
        line = lines[index]

        if not line.strip():
            index += 1
            continue

        if line.startswith("```"):
            language = html.escape(line.strip().strip("`").strip())
            code_lines: list[str] = []
            index += 1
            while index < len(lines) and not lines[index].startswith("```"):
                code_lines.append(lines[index])
                index += 1
            index += 1
            class_attr = f' class="language-{language}"' if language else ""
            blocks.append(f"<pre><code{class_attr}>{html.escape(chr(10).join(code_lines))}</code></pre>")
            continue

        table = parse_table(lines, index, lang, src, out)
        if table:
            block, index = table
            blocks.append(block)
            continue

        heading = re.match(r"^(#{1,6})\s+(.+)$", line)
        if heading:
            level = len(heading.group(1))
            text = inline_format(heading.group(2), lang, src, out)
            anchor = re.sub(r"[^a-z0-9]+", "-", strip_markdown(heading.group(2)).lower()).strip("-")
            blocks.append(f'<h{level} id="{html.escape(anchor)}">{text}</h{level}>')
            index += 1
            continue

        if re.match(r"^\s*[-*_]{3,}\s*$", line):
            blocks.append("<hr>")
            index += 1
            continue

        if line.lstrip().startswith(">"):
            quote_lines: list[str] = []
            while index < len(lines) and lines[index].lstrip().startswith(">"):
                quote_lines.append(lines[index].lstrip()[1:].strip())
                index += 1
            blocks.append(f"<blockquote>{inline_format(' '.join(quote_lines), lang, src, out)}</blockquote>")
            continue

        if re.match(r"^\s*[-*+]\s+", line):
            items: list[str] = []
            while index < len(lines) and re.match(r"^\s*[-*+]\s+", lines[index]):
                item = re.sub(r"^\s*[-*+]\s+", "", lines[index]).strip()
                items.append(f"<li>{inline_format(item, lang, src, out)}</li>")
                index += 1
            blocks.append("<ul>" + "".join(items) + "</ul>")
            continue

        if re.match(r"^\s*\d+\.\s+", line):
            items = []
            while index < len(lines) and re.match(r"^\s*\d+\.\s+", lines[index]):
                item = re.sub(r"^\s*\d+\.\s+", "", lines[index]).strip()
                items.append(f"<li>{inline_format(item, lang, src, out)}</li>")
                index += 1
            blocks.append("<ol>" + "".join(items) + "</ol>")
            continue

        if line.strip().startswith("<") and line.strip().endswith(">"):
            raw_lines: list[str] = []
            while index < len(lines) and lines[index].strip():
                raw_lines.append(lines[index])
                index += 1
            raw = "\n".join(raw_lines)
            raw = rewrite_raw_hrefs(raw, lang, src, out)
            blocks.append(raw)
            continue

        paragraph: list[str] = []
        while index < len(lines) and lines[index].strip():
            if (
                lines[index].startswith("```")
                or re.match(r"^(#{1,6})\s+", lines[index])
                or re.match(r"^\s*[-*+]\s+", lines[index])
                or re.match(r"^\s*\d+\.\s+", lines[index])
            ):
                break
            paragraph.append(lines[index].strip())
            index += 1
        blocks.append(f"<p>{inline_format(' '.join(paragraph), lang, src, out)}</p>")

    return "\n".join(blocks)


def rewrite_raw_hrefs(raw: str, lang: str, src: Path, out: Path) -> str:
    def repl(match: re.Match[str]) -> str:
        quote = match.group(1)
        href = html.unescape(match.group(2))
        rewritten = rewrite_local_href(lang, src, out, href)
        if rewritten is None:
            rewritten = "#"
        return f'href={quote}{html.escape(rewritten)}{quote}'

    return re.sub(r"href=(['\"])(.*?)\1", repl, raw)


def nav_html(lang: str, current_out: Path) -> str:
    links: list[str] = []
    for slug in LESSON_SLUGS:
        src = LANGS[lang]["root"] / slug / "README.md"
        if not src.exists():
            src = ROOT / slug / "README.md"
        target = SOURCE_TO_OUTPUT.get((lang, src.resolve()))
        if not target:
            continue
        title = first_heading(src.read_text(encoding="utf-8"), slug)
        current = ' aria-current="page"' if target == current_out else ""
        href = relative_href(current_out, target)
        links.append(f'<a class="lesson-link" href="{html.escape(href)}"{current}>{html.escape(title)}</a>')
    return "\n".join(links)


def render_page(lang: str, src: Path, out: Path) -> None:
    markdown = src.read_text(encoding="utf-8")
    title = first_heading(markdown, "AI Agents Course")
    content = markdown_to_html(markdown, lang, src, out)
    asset_prefix = Path(shutil.os.path.relpath(OUT_DIR, out.parent)).as_posix()
    if asset_prefix == ".":
        asset_prefix = ""
    else:
        asset_prefix += "/"

    home_target = OUT_DIR / lang / "index.html"
    guide_target = SOURCE_TO_OUTPUT.get((lang, (LANGS[lang]["root"] / "STUDY_GUIDE.md").resolve()), home_target)

    html_doc = TEMPLATE
    replacements = {
        "lang": lang,
        "title": html.escape(title),
        "description": html.escape(LANGS[lang]["description"]),
        "asset_prefix": asset_prefix,
        "home_href": html.escape(relative_href(out, home_target)),
        "home_label": html.escape(LANGS[lang]["home"]),
        "guide_href": html.escape(relative_href(out, guide_target)),
        "guide_label": html.escape(LANGS[lang]["guide"]),
        "repo_href": "https://github.com/microsoft/ai-agents-for-beginners",
        "lang_switch_href": html.escape(lang_counterpart(lang, src, out)),
        "lang_switch_label": html.escape(LANGS[lang]["switch"]),
        "search_label": html.escape(LANGS[lang]["search"]),
        "search_placeholder": html.escape(LANGS[lang]["placeholder"]),
        "nav": nav_html(lang, out),
        "content": content,
    }
    for key, value in replacements.items():
        html_doc = html_doc.replace("{{ " + key + " }}", value)

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html_doc, encoding="utf-8")


def copy_assets() -> None:
    shutil.copytree(SITE_DIR / "assets", OUT_DIR / "assets", dirs_exist_ok=True)
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in ASSET_EXTENSIONS:
            continue
        rel = path.relative_to(ROOT)
        if any(part in EXCLUDED_DIRS for part in rel.parts):
            continue
        if rel.parts[0] == "translated_images" and (len(rel.parts) < 2 or rel.parts[1] != "vi"):
            continue
        target = OUT_DIR / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)


def write_root_redirect() -> None:
    (OUT_DIR / "index.html").write_text(
        """<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="refresh" content="0; url=en/">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>AI Agents Course</title>
    <link rel="canonical" href="en/">
  </head>
  <body>
    <p><a href="en/">Open the AI Agents Course</a></p>
  </body>
</html>
""",
        encoding="utf-8",
    )


def validate_output() -> None:
    bad_links: list[str] = []
    pattern = re.compile(r'href=["\']([^"\']+)["\']')
    for page in OUT_DIR.rglob("*.html"):
        text = page.read_text(encoding="utf-8")
        for href in pattern.findall(text):
            clean = href.split("#", 1)[0].split("?", 1)[0]
            if any(clean.endswith(ext) for ext in [".md", ".ipynb", ".py", ".cs"]):
                bad_links.append(f"{page.relative_to(OUT_DIR)} -> {href}")
    if bad_links:
        details = "\n".join(bad_links[:40])
        raise SystemExit(f"Found links to source or runnable files:\n{details}")


def main() -> None:
    if OUT_DIR.exists():
        shutil.rmtree(OUT_DIR)
    OUT_DIR.mkdir(parents=True)
    collect_sources()
    copy_assets()
    for (lang, src), out in sorted(SOURCE_TO_OUTPUT.items(), key=lambda item: str(item[1])):
        render_page(lang, src, out)
    write_root_redirect()
    validate_output()
    print(f"Built {len(SOURCE_TO_OUTPUT)} pages into {OUT_DIR}")


if __name__ == "__main__":
    main()
