---
marp: true
theme: pach
paginate: true
title: "Software Engineering"
---

# Software Engineering

*Lecture 7*

---

## Today’s Agenda

Git

- Rebase
- reset
- Common Git Scenarios and How to Handle Them

---

## Gitlens?

- extension

---

- Create and log in in GitHub account
- Please turn of AI

![Content Placeholder 10](assets/image2.png)

---

## Git Rebase vs. Merge

**Merge**

- A **merge** combines changes from one branch into another.
- Typically, we merge *into* the **main/master** branch.
- Example workflow:
  - Switch/Checkout main
  - Run git merge feature-branch
  - main now includes the changes from feature-branch
- A merge creates a **merge commit** that keeps both branch histories visible.
- Useful when you want a **complete history** of how branches diverged and then rejoined.
- A---B---C---D  (main)
- \
- E---F (feature)
- A---B---C---D---M  (main)
- \     /
- E---F

---

## Git Rebase vs. Merge

**Rebase**

- A **rebase** moves commits from one branch onto the tip of another branch.
- **Important**: You **never run rebase from main/master**.
  - Instead, you rebase your **feature branch** onto main.
- Example workflow:
  - Checkout feature-branch
  - Run git rebase main
  - Commits from feature-branch are “replayed” on top of main.
- Rebase creates a **linear history**, making it look like work happened in sequence.
- A---B---C---D  (main)
- \
- E---F (feature)
- A---B---C---D---E'---F'  (feature)

---

## Git Rebase vs. Merge - Key Differences

**Merge**

- Safe, preserves history
- Creates a merge commit
- Run from main

**Rebase**

- Rewrites history (dangerous if branch is public)
- Produces a clean, linear history
- Run from the feature branch, never from main

---

## Git Rebase vs. Merge - Rule of Thumb

- Merge when integrating finished work into main.
- Rebase when updating your feature branch to stay current with main.

It is important to remember that neither rebase nor merge deletes branches. This means that after the changes, git status will still show that these branches exist and they can still be developed further, which most often leads to chaos. That is why company policies usually recommend deleting branches that are no longer in use

---

## Introduction to git reset

**What is git reset?**

- git reset is a command that **moves references back in history**.
- It is mainly used to:
  - **Unstage files** (remove from index).
  - **Undo commits** (move the HEAD pointer back).
  - Optionally, **discard changes** in your working directory.
- **Think of it as:**

“Go back to an earlier commit or state, and decide what happens to the index and working directory.”

---

## Introduction to git reset

**Three operating modes**

The behavior of git reset depends on the option:

- **--soft**
- **--mixed (default)**
- **--hard**

---

## git reset --soft

**a) --soft**

- Moves HEAD to the target commit.
- Keeps all changes **staged** (ready to commit).
- Useful when you want to redo a commit but keep the changes staged.

Effect: last commit undone, but changes still staged.

- git reset --soft HEAD~1

---

## git reset --mixed (default)

**b) --mixed (default)**

- Moves HEAD to the target commit.
- Clears the **index (staged area)**, but keeps changes in the **working directory**.
- Default behavior if you run git reset without flags.

Effect: last commit undone, changes remain in files, but are **unstaged**.

- git reset --mixed HEAD~1

---

## git reset --hard

**c) --hard**

- Moves HEAD to the target commit.
- Clears the **index** and resets the **working directory**.
- All changes are **discarded permanently** (unless recovered via reflog).
- Effect: last commit undone, changes are lost.

Dangerous – use with caution.

- git reset --hard HEAD~1

---

## git reset - File-level usage

git reset can also be used on specific files:

Removes file from staged area.

Leaves changes in the working directory.

Equivalent to: “Unstage this file.”

- git reset HEAD filename

---

## git reset - Summary

reset moves the HEAD pointer and updates index / working directory depending on the mode.

Modes:

- --soft → keep staged.
- --mixed (default) → keep changes, unstaged.
- --hard → discard everything.

File-specific reset is a safe way to unstage files.

Use reset carefully – it can rewrite history and delete changes.

---

# Common Git Scenarios

---

## Reverting changes in a file

**Situation:** You modified a file in your branch and want to discard the changes.

- Discard changes in a **tracked file** (not yet staged):
- Discard changes that are **staged for commit**:
- git checkout – filename
- git reset HEAD filename   # Unstage
- git checkout -- filename  # Discard changes

---

## Accidentally adding files that should not be tracked

- **Situation:** You accidentally ran git add . and added files that should be ignored, e.g., compiled objects in obj/.
- **Check what’s staged and Unstage the unwanted files:**
- **Remove unwanted files from working directory** (but keep in .gitignore for the future):

**Important:** Make sure your .gitignore is correct.

- If you want to ignore obj/ folder, it should be:
- Git status
- git reset HEAD path/to/file
- git rm --cached path/to/file
- obj/

---

## Undoing a commit

- **Scenario A:** Last commit was a mistake, **you haven’t pushed yet**:
- **Scenario B:** Undo commit **after it was pushed**:
- git reset --soft HEAD~1   # Keep changes staged
- git reset --mixed HEAD~1  # Keep changes unstaged
- git reset --hard HEAD~1   # Discard changes completely
- git revert &lt;commit-id&gt;    #Safer than reset if others already pulled your changes.

---

## Modifying a commit message

- **Situation:** You want to change the last commit message **before pushing**:
- git commit --amend -m "New commit message“

---

## Recovering deleted files

- **Scenario:** A file was deleted by mistake and not committed yet:
- **Scenario B:** File was deleted in a previous commit:
- git checkout – filename
- git checkout &lt;commit-id&gt; -- filename

---

## Working with branches

- **Switching branches while having uncommitted changes**:
- Git may prevent switching if changes would be overwritten.
- Options:
  - Stash changes:
  - Or commit to a temporary branch:
- git stash
- git checkout other-branch
- git stash apply
- git checkout -b temp-branch
- git commit -m "WIP“

---

## Common mistakes

- Adding obj/ or compiled files → use .gitignore correctly and git rm --cached.
- Forgetting which files are staged → always check git status.
- Resetting without understanding → can permanently delete changes if using --hard.
- Using git stash without knowing the stack → can apply stashes to the wrong branch.

Practice these **on a test repository** first. Small mistakes in a test repo are much safer than in a “real” repo.

---

# Thank

*You!*
