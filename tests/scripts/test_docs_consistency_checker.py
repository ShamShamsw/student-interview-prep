from __future__ import annotations

import importlib.util
from pathlib import Path


def load_checker_module():
    repo_root = Path(__file__).resolve().parents[2]
    checker_path = repo_root / ".github" / "scripts" / "check_docs_consistency.py"
    spec = importlib.util.spec_from_file_location("check_docs_consistency", checker_path)
    assert spec is not None
    assert spec.loader is not None

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_slugify_heading_handles_punctuation_and_spaces() -> None:
    checker = load_checker_module()
    slug = checker.slugify_heading("Model Evaluation Metrics!")
    assert slug == "model-evaluation-metrics"


def test_collect_markdown_anchors_handles_duplicates(tmp_path) -> None:
    checker = load_checker_module()
    md_file = tmp_path / "sample.md"
    md_file.write_text("# Intro\n## Topic\n## Topic\n", encoding="utf-8")

    anchors = checker.collect_markdown_anchors(md_file)
    assert "intro" in anchors
    assert "topic" in anchors
    assert "topic-1" in anchors


def test_split_target_and_fragment_extracts_decoded_fragment() -> None:
    checker = load_checker_module()
    path_part, fragment = checker.split_target_and_fragment("guide.md#Quick%20Start")
    assert path_part == "guide.md"
    assert fragment == "quick-start"


def test_resolve_target_path_uses_current_file_for_fragment_only(tmp_path) -> None:
    checker = load_checker_module()
    source_file = tmp_path / "doc.md"
    source_file.write_text("# Title\n", encoding="utf-8")

    resolved = checker.resolve_target_path(source_file, "#title")
    assert resolved == source_file


def test_iter_markdown_files_excludes_vendored_paths(tmp_path) -> None:
    checker = load_checker_module()
    (tmp_path / "docs").mkdir(parents=True)
    (tmp_path / "docs" / "guide.md").write_text("# Guide\n", encoding="utf-8")
    (tmp_path / "node_modules").mkdir(parents=True)
    (tmp_path / "node_modules" / "README.md").write_text("# Vendor\n", encoding="utf-8")

    files = checker.iter_markdown_files(tmp_path)
    relative = {path.relative_to(tmp_path).as_posix() for path in files}
    assert "docs/guide.md" in relative
    assert "node_modules/README.md" not in relative


def test_strip_fenced_code_blocks_removes_example_links() -> None:
    checker = load_checker_module()
    content = """# Title

Text before.

```md
[Example](docs/guide.md)
```

[Real](README.md)
"""
    stripped = checker.strip_fenced_code_blocks(content)
    assert "docs/guide.md" not in stripped
    assert "README.md" in stripped


def test_parse_repository_tree_paths_builds_nested_paths(tmp_path) -> None:
    checker = load_checker_module()
    structure_doc = tmp_path / "REPOSITORY_STRUCTURE.md"
    structure_doc.write_text(
        """# Repository Structure

```
student-interview-prep/
├── languages/
│   ├── python/
│   │   └── problems/
│   └── javascript/
└── README.md
```
""",
        encoding="utf-8",
    )

    paths = checker.parse_repository_tree_paths(structure_doc)
    assert "languages" in paths
    assert "languages/python" in paths
    assert "languages/python/problems" in paths
    assert "languages/javascript" in paths
    assert "README.md" in paths
