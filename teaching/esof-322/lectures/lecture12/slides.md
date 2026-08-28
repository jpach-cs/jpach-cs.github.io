---
marp: true
theme: pach
paginate: true
class: compact
footer: "ESOF 322 | Software Engineering | J. L. Pach"
title: "Software Engineering"
---

<!-- _class: compact lead -->

# Software Engineering

## Lecture 12

---

# Today’s Agenda

- continuation of the makefile

---

# continuation of the makefile

---

# Last time

```make
CC     := gcc
CFLAGS := -g -Wall -std=c99 -pedantic # compiler flags
LFLAG  := -g # linker flag

TARGET := main.exe
OBJS   := main.o other.o

RM := -rm -f

ifeq ($(SHELL),sh.exe) # without any space!
    # cmd/powershell
    RM := del
endif

.PHONY: all clean

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CC) $(LFLAG) $(OBJS) -o $(TARGET)

main.o: main.c  # we dont have the main.h
	$(CC) $(CFLAGS) -c main.c -o main.o

other.o: other.h other.c
	$(CC) $(CFLAGS) -c other.c -o other.o
clean:
	$(RM) $(OBJS)
```

---

# extension

```make
CC     := gcc
CFLAGS := -g -Wall -std=c99 -pedantic # compiler flags
LFLAG  := -g # linker flag

TARGET := main.exe
OBJS   := main.o other.o

RM := -rm -f

ifeq ($(SHELL),sh.exe) # without any space!
    # cmd/powershell
    RM := del
endif

.PHONY: all clean

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CC) $(LFLAG) $(OBJS) -o $(TARGET)

main.o: main.c  # we dont have the main.h
	$(CC) $(CFLAGS) -c main.c -o main.o

other.o: other.h other.c
	$(CC) $(CFLAGS) -c other.c -o other.o
clean:
	$(RM) $(OBJS)
```

```make
INC_DIR :=inc#include for headers

CC     := gcc
CFLAGS := -g -Wall -std=c99 -pedantic -I $(INC_DIR) # compiler flags
LFLAG  := -g # linker flag

TARGET := main.exe #$(SCR_DIR)/main.exe
OBJS   := main.o other.o
RM := -rm -f

.PHONY: all clean

all: $(TARGET)




$(TARGET): $(OBJS)
	$(CC) $(LFLAG) $(OBJS) -o $(TARGET)

main.o: main.c
	$(CC) $(CFLAGS) -c main.c -o main.o

other.o: $(INC_DIR)/other.h other.c
	$(CC) $(CFLAGS) -c other.c -o other.o

clean:
	$(RM) $(OBJS)
```

---

<!-- _class: compact fit-90 -->

# Splitting a Project into Directories with Makefile

**Path separator in Makefiles**

- Make (originally from Linux) uses / instead of \ for paths.
- On Windows, cmd does not understand / in commands like
  - RM := del $(OBJ\_DIR)\\\*.o
  - while Bash (MinGW/Git Bash) does.
- In theory, you could define a SEP variable and substitute everywhere depending on the shell — but in practice this is **not worth it**.

**Convention:** Always write Makefiles for **Bash**, even on Windows (MinGW/Git includes Bash by default).

---

<!-- _class: compact fit-80 -->

# Splitting a Project into Directories with Makefile

**Backslash problem:**

- A single \ in Make is treated as a line continuation symbol.
- To insert a literal backslash in a command or path, you must write \\.

**Directory variables:**

- Usual naming convention: UPPERCASE with underscores (snake\_case), treated like constants:
  - OBJ\_DIR := obj
  - BIN\_DIR := bin
  - SRC\_DIR := src
- Usage inside rules:
  - $(BIN\_DIR)/main.exe

---

<!-- _class: compact fit-90 -->

# Splitting a Project into Directories with Makefile

**Header files and -I option**

- GCC automatically searches for headers in the **same directory** as the source file being compiled.
- If your headers are in a separate folder (e.g., include/), you must tell the compiler:
  - -I $(INC\_DIR)

---

# extension

```make
CC     := gcc
CFLAGS := -g -Wall -std=c99 -pedantic # compiler flags
LFLAG  := -g # linker flag

TARGET := main.exe
OBJS   := main.o other.o

RM := -rm -f

ifeq ($(SHELL),sh.exe) # without any space!
    # cmd/powershell
    RM := del
endif

.PHONY: all clean

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CC) $(LFLAG) $(OBJS) -o $(TARGET)

main.o: main.c  # we dont have the main.h
	$(CC) $(CFLAGS) -c main.c -o main.o

other.o: other.h other.c
	$(CC) $(CFLAGS) -c other.c -o other.o
clean:
	$(RM) $(OBJS)
```

```make
INC_DIR :=inc#include for headers

CC     := gcc
CFLAGS := -g -Wall -std=c99 -pedantic -I $(INC_DIR) # compiler flags
LFLAG  := -g # linker flag

TARGET := main.exe #$(SCR_DIR)/main.exe
OBJS   := main.o other.o
RM := -rm -f

.PHONY: all clean

all: $(TARGET)




$(TARGET): $(OBJS)
	$(CC) $(LFLAG) $(OBJS) -o $(TARGET)

main.o: main.c
	$(CC) $(CFLAGS) -c main.c -o main.o

other.o: $(INC_DIR)/other.h other.c
	$(CC) $(CFLAGS) -c other.c -o other.o

clean:
	$(RM) $(OBJS)
```

---

<!-- _class: compact fit-50 -->

# Adding a Dedicated inc/ Directory for Headers

In this example, we moved other.h into a new inc/ directory. Unlike bin/ or obj/, this directory does **not** need to be created by the Makefile, because it is already part of the repository structure — headers are expected to live there.

Three important changes were required to make compilation work:

- **Define INC\_DIR**
- **Add the -I flag to the compiler options** so GCC knows where to look for headers:
- **Update dependencies for other.o** to point explicitly to the header in

With these adjustments, the compiler will correctly find other.h in the inc/ directory, and the build process completes successfully.

```make
INC_DIR :=inc#include for headers

CC     := gcc
CFLAGS := -g -Wall -std=c99 -pedantic -I $(INC_DIR) # compiler flags
LFLAG  := -g # linker flag

TARGET := main.exe #$(SCR_DIR)/main.exe
OBJS   := main.o other.o
RM := -rm -f

.PHONY: all clean

all: $(TARGET)




$(TARGET): $(OBJS)
	$(CC) $(LFLAG) $(OBJS) -o $(TARGET)

main.o: main.c
	$(CC) $(CFLAGS) -c main.c -o main.o

other.o: $(INC_DIR)/other.h other.c
	$(CC) $(CFLAGS) -c other.c -o other.o

clean:
	$(RM) $(OBJS)
```

---

<!-- _class: compact fit-60 -->

# Make is extremely sensitive to spaces.

For example, if you write

```make
INC_DIR :=inc#include for headers
```

everything works fine. But if you accidentally insert a space before the comment, like this:

```make
INC_DIR :=inc #include for headers
```

then make will fail with an error such as:

```text
mingw32-make: *** No rule to make target '/other.h', needed by 'other.o'.  Stop.
```

One way to avoid this issue is to always place the # for comments **immediately after the declaration, with no spaces in between**. This guarantees there are no stray whitespace characters that could break the Makefile

```make
INC_DIR :=inc#include for headers

CC     := gcc
CFLAGS := -g -Wall -std=c99 -pedantic -I $(INC_DIR) # compiler flags
LFLAG  := -g # linker flag

TARGET := main.exe #$(SCR_DIR)/main.exe
OBJS   := main.o other.o
RM := -rm -f

.PHONY: all clean

all: $(TARGET)




$(TARGET): $(OBJS)
	$(CC) $(LFLAG) $(OBJS) -o $(TARGET)

main.o: main.c
	$(CC) $(CFLAGS) -c main.c -o main.o

other.o: $(INC_DIR)/other.h other.c
	$(CC) $(CFLAGS) -c other.c -o other.o

clean:
	$(RM) $(OBJS)
```

---

# extension

```make
INC_DIR :=inc#include for headers
BIN_DIR :=bin# *.exe

CC     := gcc
CFLAGS := -g -Wall -std=c99 -pedantic -I $(INC_DIR) # compiler flags
LFLAG  := -g # linker flag

TARGET := $(BIN_DIR)/main.exe #$(SCR_DIR)/main.exe
OBJS   := main.o other.o
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

```make
INC_DIR :=inc#include for headers

CC     := gcc
CFLAGS := -g -Wall -std=c99 -pedantic -I $(INC_DIR)
LFLAG  := -g # linker flag

TARGET := main.exe #$(SCR_DIR)/main.exe
OBJS   := main.o other.o
RM := -rm -f

.PHONY: all clean

all: $(TARGET)




$(TARGET): $(OBJS)
	$(CC) $(LFLAG) $(OBJS) -o $(TARGET)

main.o: main.c
	$(CC) $(CFLAGS) -c main.c -o main.o

other.o: $(INC_DIR)/other.h other.c
	$(CC) $(CFLAGS) -c other.c -o other.o

clean:
	$(RM) $(OBJS)
```

---

<!-- _class: compact fit-40 -->

# Adding a Dedicated bin/

The compilation output (main.exe) is now placed inside the bin directory, which will **not be tracked in the repository**. This is recorded in .gitignore, so when cloning the repository locally, the bin folder will not be present.

- The mkdir command is used to create the bin directory. Note that in Windows cmd, there is **no -p parameter**, so GPT’s suggestion was incorrect.
- To avoid errors if the directory already exists and to prevent make from stopping, the **order-only prerequisite operator |** is used. This tells make to check if the target exists (file or directory). If it exists, make does nothing; if it doesn’t, it runs the recipe exactly once. This is precisely what is needed for our scenario.

Modifications include:

- Adding a variable for the bin directory (BIN\_DIR).
- Extending the TARGET variable to include the directory path, so we **don’t have to modify the actual target recipe later**.
- Adding a dedicated $(BIN\_DIR) target. **Note:** this is **not a phony target**, because we want make to check for the existence of the directory.

These changes ensure that the build artifacts are separated from the source code and repository, and that make handles the directory creation safely and efficiently.

```make
INC_DIR :=inc#include for headers
BIN_DIR :=bin# *.exe

CC     := gcc
CFLAGS := -g -Wall -std=c99 -pedantic -I $(INC_DIR) # compiler flags
LFLAG  := -g # linker flag

TARGET := $(BIN_DIR)/main.exe #$(SCR_DIR)/main.exe
OBJS   := main.o other.o
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

<!-- _class: compact caption-slide -->

# Thank You!
