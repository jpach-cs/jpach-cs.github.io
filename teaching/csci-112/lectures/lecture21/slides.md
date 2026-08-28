---
marp: true
theme: pach
paginate: true
class: compact
footer: "CSCI 112 | Programming with C | J. L. Pach"
title: "CSSI112lec 21"
---

<!-- _class: compact lead -->

# CSCI 112<br><br>Programming with C

- Lecture 21
- Dr. Jakub L. Pach
- Fall 2025

---

# Outline

- Review
- Standard C Library Overview
  - stdlib.h
  - assert.h
  - stdio.h

---

# Review

---

# 1. Character Classification and Conversion (&lt;ctype.h&gt;)

Used for testing and converting characters.

|Function|Description|Example|
|---|---|---|
|isalpha(c)|Checks if character is a letter (A–Z, a–z).|if (isalpha(c)) ...|
|isdigit(c)|Checks if character is a decimal digit.|if (isdigit(c)) ...|
|isalnum(c)|Checks if character is alphanumeric.|if (isalnum(c)) ...|
|iscntrl(c)|Checks if character is a control character.|if (iscntrl(c)) ...|
|islower(c)|Checks if character is lowercase.|if (islower(c)) ...|
|isupper(c)|Checks if character is uppercase.|if (isupper(c)) ...|
|isspace(c)|Checks for whitespace (space, tab, newline, etc.).|if (isspace(c)) ...|
|isprint(c)|Checks if character is printable.|if (isprint(c)) ...|
|ispunct(c)|Checks if character is punctuation. <br>(. , ; : ! ? ( ) \[ \] { } ‚ „ + - \* / % # @ $ &amp; = ^ ~ \| &lt; &gt;)|if (ispunct(c)) ...|
|tolower(c)|Converts uppercase to lowercase.|tolower('A') → 'a'|
|toupper(c)|Converts lowercase to uppercase.|toupper('b') → 'B'|

---

# 2. String Handling (&lt;string.h&gt;)

Used for manipulating null-terminated character arrays.

|Function|Description|Example|
|---|---|---|
|strcpy(dest, src)|Copies a string.|strcpy(name, "Alice");|
|strncpy(dest, src, n)|Copies up to n characters.|strncpy(buf, input, 10);|
|strcat(dest, src)|Concatenates two strings.|strcat(full, last);|
|strncat(dest, src, n)|Concatenates up to n characters.|strncat(buf, ext, 4);|
|strcmp(a, b)|Compares two strings.|if (strcmp(a,b)==0)|
|strlen(s)|Returns string length.|len = strlen(name);|
|strchr(s, c)|Finds first occurrence of c.|p = strchr(s, 'x');|
|strrchr(s, c)|Finds last occurrence of c.|p = strrchr(s, '.');|
|strstr(hay, needle)|Finds substring.|p = strstr(text, "cat");|
|strtok(s, delim)|Splits string into tokens (destructive!).|token = strtok(str, ",");|

---

# 3. Memory Handling (&lt;string.h&gt;)

Used for working with raw memory blocks.

|Function|Description|Example|
|---|---|---|
|memcpy(dest, src, n)|Copies n bytes.|memcpy(buf2, buf1, n);|
|memmove(dest, src, n)|Safe copy (handles overlap).|memmove(a, b, 5);|
|memcmp(a, b, n)|Compares n bytes.|if (memcmp(a,b,4)==0)|
|memset(ptr, val, n)|Fills memory with byte value.|memset(buf, 0, 10);|
|memchr(ptr, val, n)|Finds a byte in memory.|p = memchr(buf, 'x', 20);|

---

# 4. Input / Output Functions (&lt;stdio.h&gt;)

Work with files and streams.

|Function|Description|Example|
|---|---|---|
|fopen(name, mode)|Opens a file.|fp = fopen("data.txt","r");|
|freopen(name, mode, fp)|Reopens an existing stream.|freopen("log.txt","w",stdout);|
|fclose(fp)|Closes file.|fclose(fp);|
|fflush(fp)|Forces buffer write to file.|fflush(stdout);|
|fread(buf, size, count, fp)|Reads from file.|fread(data,1,10,fp);|
|fwrite(buf, size, count, fp)|Writes to file.|fwrite(data,1,10,fp);|
|fseek(fp, offset, origin)|Moves file position.|fseek(fp, 0, SEEK\_SET);|
|ftell(fp)|Returns current position.|pos = ftell(fp);|
|rewind(fp)|Moves position to start.|rewind(fp);|
|remove(name)|Deletes file.|remove("old.txt");|
|rename(old, new)|Renames file.|rename("a.txt","b.txt");|
|tmpfile()|Opens temporary file.|FILE \*fp = tmpfile();|
|tmpnam(buf)|Generates unique temp name.|tmpnam(name);|
|feof(fp)|Checks end-of-file.|while(!feof(fp))...|
|ferror(fp)|Checks read/write error.|if (ferror(fp))...|
|clearerr(fp)|Clears EOF/error flags.|clearerr(fp);|
|perror(msg)|Prints system error message.|perror("File open failed");|

---

# 5. Conversion Functions (&lt;stdlib.h&gt;)

Convert strings to numbers.

|Function|Description|Example|
|---|---|---|
|atoi(str)|Converts to int.|x = atoi("123");|
|atol(str)|Converts to long.|y = atol("12345");|
|atof(str)|Converts to double.|z = atof("3.14");|
|strtol(str, end, base)|String → long, supports base.|val = strtol(s, NULL, 16);|
|strtoul(str, end, base)|String → unsigned long.|val = strtoul(s, NULL, 10);|
|strtod(str, end)|String → double.|d = strtod(s, NULL);|

---

# 6. Math Functions (&lt;math.h&gt;)

Convert strings to numbers.

|Function|Description|Example|
|---|---|---|
|abs(x)|Absolute value (int).|abs(-5) → 5|
|labs(x)|Absolute (long).|labs(-100L)|
|fabs(x)|Absolute (float/double).|fabs(-3.2)|
|sqrt(x)|Square root.|sqrt(9) → 3.0|
|pow(a,b)|Exponentiation.|pow(2,3) → 8.0|
|sin(x), cos(x)|Trigonometric.|sin(3.14)|
|ceil(x), floor(x), round(x)|Rounding operations.|ceil(3.2) → 4.0|
|fmod(a,b)|Floating-point remainder.|fmod(7.5,2) → 1.5|
|hypot(x,y)|√(x²+y²).|hypot(3,4) → 5.0|

---

<!-- _class: compact fit-80 -->

# Standard C Library Overview

- Character Classification and Conversion (&lt;ctype.h&gt;)
- String Handling (&lt;string.h&gt;)
- Memory Handling (&lt;string.h&gt;)
- Input / Output Functions (&lt;stdio.h&gt;)
- Conversion Functions (&lt;stdlib.h&gt;)
- Math Functions (&lt;math.h&gt;)
- Utility Functions (&lt;stdlib.h&gt;)
- Diagnostics and Assertions (&lt;assert.h&gt;)
- Time and Date Functions (&lt;time.h&gt;)
- Variable Argument Lists (&lt;stdarg.h&gt;)

---

# Standard C Library Overview<br> (MinGW / C Standard)

---

# Utility Functions

---

# 7. Utility Functions (&lt;stdlib.h&gt;)

Convert strings to numbers.

|Function|Description|Example|
|---|---|---|
|rand()|Returns pseudo-random number.|x = rand() % 10;|
|srand(seed)|Seeds random generator.|srand(time(NULL));|
|abort()|Terminates program abnormally.|abort();|
|exit(status)|Ends program normally.|exit(0);|
|atexit(func)|Registers cleanup function.|atexit(close\_files);|
|system(cmd)|Runs shell command.|system("cls");|
|bsearch(key, base, n, size, cmp)|Binary search.|bsearch(&amp;x, arr, n, sizeof(int), cmp);|
|qsort(base, n, size, cmp)|Sorts array.|qsort(arr, n, sizeof(int), cmp);|

---

# rand() – Returns a pseudo-random integer in the range 0 … RAND\_MAX (0x7FFF - 32767).

- The sequence is the same each program run unless seeded with srand()!

```c
#include <stdio.h>
#include <stdlib.h>

int main()
{
	int r = rand() % 10;   // random number 0–9
	printf("%d", r);
    return 0;
}
```

- rand()

```text
Header: <stdlib.h>
```

**Result:**

```text
5
```

**Result:**

```text
5
```

**Result:**

```text
5
```

---

<!-- _class: compact fit-90 -->

# But…

- The rand() function returns a number in the range of 0 to RAND\_MAX (which is typically 32767). To achieve a desired, custom range, you can use the modulo operator (%) trick.

```c
#include <stdio.h>
#include <stdlib.h>

int main()
{
    int min_val = 1 ;
    int max_val = 5;
    int r = (rand() % max_val) + min_val ;
    printf("%d", r);
    return 0;
}
```

```text
Header: <stdlib.h>
```

**Result:**

```text
5
```

---
<!-- _class: compact long-title -->

# srand(unsigned int seed) – Sets the starting point (seed) for the pseudo-random generator.

- Use current time to get different results each run.

```c
#include <stdio.h>
#include <stdlib.h>

int main()
{
    srand(time(NULL));
    int min_val = 1 ;
    int max_val = 5;
    int r = (rand() % max_val) + min_val ;
    printf("%d", r);
    return 0;
}
```

- srand(time(NULL));

```text
Header: < stdlib.h>
```

**Result:**

```text
2
```

**Result:**

```text
4
```

**Result:**

```text
3
```

---

# abort() – Immediately terminates the program with an abnormal termination signal.

- Does **not** call cleanup handlers, destructors, or flush buffers.

```c
#include <stdio.h>
#include <stdlib.h>

int main()
{
    int * ptr = NULL;
    if (ptr == NULL)
    {
        abort();
    }
    return 0;
}
```

- abort()

```text
Header: < stdlib.h>
```

---

# exit() – Stops the program normally.

- **Calls** all cleanup functions registered with atexit() and flushes stdio buffers.

```c
#include <stdio.h>
#include <stdlib.h>

int main()
{
	exit(0);  // success
}
```

- exit(int)

```text
Header: < stdlib.h>
```

---

<!-- _class: compact long-title -->

# atexit() – Registers a function to be called automatically when the program exits (via return or exit() — but NOT abort()).

```c
#include <stdio.h>
#include <stdlib.h>

FILE *logFile = NULL;
int *buffer = NULL;

// --- CLEANUP FUNCTIONS ---
void closeLogFile()
{
    if (logFile != NULL)
    {
        fprintf(logFile, "[CLEANUP] Closing log file.\n");
        fclose(logFile);
        logFile = NULL;
    }
}
void freeBuffer()
{
    if (buffer != NULL)
    {
        printf("[CLEANUP] Freeing buffer.\n");
        free(buffer);
        buffer = NULL;
    }
}
```

- \*atexit(void (func)(void))

```text
Header: < stdlib.h>
```

```c
void finalMessage()
{
    printf("[CLEANUP] Program exited. Goodbye!\n");
}
int main()
{
    // Register cleanup functions (they run in reverse order)
    atexit(finalMessage);
    atexit(freeBuffer);
    atexit(closeLogFile);
    // Allocate something
    buffer = malloc(100 * sizeof(int));
    if (!buffer) {
        fprintf(stderr, "Memory allocation failed.\n");
        exit(EXIT_FAILURE);  // cleanup will still run!
    }
    // Open log file
    logFile = fopen("program.log", "w");
    if (!logFile) {
        fprintf(stderr, "Failed to open log file.\n");
        exit(EXIT_FAILURE);  // cleanup will still run!
    }
    fprintf(logFile, "[INFO] Program started.\n");
    printf("Program is running...\n");
    // Try triggering early exit
    // exit(0); // Uncomment to test
    // Normal return also triggers cleanup
    return 0;
}
```

**program.log:**

```text
[INFO] Program started.
[CLEANUP] Closing log file.
```

- In this program we show how the atexit() function works. It allows us to register functions that will be called automatically when the program ends. This is useful because we don’t have to remember to manually close files or free memory — the program will do it for us when it finishes.

In the example, we register three cleanup functions: one that closes a file, one that frees memory, and one that prints a final message. An important detail is that functions registered with atexit() are executed in reverse order: the last one you register will run first.

During the program’s execution, we open a file and allocate memory. Even if something goes wrong and the program ends early using exit(), all the registered cleanup functions will still run. This guarantees that the file is properly closed and the memory is freed, no matter how the program exits.

---
<!-- _class: compact long-title -->

# system(const char command) – Executes a shell command as if typed in the terminal/console.

- **Platform-dependent**, potentially unsafe. Use only for learning.

```c
#include <stdio.h>
#include <stdlib.h>

int main()
{
    printf("%s", "sometext");
    system("cls");   // Windows
    // system("clear"); // Linux/macOS
    return 0;
}
```

- system(\*char)

```text
Header: < stdlib.h>
```

**Result:**

```text
<<NONE>>
```

---

<!-- _class: compact long-title fit-50 -->

# bsearch() – Binary search on a sorted array.<br>Returns pointer to the found element or NULL if not found.

- Binary search works by requiring the array to be **sorted**. Instead of checking every element one by one to determine whether a value appears in the array, we repeatedly **divide the search interval in half**. If the target value is smaller than the middle element, we continue searching in the left half; if it is larger, we search in the right half. This approach dramatically increases efficiency, especially when working with very large datasets.
- The built-in functions **bsearch()** and **qsort()** rely on **comparator functions**. A comparator is a user-provided function that defines how two elements should be compared. Since these library functions only receive raw pointers to memory, they do not know the actual type of the elements. Therefore, the last parameter of both functions is a pointer to a comparator function that tells them how to compare two values correctly.

```c
#include <stdio.h>
#include <stdlib.h>

/* Comparison function for integers */
int cmpInt(const void* a, const void* b)
{
    int x = *(const int*) a;
    int y = *(const int*) b;
    if (x < y) return -1;
    if (x > y) return 1;
    return 0;
}
int main()
{
    int arr[] = { 1, 2, 4, 5, 7, 8, 11 };
    int n = sizeof(arr) / sizeof(arr[0]);
    /* Search for a key */
    int key = 7;
    int* found = (int*) bsearch( &key, arr, n, sizeof(int), cmpInt);
    if (found)
    {
        int index = (int)(found - arr);   // pointer arithmetic
        printf("\nFound %d at index %d.\n", key, index);
    }
    else
        printf("\nValue %d not found in array.\n", key);
    return 0;
}
```

- bsearch(\*void, \*void, int, int, (\*function))

```text
Header: < stdlib.h>
```

**Result:**

```text
Found 7 at index 4.
```

---

<!-- _class: compact long-title -->

# bsearch() – Binary search on a sorted array.<br>Returns pointer to the found element or NULL if not found.

In the C language, there are **no built-in comparator functions**. For this reason, you will very often see comparator functions written in a short, generic form—just like in the example. This simplified version works for general types because it receives two const void\* pointers, casts them to the correct type, and then compares the values manually.

```c
int cmpIntAsc(const void* a, const void* b)
{
    return (*(int*)a - *(int*)b);
}
int cmpIntDesc(const void* a, const void* b)
{
    return (*(int*)b - *(int*)a);
}
int cmpChar(const void* a, const void* b)
{
    return (*(unsigned char*)a - *(unsigned char*)b);
}
int cmpFloat(const void* a, const void* b)
{
    float fa = *(float*)a;
    float fb = *(float*)b;
    return (fa > fb) - (fa < fb); // correct for floats
}
```

- But…

```text
Header: < stdlib.h>
```

---

<!-- _class: compact long-title fit-50 -->

# qsort() – General-purpose quicksort provided by the standard library.<br>Sorts any array given element size and comparator.

- **Quicksort** is one of the fastest and most widely used sorting algorithms. It performs significantly better than simpler methods such as insertion sort or bubble sort, especially on large datasets. When using C’s built-in qsort function, you do not need to know the internal implementation of quicksort — you only need to provide a correct comparator function and call qsort with the proper arguments.
- The built-in functions **bsearch()** and **qsort()** rely on **comparator functions**. A comparator is a user-provided function that defines how two elements should be compared. Since these library functions only receive raw pointers to memory, they do not know the actual type of the elements. Therefore, the last parameter of both functions is a pointer to a comparator function that tells them how to compare two values correctly.

```c
#include <stdio.h>
#include <stdlib.h>

/* Comparison function for integers */
int cmpInt(const void* a, const void* b)
{
    int x = *(const int*) a;
    int y = *(const int*) b;
    if (x < y) return -1;
    if (x > y) return 1;
    return 0;
}
int main()
{
    int arr[] = { 42, 7, 13, 99, 5, 18, 2 };
    int n = sizeof(arr) / sizeof(arr[0]);
    printf("Original array:\n");
    for (int i = 0; i < n; i++)
        printf("%d ", arr[i]);
    printf("\n");
    /* Sort array */
    qsort(arr, n, sizeof(int), cmpInt);
    printf("\nSorted array:\n");
    for (int i = 0; i < n; i++)
        printf("%d ", arr[i]);
    printf("\n");
    return 0;
}
```

- qsort(\*void, int, int, (\*function))

```text
Header: < stdlib.h>
```

**Result:**

```text
Original array:
42 7 13 99 5 18 2

Sorted array:
2 5 7 13 18 42 99
```

---

# Diagnostics and Assertions

---

# 8. Diagnostics and Assertions (&lt;assert.h&gt;)

Useful for debugging and safety.

|Function / Macro|Description|Example|
|---|---|---|
|assert(expr)|Stops program if condition is false.|assert(ptr != NULL);|
|\_\_FILE\_\_, \_\_LINE\_\_|Preprocessor macros with file and line info.|printf("%s:%d", \_\_FILE\_\_, \_\_LINE\_\_);|

---

<!-- _class: compact fit-90 -->

# assert() – tops the program immediately if the given expression evaluates to false.

- It is mainly used for debugging to verify assumptions that *must* be true at runtime.
- It's crucial to remember that the **assert() macro does not call exit()** upon failure.
- When an assertion fails, the program prints an error message to stderr and then calls **abort()**.

```c
#include <assert.h>

// code

void process(int *ptr)
{
    assert(ptr != NULL);   // program stops here if ptr is NULL
    printf("Value = %d\n", *ptr);
}
```

- assert(expr)

```text
Header: <assert.h>
```

---

<!-- _class: compact long-title -->

# \_\_FILE\_\_ and \_\_LINE\_\_ - These are built-in preprocessor macros that expand to the current source file name and current line number.

- They are extremely useful for debugging, logging, and diagnostic messages.

```c
#include <stdio.h>

int main()
{
    printf("This message comes from %s at line %d\n", __FILE__, __LINE__);
    return 0;
}
```

```text
Header: <stdio.h>
```

**Result:**

```text
This message comes from src/main.c at line 4
```

---

# Thank you

- Jakub Leszek Pach
- <jpach@mtech.edu>
