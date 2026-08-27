---
marp: true
theme: pach
paginate: true
title: "Software Engineering"
---

# Software Engineering

*Lecture 3*

---

## Today’s Agenda

Git

- init
- status
- add
- commit
- log
- branch
- switch / checkout

---

- Create and log in in GitHub account
- Please turn of AI

![w:606px Content Placeholder 10](assets/image2.png)

---

- Touch!

---

## Git Settings

- Let’s start by configuring Git. Every user—whether on Windows or Linux—has their own local Git settings. Here are the key commands:

```

git config --global user.name "Jacob Pach"       # Sets your name for commits
git config --global user.email "jpach@mtech.edu" # Sets your email for commits
git config --global core.editor "code --wait"    # Sets VS Code as the default editor
git config --global -e                           # Opens the global config file for editing
git config --global core.autocrlf true           # Handles line endings (important on Windows)

```

---

## Download and install warp ( Homework )

- <https://www.warp.dev/download>

![w:808px Picture 6](assets/image3.png)

---

## git config --global core.autocrlf true This Git configuration command ensures consistent handling of line endings across different operating systems. When set to true, Git automatically converts Windows-style carriage return + line feed (CRLF) to Unix-style line feed (LF) when committing, and converts back to CRLF when checking out files on Windows. This helps prevent issues caused by inconsistent line endings in collaborative projects involving multiple platforms.

- CRLF
- LF

---

## posh-git -  extension (install on your PC)

- In powershell:
- Przestalo dzialac nie wiem czemu

---

## Git init

This command initializes a new Git repository in the current directory. It creates a hidden .git folder that stores all version control data. After running git init, you can start tracking changes, committing files, and using other Git features. It’s typically the first step when starting a new project with Git.

```
.git
+---hooks
+---info
+---logs
+---objects
+---refs
|   COMMIT_EDITMSG
|   config
|   description
|   HEAD
|   index
```

```
git init
Initialized empty Git repository in ...
```

---

## Git status This command displays the current state of the working directory and staging area. It shows which files have been modified, staged for commit, or are untracked. It helps developers understand what changes are pending and whether they need to add, commit, or discard changes. It’s a key tool for tracking progress and avoiding mistakes during version control.

```
$ git status
On branch master

No commits yet

nothing to commit (create/copy files and use "git add" to track)
```

---

## git status -s – Short Status View

This command shows a condensed version of git status, making it easier to quickly scan changes. It uses symbols to indicate the state of each file:

?? – Untracked file (not added to Git yet)

A – File added to staging area

M – Modified file

D – Deleted file

R – Renamed file

Each line shows the status and the filename, making it ideal for fast reviews during development.

git status -s is especially useful when working with many files. It helps you stay focused and avoid clutter from long status messages.

```
$ git status –s

```

---

## Git Workflow: Understanding the Three Main Areas

- **Directory / Working Space**
  - This is where you actively edit files. Changes made here are not yet tracked by Git unless added to the staging area. It reflects your current work-in-progress.
- **Staging Area**
  - Also known as the index (“checkpoint”), this is a preparation zone where you place changes that you intend to commit. It allows you to selectively group changes before saving them to the repository.
- **Repository**
  - This is the permanent storage area where committed changes are saved. It contains the full history of your project and allows you to track, revert, or collaborate on code over time.

---

## Adding a file to our directory

Let's try adding a file to our directory by creating the first file, firstFile.txt, using the touch command. Then, we can check the status of our repository to see how Git tracks this new file.

- Git has detected a new file, firsFile.txt, but it is untracked, meaning it is not yet being monitored by Git.
- Git suggests using git add &lt;file&gt; to start tracking the file and include it in the next commit.
- This is a typical state right after creating a new file in a freshly initialized repository.

```
$ touch firstFile.txt
$ git status
On branch master
No commits yet
Untracked files:
  (use "git add <file>..." to include in what will be committed)
        firstFile.txt
nothing added to commit but untracked files present (use "git add" to track)
```

---

## Git Add – Wildcards and Patterns

Git allows you to use patterns to add multiple files at once. Here’s what each one does:

**git add \*.\***

Adds all files in the current directory that have a dot in their name — typically files with extensions (e.g., .txt, .js, .py). It won’t add files without extensions.

**git add \*.txt**

Adds only files with the .txt extension in the current directory. This is useful when you want to stage a specific type of file.

**git add .**

Adds all changes in the current directory and subdirectories — including new, modified, and deleted files. This is the most comprehensive option and is commonly used when you're ready to stage everything.

---

## Git Add – Be Careful with Bulk Actions

Although Git offers graphical interfaces and many conveniences — including the ability to add multiple files at once using patterns like git add . — in practice, especially early in your Git journey (and even later as a professional), it's often safer to add files individually or in a carefully reviewed list.

Why?

- Bulk adding (git add . or git add \*.txt) can easily include unintended changes.
- Mistakes in staging can lead to confusing commits or even bugs.
- While it's possible to revert to a previous commit, it’s more complex than simply taking a moment to review and add files intentionally.

---

## First commit – 'git commit'

- When you run git commit, Git opens your default text editor (like Notepad or VSC) and waits for you to enter a commit message. This message should briefly describe the changes you’re saving to the repository.
- The message is important because it becomes part of the project’s history and helps others (and your future self) understand what was changed and why.

```
$ git commit
hint: Waiting for your editor to close the file...
```

---

## Commit Message Conventions

- It’s important to be consistent in how you write commit messages. Two common styles are:
- **Present tense** (recommended):
  - Fix bug in login form
  - Add validation to email field
  - This style is preferred because it describes what the commit does to the codebase.
- **Past tense**:
  - Fixed bug in login form
  - Added validation to email field
  - This is also acceptable, but less common in collaborative projects.
- **Avoid progressive** tense (e.g., “fixing”, “adding”) because it suggests an ongoing action, not a completed change.

Use short, clear messages in the **present tense** to describe what your commit does. This keeps the project history clean and easy to read. Choose one style (present or past) and be consistent throughout your project. Most teams prefer present tense for clarity and uniformity, e.g., Add feature, Fix bug, Update README.

---

## Git Commit – Editor Message Flow

When you run git commit without the -m flag, Git opens your default text editor — in our case, Visual Studio Code (VSC) — and waits for you to write a commit message.

- The first line of the message should be short and descriptive — this is the summary that appears in logs and history.
- You can optionally add a longer description below, separated by a blank line, to explain the change in more detail.
- The rest of the file may contain comments or instructions from Git (lines starting with #). These can be left as-is or removed.
- Once you're done, save and close the file. Git will then finalize the commit and return you to the terminal.

```
Add firstFile.txt
# Please enter the commit message for your changes. Lines starting
# with '#' will be ignored, and an empty message aborts the commit.
#
# On branch master
#
# Initial commit
#
# Changes to be committed:
#	new file:   firstFile.txt
#
```

---

## Using git commit -m – Shortcut for Commit Messages

- Instead of typing git commit and opening the default editor, you can write your commit message directly in the terminal using:
- This saves time and avoids switching to the editor. The message should be short and descriptive.
- Use -m when your message is simple and clear. For longer or multi-line messages, it's better to use the editor to provide more context

```
$ git commit -m "Your commit message"
```

---

## git ls-files – List Tracked Files

This command displays all the files that Git is currently tracking in your repository. It shows the contents of the index (staging area), not the working directory. That means:

- Files listed by git ls-files are already added to Git using git add.
- Untracked files (new files not yet added) will not appear in this list.
- It’s useful for checking which files are under version control, especially in large projects.

Use git ls-files to verify which files are being tracked by Git. If a file doesn’t appear, it’s either untracked or ignored via .gitignore.

```
$ git ls-files
firstFile.txt
```

---

## git log – Commit History

This command displays the complete commit history of the repository. Each entry includes:

- The commit hash (a unique ID)
- Author name and email
- Date and time of the commit
- The full commit message
- It’s useful for reviewing detailed information about each change made to the project.

```
$ git status
On branch master
nothing to commit, working tree clean
```

```
$ git log
commit d06aafaf2cd37f5bc7cd4015656e1ae15241c996 (HEAD -> master)
Author: Jacob Pach <jpach@mtech.edu>
Date:   Thu Aug 28 20:09:17 2025 -0600

    Add firstFile.txt
```

---

## git log --oneline – Simplified View

This version shows a **condensed list** of commits, with:

- A shortened commit hash
- The first line of the commit message

It’s ideal for quickly scanning the history or identifying specific commits without all the extra details.

Use git log when you need full context, and git log --oneline when you want a quick overview. Both are essential tools for navigating and understanding your project’s history.

```
$ git log --oneline
d06aafa (HEAD -> master) Add firstFile.txt

```

---

## Removing Committed Files in Git – Important Note

- Be careful when removing files that have already been committed. If, for example, firstFile.txt is no longer needed in future commits, and you delete it manually from the repository folder, Git won’t automatically recognize this change.
- To inform Git that the file was intentionally removed, you must add the deletion using:
- This may seem counterintuitive, but it tells Git: “I want this deletion to be part of the next commit.” Once committed, the file will no longer exist in the current branch.
- Of course, you can always **restore the file** by checking out a previous commit where it still existed.
- Git tracks changes — including deletions — only when you explicitly stage them. Use git add even for removed files to make the change part of your commit history.

```
$ git add firstFile.txt
```

---

## Renaming Files in Git – Important Note

When working with Git, it's important to understand how file renaming is handled. Git does not automatically detect a rename as a single action. Instead, it treats it as:

- Deletion of the old file
- Creation of a new, untracked file

So, if you rename a file manually (e.g., from oldName.txt to newName.txt), Git will see oldName.txt as deleted and newName.txt as a new file.

- To properly reflect this change in Git, you should:
- Git doesn’t track file names — it tracks content. Renaming a file is treated as removing one and adding another. Always stage both the deletion and the new file to keep your history clean and understandable.

```
$  git add oldName.txt
$  git add newName.txt
$  git commit -m "Renamed file from oldName.txt to newName.txt"
```

---

## What is .gitignore?

The .gitignore file tells Git which files or directories to ignore — meaning they won’t be tracked, staged, or committed to the repository.

This is useful for:

- Temporary files (e.g., .log, .tmp)
- Build artifacts (e.g., bin/, obj/)
- IDE-specific files (e.g., .vscode/, .DS\_Store)
- Secrets or configuration files (e.g., .env, config.local.json)

---

## How It Works - .gitignore?

You create a file named .gitignore in the root of your repository and list patterns for files or folders you want Git to skip. Example:

Git will ignore any file or folder that matches these patterns — even if they exist in your working directory.

Use .gitignore to keep your repository clean and focused only on the files that matter. It helps avoid accidentally committing sensitive data or unnecessary clutter.

```
*.log
*.tmp
node_modules/
.env
```

---

## Understanding .gitignore – File, Not a Folder

It’s important to know that .gitignore is a file, not a folder. The naming convention comes from Linux/Unix systems, where files that start with a dot (.) are treated as hidden or configuration files.

From a Windows perspective, .gitignore may appear as a file without a name and with an extension, or simply as a special file with no extension, starting with a dot. This can be confusing at first, but it’s a common pattern in many development environments.

Examples of similar hidden/config files in Linux:

- .ssh/    – stores SSH keys and config
- .vscode/    – stores VS Code workspace settings

These dot-prefixed files and folders are used to configure tools and environments without cluttering the main workspace.

---

## What Is a Git Branch?

- A branch in Git is like a separate line of development. It allows you to work on new features, bug fixes, or experiments without affecting the main codebase. The default branch is usually called main or master.
- Branches help teams collaborate safely and efficiently by isolating changes until they’re ready to be merged.
- Think of branches as parallel timelines. You can develop safely in one branch, test your changes, and merge them back when everything works. This is a core concept in modern version control.

---

## git branch – Create a new branch

- The command git branch shows a list of all branches in your repository. The currently active branch is marked with an asterisk (\*).
- When working with a repository that has multiple branches, we can switch between them using two different commands. This is because modern versions of Git introduced standardized naming conventions, but the older commands were kept to ensure backward compatibility and to avoid forcing experienced users to relearn everything from scratch.

```
git branch new_branch
```

```
$ git switch second_branch
```

```
$ git checkout second_branch
```

---

## Branch - head

It is worth mentioning that Git stores information about branches in the .git/refs/head directory, where each file represents a local branch and contains the commit hash it points to. The currently active branch is indicated by the .git/HEAD file, which usually contains a reference like ref: refs/heads/main.

```
.git
+---hooks
+---info
+---logs
+---objects
+---refs
|   COMMIT_EDITMSG
|   config
|   description
|   HEAD
|   index
```

```
$ git status
On branch master
...
```

---

## Git status &amp; git branch Depending on the shell or terminal, Git can display additional information in the prompt, such as the current branch, whether all files are tracked, or if there are uncommitted changes. However, to check which branch you are on, you can always use the git status command or git branch without any parameters.

```
$ git branch
* master
  second
```

```
$ git status
On branch master
...
```

---

# Thank

*You!*
