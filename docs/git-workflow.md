# Git & GitHub Workflow Guide

## Daily Git Workflow (Simple Version)

### Step 1: Initialize Git (Do this ONCE, first time only)

```bash
cd D:\AI_Agent_DocuMind
git init
```

### Step 2: Create GitHub Repository

1. Go to https://github.com
2. Click "New repository"
3. Name it: `documind-ai` (or any name you like)
4. **DON'T** initialize with README (we already have files)
5. Click "Create repository"
6. Copy the repository URL (e.g., `https://github.com/yourusername/documind-ai.git`)

### Step 3: Connect Local to GitHub (Do this ONCE)

```bash
git remote add origin https://github.com/yourusername/documind-ai.git
```

(Replace with your actual repository URL)

### Step 4: Daily Workflow (Do this EVERY DAY after coding)

```bash
# 1. Check what files changed
git status

# 2. Add all changes
git add .

# 3. Commit with a descriptive message
git commit -m "Day 1: Project structure setup, config.py and Gemini client"

# 4. Push to GitHub
git push -u origin main
```

(First time only: use `git push -u origin main`. After that, just `git push`)

---

## Good Commit Messages (Examples)

**Format:** `Day X: What you did`

Examples:
- `Day 1: Project structure setup, config.py and Gemini client`
- `Day 2: FastAPI app setup, health endpoint`
- `Day 3: Document parsers (PDF, DOCX, TXT)`
- `Day 4: LangChain text splitter implementation`
- `Day 5: ChromaDB integration and vector storage`

**Why good commit messages matter:**
- You can see your progress over time
- Easy to find when you added a feature
- Shows professionalism (important for interviews!)

---

## Common Git Commands You'll Use

```bash
# See what changed
git status

# See detailed changes
git diff

# Add specific file
git add app/config.py

# Add all changes
git add .

# Commit changes
git commit -m "Your message here"

# Push to GitHub
git push

# Pull latest changes (if working on multiple computers)
git pull

# See commit history
git log --oneline
```

---

## Troubleshooting

### "fatal: not a git repository"
**Solution:** Run `git init` first

### "error: failed to push"
**Solution:** Make sure you've committed first (`git commit -m "message"`)

### "Please tell me who you are"
**Solution:** Set your identity (do this once):
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### "Everything up-to-date" but you made changes
**Solution:** You forgot to `git add .` and `git commit` first!

---

## Why This Matters for Learning

1. **Version Control**: You can always go back if something breaks
2. **Portfolio**: Your GitHub becomes your portfolio
3. **Interview Prep**: Employers love seeing active GitHub activity
4. **Learning History**: See how you progressed day by day
5. **Backup**: Your code is safe on GitHub

---

## Pro Tip

At the end of each day, push your code. Even if it's incomplete or has bugs. This shows:
- Consistent work
- Learning progress
- Real-world development practices

**Remember:** Perfect code isn't the goal. Learning and progress is! 🚀

