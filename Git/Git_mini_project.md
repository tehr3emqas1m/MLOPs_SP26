# Git Tutorial
<img width="400" height="150" alt="Git-logo svg" src="https://github.com/user-attachments/assets/2e8094fd-9ed0-49d7-a46c-d6a5d446324b" />

---

# Git
Git is a version control system that tracks file changes and enables collaboration.

- Created by Linus Torvalds in 2005.
- Distributed version control system.
- Designed to be fast, distributed, and reliable.
- Replaced older systems like BitKeeper for Linux kernel development.
- Tracks changes to files over time.

## Key Concepts

**Repository (repo)**  
Folder containing your project and Git history.  
- Can be local (your computer) or remote (GitHub, GitLab, etc.)

**Commit**  
Snapshot of your project at a point in time.
```bash
git commit
```

**Staging area**  
Select changes before committing.
```bash
git add
```

**Branches**  
Independent lines of development.
```bash
git branch
```

- Lets you work safely without affecting main code.
- Each branch has its own commit history.
- Can be merged later.

**Merge**
```bash
git merge
```

**View changes**
```bash
git diff
```

**View history**
```bash
git log
```

**Remote repositories**
```bash
git push
git pull
```

**Undo changes**
```bash
git checkout
git reset
git revert
```

---

# The 3 States

```
Working Directory → Staging Area → Repository
     (edit)        (git add)     (git commit)
```

---

# Initial Setup

```bash
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
```

Set default branch name:

```bash
git config --global init.defaultBranch main
```

---

# Example Mini Project

## Create folder

```bash
mkdir git-intro
cd git-intro
```

## Initialize Git

```bash
git init
```

Check contents:

```bash
ls -la
```

You will see:

```
.git
```

Git stores everything here.

Example commit structure:

```
master
 ├── commit A
 ├── commit B
 └── commit C
```

---

# Create First Python Program

Create file:

```python
# hello.py
print("Welcome to Git!")
print("This is version 1")
```

Check status:

```bash
git status
```

Track file:

```bash
git add hello.py
```

Commit:

```bash
git commit -m "Initial commit - add hello.py v1"
```

Output example:

```
[master (root-commit) cc9612d] Initial commit - add hello.py v1
1 file changed, 3 insertions(+)
create mode 100644 hello.py
```

Explanation:

- master → current branch
- root-commit → first commit
- cc9612d → commit ID
- message → your description

---

# Swap Files (.swp)

Example:

```
.hello.py.swp
```

Created by editors like Vim. Usually should NOT commit.

Use `.gitignore` later to ignore them.

---

# Make First Change

Edit file:

```python
print("Welcome to Git!")
print("This is version 2 - with a new feature!")

print("This is version 2 - we added some more code!")
```

See changes:

```bash
git diff
```

Meaning:

- `+` added lines
- `-` removed lines

Commit change:

```bash
git add hello.py
git commit -m "Add user interaction"
```

---

# View History

Full history:

```bash
git log
```

Compact history:

```bash
git log --oneline
```

---

# Branching

Check current branch:

```bash
git branch
```

Create branch:

```bash
git branch new_feature
git checkout new_feature
```

Or in one command:

```bash
git checkout -b new_feature
```

Add new feature in code:

```python
print("New feature added")
```

Commit:

```bash
git add hello.py
git commit -m "Add new feature"
```

---

# Merge Branch

Switch back:

```bash
git checkout master
```

Merge:

```bash
git merge new_feature
```

Example output:

```
Updating 3e79559..b4d130a
hello.py | 3 +++
```

---

# Clean Up

Delete branch:

```bash
git branch -d new_feature
```

View final history graph:

```bash
git log --oneline --graph --all
```

---

# Summary Workflow

```
edit file
↓
git add file
↓
git commit
↓
git branch (optional)
↓
git merge (optional)
↓
git push (remote)
```

---

# Most Important Commands

```bash
git init
git status
git add file
git commit -m "message"
git log
git branch
git checkout branch
git merge branch
git push
git pull
```

---
