---
marp: true
theme: pach
paginate: true
title: "CSSI112lec 22"
---

- Memset() mozna laczyc z malloc zamiast calloc
- Czy mozna uzyc bezporsrednio realloc na wskazniku wczesniej stworzonej pamieci dynamicznej za pomoca (malloc)
- Memory leaks

<!-- Zielone zrobione, czerwone na nastepne zajecia -->

---

# CSCI 112<br><br>Programming with C

- Lecture 22
- Dr. Jakub L. Pach
- Fall 2025

---

![w:277px Graphic 3](assets/image3.png)

---

## Outline

- Review
- Standard C Library Overview
  - time.h
  - stdarg.h

---

# Review

---

## 1. Character Classification and Conversion (&lt;ctype.h&gt;) Used for testing and converting characters.

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

## 2. String Handling (&lt;string.h&gt;) Used for manipulating null-terminated character arrays.

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

## 3. Memory Handling (&lt;string.h&gt;) Used for working with raw memory blocks.

|Function|Description|Example|
|---|---|---|
|memcpy(dest, src, n)|Copies n bytes.|memcpy(buf2, buf1, n);|
|memmove(dest, src, n)|Safe copy (handles overlap).|memmove(a, b, 5);|
|memcmp(a, b, n)|Compares n bytes.|if (memcmp(a,b,4)==0)|
|memset(ptr, val, n)|Fills memory with byte value.|memset(buf, 0, 10);|
|memchr(ptr, val, n)|Finds a byte in memory.|p = memchr(buf, 'x', 20);|

---

## 4. Input / Output Functions (&lt;stdio.h&gt;) Work with files and streams.

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

## 5. Conversion Functions (&lt;stdlib.h&gt;) Convert strings to numbers.

|Function|Description|Example|
|---|---|---|
|atoi(str)|Converts to int.|x = atoi("123");|
|atol(str)|Converts to long.|y = atol("12345");|
|atof(str)|Converts to double.|z = atof("3.14");|
|strtol(str, end, base)|String → long, supports base.|val = strtol(s, NULL, 16);|
|strtoul(str, end, base)|String → unsigned long.|val = strtoul(s, NULL, 10);|
|strtod(str, end)|String → double.|d = strtod(s, NULL);|

---

## 6. Math Functions (&lt;math.h&gt;) Convert strings to numbers.

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

## 7. Utility Functions (&lt;stdlib.h&gt;) Convert strings to numbers.

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

## 8. Diagnostics and Assertions (&lt;assert.h&gt;) Useful for debugging and safety.

|Function / Macro|Description|Example|
|---|---|---|
|assert(expr)|Stops program if condition is false.|assert(ptr != NULL);|
|\_\_FILE\_\_, \_\_LINE\_\_|Preprocessor macros with file and line info.|printf("%s:%d", \_\_FILE\_\_, \_\_LINE\_\_);|

---

## Standard C Library Overview

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

# Time and Date Functions

---

## 9. Time and Date Functions (&lt;time.h&gt;) Work with clocks and timestamps.

|Function|Description|Example|
|---|---|---|
|time(NULL)|Current time (seconds since epoch).|t = time(NULL);|
|clock()|CPU time used.|clock();|
|difftime(t1,t2)|Difference in seconds.|difftime(t1,t2);|
|mktime(&amp;tm)|Converts struct tm → time\_t.|mktime(&amp;local);|
|asctime(&amp;tm)|Converts struct tm to string.|asctime(localtime(&amp;t));|
|localtime(&amp;t)|Converts to local time struct.|localtime(&amp;t);|
|ctime(&amp;t)|Converts directly to human string.|ctime(&amp;t);|
|strftime(buf, n, fmt, &amp;tm)|Formats time as text.|strftime(s, 20, "%H:%M", &amp;tm);|

---

## time(time\_t \*) – Returns the current calendar time

- (seconds since January 1, 1970 — Unix epoch).

```c
#include <stdio.h>
#include <time.h>

int main()
{
    time_t now = time(NULL);

    printf("Now = %ld\n", now);
    return 0;
}
```

- time()

```c
Header: <time.h>
```

```c
#include <stdio.h>
#include <time.h>

int main()
{
    time_t now;
    time(&now);
    printf("Now = %ld\n", now);
    return 0;
}
```

```c
Now = 1763952307

```

- Result:

---

## time() Function and the Unix Epoch

**The Unix Epoch and time\_t**

- Definition:     The function time\_t time(time\_t \*timer) returns time measured as the number of seconds (type time\_t) that have elapsed since     midnight, January 1, 1970,     UTC (Coordinated Universal Time). This is known as the Unix Epoch.
- Value:     If today were November 23, 2025, the time\_t value would already be over 1,760,000,000 seconds.

**The Year 2038 Problem (Y2K38)**     <br>This issue stems from the historical implementation of the time\_t type:

- **Cause**:     Traditionally, on many 32-bit systems(minGW32), time\_t is implemented as a 32-bit signed integer (signed 32-bit integer).
- **Limit**:     The maximum value this variable can hold is $2^{31} - 1$ seconds.
- **Failure** **Point**:     This limit will be reached on January 19, 2038, at 03:14:07 UTC. After this point, the time counters will "overflow" to the largest negative value,     potentially causing critical system failures based on dating errors.
- **Solution** (64-bit):     Modern systems (including MinGW-w64, Linux, macOS) compiled for 64-bit architecture use a 64-bit time\_t type. This solves the problem for an     extremely long time.
- **New Limit**:     A 64-bit time\_t is sufficient for over 292 billion years. Thus, the Year 2038 problem has been postponed until approximately the     year 292,277,026,596 CE.

---

## time() Function and the Unix Epoch

|**Call Variant**|**Argument Purpose**|**Operation Description**|
|---|---|---|
|**time\_t seconds = time(NULL);**|**NULL** pointer|**The Simplest and Modern Variant.** The programmer is interested **only in the return value** of the function. The function calculates and returns the time, ignoring any memory write.|
|**time(&amp;seconds);**|Pointer to a variable (&amp;seconds)|**The Historical/Compatibility Variant.** The function **writes** the time value to the seconds variable AND **returns** the same value. This is useful when the variable needs to be immediately passed as a pointer to other functions in the &lt;time.h&gt; library (e.g., localtime).|

---

## time() Function and the Unix Epoch

Why a Signed Integer for time\_t?

- time\_t was historically implemented as a signed integer, and this historical decision is precisely the cause of the Year 2038 Problem (Y2K38).

Why a Signed Number (signed) Was Used?

- The reason for using a 32-bit signed integer for time\_t was the initial assumption that Unix systems would need to represent dates preceding the Unix Epoch (before January 1, 1970).Dates before 1970: These are represented by negative numbers (e.g., January 1, 1969, is -31,536,000 seconds).Dates after 1970: These are represented by positive numbers.

---

## Seconds alone tell you nothing about the calendar

We cannot look at it and immediately know the year, month, day, or even the hour. To understand the calendar date, you would need to manually account for:

- leap years
- different month lengths (28/29/30/31)
- daylight saving time
- time zones
- leap seconds (rare, but real)

Doing this manually is error-prone and extremely complicated. Because of this, C provides functions that can convert raw seconds into a structured, human-readable calendar form.

```c
Now = 1763952307

```

- Result:

---

## localtime() – Converting Seconds Into a Calendar Structure

- 1900?

```c
#include <stdio.h>
#include <time.h>

int main()
{
    time_t now;
    time(&now);
    struct tm* info = localtime(&now);
    printf("Year: %d\n", info->tm_year + 1900);
    return 0;
}
```

- localtime(time\_t \*)

```c
Header: <time.h>
```

```c
Year: 2025

```

- Result:

```c
localtime() transforms time_t into a struct tm, which contains:
int tm_sec;
int tm_min;
int tm_hour;
int tm_mday;
int tm_mon;
int tm_year;
int tm_wday;
int tm_yday;
int tm_isdst;
```

---

## Why does struct tm store the year as *years since 1900*?

Historical reason — backward compatibility

- When early operating systems and time libraries were created (1960s–1970s), memory was extremely limited and expensive. Saving even a few bytes mattered.
- The year was stored as a 2-digit number
- Early systems stored the year in just 2 decimal digits (e.g., 74 → 1974), because it fit in 1 byte instead of using 4 full digits.
- Unix and the C language inherited this design
- When Unix time libraries were developed, they reused concepts from older systems.

When the struct tm type was defined, the designers decided to:

- use a full 32-bit integer for convenience,
- but keep the old representation for backward compatibility.

---

## Summary

- struct tm originates from early systems with extremely limited memory.
- The year used to be stored in **two digits**, so an offset of **1900** was added.
- POSIX and the C standard preserved this for backward compatibility.
- Therefore, we must always compute: year = tm\_year + 1900;

---

## struct tm

- **Leap second**

The field tm\_sec may legally have the value 60.

This happens because of the leap second — occasionally astronomers add one extra second to keep atomic time aligned with Earth's rotation.

```c
struct tm {
    int tm_sec;   // seconds after the minute — [0, 60]
    int tm_min;   // minutes after the hour — [0, 59]
    int tm_hour;  // hours since midnight — [0, 23]
    int tm_mday;  // day of the month — [1, 31]
    int tm_mon;   // months since January — [0, 11]
    int tm_year;  // years since 1900
    int tm_wday;  // days since Sunday — [0, 6]
    int tm_yday;  // days since January 1 — [0, 365]
    int tm_isdst; // Daylight Saving Time flag
};
```

- Most fields are zero-based, meaning they start from 0:
  - tm\_sec    — 0–59 normally, 60 during a leap second
  - tm\_min    — 0–59
  - tm\_hour    — 0–23
  - tm\_wday    — day of week, 0 = Sunday
  - tm\_yday    — day of year, 0 = January 1st
  - tm\_mon    — 0 = January, 11 = December
- However, there is one exception:
  - tm\_mday (day of month)
    - is 1-based → range 1–31(because real-world months do not start from day 0)

---

## struct tm

```c
#include <stdio.h>
#include <time.h>

int main()
{
    time_t now;
    time(&now);
    struct tm* info = localtime(&now);
    printf("Sec: %d\n", info->tm_sec );
    printf("Min: %d\n", info->tm_min );
    printf("Hour: %d\n", info->tm_hour );
    printf("Day: %d\n", info->tm_mday );
    printf("Month: %d\n", info->tm_mon );
    printf("Year: %d\n", info->tm_year + 1900 );
    printf("Day of the week: %d\n", info->tm_wday);
    printf("Day of the year: %d\n", info->tm_yday);
    printf("Daylight Saving Time flag: %d\n", info->tm_isdst);
    return 0;
}
```

```c
Sec: 57
Min: 7
Hour: 21
Day: 23
Month: 10
Year: 2025
Day of the week: 0
Day of the year: 326
Daylight Saving Time flag: 0
```

- Result:

---

## clock() – Returns the number of CPU clock ticks since the program started

- Used for measuring **CPU time**, not real time.

```c
#include <stdio.h>
#include <time.h>

int main()
{
    clock_t start = clock();
    // ... some work ...
    for (int i = 0; i < __INT32_MAX__; i++) 1;
    clock_t end = clock();
    double cpu_time = (double)(end - start) / CLOCKS_PER_SEC;
    printf("CPU time = %f seconds\n", cpu_time);
    return 0;
}
```

- clock()

```c
Header: <time.h>
```

```c
CPU time = 0.895000 seconds

```

- Result:

```c
#define CLOCKS_PER_SEC ((clock_t)(1000))
Number of clock ticks per second. A clock tick is the unit by which
processor time is measured and is returned by 'clock'.
Expands to:
((clock_t)(1000))
```

---

## Understanding clock() in C

**What clock() Was Originally Designed For**

- When C and POSIX were being developed, **computers ran at fixed CPU frequencies**.
- clock() returned the **number of CPU ticks consumed by the program**.
- Dividing ticks by a constant (CLOCKS\_PER\_SEC) gave an **approximate runtime in seconds**.
- This worked **only because CPU frequency did not change**.

---

## What clock() Actually Measures

- It does not measure real-world (wall-clock) time.
- It measures CPU time used by the process, NOT time spent waiting.
- Example:
  - If your program waits for keyboard input, sleeps, or blocks on I/O:
    - This waiting time is NOT counted.
- Therefore, clock() only represents processor cycles actively spent executing your code.

---

## Why clock() No Longer Corresponds to Real Seconds

- Modern CPUs constantly change frequency:
  - turbo boost
  - thermal throttling
  - power-saving modes
  - multiple cores &amp; dynamic scaling
- Because of this:
  - CPU ticks do not correspond to real time in a stable way.
  - The original assumption (“ticks / frequency = seconds”) is now invalid.

---

## The Real Purpose of clock()

- Its true purpose remains:
  - **measure CPU usage**,
  - primarily for **performance comparison** between code variants.
- It is **not** suitable for:
  - measuring real elapsed time,
  - timing user interactions,
  - benchmarking I/O,
  - measuring delays or pauses.

---

## difftime() – Returns the difference between two time\_t values in seconds: t1 − t2

- Measuring Wall-Clock Time Differences: It is ideal for measuring real-world time intervals (wall-clock time) between two points (e.g., the start and end of some operation).
- Lack of CPU Time Precision: It should not be used for measuring CPU time or for micro-profiling, as it is based on the time\_t type, which typically only has second-level precision.

```c
#include <stdio.h>
#include <time.h>

int main()
{
    time_t now;
    time(&now);
    time_t start, stop;
    start = time(NULL);
    for (int i = 0; i < __INT32_MAX__; i++) 1;  // ... some work ...
    stop = time(NULL);
    double real_time = difftime(stop, start);
    printf("Real time = %f seconds\n", real_time);
    return 0;
}
```

- difftime(int, int)

```c
Header: <time.h>
```

```c
Real time = 1.000000 seconds

```

- Result:

---

## mktime() – Converts a filled struct tm into a time\_t

- Also automatically normalizes values (e.g., month = 13 → next year).

```c
#include <stdio.h>
#include <time.h>

int main()
{
    struct tm tmval = {0};
    tmval.tm_year = 2025 - 1900;
    tmval.tm_mon  = 11;  // November
    tmval.tm_mday = 24;

    time_t t = mktime(&tmval);
    printf("Epoch time = %ld\n", t);
    return 0;
}
```

- mktime(\*tm)

```c
Header: <time.h>
```

```c
Epoch time = 1766559600

```

- Result:

---

## asctime() – Converts a struct tm into a human-readable string

- Returns a static string (NOT thread safe).

```c
#include <stdio.h>
#include <time.h>

int main()
{
    struct tm tmval = {0};
    tmval.tm_year = 2025 - 1900;
    tmval.tm_mon  = 11;  // November
    tmval.tm_mday = 24;


    printf("%s", asctime(&tmval));
    return 0;
}
```

- asctime(\*tm)

```c
Header: <time.h>
```

```c
Sun Dec 24 00:00:00 2025

```

- Result:

---

## ctime() – Converts time\_t directly into a readable string

- (similar to asctime, also not thread-safe).

```c
#include <stdio.h>
#include <time.h>

int main()
{
    struct tm tmval = {0};
    tmval.tm_year = 2025 - 1900;
    tmval.tm_mon  = 11;  // November
    tmval.tm_mday = 24;


    printf("%s", asctime(&tmval));
    return 0;
}
```

- ctime(\*t)

```c
Header: <time.h>
```

```c
Now: Sun Nov 23 21:55:04 2025
```

- Result:

---

## strftime() – Formats a struct tm into a custom string according to fmt

- (similar to asctime, also not thread-safe).

```c
#include <stdio.h>
#include <time.h>

int main()
{
    char buf[64];
    struct tm *info;
    time_t now;

    now = time(NULL);
    info = localtime(&now);
    strftime(buf, sizeof(buf), "%Y-%m-%d %H:%M:%S", info);
    printf("Formatted date = %s\n", buf);
    return 0;
}
```

- strftime(buf, n, fmt, \*tm)

```c
Header: <time.h>
```

```c
Formatted date = 2025-11-23 21:58:37
```

- Result:

---

# Variable Argument Lists

---

## 10. Variable Argument Lists (&lt;stdarg.h&gt;) For functions that accept a variable number of parameters.

|Macro|Description|Example|
|---|---|---|
|va\_start(list, last)|Initializes argument list.|va\_start(args, n);|
|va\_arg(list, type)|Retrieves next argument.|sum += va\_arg(args, int);|
|va\_end(list)|Cleans up argument list.|va\_end(args);|

---

## Variadic Functions (stdarg.h)

- Some functions can accept a **variable number of arguments**.
- Classic examples: printf(), scanf(), fprintf().
- Because C does *not* store information about how many arguments were passed or what their types are, the programmer must manually manage access to them using the mechanisms from &lt;stdarg.h&gt;:
- va\_list
- va\_start()
- va\_arg()
- va\_end()
- These four elements always work **together** and should be understood as one mechanism.

---

## How variadic functions work in C

A variadic function has the following form: int example(int fixed\_param, ...);

- Everything before the ellipsis (...) is **fixed**. Everything after is **unknown**, and C does *not* record:
- how many arguments were passed,
- what types they have,
- how large they are.

Therefore, the programmer must provide enough **context** for the function to decode the arguments safely — usually through an explicit parameter like:

- a count (printf("%d %d", ...) has the format string),
- a terminating value,
- or a fixed "type code" before each argument.

---

## The va\_list mechanism

- **1. va\_list**
  - A special type that represents the current position inside the variable argument list. va\_list args;
- **2. va\_start(list, last\_fixed\_param)**
  - Initializes the va\_list so you can begin reading additional arguments.:
    - The second parameter **must** be the name of the last fixed argument.
    - C calculates where the variable arguments begin using its memory layout.
    - Example:  va\_start(args, count);
- **3. va\_arg(list, type)**
  - Retrieves the **next** argument from the list.
    - You must specify the exact type stored.
    - If you use the wrong type → Undefined Behavior.
    - Example: int x = va\_arg(args, int);
- **4. va\_end(list)**
  - Cleans up the va\_list. You **must** call this before leaving the function.

---

## Variadic Functions - example

**Explanation:**

- count tells the function how many integers to read.
- va\_start initializes access to the extra arguments.
- each va\_arg(args, int) retrieves one integer.
- va\_end finishes the process.

```c
#include <stdio.h>
#include <time.h>

int main()
{
    printf("%d\n", sum_ints(4, 10, 20, 30, 40));
	// prints 100
    return 0;
}
```

```c
Header: <stdarg.h>
```

```c
100

```

- Result:

```c
int sum_ints(int count, ...)
{
    va_list args;
    va_start(args, count);
    int sum = 0;
    for (int i = 0; i < count; i++)
    {
        sum += va_arg(args, int);
    }
    va_end(args);
    return sum;
}
```

---

## Variadic Functions - example

Because C does not know the types of the variable arguments, the programmer must encode them manually.

**Common pitfalls:**

- C does not store argument types — you *must* know them
- You must call va\_end()
- Passing complex structs by value is unsafe
- Using the wrong type in va\_arg → undefined behavior
- Cannot be used to inspect arguments at runtime (no reflection)

```c
Header: <stdarg.h>
```

```c
void print_values(int count, ...)
{
    va_list args;
    va_start(args, count);
    for (int i = 0; i < count; i++)
    {
        int type = va_arg(args, int);   // read a type code first
        if (type == 0)
        {
            printf("int: %d\n", va_arg(args, int));
        }
        else if (type == 1)
        {
            printf("double: %f\n", va_arg(args, double));
        }
        else if (type == 2)
        {
            printf("string: %s\n", va_arg(args, char*));
        }
    }
    va_end(args);
}
```

---

# Thank you

- Jakub Leszek Pach
- <jpach@mtech.edu>

---

## Most Common System Libraries in Windows (WinAPI) These headers are provided with the Windows SDK and are available in compilers such as MinGW, MSVC, and others for the Windows platform.

|Library|Description|Typical Functions|
|---|---|---|
|**windows.h**|The main gateway to the Windows API – contains basic type definitions, macros, and core system functions.|CreateFile(), ReadFile(), Sleep(), MessageBox()|
|**winuser.h**|Part of the Windows API responsible for creating and managing windows, messages, and user interface elements.|CreateWindow(), ShowWindow(), GetMessage()|
|**wincon.h**|Provides access to the Windows console (terminal) and its properties.|SetConsoleTextAttribute(), GetConsoleScreenBufferInfo()|
|**processthreadsapi.h**|Manages processes and threads.|CreateProcess(), ExitProcess(), GetCurrentThreadId()|
|**synchapi.h**|Synchronization mechanisms such as mutexes, semaphores, and events.|CreateMutex(), WaitForSingleObject()|
|**fileapi.h**|Handles file and directory operations.|CreateFile(), ReadFile(), WriteFile()|
|**timeapi.h**|Provides system time and timer-related functions.|timeGetTime(), Sleep()|
|**winsock2.h**|Networking (sockets) – TCP/IP interface for Windows.|socket(), connect(), send(), recv()|
|**shellapi.h**|Integrates applications with the Windows shell (opening files, shortcuts, icons).|ShellExecute(), ExtractIcon()|
|**commdlg.h**|Provides standard dialog boxes (open/save file, color picker, font selection).|GetOpenFileName(), ChooseColor()|
