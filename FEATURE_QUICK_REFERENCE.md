# 🚀 Quick Reference - New Features

## One-Line Commands

### Progress Tracking
```bash
python scripts/progress_tracker.py                              # View progress
python scripts/progress_tracker.py --detailed                   # Detailed breakdown
python scripts/progress_tracker.py --mark-complete 01-two-sum   # Mark complete
```

### Daily Challenges
```bash
python scripts/daily_challenge.py                               # Today's challenge
python scripts/daily_challenge.py --difficulty Easy             # Easy challenge
python scripts/daily_challenge.py --topic arrays                # Topic-specific
python scripts/daily_challenge.py --complete 01-two-sum --success  # Mark done
```

### Achievements
```bash
python scripts/achievements.py                                  # View achievements
python scripts/achievements.py --next                           # Next goals
python scripts/achievements.py --export badges.md               # Export badges
```

### Visualization
```bash
# Terminal
python scripts/visualize.py two-sum --array "[2,7,11,15]" --target 9
python scripts/visualize.py binary-search --array "[1,2,3,4,5]" --target 3
python scripts/visualize.py merge-sort --array "[5,2,8,1,9]"

# Web (open in browser)
open visualizer.html
```

### Hints
```bash
python scripts/hints.py 01-two-sum                             # First hint
python scripts/hints.py 01-two-sum --level 3                   # Level 3 hint
python scripts/hints.py 01-two-sum --all                       # All hints
```

### Code Analysis
```bash
python scripts/analyze_code.py solutions/01-two-sum.py         # Analyze file
python scripts/analyze_code.py solutions/ --all                # Analyze all
python scripts/analyze_code.py solutions/35-coin-change.py --detailed  # Detailed
```

### JavaScript
```bash
cd languages/javascript
npm install                                                     # Setup
npm test                                                        # Run all tests
npm test -- 01-two-sum                                          # Specific test
npm run lint                                                    # Check style
```

---

## Feature Comparison

| Feature | Purpose | Best For |
|---------|---------|----------|
| **Progress Tracker** | Visual progress & streaks | Daily motivation |
| **Daily Challenge** | Personalized problems | Consistent practice |
| **Achievements** | Gamification & goals | Long-term motivation |
| **Visualizer** | See algorithms in action | Understanding concepts |
| **Hints** | Progressive help | When stuck |
| **Code Analyzer** | Solution quality feedback | Improvement |
| **JavaScript** | Alternative language | Frontend devs |

---

## Keyboard Shortcuts

### Progress Tracker
- `Ctrl+C` to stop during display

### Visualizer (HTML version)
- Click "Visualize" to start
- Change speed dropdown for faster/slower animation
- Select different algorithms from dropdown

---

## Tips & Tricks

1. **Chain commands** for efficiency:
   ```bash
   python scripts/daily_challenge.py && python scripts/hints.py $(grep -oP 'problem_id: \K\S+' .daily_challenge.json)
   ```

2. **Alias common commands** (add to `.bashrc` or `.zshrc`):
   ```bash
   alias progress='python scripts/progress_tracker.py'
   alias challenge='python scripts/daily_challenge.py'
   alias achieve='python scripts/achievements.py'
   ```

3. **Create a morning routine script**:
   ```bash
   python scripts/progress_tracker.py
   python scripts/achievements.py --next
   python scripts/daily_challenge.py
   ```

4. **Use watch mode** for JavaScript tests:
   ```bash
   cd languages/javascript && npm run test:watch
   ```

---

## Troubleshooting

### Progress not updating?
```bash
python scripts/progress_tracker.py --mark-complete <problem-id>
```

### Visualizer not working?
- Ensure Python 3.10+
- Check terminal supports colors
- For HTML: Use modern browser (Chrome, Firefox, Edge)

### Hints not showing?
```bash
python scripts/hints.py --list  # Check available problems
```

### Code analyzer errors?
```bash
# Make sure file exists and is valid Python
python -m py_compile <file>
```

---

## Integration Ideas

### Git Hooks
Add to `.git/hooks/pre-commit`:
```bash
#!/bin/bash
python scripts/analyze_code.py languages/python/problems/solutions/ --all
```

### VS Code Tasks
Add to `.vscode/tasks.json`:
```json
{
  "label": "Daily Challenge",
  "type": "shell",
  "command": "python scripts/daily_challenge.py"
}
```

### Automated Reminders
Use cron (Linux/Mac) or Task Scheduler (Windows):
```bash
0 9 * * * cd ~/interview-prep && python scripts/daily_challenge.py
```

---

Need more help? See [NEW_FEATURES.md](NEW_FEATURES.md) for detailed guides!
