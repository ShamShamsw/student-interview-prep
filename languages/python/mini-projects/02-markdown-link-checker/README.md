# Mini-Project 02: Markdown Link Checker

**Time:** 1–1.5 hours  
**Difficulty:** Easy–Medium  
**Concepts:** File I/O, regular expressions, HTTP requests, CLI arguments

---

## Objective

Build a command-line tool that scans a Markdown file (or directory of Markdown files) for links and reports which ones are broken.

This is a practical tool you could actually use on this very repository!

## Requirements

```bash
# Check a single file
python link_checker.py README.md

# Check all markdown files in a directory
python link_checker.py learn/ --recursive

# Example output
Checking learn/guides/BEGINNER_START_HERE.md...
  ✅ learn/paths/LEARNING_PATH.md (local file exists)
  ✅ https://python.org (200 OK)
  ❌ learn/old-guide.md (file not found)
  ❌ https://example.com/broken (404 Not Found)

Results: 2 OK, 2 broken
```

### Features

1. **Parse Markdown links** — extract all `[text](url)` patterns
2. **Check local links** — verify the file exists relative to the Markdown file's location
3. **Check HTTP links** — send a HEAD request and check the status code
4. **Report results** — show pass/fail for each link with the reason
5. **Exit code** — return 0 if all links are valid, 1 if any are broken

## Approach

1. Use `argparse` to handle CLI arguments (file path, `--recursive` flag)
2. Use `re.findall()` with a regex pattern to extract Markdown links
3. Classify each link: local file vs. HTTP URL
4. For local files: use `os.path.exists()` relative to the source file
5. For HTTP: use `requests.head()` with a timeout
6. Print results and exit with appropriate code

## Hints

<details>
<summary>Hint 1: Regex for Markdown links</summary>

```python
import re
pattern = r'\[([^\]]+)\]\(([^)]+)\)'
matches = re.findall(pattern, markdown_text)
# Each match is (link_text, url)
```
</details>

<details>
<summary>Hint 2: Distinguishing link types</summary>

```python
def is_url(link):
    return link.startswith('http://') or link.startswith('https://')

def is_anchor(link):
    return link.startswith('#')
```
</details>

<details>
<summary>Hint 3: Handling HTTP gracefully</summary>

```python
import requests

def check_url(url, timeout=5):
    try:
        resp = requests.head(url, timeout=timeout, allow_redirects=True)
        return resp.status_code < 400
    except requests.RequestException:
        return False
```
</details>

## Tests to Write

```python
def test_extract_links():
    text = "See [guide](docs/guide.md) and [Google](https://google.com)"
    links = extract_links(text)
    assert len(links) == 2

def test_local_file_exists(tmp_path):
    # Create a temp file and verify it's found
    (tmp_path / "test.md").write_text("hello")
    assert check_local_link(tmp_path, "test.md") is True

def test_local_file_missing(tmp_path):
    assert check_local_link(tmp_path, "nonexistent.md") is False

def test_ignores_anchor_links():
    text = "See [section](#overview)"
    links = extract_links(text)
    # Anchors should be skipped or handled separately
```

## Stretch Goals

1. Handle anchor links (`#section-name`) — verify the heading exists in the target file
2. Add `--ignore` patterns to skip specific URLs
3. Add concurrent checking with `concurrent.futures.ThreadPoolExecutor`
4. Cache results so the same URL isn't checked twice across files
5. Output results as JSON for CI integration
