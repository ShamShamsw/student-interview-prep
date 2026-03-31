from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote

REPO_ROOT = Path(__file__).resolve().parents[2]
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
TREE_ENTRY_RE = re.compile(r"^[\s│]*[├└]──\s+([^\s#]+)")
HEADING_RE = re.compile(r"^#{1,6}\s+(.+?)\s*$")
EXCLUDED_PARTS = {
    ".git",
    "htmlcov",
    "node_modules",
    ".venv",
    "venv",
    ".pytest_cache",
    ".ruff_cache",
}


def iter_markdown_files(root: Path) -> list[Path]:
    return sorted(
        path
        for path in root.rglob("*.md")
        if not any(part in EXCLUDED_PARTS for part in path.parts)
    )


def normalize_target(raw_target: str) -> str:
    target = raw_target.strip()
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1]
    return target


def slugify_heading(heading_text: str) -> str:
    """Build a GitHub-style markdown anchor slug from heading text."""
    slug = heading_text.strip().lower()
    # Drop inline code markers first to reduce noisy punctuation stripping.
    slug = slug.replace("`", "")
    slug = re.sub(r"[^\w\- ]", "", slug)
    slug = slug.replace(" ", "-")
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug


def collect_markdown_anchors(markdown_file: Path) -> set[str]:
    """Collect heading anchors from a markdown file, including duplicate suffixes."""
    content = markdown_file.read_text(encoding="utf-8")
    anchors: set[str] = set()
    duplicates: dict[str, int] = {}

    in_code_block = False
    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue

        match = HEADING_RE.match(stripped)
        if not match:
            continue

        heading_text = match.group(1).strip().rstrip("#").strip()
        slug = slugify_heading(heading_text)
        if not slug:
            continue

        count = duplicates.get(slug, 0)
        duplicates[slug] = count + 1

        if count == 0:
            anchors.add(slug)
        else:
            anchors.add(f"{slug}-{count}")

    return anchors


def is_ignored_target(target: str) -> bool:
    return (
        target.startswith("http://")
        or target.startswith("https://")
        or target.startswith("mailto:")
    )


def strip_fenced_code_blocks(content: str) -> str:
    """Remove fenced code blocks to avoid parsing example links as real links."""
    output: list[str] = []
    in_code_block = False
    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
        if not in_code_block:
            output.append(line)
    return "\n".join(output)


def is_probable_local_path(path_target: str) -> bool:
    """Heuristic to ignore placeholders like 'url' while keeping real file paths."""
    if path_target == "":
        return True
    return (
        "/" in path_target
        or "\\" in path_target
        or "." in path_target
        or path_target.startswith("..")
        or path_target.startswith("/")
    )


def split_target_and_fragment(target: str) -> tuple[str, str]:
    if "#" not in target:
        return target, ""
    path_part, fragment = target.split("#", 1)
    return path_part, slugify_heading(unquote(fragment).strip())


def resolve_target_path(source_file: Path, target: str) -> Path:
    clean_target = target.split("#", 1)[0].split("?", 1)[0].strip()
    clean_target = unquote(clean_target)
    if clean_target.startswith("/"):
        clean_target = clean_target[1:]
        return REPO_ROOT / clean_target
    if clean_target == "":
        return source_file
    return (source_file.parent / clean_target).resolve()


def check_markdown_links() -> list[str]:
    errors: list[str] = []
    anchor_cache: dict[Path, set[str]] = {}

    def get_anchors(path: Path) -> set[str]:
        if path not in anchor_cache:
            anchor_cache[path] = collect_markdown_anchors(path)
        return anchor_cache[path]

    for md_file in iter_markdown_files(REPO_ROOT):
        content = md_file.read_text(encoding="utf-8")
        scan_content = strip_fenced_code_blocks(content)
        for match in MARKDOWN_LINK_RE.finditer(scan_content):
            target = normalize_target(match.group(1))
            if not target or is_ignored_target(target):
                continue

            path_target, fragment = split_target_and_fragment(target)
            if not is_probable_local_path(path_target):
                continue

            resolved = resolve_target_path(md_file, target)
            if not resolved.exists():
                rel_source = md_file.relative_to(REPO_ROOT)
                errors.append(
                    f"{rel_source}: broken link '{target}' (resolved to '{resolved}')"
                )
                continue

            # Validate markdown heading fragment links when target is a markdown file.
            if fragment and (path_target == "" or resolved.suffix.lower() == ".md"):
                anchors = get_anchors(resolved)
                if fragment not in anchors:
                    rel_source = md_file.relative_to(REPO_ROOT)
                    rel_target = resolved.relative_to(REPO_ROOT)
                    errors.append(
                        f"{rel_source}: broken anchor '#{fragment}' in link '{target}' "
                        f"(target: {rel_target})"
                    )

    return errors


def parse_repository_tree_paths(structure_doc: Path) -> list[str]:
    content = structure_doc.read_text(encoding="utf-8")
    paths: list[str] = []
    stack: list[str] = []

    in_code_block = False
    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
        if not in_code_block:
            continue

        match = TREE_ENTRY_RE.match(line)
        if not match:
            continue

        prefix_match = re.match(r"^([\s│]*)[├└]──\s+", line)
        if prefix_match is None:
            continue
        prefix = prefix_match.group(1)
        depth = len(prefix) // 4

        entry = match.group(1).strip()
        # Skip intentionally grouped pseudo-entry.
        if "," in entry or "etc" in entry.lower():
            continue

        normalized_entry = entry.rstrip("/")
        if len(stack) <= depth:
            stack.extend([""] * (depth - len(stack) + 1))
        stack = stack[: depth + 1]
        stack[depth] = normalized_entry

        full_path = Path(*[segment for segment in stack[: depth + 1] if segment])
        paths.append(str(full_path).replace("\\", "/"))

    return paths


def check_repository_structure_doc() -> list[str]:
    structure_doc = REPO_ROOT / "docs" / "REPOSITORY_STRUCTURE.md"
    if not structure_doc.exists():
        return ["docs/REPOSITORY_STRUCTURE.md is missing"]

    errors: list[str] = []
    tree_entries = parse_repository_tree_paths(structure_doc)

    if not tree_entries:
        return ["docs/REPOSITORY_STRUCTURE.md: no tree entries detected"]

    for entry in tree_entries:
        normalized = entry.rstrip("/")
        target = REPO_ROOT / normalized
        if not target.exists():
            errors.append(
                f"docs/REPOSITORY_STRUCTURE.md: listed path '{entry}' does not exist"
            )

    return errors


def main() -> int:
    all_errors: list[str] = []
    all_errors.extend(check_markdown_links())
    all_errors.extend(check_repository_structure_doc())

    if all_errors:
        print("Documentation consistency checks failed:")
        for error in all_errors:
            print(f"- {error}")
        return 1

    print("Documentation consistency checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
