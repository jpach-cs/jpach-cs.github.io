---
marp: true
theme: pach
paginate: true
title: "Software Engineering"
---

# Software Engineering

*Lecture 13*

---

## Today’s Agenda

- Modular makefile
- Wildcard, patsubst
- Automatic Variables
- .dep files
- Debug

---

- Do tego makefile można dzielic na moduly, gdzie pliki o rozszrzeniu .mk będą modulami makefile za pomocą include jak w C
- *prerequisites* mogą być oddzielane  &amp; oznacza budowę asynchroniczna rownolegla, przyspiesza działanie make, jeśli istnieje wiele zaleznosci to można kazda z nich robic rownolegle bo sa niezależne – opcja profesionalna dla gigantycznych projektów
- make.RECIPEPREFIX – można zmienić tab na cos innego

---

# modular

*makefile*

---

## Modular Makefile

**Why Split a Makefile?**

- A single Makefile can quickly become **long and hard to maintain**.
- Splitting into smaller .mk files makes it easier to:
  - **organize code** (e.g., separate paths, compilation, cleaning),
  - **reuse** pieces in other projects,
  - **keep things clear** – each file has one responsibility

---

## Modular Makefile

**Why Split a Makefile?**

- A single Makefile can quickly become **long and hard to maintain**.
- Splitting into smaller .mk files makes it easier to:
  - **organize code** (e.g., separate paths, compilation, cleaning),
  - **reuse** pieces in other projects,
  - **keep things clear** – each file has one responsibility

```
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

## Modular Makefile

```
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

```
INC_DIR :=inc#
BIN_DIR :=bin#

CC     := gcc
CFLAGS := -g -Wall -std=c99 -pedantic -I $(INC_DIR)
LFLAG  := -g

TARGET := $(BIN_DIR)/main.exe
OBJS   := main.o other.o
RM := -rm -f
```

- paths.mk

```
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

- rules.mk

---

## Modular Makefile

How It Works:

- make reads the main Makefile.
- Then it includes the contents of paths.mk, rules.mk.
- The end result is one big Makefile, but structured into smaller logical pieces.

```
# Combine everything together
include paths.mk
include rules.mk
```

```
INC_DIR :=inc#
BIN_DIR :=bin#

CC     := gcc
CFLAGS := -g -Wall -std=c99 -pedantic -I $(INC_DIR)
LFLAG  := -g

TARGET := $(BIN_DIR)/main.exe
OBJS   := main.o other.o
RM := -rm -f
```

- paths.mk

```
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

- rules.mk

---

## Organizing Makefiles in mk/ Directory

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

```
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

# Using wildcard and patsubst

*in Makefiles*

---

## Using wildcard in Makefiles

- **$(wildcard pattern)**
  - Expands to all files matching a given pattern.
  - Commonly used to collect source files automatically.
- \# Expands to:

```
SOURCES = $(wildcard src/*.c)
```

```
src/main.c src/other.c ...
```

---

## Using patsubst in Makefiles

- **$(patsubst pattern,replacement,text)**
  - Performs pattern substitution on a list of words.
  - Often used to map .c files to corresponding .o object files.
- \# Expands to:

```
OBJECTS = $(patsubst src/%.c,obj/%.o,$(SOURCES))
```

```
obj/main.o obj/other.o ...
```

---

## Using patsubst in Makefiles - Benefits

- Automation → no need to manually list every file.
- Scalability → new .c files are picked up automatically.
- Clarity → clear mapping from source → object directories.

---

# Automatic Variables

*in Makefiles*

---

## Automatic Variables

- Purpose: Shortcuts that let you reference targets and dependencies without repeating file names.
- Used inside rules to simplify commands.

---

## Automatic Variables - $@ – The Target File

- Represents the **name of the file to be created**.

→ $@ expands to main.o.

```
main.o: main.c
    gcc -c main.c -o $@
```

---

## Automatic Variables - $&lt; – The First Dependency

- Represents the first prerequisite of the rule.
- Commonly used in compilation rules.

→ $&lt; expands to main.c.

```
main.o: main.c
    gcc -c $< -o $@
```

---

## Automatic Variables - $^ – All Dependencies

- Expands to a space-separated list of all prerequisites.
- Removes duplicates.

→ $^ expands to main.o utils.o.

```
app: main.o utils.o
    gcc $^ -o $@
```

---

## Automatic Variables - $? – Newer Dependencies

- Expands to dependencies newer than the target.
- Useful for incremental builds.

→ recompiles only when needed.

```
app: main.o utils.o
    gcc $? -o $@
```

---

## Automatic Variables - $\* – The Stem

- Represents the stem (base name) of the target.
- Mainly used in implicit rules.

→ Here $\* would expand to main if the target is main.o.

```
%.o: %.c
    gcc -c $< -o $@
```

---

## Automatic Variables - Summary

|Variable|Expands To|Example Use|Example Expansion|
|---|---|---|---|
|**$@**|Target file name|gcc -c main.c -o $@|main.o|
|**$&lt;**|First dependency|gcc -c $&lt; -o $@|main.c|
|**$^**|All dependencies (unique)|gcc $^ -o $@|main.o utils.o|
|**$?**|Only newer dependencies|gcc $? -o $@|utils.o (if newer)|
|**$**\*|Stem (base name) of target|Used in implicit rules|main (for main.o)|

---

# .dep files

*in Makefiles*

---

## A Solved Problem Creates a New One

- Previously, in dependencies, we explicitly listed header files (.h).
- With automatic source discovery (wildcard, patsubst), we no longer directly know which .c file includes which .h file.
- This creates a problem:
  - If a header file changes, how do we ensure the correct .o files are rebuilt?
- Solution: Use dependency files (.d or .p)
  - Generated automatically by the compiler (gcc -MMD -MP)
  - Contain precise header-to-source relationships
  - Included by the Makefile to ensure only the necessary files are recompiled

---

## Using Dependency Files (.d / .p)

- Problem: Make doesn’t know which .c includes which .h.
- Solution: Let the compiler generate dependency files.
- -MMD: Create a .d file for each .o
- -MP: Add phony targets to avoid errors if headers are deleted
- -include $(DEPS): Load dependencies if they exist (ignore missing ones at first run)

```
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

## Gcc -MMD -MP

- -MMD → generuje plik .d (dependency file) dla każdego .o
- -MP → dodaje „puste reguły” dla nagłówków, żeby uniknąć błędów gdy nagłówek zniknie
- DEP = $(SRC:.c=.d)

---

```
# Directories
SRC_DIR := src
INC_DIR := inc
OBJ_DIR := obj
BIN_DIR := bin

# Compiler and flags
CC     := gcc
CFLAGS := -Wall -Wextra -std=c99 -g -I$(INC_DIR) -MMD -MP
LDFLAGS := -g

# Files
SRCS := $(wildcard $(SRC_DIR)/*.c)
OBJS := $(patsubst $(SRC_DIR)/%.c, $(OBJ_DIR)/%.o, $(SRCS))
DEPS := $(OBJS:.o=.d)

TARGET := $(BIN_DIR)/main.exe

# Tools
RM := -rm -f
MKDIR := mkdir

.PHONY: all clean dirs

# Default target
all: dirs $(TARGET)

# Link
$(TARGET): $(OBJS)
	$(CC) $(LDFLAGS) $^ -o $@

# Compile rule
$(OBJ_DIR)/%.o: $(SRC_DIR)/%.c
	$(CC) $(CFLAGS) -c $< -o $@

# Make sure dirs exist
dirs:
	@$(MKDIR) $(OBJ_DIR) $(BIN_DIR)

# Clean
clean:
	$(RM) $(OBJ_DIR)/* $(TARGET)

# Include dependency files
-include $(DEPS)
```

---

## Adding a Dedicated bin/

The compilation output (main.exe) is now placed inside the bin directory, which will **not be tracked in the repository**. This is recorded in .gitignore, so when cloning the repository locally, the bin folder will not be present.

- The mkdir command is used to create the bin directory. Note that in Windows cmd, there is **no -p parameter**, so GPT’s suggestion was incorrect.
- To avoid errors if the directory already exists and to prevent make from stopping, the **order-only prerequisite operator |** is used. This tells make to check if the target exists (file or directory). If it exists, make does nothing; if it doesn’t, it runs the recipe exactly once. This is precisely what is needed for our scenario.

Modifications include:

- Adding a variable for the bin directory (BIN\_DIR).
- Extending the TARGET variable to include the directory path, so we **don’t have to modify the actual target recipe later**.
- Adding a dedicated $(BIN\_DIR) target. **Note:** this is **not a phony target**, because we want make to check for the existence of the directory.

These changes ensure that the build artifacts are separated from the source code and repository, and that make handles the directory creation safely and efficiently.

```
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

---

# Debug

*in Makefiles*

---

## Introduction to Makefile Debugging

**Goal:** Understand how to debug Makefile builds and figure out why targets are rebuilt.

Common situations:

- A target is rebuilt unexpectedly
- Dependencies are not behaving as expected
- Implicit rules are not applied correctly

---

## Debugging Options

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

## Example Usage - debug

- Tips for Using Make Debugging:
- Use --debug=b first to see basic rebuild information.
- Use --debug=why if a target rebuilds unexpectedly.
- Combine with -n (dry run) to see commands without executing:
  - make --debug=why -n
- Helps understand dependency issues, missing files, or outdated targets.
- Essential when working with complex Makefiles or large projects.

```
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

- echo %ERRORLEVEL%

---

# Thank

*You!*
