---
marp: true
theme: pach
paginate: true
footer: "ESOF 322 | Software Engineering | J. L. Pach"
title: "Software Engineering"
---

<!-- _class: lead -->

# Software Engineering

## Lecture 18

---

# Today’s Agenda

- Memory Integrity Checks
- Code Injection Defense

---

<!-- _class: fit-90 -->

# Memory Integrity and Anti-Tampering Techniques

**Learning Objectives:**

- Understand how memory can be manipulated externally (e.g., Cheat Engine).
- Implement basic integrity checks for critical variables.
- Explore code injection and how to defend against it.
- Learn how games and secure applications protect runtime data.

---

# Part 1: Memory Integrity Checks

- Example: Protecting a variable like health
- Call check\_health\_integrity() periodically\*.
- Use volatile to ensure the variable stays in RAM.
- You can also use XOR, CRC, or even SHA-based checksums.

```c
int health = 100;
int health_checksum = ~health;

void check_health_integrity()
{
    if (health_checksum != ~health)
    {
        printf("Memory tampering detected!\n");
        exit(1);
    }
}
```

---

# Part 2: Code Injection Defense

**Problem:**

- An attacker can inject code or modify control flow to **skip integrity checks**, e.g., jump over check\_health\_integrity().

---

<!-- _class: fit-50 -->

# Defensive Techniques

**1. Control Flow Integrity (CFI)**

- Use indirect checks to verify that critical functions were executed.
- Example: set a flag inside check\_health\_integrity() and verify it later.

**2. Function Call Randomization**

- Randomize the timing or order of integrity checks.
- Makes it harder to predict and patch.

**3. Self-modifying code / code hashing**

- Hash parts of your own code and verify they haven’t changed.
- Example: compute a hash of check\_health\_integrity() and compare it to a known value.

**4. Anti-debugging**

- Detect if a debugger is present (IsDebuggerPresent() on Windows).
- If detected, disable features or exit.

```c
bool integrity_checked = false;


void check_health_integrity()
{
    integrity_checked = true;
    if (health_checksum != ~health)
    {
        printf("Memory tampering detected!\n");
        exit(1);
    }
}

void verify_integrity_check()
{
    if (!integrity_checked)
    {
        printf("Integrity check was skipped!\n");
        exit(1);
    }
}
```

---

# modular makefile

---

# Modular Makefile

**Why Split a Makefile?**

- A single Makefile can quickly become **long and hard to maintain**.
- Splitting into smaller .mk files makes it easier to:
  - **organize code** (e.g., separate paths, compilation, cleaning),
  - **reuse** pieces in other projects,
  - **keep things clear** – each file has one responsibility

---

# Modular Makefile

**Why Split a Makefile?**

- A single Makefile can quickly become **long and hard to maintain**.
- Splitting into smaller .mk files makes it easier to:
  - **organize code** (e.g., separate paths, compilation, cleaning),
  - **reuse** pieces in other projects,
  - **keep things clear** – each file has one responsibility

```text
project/
│── Makefile        <- main file
│── paths.mk        <- directories, paths
│── rules.mk        <- compilation rules
│── clean.mk        <- cleaning rules
│── deps.mk         <- dependencies (optional)
├── src/
│   ├── main.c
│   └── other.c
└── inc/
    └── other.h

```

---

# Modular Makefile

```make
INC_DIR :=inc#include for headers
BIN_DIR :=bin# *.exe

CC     := gcc
CFLAGS := -g -Wall -std=c99 -pedantic -I $(INC_DIR) # compiler flags
LFLAG  := -g # linker flag

TARGET := $(BIN_DIR)/main.exe #$(SCR_DIR)/main.exe
OBJS   := main.o other.o
RM := -rm -f

.PHONY: all clean check-shell

all: $(TARGET)

$(TARGET): $(OBJS) | $(BIN_DIR) #order-only prerequisite
    $(CC) $(LFLAG) $(OBJS) -o $(TARGET)

main.o: main.c
    $(CC) $(CFLAGS) -c main.c -o main.o

other.o: $(INC_DIR)/other.h other.c
    $(CC) $(CFLAGS) -c other.c -o other.o

$(BIN_DIR):
    mkdir $(BIN_DIR)

clean:
    $(RM) $(OBJS)
```

**paths.mk**

```make
INC_DIR :=inc#
BIN_DIR :=bin#

CC     := gcc
CFLAGS := -g -Wall -std=c99 -pedantic -I $(INC_DIR)
LFLAG  := -g

TARGET := $(BIN_DIR)/main.exe
OBJS   := main.o other.o
RM := -rm -f
```

**rules.mk**

```make
.PHONY: all clean check-shell
all: $(TARGET)

$(TARGET): $(OBJS) | $(BIN_DIR) #
    $(CC) $(LFLAG) $(OBJS) -o $(TARGET)

main.o: main.c
    $(CC) $(CFLAGS) -c main.c -o main.o

other.o: $(INC_DIR)/other.h other.c
    $(CC) $(CFLAGS) -c other.c -o other.o

$(BIN_DIR):
    mkdir $(BIN_DIR)
clean:
    $(RM) $(OBJS)
```

---

<!-- _class: fit-90 -->

# Modular Makefile

How It Works:

- make reads the main Makefile.
- Then it includes the contents of paths.mk, rules.mk.
- The end result is one big Makefile, but structured into smaller logical pieces.

```make
# Combine everything together
include paths.mk
include rules.mk
```

**paths.mk**

```make
INC_DIR :=inc#
BIN_DIR :=bin#

CC     := gcc
CFLAGS := -g -Wall -std=c99 -pedantic -I $(INC_DIR)
LFLAG  := -g

TARGET := $(BIN_DIR)/main.exe
OBJS   := main.o other.o
RM := -rm -f
```

**rules.mk**

```make
.PHONY: all clean check-shell
all: $(TARGET)

$(TARGET): $(OBJS) | $(BIN_DIR) #
    $(CC) $(LFLAG) $(OBJS) -o $(TARGET)

main.o: main.c
    $(CC) $(CFLAGS) -c main.c -o main.o

other.o: $(INC_DIR)/other.h other.c
    $(CC) $(CFLAGS) -c other.c -o other.o

$(BIN_DIR):
    mkdir $(BIN_DIR)
clean:
    $(RM) $(OBJS)
```

---

<!-- _class: fit-60 -->

# Organizing Makefiles in mk/ Directory

- In larger projects, it’s common to separate Makefiles into a dedicated mk/ directory.
- The main Makefile stays clean and minimal, while detailed configuration lives inside modular .mk files.

**Main Makefile**

- include mk/paths.mk
- include mk/compiler.mk
- include mk/rules.mk

**Benefits**

- **Readability** → new contributors see a simple top-level Makefile.
- **Modularity** → easy to swap out compilers or rule sets.
- **Portability** → different .mk sets for Windows, Linux, macOS.
- **Industry Standard** → many open-source projects follow this convention.

```text
project/
│── Makefile
│── src/
│── inc/
│── mk/
│ ├── paths.mk
│ ├── compiler.mk
│ └── rules.mk
```

---

# Using wildcard and patsubst in Makefiles

---

# Using wildcard in Makefiles

- **$(wildcard pattern)**
  - Expands to all files matching a given pattern.
  - Commonly used to collect source files automatically.

```make
SOURCES = $(wildcard src/*.c)
```

\# Expands to:

```text
src/main.c src/other.c ...
```

---

# Using patsubst in Makefiles

- **$(patsubst pattern,replacement,text)**
  - Performs pattern substitution on a list of words.
  - Often used to map .c files to corresponding .o object files.

```make
OBJECTS = $(patsubst src/%.c,obj/%.o,$(SOURCES))
```

\# Expands to:

```text
obj/main.o obj/other.o ...
```

---

# Using patsubst in Makefiles - Benefits

- Automation → no need to manually list every file.
- Scalability → new .c files are picked up automatically.
- Clarity → clear mapping from source → object directories.

---

# Automatic Variables in Makefiles

---

# Automatic Variables

- Purpose: Shortcuts that let you reference targets and dependencies without repeating file names.
- Used inside rules to simplify commands.

---

# Automatic Variables - $@ – The Target File

- Represents the **name of the file to be created**.

→ $@ expands to main.o.

```make
main.o: main.c
    gcc -c main.c -o $@
```

---

<!-- _class: fit-90 -->

# Automatic Variables - $&lt; – The First Dependency

- Represents the first prerequisite of the rule.
- Commonly used in compilation rules.

→ $&lt; expands to main.c.

```make
main.o: main.c
    gcc -c $< -o $@
```

---

# Automatic Variables - $^ – All Dependencies

- Expands to a space-separated list of all prerequisites.
- Removes duplicates.

→ $^ expands to main.o utils.o.

```make
app: main.o utils.o
    gcc $^ -o $@
```

---

<!-- _class: fit-90 -->

# Automatic Variables - $? – Newer Dependencies

- Expands to dependencies newer than the target.
- Useful for incremental builds.

→ recompiles only when needed.

```make
app: main.o utils.o
    gcc $? -o $@
```

---

# Automatic Variables - $\* – The Stem

- Represents the stem (base name) of the target.
- Mainly used in implicit rules.

→ Here $\* would expand to main if the target is main.o.

```make
%.o: %.c
    gcc -c $< -o $@
```

---

# Automatic Variables - Summary

|Variable|Expands To|Example Use|Example Expansion|
|---|---|---|---|
|**$@**|Target file name|gcc -c main.c -o $@|main.o|
|**$&lt;**|First dependency|gcc -c $&lt; -o $@|main.c|
|**$^**|All dependencies (unique)|gcc $^ -o $@|main.o utils.o|
|**$?**|Only newer dependencies|gcc $? -o $@|utils.o (if newer)|
|**$**\*|Stem (base name) of target|Used in implicit rules|main (for main.o)|

---

# .dep files in Makefiles

---

# A Solved Problem Creates a New One

- Previously, in dependencies, we explicitly listed header files (.h).
- With automatic source discovery (wildcard, patsubst), we no longer directly know which .c file includes which .h file.
- This creates a problem:
  - If a header file changes, how do we ensure the correct .o files are rebuilt?
- Solution: Use dependency files (.d or .p)
  - Generated automatically by the compiler (gcc -MMD -MP)
  - Contain precise header-to-source relationships
  - Included by the Makefile to ensure only the necessary files are recompiled

---

<!-- _class: fit-60 -->

# Using Dependency Files (.d / .p)

- Problem: Make doesn’t know which .c includes which .h.
- Solution: Let the compiler generate dependency files.
- -MMD: Create a .d file for each .o
- -MP: Add phony targets to avoid errors if headers are deleted
- -include $(DEPS): Load dependencies if they exist (ignore missing ones at first run)

```make
# Compiler flags for dependency generation
CFLAGS := -g -Wall -std=c99 -pedantic -I inc -MMD -MP
# Sources and objects
SOURCES := $(wildcard src/*.c)
OBJECTS := $(patsubst src/%.c,obj/%.o,$(SOURCES))
DEPS    := $(OBJECTS:.o=.d)
# Build rule (note use of $@ and $<)
obj/%.o: src/%.c
    $(CC) $(CFLAGS) -c $< -o $@
# Link final binary
bin/main.exe: $(OBJECTS)
    $(CC) $(OBJECTS) -o $@
# Include generated dependency files
-include $(DEPS)
```

---

# Debug in Makefiles

---

# Introduction to Makefile Debugging

**Goal:** Understand how to debug Makefile builds and figure out why targets are rebuilt.

Common situations:

- A target is rebuilt unexpectedly
- Dependencies are not behaving as expected
- Implicit rules are not applied correctly

---

# Debugging Options

make debug flags:

|Option|Description|
|---|---|
|--debug=b|Basic: shows which targets are considered out-of-date|
|--debug=why|Explains why a target must be rebuilt|
|--debug=i|Traces implicit rules applied by Make|
|--debug=j|Shows sub-command invocations (jobs)|
|--debug=m|Also traces rebuilding of Makefiles|
|-d|Everything (--debug=a), full verbose debugging|

---

<!-- _class: fit-80 -->

# Example Usage - debug

- Tips for Using Make Debugging:
- Use --debug=b first to see basic rebuild information.
- Use --debug=why if a target rebuilds unexpectedly.
- Combine with -n (dry run) to see commands without executing:
  - make --debug=why -n
- Helps understand dependency issues, missing files, or outdated targets.
- Essential when working with complex Makefiles or large projects.

```console
# Show which targets are out-of-date
make --debug=b
# Explain why a target is rebuilt
make --debug=why
# Trace implicit rules
make --debug=i
# Debug sub-command invocations
make --debug=j
# Debug Makefile rebuilds
make --debug=m
# Full debug output (equivalent to --debug=a)
make -d
```

---

<!-- _class: caption-slide -->

# Thank You!
