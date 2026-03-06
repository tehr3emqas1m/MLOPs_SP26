# Git and GitHub Basics

This document explains the relationship between a **local Git repository** on your computer and a **remote GitHub repository**, along with the most common workflow commands.

---

## Local Repository vs GitHub Repository

| Local Repository (Git) | GitHub Repository |
|---|---|
| Stored on your computer | Stored on GitHub’s servers (cloud) |
| You work on the code directly | You push/pull changes to synchronize |
| Only accessible from your machine (unless shared) | Can be public or shared with others |
| If your hard drive fails, the data may be lost | Acts as a backup of your work |

---

## Local vs Remote Concept

```
Your Computer (Local)              GitHub (Remote/Cloud)
+-------------------+              +-------------------+
|                   |              |                   |
|  Your code        |  -- push --> |  Your code        |
|  Your commits     |  <-- pull -- |  Your commits     |
|                   |              |                   |
+-------------------+              +-------------------+
```

**Push** sends your commits from your computer to GitHub.  
**Pull** downloads the latest commits from GitHub to your computer.

---

## Cloning a Repository

When you clone a GitHub repository, you download a full copy of it to your computer.

After cloning, two copies exist:

- One on **GitHub (remote/origin)**
- One on **your computer (local)**

Changes in one location do **not automatically appear** in the other.  
You must explicitly use `push` or `pull` to synchronize them.

---

## Typical Git Workflow

```
git clone
git add
git commit
git push
git pull
git branch
git merge
```

---

# Mini Project: Working with Git and GitHub

## 1. Create a New Local Git Repository

Initialize a repository on your computer and make a few commits.

---

## 2. Create a Repository on GitHub

Create a new repository from your GitHub account.

---

## 3. Connect the Local Repository to the Remote Repository

```
git remote add origin https://github.com/tehr3emqas1m/my_repo_e.git
```

Verify the connection:

```
git remote -v
```

### Notes

- `origin` is the name of the remote repository.
- It acts as a nickname for the GitHub repository.
- A project can have multiple remotes, but usually only one is used.

---

## 4. Push Your Code to GitHub

```
git push -u origin master
```

You will be prompted for credentials:

- **Username:** Your GitHub username  
- **Password:** GitHub no longer accepts account passwords for Git operations.

Instead, you must use a **Personal Access Token (PAT)**.

---

## 5. Creating a Personal Access Token (PAT)

1. Go to GitHub and click your **profile photo → Settings**
2. Scroll down to **Developer settings**
3. Click **Personal access tokens**
4. Select **Tokens (classic)**
5. Click **Generate new token → Generate new token (classic)**
6. Give it a name (for example: `git-from-terminal`)
7. Select scope: `repo`
8. Click **Generate token**
9. Copy the token immediately (you will not be able to see it again)

When Git asks for your password, **paste the token instead**.

Your code is now stored on GitHub.

---

## 6. Make Changes and Push Updates

After modifying files:

```
git push
```

---

## 7. Clone a Repository from GitHub

Download a repository from GitHub to your computer:

```
git clone https://github.com/YOUR_USERNAME/git-intro.git git-intro-clone
```

Enter the cloned directory:

```
cd git-intro-clone
```

View commit history:

```
git log --oneline
```

---

## 8. Pull Updates from GitHub

Download the latest changes from the remote repository:

```
git pull origin master
```

---
