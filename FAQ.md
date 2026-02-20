# Frequently Asked Questions (FAQ)

Quick answers to common questions about using this repository.

## Getting Started

### Q: I'm completely new to coding. Where do I start?

Start with [BEGINNER_START_HERE.md](BEGINNER_START_HERE.md). Follow the Week 1 daily plan exactly. Don't skip ahead or try to do multiple things at once.

### Q: What programming language should I learn first?

This repository currently focuses on **Python** because it:
- Has simpler syntax than Java/C++
- Is widely used in interviews
- Has great learning resources

If your target role requires a specific language (like Java for Android), focus on that instead.

### Q: Which track should I choose: 8-week or 12-week?

**Choose 8-week if:**
- You can dedicate 10-15 hours per week
- You have a coding background
- You have an interview scheduled soon

**Choose 12-week if:**
- You can dedicate 5-8 hours per week
- You're learning to code for the first time
- You prefer steady, sustainable progress

### Q: Do I need to complete every problem?

No. The learning paths prioritize problems by importance. Focus on the required problems for your track. Optional problems are for additional practice.

---

## Setup and Tools

### Q: What Python version should I use?

**Python 3.10 or newer.** Most code works on 3.10+. Check your version:
```bash
python --version
```

If you have an older version, download from [python.org](https://www.python.org/downloads/).

### Q: What IDE or editor should I use?

**Recommended for beginners:**
- [VS Code](https://code.visualstudio.com/) with Python extension

**Alternatives:**
- PyCharm Community Edition
- Jupyter Notebook (for exploratory learning)

See [IDE_SETUP_GUIDE.md](IDE_SETUP_GUIDE.md) for detailed setup instructions.

### Q: How do I run tests locally?

Navigate to the directory and run pytest:
```bash
# Test a specific file
pytest languages/python/problems/tests/test_core_algorithms.py

# Test all Python problems
pytest languages/python/problems/tests/

# Test a specific project
cd languages/python/projects/interview-patterns-api
pytest tests/
```

Install pytest if needed:
```bash
pip install pytest
```

### Q: Tests are failing. Is something broken?

Maybe, or maybe your solution needs adjustment. Check:
1. Are you running the test from the correct directory?
2. Did you implement the function with the exact name the test expects?
3. Check the error message — does it say "not found" or "wrong answer"?

If you believe it's a repository bug, [open an issue](https://github.com/ShamShamsw/student-interview-prep/issues/new/choose).

---

## Learning and Progress

### Q: I don't understand a problem. What should I do?

Follow this sequence:
1. Read the problem 3 times slowly
2. Write down what you know and what you need to find
3. Check [GLOSSARY.md](GLOSSARY.md) for unfamiliar terms
4. Look at the hints in the problem file
5. Try the simplest solution first (even brute force)
6. Compare with the canonical solution and understand the difference

See [LEARNING_PATH.md](LEARNING_PATH.md) section "Stuck? Troubleshoot and Re-approach" for more.

### Q: How long should I spend on one problem?

**Time limits by experience level:**
- **Beginner (solving first 20 problems):** 45-60 minutes, then check solution
- **Intermediate (solved 20-50 problems):** 30-45 minutes, then check hints
- **Advanced (preparing for interviews):** 20-30 minutes, match interview conditions

Never spend more than 60 minutes stuck without making progress.

### Q: Is it okay to look at the solution?

**Yes**, but follow this process:
1. Attempt the problem yourself first (minimum 20 minutes)
2. Read the solution, don't just copy-paste
3. Close the solution and implement it from memory
4. Solve a similar problem the next day
5. Re-solve the original problem 3 days later

Learning happens through repetition and understanding, not just seeing answers.

### Q: How do I track my progress?

Use [LEARNING_PATH_CHECKLIST.md](LEARNING_PATH_CHECKLIST.md) to check off completed items weekly.

Also do [WEEKLY_CONFIDENCE_CHECK.md](WEEKLY_CONFIDENCE_CHECK.md) to reflect on your confidence and areas for improvement.

### Q: I'm behind schedule. Should I give up?

No! Follow the catch-up protocol in [LEARNING_PATH.md](LEARNING_PATH.md):
- Keep project milestones (they're most important)
- Reduce problem count by 30% for one week
- Focus on weak topics, not random variety
- Add one extra focused session next week to recover

Consistency matters more than speed.

---

## Projects

### Q: What's the difference between "starter" and "final"?

- **starter/**: Partially complete code with TODOs for you to implement
- **final/**: Complete reference implementation

Always work in `starter/` first. Check `final/` only when stuck or to compare approaches.

### Q: Can I use the projects in my portfolio?

**Yes!** But:
1. Actually implement the starter code yourself
2. Add your own features or improvements
3. Write a clear README explaining what you built
4. Credit this repository as a learning resource

See [RESUME_AND_PORTFOLIO.md](RESUME_AND_PORTFOLIO.md) for portfolio guidance (if available).

### Q: Do I need to do all three projects?

The projects are ordered by complexity:
1. **sample-to-do-app**: Must do (teaches basics)
2. **study-session-tracker**: Recommended (reinforces concepts)
3. **interview-patterns-api** and **interview-prep-capstone**: Choose one based on your track

Completing at least 2 projects strongly recommended for interview preparation.

---

## Contributing

### Q: I found a bug. How do I report it?

[Open a bug report issue](https://github.com/ShamShamsw/student-interview-prep/issues/new?template=bug_report.yml) with:
- What you expected
- What actually happened
- Steps to reproduce
- Your environment (OS, Python version)

### Q: Can I suggest a new problem?

Yes! [Open a problem suggestion issue](https://github.com/ShamShamsw/student-interview-prep/issues/new?template=problem_suggestion.yml).

Include:
- Problem name and difficulty
- Why it's useful
- Whether you can contribute the solution

### Q: How do I contribute code?

1. Read [CONTRIBUTING.md](CONTRIBUTING.md)
2. Fork the repository
3. Create a feature branch
4. Make your changes with tests
5. Submit a pull request

Look for issues labeled `good first issue` if you're new to open source.

### Q: I want to add support for Java/C++/JavaScript. How?

That's great! Start by:
1. Opening a feature request issue to discuss the plan
2. Following the language template in [CONTRIBUTING.md](CONTRIBUTING.md)
3. Starting with 3-5 example problems to establish patterns
4. Submitting a PR for review

We welcome multi-language support.

---

## Interview Preparation

### Q: How many problems should I solve before interviewing?

**Minimum:** 40-50 problems across different topics  
**Comfortable:** 100+ problems  
**Optimal:** Quality over quantity — deeply understand 50 problems rather than rushing through 200

Focus on the problems in your learning track. They're curated for interview relevance.

### Q: Should I memorize solutions?

**No.** Memorizing doesn't help when problems have small variations.

Instead:
- Understand the pattern (two pointers, sliding window, etc.)
- Practice recognizing when to use each pattern
- Be able to derive the solution from first principles

### Q: How do I prepare for behavioral interviews?

Use [INTERVIEW_QUESTIONS.md](INTERVIEW_QUESTIONS.md) to practice common questions.

Use the STAR method:
- **S**ituation: Context
- **T**ask: Your role
- **A**ction: What you did
- **R**esult: Outcome and learning

### Q: What about system design interviews?

See [SYSTEM_DESIGN_BASICS.md](SYSTEM_DESIGN_BASICS.md) for fundamentals and practice exercises.

System design typically matters for mid-level+ roles. Junior roles focus more on coding problems.

### Q: How do I practice mock interviews?

Use [MOCK_INTERVIEW_GUIDE.md](MOCK_INTERVIEW_GUIDE.md) with three modes:
- Solo (start here)
- Peer (practice with another learner)
- Mentor (with experienced developer)

Aim for 1 mock interview per week during weeks 5-12 of your learning track.

---

## Technical Issues

### Q: pip install fails with SSL error

**On Windows:**
```bash
python -m pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org pytest
```

**Long-term fix:** Update your Python installation or certificates.

### Q: pytest not found

Make sure pytest is installed:
```bash
pip install pytest

# Verify installation
pytest --version
```

If still not found, try:
```bash
python -m pytest
```

### Q: Import errors when running tests

Make sure you're in the correct directory and the solution file exists:
```bash
# From repository root
cd languages/python/problems
python -m pytest tests/test_core_algorithms.py
```

### Q: GitHub Actions failing on my PR

Check the CI logs in your pull request. Common issues:
- Linting errors (use `black` and `flake8` to fix)
- Test failures (run `pytest` locally first)
- YAML syntax (use a YAML validator)

Fix locally, commit, and push. The CI will re-run automatically.

---

## Still Have Questions?

- Check [LEARNING_PATH.md](LEARNING_PATH.md) for detailed guidance
- Browse [existing GitHub issues](https://github.com/ShamShamsw/student-interview-prep/issues)
- [Open a question issue](https://github.com/ShamShamsw/student-interview-prep/issues/new?template=question.yml)

Happy learning! 🚀
