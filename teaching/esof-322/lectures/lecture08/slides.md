---
marp: true
theme: pach
paginate: true
footer: "ESOF 322 | Software Engineering | J. L. Pach"
title: "Software Engineering"
---

<!-- _class: lead -->

# Software Engineering

## Lecture 8

---

# Today’s Agenda

Git

- Revert
- Git Best Practices

---

# git revert

---

<!-- _class: fit-90 -->

# Practical Scenario – Restoring a Broken File Locally

**Situation:**

- You have a local branch of the project.
- You notice that **some functionality is broken**, but the problem appeared several commits ago.
- You do **not want to revert the entire history** or delete commits, because other changes were made along the way.

---

<!-- _class: fit-90 -->

# Practical Scenario – Restoring a Broken File Locally

**Solution – restoring a file from a previous commit:**

- This command retrieves the version of the file from the specified commit and places it in your working directory.
- Other files in the project remain unchanged.

```bash
git checkout <commit-id> -- path/to/file
```

---

<!-- _class: fit-90 -->

# Practical Scenario – Restoring a Broken File Locally

**Optional: check differences:**

- Compare the current state of the file (after checkout) with the latest version in the branch to see what has changed.

```bash
git diff
```

---

<!-- _class: fit-90 -->

# Practical Scenario – Restoring a Broken File Locally

**Modify and test:**

- You can edit the file in your working directory.
- Test the changes locally.

---

<!-- _class: fit-90 -->

# Practical Scenario – Restoring a Broken File Locally

**Commit the changes:**

- Creates a new commit that restores and/or fixes the file.
- The history remains intact, all previous commits are preserved.

**Effect:**

- Works similarly to git revert, but only affects specific files, not the entire commit.
- Does not require force push or rewriting history.

```bash
git add path/to/file
git commit -m "Fix broken functionality in <file>"
```

---

# Introduction to Git Revert

- git revert is used to **undo changes from a previous commit** by creating a **new commit**.
- Important: it does **not delete the original commit** – history remains intact.
- Safe for **shared branches** because it does not require --force.

---

<!-- _class: fit-90 -->

# When to Use git revert - Use Cases for git revert

- Undo a commit that **introduced a bug** without affecting later commits.
- Correct mistakes on a **shared branch** without rewriting history.
- Can revert **single commits** or a **range of commits**.

---

# How git revert Works - Mechanics of git revert

- Git calculates the changes made in the target commit.
- Creates **inverse changes** in the working directory (staging area).
- Creates a **new commit** that applies these inverse changes.
- Later commits remain unchanged.

---

# git revert - Reverting a Commit Example

- C' is a new commit that undoes changes from C.
- Commits D and earlier remain untouched.

```text
A --- B --- C --- D  (branch)
```

```bash
git revert C
```

```text
A --- B --- C --- D --- C'
```

---

# git revert - Key Points About git revert

- Creates a new commit, does not remove old commits.
- Does not require force push, safe for shared branches.
- Conflicts occur only if revert touches the same lines as later commits.
- Can be applied to single files (optional advanced usage).

---

# git revert - Comparison to Other Methods

|Method|Effect on History|Force Push Required?|Safe for Shared Branch?|
|---|---|---|---|
|git reset --hard|Rewrites history, discards commits|Yes|No|
|git commit --amend|Changes last commit locally|Yes if pushed|No|
|git revert|Adds new commit that undoes changes|No|Yes|

---

# Git Best Practices

---

<!-- _class: fit-70 -->

# Best Practices for Commits and Branching

- Small, thematic commits:
  - One commit = one logical change / one functionality / one file (or tightly related files).
- Feature or fix branches:
  - Create a new branch for each independent change or bug fix.
  - Base it on main or develop.
  - Merge or rebase back after testing.
- One file per developer (or minimal overlap):
  - Reduces the chance of merge conflicts.
  - Encourages clear ownership and accountability.
- Use revert, not reset/amend, on shared branches:
  - Revert creates a safe new commit.
  - Avoids rewriting history in a collaborative environment.

---

<!-- _class: fit-90 -->

# Consequences / Why It Matters

- Small commits make reverts safe:
  - If a commit breaks something, it can be reverted without affecting unrelated changes.
- Dedicated branches reduce conflicts:
  - Developers can work independently on different files without interfering with each other.
- One file per change / class (Python principle):
  - Mirrors good coding practices (e.g., one class per file).
  - Minimizes the probability of multiple developers editing the same file.
- Clear, readable history:
  - Easier code review and debugging.
  - Helps maintain project quality in Agile / fast-moving environments.

---

<!-- _class: caption-slide -->

# Thank You!
