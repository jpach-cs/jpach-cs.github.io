---
marp: true
theme: pach
paginate: true
footer: "CSCI 112 | Programming with C |  J. L. Pach"
backgroundColor: "#fdfaf3"
title: "CSCI 112"
---

<!-- _class: lead -->

<!-- _paginate: skip -->

# CSCI 112

## Programming with C

### Laboratory: 01

J. L. Pach

---

# Outline:

- Guide and rules
- File System Hierarchy
- CLI
- Console - Asignment 01
- Toolchains etc.
- Practical Exercise
- How to get Visual Studio Code

<!--
TUTAJ WPISZ TO, CO CHCESZ POWIEDZIEĆ:
- Przywitaj studentów CSCI 112.
- Podkreśl, że IDE to nie tylko edytor, ale cały ekosystem.
- Wspomnij o debuggerze jako narzędziu, które oszczędza godziny pracy.
-->

---

<!-- _class: caption-slide -->

<!-- _paginate: skip -->

# Guide

## and rules

<!--
## Subtitle
-->

---

# ANSI(C89) vs C99

<div class="justify">

- Last years, the course was taught using the oldest and most widely adopted ANSI standard — C89. This choice was made because C89 does not include many of the conveniences introduced in later versions. While these conveniences make life easier for professional programmers, they can make it harder for beginners to fully grasp the fundamentals of programming in C.

- The standard now used in our classes is **C99**, which is widely applied in embedded systems, especially in the field of electronics. This standard significantly lowers the entry barrier for beginners (for example, allowing variable declarations inside a for loop and supporting single-line comments //), while avoiding the complex and sometimes confusing features introduced in newer standards.

</div>

---

<div class="justify">

# Grading Breakdown

The final course grade will be determined by two equally weighted components:

- Lecture Component: 40%
- Laboratory Component: 60%

The Laboratory Component is evaluated according to the following criteria:

- Entrance Quiz: 30%
- Assignments: 40%
- Brief Concluding Quiz: 30%

Not every laboratory session will necessarily include an entrance quiz or a concluding quiz. When scheduled, these assessments will count toward the corresponding laboratory component.

</div>

---

<div class="justify">

# In-Person Format

This is strictly an in-person course. Regular attendance and active participation are expected.

## Attendance Policy

- Attendance at every class is required.
- Students are allowed up to two unexcused absences during the semester without penalty.

**Each additional unexcused absence beyond this two-absence allowance will result in a 1 percentage-point deduction from the final course grade.**

</div>

---

<div class="justify lh-20">

# Excused Absences & Emergencies

- Official university-excused absences, university-sanctioned activities, serious personal emergencies, and documented medical circumstances will not count toward the unexcused absence allowance.
- Students should notify the instructor as soon as reasonably possible when an emergency or officially excused absence occurs.

</div>

---

<div class="justify lh-25">

# Laboratory Rules

## Entrance Quiz

- When an entrance quiz is scheduled, it will consist of three questions.
- A score of at least 2 out of 3 is required to pass.
- A failed entrance quiz may be retaken up to two times during the semester. Only failed entrance quizzes may be retaken.

</div>

---

<div class="justify">

# Assignments & Deadline

- Students will have six calendar days to complete and submit each assignment.
- The deadline is strict. Once the six-day submission period has closed, the normal submission path will be closed and late or makeup submissions will not be accepted, except where an official University policy, documented emergency, or approved accommodation requires otherwise.
- Students are responsible for submitting their work before the deadline. Students should not wait until the final minutes before the deadline to submit an assignment.

## Brief Concluding Quiz

- When scheduled, the concluding quiz is a short summative assessment covering the material addressed during the laboratory session.

</div>

---

<div class="justify">

# Code Formatting, Authorship & Declaration

- Every submitted source file must begin with exactly four lines of comments containing the required authorship declaration.
- The following template must be used:

```c
// Your Name
// CSCI 112 Fall 2026
// Programming Assignment #1
// I declare that I am the author of this work, take full responsibility for it, and have disclosed any material external assistance.
```

</div>

---

<div class="justify">

# Authorship Requirement

- The four-line declaration is **mandatory**.
- A source file submitted without the required declaration will receive **0 points**.
- If a student submits an assignment before the deadline but accidentally omits the required declaration, the instructor may allow the student to resubmit **the same code with the declaration added** after the deadline as a correction of an administrative omission.
- This correction is limited strictly to adding the required declaration. No modification, improvement, debugging, or other change to the submitted code is permitted after the original deadline.
- Repeated failure to include the required declaration may be treated as failure to comply with the assignment requirements.

</div>

---

# Academic Integrity, Collaboration & External Resources

<div class="justify">

Students are encouraged to use appropriate external resources to learn and solve problems. Such resources may include:

- textbooks and other books;
- official programming documentation;
- technical websites and documentation;
- Stack Overflow and similar technical resources;
- ChatGPT, Gemini, GitHub Copilot, and other AI-assisted tools.

**The use of an external resource does not, by itself, constitute academic misconduct.** However, students remain fully responsible for the work they submit.

</div>

---

<div class="justify">

# Disclosure of External Assistance

- Students must disclose **material external assistance** that contributed to their submitted work.
- Such assistance may include, but is not limited to, substantial assistance from another person, technical resources, or generative AI tools.
- The disclosure should be made in an appropriate comment in the source code.

For example:

```
// I used the C standard library documentation to verify the behavior of strtok().
```

or:

```
// I used ChatGPT to help explain pointer arithmetic.
// I wrote, tested, and verified the submitted implementation myself.
```

</div>

---

# Disclosure of External Assistance

<div class="justify lh-30">

The purpose of this requirement is not to prohibit the use of external resources. Its purpose is to ensure that the origin of significant assistance is honestly acknowledged.
Students are **not required to document ordinary searches or routine consultation of documentation** that do not materially contribute to the submitted work.

</div>

---

# Responsibility for Submitted Work

- Regardless of what resources were used during the development process, each student is fully responsible for understanding the work submitted under their name.
- Assignments may be reviewed orally by the instructor.
- During such a review, the instructor may ask the student to:
  - explain specific lines of code, how an algorithm works;
  - explain why a particular implementation was chosen;
  - predict what the program will do for a particular input;
  - identify or explain an error;
  - modify part of the submitted code;
  - demonstrate the operation of the submitted program.

---

<div class="justify lh-20">

# Responsibility for Submitted Work

The purpose of such a review is to establish that the student understands and is responsible for the submitted work.
A student's inability to explain substantial portions of submitted work, particularly after reasonable questioning and clarification, may be considered as evidence when determining whether the work was genuinely authored by the student. Such evidence will be evaluated together with the other available evidence in accordance with the Montana Tech Student Code of Conduct.

</div>

---

# Declaration of Responsibility

By submitting an assignment, the student declares that:

1. I am the author of the work I am submitting.
2. I have disclosed any material external assistance used in preparing this work.
3. I understand the code and other work that I am submitting.
4. I take full responsibility for the submitted work.
5. I understand that submitting work that is not my own, or concealing material external assistance, may constitute academic misconduct and may be referred to the appropriate University authority.

**The four-line source-file declaration constitutes the student's acknowledgment of these requirements.**

---

# University Accommodations

<div class="justify lh-20">

- Students who require academic accommodations should work directly with Montana Tech Disability Services and provide the appropriate documentation to the instructor as soon as possible.
- Approved accommodations will be provided in accordance with University policy.

</div>

---

<!-- _class: caption-slide -->

<!-- _paginate: skip -->

# File System

## Hierarchy

---

# File System Hierarchy - Windows

![Windows h:520](win.svg)

---

# File System Hierarchy - Linux

![Linux h:520](lin.svg)

---

# File System Hierarchy - Comparison

![Windows h:450](win2.svg) ![Linux h:450](lin2.svg)

1. Files of user , 2. Apps of user, 3. External devices e.g. pendrive

---

<div class="justify lh-10">

# Differences in File Hierarchy

## Windows - My Computer concept:

- Provides a graphical view of all available drives and partitions, including the system drive (usually C:), external drives, network drives, etc.

- System drive (C:):
  - Typically, the main drive where the Windows operating system and most programs are installed.

- Peripherals:
  - Each peripheral device (e.g., USB drive, external hard drive) is usually visible as a separate entity in "My Computer".

</div>

---

<div class="justify lh-10">

# Differences in File Hierarchy

## Linux

**Root directory (/):**

- This is the starting point for the entire file hierarchy. All files and directories are located directly or indirectly within the root directory.

**Directory hierarchy:**

- The directory structure is more consistent and logical. Each directory has a specific purpose (e.g., /etc for configuration files, /home for user home directories).

**Peripheral devices in /media or /mnt:**

- When a peripheral device is connected, the system automatically creates a mount point for it in the /media or /mnt directory.

</div>

---

# Summary of differences

| Feature | Windows | Linux |
| --- | --- | --- |
| Main concept | "My Computer" | Root directory (/) |
| System drive | C: | Usually no direct equivalent, system files are scattered across various directories |
| Peripherals | Visible as separate entities | Mounted in /media or /mnt |
| Structure | Less formal, more visual | Formal, hierarchical, based on conventions |

---

# Summary of differences

<div class="justify lh-20">

Why are there such differences?

- **History:** Windows was created as an operating system for home computers, with a more user-friendly interface. Linux, on the other hand, has its roots in the server environment, where consistency and efficiency are more important.
- **Philosophy:** Linux places a greater emphasis on standards and consistency, as reflected in its file hierarchy. Windows, on the other hand, offers a more intuitive interface that may be easier for novice users.

</div>

---

<!-- _class: caption-slide -->

<!-- _paginate: skip -->

# CLI

## (Command-Line Interface)

---

<div class="justify lh-20">

# CLI

A command-line interface (CLI), also known as a command-line shell, is a means of interacting with software via commands – each formatted as a line of text.

```powershell
Windows PowerShell
Copyright (C) Microsoft Corporation. All rights reserved.

Install the latest PowerShell for new features and improvements! https://aka.ms/PSWindows

PS C:\Users\Jacob> cd .\Desktop\
PS C:\Users\Jacob\Desktop> ls
PS C:\Users\Jacob\Desktop>
```

</div>

---

# Navigating the Command Line: Windows

## From the Start menu:

1. Click the Start button in the lower left corner of the screen.
2. Type `cmd` and press Enter.

## From the Run dialog box

1. Simultaneously press the Windows key and R.
2. In the opened window, type `cmd` press Enter.

```powershell
Microsoft Windows [Version 10.0.22631.4602]
(c) Microsoft Corporation. All rights reserved.
C:\Users\Jacob> whoami
notebooki7\Jacob
C:\Users\Jacob>
```

---

# Navigating the Command Line: Linux

## From the Start menu:

1. Click the Start button in the lower left corner of the screen.
2. Click the Accessories.
3. Click the Terminal.

## Keyboard shortcut:

1. The most commonly used shortcut is Ctrl+Alt+T.

```bash
jacob@raspberrypi:~ $ pwd
/home/jacob
jacob@raspberrypi:~ $
```

---

# Navigating the Command Line

## Shell

### Windows:

- **Cmd:** The most commonly used command to open the command prompt.
  To obtain the username and device name, we use the whoami command.

### Linux:

- **Terminal:** A generic term for the window where commands are typed.
  To obtain the current directory path, we use the pwd command.

### Notes:

- **Up/down arrows:** Browse command history.
- **Tab:** Autocompletes filenames, directories, and commands.

---

# Differences in Command Prompt Messages

## Between Windows and Linux

### Windows

- **Default message:** Typically displays the full path to the currently open directory.
- **Example:** `C:\Users\User\Documents>`
- **Purpose:** Provides the exact location of the user within the file system hierarchy.

### Linux

- **Default message:** Most often presents the username and hostname (device name).
- **Example:** `user@computer:~$`
- **Purpose:** Informs about the currently logged-in user and the machine they are working on.

---

# Basic Navigation and Directory Management

<div class="columns justify">

<div class="card">

## Windows:

- `dir`: Lists files and directories in the current directory.
- `cd`: Changes the current directory.
- `cd..`: Moves up one directory level.

</div>

<div class="card">

## Linux:

- `ls`: Lists files and directories in the current directory.
- `cd`: Changes the current directory.
- `cd ..`: Moves up one directory level.

</div>

</div>

Notes:

- Both `dir` and `ls` are used to list directory contents in both different systems.
- In Linux, `cd ..` **requires a space between the dots, Windows does not.**

---

# Example 1 - `dir`,`ls`

<div class="columns">

<div class="card">

`dir`: Lists files and directories in the current directory.

```powershell
C:\Users\Jacob>dir
12/19/2024  12:14 PM    <DIR>          .
09/05/2023  09:06 AM    <DIR>          ..
10/05/2022  11:55 PM    <DIR>          Contacts
01/04/2025  08:29 AM    <DIR>          Desktop
09/07/2024  08:51 AM    <DIR>          Documents
01/03/2025  05:47 PM    <DIR>          Downloads
               4 File(s)            818 bytes
              42 Dir(s)  62,825,164,800 bytes free
C:\Users\Jacob>ls
ls
'ls' is not recognized as an internal or external command,
operable program or batch file.
C:\Users\Jacob>
```

</div>

<div class="card">

`ls`: Lists files and directories in the current directory.

```bash
jacob@raspberrypi:~ $ ls
Bookshelf  Desktop  Documents  Downloads  Music
Pictures  Public  Templates  Videos
jacob@raspberrypi:~ $ dir
Bookshelf  Desktop  Documents  Downloads  Music
Pictures  Public  Templates  Videos
jacob@raspberrypi:~ $


```

</div>

</div>

---

# Example 2 - `cd`, `cd..`

<div class="columns">

<div class="card">

## Windows

- `cd`: Changes the current directory.
- `cd..`: Moves up one directory level.

```powershell
C:\Users\Jacob>cd Desktop
C:\Users\Jacob\Desktop>cd..
C:\Users\Jacob>cd Desktop
C:\Users\Jacob\Desktop>cd ..
C:\Users\Jacob>cd /
C:\>
```

</div>

<div class="card">

## Linux

- `cd`: Changes the current directory.
- `cd ..`: Moves up one directory level.

```bash
jacob@raspberrypi:~ $ cd Desktop
jacob@raspberrypi:~/Desktop $ cd ..
jacob@raspberrypi:~ $ cd Desktop
jacob@raspberrypi:~/Desktop $ cd..
-bash: cd..: command not found
jacob@raspberrypi:~/Desktop $ cd /
jacob@raspberrypi:/ $ pwd
/
jacob@raspberrypi:/ $
```

</div>

</div>

---

# Text Manipulation and Output

## Windows:

`echo`: Displays a message on the screen.

## Linux:

`echo`: Displays a message on the screen.

**Note**: Both `echo` commands have similar functionality, but there might be slight variations in options and behavior.

---

# Example 3 - `echo`

`echo`: Displays a message on the screen.

<div class="columns">

<div class="card">

## Windows

```powershell
C:\Users\Jacob>echo Hello World!
Hello World!
C:\Users\Jacob> echo "Hello World!"
"Hello World!"
C:\Users\Jacob>echo.

C:\Users\Jacob>echo
ECHO is on.
C:\Users\Jacob>

```

</div>

<div class="card">

## Linux

```bash
jacob@raspberrypi:~ $ echo Hello World!
Hello World!
jacob@raspberrypi:~ $ echo "Hello World!"
Hello World!
jacob@raspberrypi:~ $echo

jacob@raspberrypi:~ $echo.
-bash: echo.: command not found
jacob@raspberrypi:~ $

```

</div>

</div>

---

<div class="justify lh-30">

# Redirection

```powershell
echo Hello, world!
```

To redirect output to a file: `echo Hello, world! > myfile.txt`

**Note**: Redirection works similarly in both systems, using the `>` symbol to overwrite a file and `>>` to append to a file.

</div>

---

<!-- _class: code-description -->

# Example 4 - `echo`

```powershell
C:\Users\Jacob>echo Hello world! > myfile.txt
C:\Users\Jacob>

```

- The simplest way to create a new file.
- Redirection works similarly in both systems, using the `>` symbol to overwrite a file and `>>` to append to a file.

<div class="result-box">

<div class="result-header">

myfile.txt

</div>

<div class="result-content">

Hello world

</div>

</div>

---

# Creating and Deleting Files and Directories

## Windows:

`copy`: Copies files.
`del`: Deletes files.
`md`: Makes a new directory.

## Linux:

`cp`: Copies files.
`rm`: Removes files or directories.
`mkdir`: Makes a new directory.

---

# Example 5 - `copy`,`del`,`md`--- `cp`,`rm`,`mkdir`

<div class="columns">

<div class="card">

## Windows

```powershell
C:\Users\Jacob>md Folder
C:\Users\Jacob>dir
01/04/2025  10:06 AM    <DIR>          Folder
07/16/2023  07:09 AM    <DIR>          Music
...
C:\Users\Jacob> cd Folder
C:\Users\Jacob\Folder> echo. > empty.txt
C:\Users\Jacob\Folder> copy empty.txt copyEmpty.txt
...
01/04/2025  12:22 PM    <DIR>          .
01/04/2025  10:08 AM    <DIR>          ..
01/04/2025  12:19 PM                 3 copyEmpty.txt
01/04/2025  12:19 PM                 3 empty.txt
...
C:\Users\Jacob\Folder> del copyEmpty.txt
C:\Users\Jacob\Folder>
```

</div>

<div class="card">

## Linux

```bash
jacob@raspberrypi:~ $ mkdir Folder
jacob@raspberrypi:~ $ ls
Bookshelf  Desktop  Documents  Downloads  Folder
...
jacob@raspberrypi:~ $ cd Folder
jacob@raspberrypi:~/Folder $ echo > empty.txt
jacob@raspberrypi:~/Folder $ cp empty.txt copyEmpty.txt
...
jacob@raspberrypi:~/Folder $ ls
copyEmpty.txt  empty.txt
...
jacob@raspberrypi:~/Folder $ rm copyEmpty.txt
jacob@raspberrypi:~/Folder $

```

</div>

</div>

---

<div class="justify lh-10">

# Executing Compiled Programs

## Windows:

- o run a compiled program, you usually just type the program name, followed by the `.exe` extension: `program_name.exe`.
- Windows will automatically add the .exe extension if it is omitted.

## Linux:

- To run a compiled program, you typically use the following syntax: `./program_name`.
- The `./` part specifies that the program should be executed in the current directory.

</div>

---

# Example 6 - ping

<div class="columns">

<div class="card">

## Windows

```powershell
C:\Users\Jacob>cd C:\Windows\System32
C:\Windows\System32>ping.exe www.google.com

Pinging www.google.com [172.217.14.228] with 32 bytes of data:
Reply from 172.217.14.228: bytes=32 time=16ms TTL=113
Reply from 172.217.14.228: bytes=32 time=16ms TTL=113
Reply from 172.217.14.228: bytes=32 time=16ms TTL=113
Reply from 172.217.14.228: bytes=32 time=16ms TTL=113

Ping statistics for 172.217.14.228:
    Packets: Sent = 4, Received = 4, Lost = 0 (0% loss),
Approximate round trip times in milli-seconds:
    Minimum = 16ms, Maximum = 16ms, Average = 16ms

C:\Windows\System32>

```

</div>

<div class="card">

## Linux

```bash
jacob@raspberrypi:/usr/bin $ ./ping www.google.com

PING www.google.com (172.217.14.228) 56(84) bytes of data.
64 bytes from sea30s02-in-f4.1e100.net (172.217.14.228): icmp_seq=1 ttl=115 time=16.2 ms
64 bytes from sea30s02-in-f4.1e100.net (172.217.14.228): icmp_seq=2 ttl=115 time=16.0 ms
64 bytes from sea30s02-in-f4.1e100.net (172.217.14.228): icmp_seq=3 ttl=115 time=16.1 ms
64 bytes from sea30s02-in-f4.1e100.net (172.217.14.228): icmp_seq=4 ttl=115 time=16.0 ms
64 bytes from sea30s02-in-f4.1e100.net (172.217.14.228): icmp_seq=5 ttl=115 time=16.0 ms
^C
--- www.google.com ping statistics ---
5 packets transmitted, 5 received, 0% packet loss, time 4006ms
rtt min/avg/max/mdev = 16.013/16.068/16.192/0.069 ms

jacob@raspberrypi:/usr/bin $


```

</div>

</div>

---

# Additional tools

## Clear the console

- To clear the console/terminal window, use the appropriate command, such as **Windows**: `cls` **Linux**: `clear`

## Rename file

- Instead of copying a file to a new name, you can use a command to rename the file. The syntax is identical to that of copying. **Windows** `rename` **Linux** `mv`

## Help

- To obtain additional assistance on using the application, please type the program name followed by a space and **Windows**: `/h`, `-h` **Linux**: `--h`

---

<div class="justify lh-20">

# IP address

An IP address is like a unique mailing address for every device connected to the internet. It allows computers to locate and communicate with each other. Think of it as a numerical label assigned to each device, making it possible for data to be sent to the correct destination.

## Windows: `ipconfig`

## Linux: `ip addr`

</div>

---

# Example 7 - IP

<div class="columns">

<div class="card">

## Windows

```powershell
C:\Users\Jacob>ipconfig
...
Ethernet adapter Ethernet 4:

   Connection-specific DNS Suffix  . : butte.campus
   Link-local IPv6 Address . . . . . : fe80::813a:b45d:4cd4:63fb%26
   IPv4 Address. . . . . . . . . . . : 10.38.32.232
   Subnet Mask . . . . . . . . . . . : 255.255.255.0
   Default Gateway . . . . . . . . . : 10.38.32.254
...
C:\Users\Jacob>


```

</div>

<div class="card">

## Linux

```bash
jacob@raspberrypi:~ $ ip addr
...
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500
qdisc pfifo_fast state UP group default qlen 1000
    link/ether b8:27:eb:dc:64:a3 brd ff:ff:ff:ff:ff:ff
    inet 10.38.32.256/24 brd 10.38.32.255 scope global dynamic noprefixroute eth0
       valid_lft 525094sec preferred_lft 438694sec
    inet6 fe80::d8c5:56d0:e193:bd13/64 scope link
       valid_lft forever preferred_lft forever
...
jacob@raspberrypi:~


```

</div>

</div>

---

<!-- _class: caption-slide -->

<!-- _paginate: skip -->

# Console

## Assignment 01

---

<div class="justify lh-25">

# Assignment 01 - Console

1. Please go to the course page on Canvas to find Assignment 01.
2. Complete the tasks and submit your result in the designated area according to the guidelines.

⏱ Time limit: 15 minutes

</div>

---

<!-- _class: caption-slide -->

<!-- _paginate: skip -->

# Toolchain

## Setup

---

# Toolchain Setup

## Read:

[https://github.com/jpach-cs/jpach-cs.github.io/releases/tag/compiler](https://github.com/jpach-cs/jpach-cs.github.io/releases/tag/compiler)

## Downolad:

[https://github.com/jpach-cs/jpach-cs.github.io/releases/download/compiler/MinGW.zip](https://github.com/jpach-cs/jpach-cs.github.io/releases/download/compiler/MinGW.zip)

---

# Git Setup

![h:300](git.svg)

## Downolad:

[https://git-scm.com/install/windows](https://git-scm.com/install/windows)

---

<!-- _class: caption-slide -->

<!-- _paginate: skip -->

# Compiler

<!--
## Subtitle
-->

---

# The Compilation Process: A Two-Stage Journey

<div class="justify lh-15">

Turning source code into a running program happens in two distinct steps:
**Stage 1**: Compilation (.c $\rightarrow$ .o)

- **What it does**: Translates your C source code into machine code (binary instructions for the CPU).
- **Command**: `gcc -g -Wall -std=c99 -pedantic -c input.c -o output.o`
- **Output**: An object file (main.o).
- **Key characteristic**: It contains machine code for your file, but it does not yet know where standard library functions (like printf or scanf) are located. References to them remain unresolved.

</div>

---

# The Compilation Process: A Two-Stage Journey

<div class="justify lh-25">

**Stage 2**: Linking (.o $\rightarrow$ Executable)

- **What it does**: Combines your object file(s) with standard libraries and startup code.
- **Command**: `gcc -g output.o -o program.exe`
- **Output**: A final executable file (main.exe or binary).
- **Key characteristic**: The linker resolves all missing references, connects external library functions, and produces a complete, runnable program.

</div>

---

# Compiler

<div class="justify lh-20">

1. A compiler takes the entire source code and translates it into a machine code file, often called **an executable**.

2. This executable file contains instructions that the computer's processor can directly execute.

3. Once compiled, the program can run independently without the need for the original source code or a compiler.

</div>

---

<style scoped>
.columns { display:flex; align-items:center; gap:30px }
.column-left { flex:0 0 auto }
.column-right { flex:1; font-size:0.52em; line-height:1.35 }
.column-right p { margin-bottom:12px }
.footer-summary { font-size:0.6em; margin-top:15px }
</style>

<div>

# Extended descrpition

<div class="columns">

<div class="column-left">

![h:460](compiler.svg)

</div>

<div class="column-right justify lh-30">

1. This is the source code you have written in the C/C++ programming language. It forms the basis of your program.
2. During this stage, the preprocessor processes your source code. It includes header files (e.g., stdio.h, math.h) using directives like #include and expands macros defined with #define. The output of this stage is the preprocessed source code.
3. The compiler takes the preprocessed source code and translates it into assembly code. This assembly code is a low-level representation of your program that is specific to the target architecture.
4. The assembler converts the assembly code into object code. Object code is a machine-readable format that contains instructions and data.
5. The linker combines the object code with other necessary libraries (e.g., standard C library) to create the final executable program. This process resolves external references and creates a complete program that can be run.
6. The loader loads the executable program into memory (RAM) so that it can be executed by the CPU. The running program is often referred to as a process.

</div>

</div>

</div>

---

<!-- _class: caption-slide -->

<!-- _paginate: skip -->

# Compilation

## Practical exercise

---

# Practical exercise - Compilation

1. Create a new folder in your desktop. ⏱ Time limit: 5 minutes
2. Create a file named main.c inside it and fill it with the simplest possible code:

```c
// main.c
#include <stdio.h>
int main()
{
  printf("%s\n", "Hello, world!");
  return 0;
}
```

1. Compile `main.c` with `cmd` into an object file `main.o`:
   `gcc -g -Wall -std=c99 -pedantic -c main.c -o main.o`
2. Link the object file `main.o` into an executable `main.exe`: `gcc -g main.o -o main.exe`

---

<!-- _class: caption-slide -->

<!-- _paginate: skip -->

# How to get

## Visual Studio Code

---

# Not here!

## On your personal computer!

- Please do not install VSC on university computers.
- Everything should already be installed. You only need to check the VSC extensions.

---

# Go to:

## [https://code.visualstudio.com/](https://code.visualstudio.com/)

![h:450](vc1.svg)

---

# Select System Installer x64:

![h:500](vc2.svg)

---

# Download & install: VSCodeSetup-x64.exe

![h:520](vc3.svg)

---

<div class="justify lh-10">

# Behind the Magic: IDE vs. Manual Control

- **Full Visual Studio**:
  Hides complexity. Project types, targets, output folders, and dependencies are "clicked" into existence automatically.
- **The Programmer's Reality**:
  A professional must understand the underlying mechanics: a source file (`.c`) and a compiler (`gcc.exe`).
- **VS Code**:
  By default, it's just a text editor. To turn it into an **IDE** that compiles, runs, and debugs step-by-step, we need explicit configuration rules.

The `.vscode folder`: Stores these rules in a specific format (JSON). For now, we will use ready-made templates — **we'll break them down piece by piece in upcoming weeks!**

</div>

---

# Integrated development environment

<div class="card justify lh-20">

An Integrated Development Environment (IDE) is a comprehensive software application that consolidates the essential tools needed for software development into a single graphical user interface. It typically combines:

1. a source **code editor** for writing code
2. a **compiler** and **linker** to transform that code into an executable program.
3. a built-in **debugger** to help developers identify and resolve logical errors

efficiently during the programming process.

</div>

---

# Open extensions

![h:520](vc4.svg)

---

# Install extensions

## C/C++; C/C++ Extension Pack; C/C++ Themes

![h:450](vc5.svg)

---

# Open Template code

![h:520](vc6.svg)

---

# Read your first C program – main.c

![main.c open in Visual Studio Code](vc7.svg)

---

# Run your first C program

![Running the program from Visual Studio Code](vc8.svg)

---

<div class="justify lh-10"></div>

---

<!-- _class: caption-slide -->

<!-- _paginate: skip -->

# Thank

## You

---

<!-- blank slide in the source -->
