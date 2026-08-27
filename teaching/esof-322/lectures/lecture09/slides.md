---
marp: true
theme: pach
paginate: true
title: "Software Engineering"
---

<!-- _class: lead -->

# Software Engineering

## Lecture 9

---

# Today’s Agenda

GitHub

- SSH
- Creating repo
- Push, fetch, pull

---

- Create and log in in GitHub account
- Please turn of AI

![w:606px Content Placeholder 10](assets/image2.png)

---

# GitHub

---

# What is GitHub?

- A **cloud-based platform** for hosting Git repositories.
- Provides **collaboration tools**: pull requests, issues, code review.
- Integrates with **CI/CD**, project management, and documentation.
- Owned by **Microsoft** since 2018.

---

# Git vs GitHub

- **Git** = version control system (local).
- **GitHub** = remote hosting + collaboration features.
- GitHub uses Git under the hood.

---

# GitHub Authentication Methods

- **HTTPS**:
  - Login with **username + password** (deprecated for push).
  - Now requires **Personal Access Token (PAT)** instead of password.
- **SSH**:
  - Secure authentication using **SSH keys**.
  - Recommended for frequent use.

---

# Authentication: University vs. Home PCs

**On University Computers**

- We’ll use **HTTPS** with a **Personal Access Token (PAT)** after you sign in to the workstation with your university username and password.
- No SSH setup required on lab machines.

**On Your Home Computer**

- Run **two PowerShell commands** to start the **SSH agent**.
- **Add your SSH key** to the agent.
- Then you can **authenticate to your GitHub account over SSH**.

*Note:* The very first time you enable the SSH agent service on Windows, you may need to run PowerShell **as Administrator**.

---

# GitHub Generating SSH Keys

<https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent>

- Command(Bash):
- Default location: ~/.ssh/id\_ed25519.
- Add the public key to GitHub:
  - **Settings → SSH and GPG keys → New SSH key**.

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

---

# Adding an SSH Key to GitHub

- **Log in** to your GitHub account.
- Click your **profile icon** (top-right corner).
- Go to **Settings**.
- In the left sidebar, select **SSH and GPG keys**.
- Click **New SSH key**.
- Enter a **Title** (e.g., "My Laptop").
- Paste your **public key** (from ~/.ssh/id\_ed25519.pub).
- Click **Add SSH key**.
- Confirm with your **GitHub password** or **2FA**.

---

# Adding your SSH key to the ssh-agent

- Adding your SSH key to the ssh-agent

```powershell
Get-Service -Name ssh-agent | Set-Service -StartupType Manual
Start-Service ssh-agent
ssh-add c:/Users/YOU/.ssh/id_ed25519
```

---

# GitHub SSH Adding Multiple Devices

- Each device should have its **own SSH key**.
- Add each key separately in GitHub settings.
- Helps track and revoke access per device.

---

# How to Create a New Repository on GitHub

- **Log in** to your GitHub account.
- Click the **"+" icon** in the top-right corner.
- Select **"New repository"**.
- Enter a **Repository name** (e.g., my-project).
- (Optional) Add a **Description**.
- Choose **Public** or **Private** visibility.
- (Optional) Initialize with:
  - **README.md**
  - **.gitignore**
  - **License**
- Click **Create repository**.
- Copy the **SSH or HTTPS URL** to clone locally.

---

# From master to main – Why the Change?

**Background:**

- Historically, Git’s default branch was named **master**.
- In recent years, the term was considered **politically and socially insensitive** in some contexts.

**GitHub’s Response:**

- GitHub changed the **default branch name** to **main** for new repositories.
- This is part of an **inclusive language initiative** across the tech industry.

**What Does This Mean for You?**

- When creating new repositories on GitHub, the default branch will be **main**.
- If your local repo still uses **master**, you can rename it:

```bash
git branch -m master main
```

---

<!-- _class: caption-slide -->

# Thank You!
