# Mini-Project 05: Word Frequency Counter

**Time:** 1 hour  
**Difficulty:** Easy  
**Concepts:** Hash maps, sorting, file I/O, CLI arguments

---

## Objective

Build a command-line tool that reads text files and reports the most common words. This exercises the hash map pattern that appears in many interview problems (Two Sum, Group Anagrams, Top K Elements).

## Requirements

```bash
# Count top 10 words in a file
python word_freq.py document.txt

# Specify number of results
python word_freq.py document.txt --top 20

# Ignore common words
python word_freq.py document.txt --stop-words stop_words.txt

# Example output:
Word Frequency Report: document.txt
=====================================
   1. the          (142 occurrences)
   2. and           (98 occurrences)
   3. algorithm     (45 occurrences)
   4. function      (38 occurrences)
   5. data          (33 occurrences)
   ...
Total unique words: 847
Total words: 3,241
```

### Features

1. **Read and tokenize** a text file into words
2. **Normalize** — lowercase, strip punctuation
3. **Count** word frequencies using a dictionary
4. **Sort** and display the top N most frequent words
5. **Stop words** — optionally ignore common words (the, a, is, it, etc.)
6. **CLI** — accept arguments with `argparse`

## Approach

1. Read the file content
2. Split into words, normalize (lowercase, strip punctuation)
3. Build a frequency dictionary: `word → count`
4. Optionally filter out stop words
5. Sort by count descending (or use `collections.Counter.most_common()`)
6. Display formatted results

## Hints

<details>
<summary>Hint 1: Quick word counting</summary>

```python
from collections import Counter
words = text.lower().split()
counts = Counter(words)
top_10 = counts.most_common(10)
```
</details>

<details>
<summary>Hint 2: Stripping punctuation</summary>

```python
import re
words = re.findall(r'\b[a-z]+\b', text.lower())
# \b matches word boundaries, [a-z]+ matches one or more letters
```
</details>

<details>
<summary>Hint 3: Default stop words</summary>

```python
DEFAULT_STOP_WORDS = {
    'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been',
    'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
    'would', 'could', 'should', 'may', 'might', 'can', 'shall',
    'to', 'of', 'in', 'for', 'on', 'with', 'at', 'by', 'from',
    'it', 'its', 'this', 'that', 'and', 'or', 'but', 'not', 'no',
    'if', 'so', 'as', 'then', 'than', 'too', 'very',
}
```
</details>

## Tests to Write

```python
def test_basic_counting():
    text = "the cat sat on the mat"
    result = count_words(text)
    assert result["the"] == 2
    assert result["cat"] == 1

def test_case_insensitive():
    text = "Hello hello HELLO"
    result = count_words(text)
    assert result["hello"] == 3

def test_punctuation_stripped():
    text = "hello, world! hello."
    result = count_words(text)
    assert result["hello"] == 2
    assert "hello," not in result

def test_stop_words_filtered():
    text = "the quick brown fox and the lazy dog"
    result = count_words(text, stop_words={"the", "and"})
    assert "the" not in result
    assert result["quick"] == 1

def test_top_n():
    text = "a a a b b c"
    top = get_top_n(count_words(text), n=2)
    assert top[0] == ("a", 3)
    assert top[1] == ("b", 2)

def test_empty_input():
    result = count_words("")
    assert len(result) == 0
```

## Stretch Goals

1. Accept multiple files and combine results
2. Add a `--format json` option that outputs JSON instead of a table
3. Generate a simple bar chart using only print statements and `█` characters
4. Compare two files and show which words are unique to each
5. Add support for reading from stdin (`cat file.txt | python word_freq.py -`)
