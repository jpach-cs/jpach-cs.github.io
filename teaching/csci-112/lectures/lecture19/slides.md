---
marp: true
theme: pach
paginate: true
title: "CSSI112lec 19"
---

- Czy isupper || islower == isalpha()
- Czy strcpy() I memcpy() moze dzialac tak samo
- strlen(s) czy moze byc uzyte na tablicy int
- Memset() mozna laczyc z malloc zamiast calloc
- Czy mozna uzyc bezporsrednio realloc na wskazniku wczesniej stworzonej pamieci dynamicznej za pomoca (malloc)
- Memory leaks

<!-- Zielone zrobione, czerwone na nastepne zajecia -->

---

# CSCI 112<br><br>Programming with C

- Lecture 19
- Dr. Jakub L. Pach
- Fall 2025

---

![w:277px Graphic 3](assets/image3.png)

---

## Outline

- Review
- Static Memory
- Dynamic Memory allocation
- Standard C Library Overview
  - stdio.h

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

## When we run a program

- ...
- ...
- 0061FF14
- (6,422,292)

```c
#include <stdio.h>
int main()
{
  int x = 0x12345678, y = 0xAABBCCDD, z = 0x11223344;
  printf("%-4s equals %d.\n", "x", &x);
  printf("%-4s equals %d.\n", "y", &y);
  printf("%-4s equals %d.\n", "z", &z);
  return 0;
}
```

```c
x    equals 6422292.
y    equals 6422288.
z    equals 6422284.
```

- Result:
- 0061FF10
- (6,422,288)
- 0061FF0C
- (6,422,284)
- The compiler, when declaring a variable x of type int, reserves 4 bytes of memory, which means it decrements the stack pointer (held in the stack pointer register) by 4, then writes the contents from the least significant bit to the most significant bit starting from that address.
- It then proceeds similarly with the next variable y of type int,
- and analogously with the variable z.

|B|B|B|B|B|B|B|B|B|B|B|B|B|B|B|B|B|B|B|B|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

- 0061FF10

```c
(Stack Pointer)
```

- 0061FF18

---

## Take a closer look at this fragment of memory

- ...
- 0061FF14
- (6,422,292)

```c
#include <stdio.h>
int main()
{
  int x = 0x12345678, y = 0xAABBCCDD, z = 0x11223344;
  printf("%-4s equals %d.\n", "x", &x);
  printf("%-4s equals %d.\n", "y", &y);
  printf("%-4s equals %d.\n", "z", &z);
  return 0;
}
```

```c
x    equals 6422292.
y    equals 6422288.
z    equals 6422284.
```

- Result:
- 0061FF10
- (6,422,288)
- 0061FF0C
- (6,422,284)

|B|B|B|B|B|B|B|B|B|B|B|B|B|B|B|B|B|B|B|B|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

- 0061FF10

```c
(Stack Pointer)
```

- 0061FF18

|Address|Value|
|---|---|
|0061FF18|...|
|0061FF17|0x12|
|0061FF16|0x34|
|0061FF15|0x56|
|0061FF14|0x78|
|0061FF13|0xAA|
|0061FF12|0xBB|
|0061FF11|0xCC|
|0061FF10|0xDD|
|0061FF0F|0x11|
|0061FF0E|0x22|
|0061FF0D|0x33|
|0061FF0C|0x44|
|0061FF0B|...|

- SP

---

## Take a closer look at this fragment of memory

```c
int main()
{  int x = 0x12345678, y = 0xAABBCCDD, z = 0x11223344; return 0;}
```

|Address|Value|
|---|---|
|0061FF18|...|
|0061FF17|0x12|
|0061FF16|0x34|
|0061FF15|0x56|
|0061FF14|0x78|
|0061FF13|0xAA|
|0061FF12|0xBB|
|0061FF11|0xCC|
|0061FF10|0xDD|
|0061FF0F|0x11|
|0061FF0E|0x22|
|0061FF0D|0x33|
|0061FF0C|0x44|
|0061FF0B|...|

- SP

Data storage in RAM in Windows systems follows the little-endian standard, which means we start counting bits from the least significant bit, i.e., from the 2^0, and at the lowest memory address after reserving space, we write the successive bytes of our multi-byte variable, array, etc.

---

## malloc() &amp; free() – Allocating/Deallocating a block of memory

- To use dynamic memory allocation functions like malloc, you need to include the stdlib.h library.
- Malloc and free are always used together.
- The malloc function does not initialize the values of the allocated memory block; the values remain as they were previously in that memory area.

```c
#include <stdio.h>
#include <stdlib.h>

int main()
{

    int stackVariable = 5; // Declare a variable on the stack
    printf("Address of stackVariable: %p\n", &stackVariable);

    // Allocate memory on the heap for an integer
    int *heapValue = (int*) malloc( sizeof(int) * 1  );  // Size multiplied by the number of elements
    //Since the malloc function returns a void pointer,
    //it is recommended to explicitly cast it to the desired type, such as int*, to avoid ambiguity.

    if (heapValue)      //(heapValue != NULL)
    {
        *heapValue = 5; // Assign a value to the allocated memory
        printf("Address of heapValue: %p\n", heapValue);
        printf("The value of dynamicVariable is = %d\n", *heapValue);

        free(heapValue); // Deallocate the memory - so important!
    }
    else
        printf("Memory allocation failed!\n");
    return 0;
}
```

```c
Address of stackVariable: 0062ff14
Address of heapValue: 00c41808
The value of dynamicVariable is = 5

```

- Result:
- Malloc expects only one argument, the number of bytes to be allocated.

---

## Memory

|B|B|B|B|B|B|B|
|---|---|---|---|---|---|---|

- FFFFFFFF
- ...

|B|B|B|B|B|B|B|
|---|---|---|---|---|---|---|

- 00000006
- 0062FF14
- (6,422,292)
- FFFFFFFE

```c
(4,294,967,295)
```

- ...

|B|B|B|B|B|B|B|
|---|---|---|---|---|---|---|

- 00000005
- 00000004
- 00000000
- stackVariable
- ...

|B|B|B|B|B|B|B|
|---|---|---|---|---|---|---|

- Stack
- Heap
- 00B81808
- (12, 064,776)
- heapValue

<!-- 0061FF14 =  06422292
00B81808 = 12064776 -->

---

## malloc() – An array

- Malloc does not require static values for allocation.
- Malloc expects only one argument, the number of bytes to be allocated.

```c
#include <stdio.h>
#include <stdlib.h>

int main()
{
    const int n = 3;
    int m = 3;
    int stackArray[n];

    printf("Address of stackArray[0]:\t %.8d\n", &stackArray[0]);
    printf("Address of stackArray[1]:\t %.8d\n", &stackArray[1]);
    printf("Address of stackArray[2]:\t %.8d\n\n", &stackArray[2]);

    int *heapArray = (int*) malloc( sizeof(int) * m  );

    if (heapArray)
    {
        printf("Address of heapArray[0]:\t %.8d\n", &heapArray[0]);
        printf("Address of heapArray[1]:\t %.8d\n", &heapArray[1]);
        printf("Address of heapArray[2]:\t %.8d\n\n", &heapArray[2]);

        free(heapArray); // so important!
    }
    else
        printf("Memory allocation failed!\n");
    return 0;
}
```

```c
Address of stackArray[0]:        06487768
Address of stackArray[1]:        06487772
Address of stackArray[2]:        06487776

Address of heapArray[0]:         06559344
Address of heapArray[1]:         06559348
Address of heapArray[2]:         06559352

```

- Result:

---

## Summary

When a process is allocated memory for itself, it is copied into RAM, and the stack is placed at the end of this allocated block. Dynamic memory—the heap—is located "outside" of this process's memory space. The operating system assigns an additional block of memory for malloc(), which is why addresses in the heap can be larger than those within the process's memory.

When a program that utilizes dynamically allocated memory crashes and fails to deallocate the memory it has requested, this memory may remain inaccessible until the system is rebooted. While operating systems have mechanisms in place to reclaim such memory, these mechanisms vary significantly between different systems. This phenomenon, where memory is unintentionally retained by a program, is known as a memory leak.

---

## calloc()

- calloc() is similar to malloc() but additionally initializes the allocated memory to zero.
- calloc() is slower than malloc() due to this extra operation. However, calloc() is more efficient when you need an array filled with zeros.
- Both malloc() and calloc() use the free function to deallocate memory.

```c
#include <stdio.h>
#include <stdlib.h>

int main()
{
    int n = 3;
    int *heapArray1 = (int*) calloc( n, sizeof(int)   );
    int *heapArray2 = (int*) malloc( sizeof(int) * n  );

    if (heapArray1)
    {
        printf("The value of heapArray1[0]:\t %.8d\n", heapArray1[0]);
        printf("The value of heapArray1[1]:\t %.8d\n", heapArray1[1]);
        printf("The value of heapArray1[2]:\t %.8d\n\n", heapArray1[2]);
        free(heapArray1); // so important!
    }
    if (heapArray2)
    {
        printf("The value of heapArray2[0]:\t %.8d\n", heapArray2[0]);
        printf("The value of heapArray2[1]:\t %.8d\n", heapArray2[1]);
        printf("The value of heapArray2[2]:\t %.8d\n\n", heapArray2[2]);

        free(heapArray2); // so important!
    }
    return 0;
}
```

```c
The value of heapArray1[0]:      00000000
The value of heapArray1[1]:      00000000
The value of heapArray1[2]:      00000000

The value of heapArray2[0]:      -1163005939
The value of heapArray2[1]:      -1163005939
The value of heapArray2[2]:      -1163005939

```

- Result:

---

## realloc()

```c
Data loss: When reducing the size of a block, data located outside the new, smaller block will be lost.
Data movement: realloc() may move the entire memory block to a new location, so always update the pointer.
Freeing memory: If realloc() is successful, the original block will be automatically freed.
void *realloc(void *ptr, size_t new_size);

```

```c
#include <stdio.h>
#include <stdlib.h>

int main()
{
    int n = 10;

    int *heapArray1 = (int*)malloc(n * sizeof(int));
    // ...
    // After some time, we want to reduce the size of the array to 5 elements
    int *newHeapArray1 = (int*)realloc(heapArray1, 5 * sizeof(int));
    if (newHeapArray1 == NULL)
    {
        printf("Handle error: allocation failed\n");
        free(heapArray1);
    }
    else
    {
        printf("Successful allocation, update the pointer\n");
        heapArray1 = newHeapArray1;
    }
    //...

    if(heapArray1)
        free(heapArray1);

    getchar();
    return 0;
}
```

```c
Successful allocation, update the pointer

```

- Result:

What does realloc() return?

- **Success:** It returns a pointer to the new (or resized) block of memory. This may be the same pointer as ptr if the enlargement operation was possible without moving the data.
- **Failure:** It returns NULL if the new memory block could not be allocated. In this case, the original block remains unchanged."

---

## Summary

When a process is allocated memory for itself, it is copied into RAM, and the stack is placed at the end of this allocated block. Dynamic memory—the heap—is located "outside" of this process's memory space. The operating system assigns an additional block of memory for malloc, which is why addresses in the heap can be larger than those within the process's memory.

When a program that utilizes dynamically allocated memory crashes and fails to deallocate the memory it has requested, this memory may remain inaccessible until the system is rebooted. While operating systems have mechanisms in place to reclaim such memory, these mechanisms vary significantly between different systems. This phenomenon, where memory is unintentionally retained by a program, is known as a memory leak.

---

## Memory fragmentation

Memory fragmentation is a problem that can occur when memory is repeatedly allocated and deallocated using functions like malloc and free. Imagine RAM memory as a long tape, on which pieces of memory are allocated. Over time, as we free some pieces, empty spaces are created between the occupied fragments. These free spaces may be too small to accommodate new, larger memory blocks, even if the total amount of free memory is sufficient. This phenomenon is called fragmentation.

**Types of fragmentation:**

- External fragmentation:
  - Occurs when there are free spaces between occupied memory blocks that are too small to satisfy new allocation requests.
- Internal fragmentation:
  - Occurs when an allocated memory block is larger than actually needed, leading to wasted memory.

---

## Consequences of fragmentation

- Memory leaks:
  - If memory is not managed carefully, fragmentation can lead to memory leaks, which is a situation where a program no longer frees unnecessary memory, which over time can lead to application crashes.
- Performance degradation:
  - Fragmentation can slow down program execution, as the operating system has to search longer for suitable free memory blocks.
- Limited available memory:
  - Even if there is a lot of free memory, fragmentation can prevent the allocation of larger blocks, which can lead to program errors.

---

## Summary

- Memory fragmentation is a serious problem that can negatively impact the performance and stability of programs. Understanding the causes of fragmentation and applying appropriate memory management techniques is key to creating efficient applications.
- To counteract the problem of memory fragmentation, a good programming practice is to use realloc() instead of malloc() or alloc() when working with the same data and needing to change its size.

---

# Standard C Library Overview<br> (MinGW / C Standard)

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

# Input / Output Functions

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

## Standard Streams in C

- C provides three predefined file streams that are automatically opened when a program starts:
- Each of these is a FILE \* object defined in **&lt;stdio.h&gt;**, just like any file opened with fopen().

|Stream|Type|Typical Use|Connected To|
|---|---|---|---|
|stdin|Input|Reading input (e.g., with scanf() or fgets())|Keyboard|
|stdout|Output|Writing normal output (e.g., with printf())|Console / Terminal|
|stderr|Output|Writing error messages|Console / Terminal (separate from stdout)|

---

## Standard Streams in C

- stdout and stderr are both used for output, but stderr is not buffered by default <br>— this means error messages appear immediately, even if the program crashes afterward.
- You can redirect them independently in the command line:
- You can also explicitly write to these streams:

```c
./program > output.txt       # redirects stdout
./program 2> errors.txt      # redirects stderr
./program > all.txt 2>&1     # redirects both
```

```c
fprintf(stdout, "Normal output\n");
fprintf(stderr, "Error message\n");
```

---

## fopen()    – Opens a file and returns a FILE\* pointer..<br>fclose()    – Closes an open file. Always close files when done Typically used for initializing arrays or structs.

- Hello, file!
- Result:

```c
#include <stdio.h>
#include <string.h>

int main()
{
    FILE *fp = fopen("data.txt", "w");
    if (fp == NULL)
    {
        printf("Failed to open file.\n");
        return 1;
    }
    fprintf(fp, "Hello, file!\n");
    fclose(fp);
    return 0;
}
```

```c
Header: <stdio.h>
```

---

## fflush()– Flushes the output buffer to the file immediately (useful before closing or switching)

- In C: Use fflush(file\_pointer) before closing critical files to guarantee data integrity. You are essentially clearing out anything that might be stuck in the buffer right before the file handle is released.
- In C++: std::endl is equivalent to the sequence of inserting a newline (\n) followed by a flush(). It is convenient, but using a simple \n is faster when immediate flushing is not strictly required.

```c
#include <stdio.h>
#include <string.h>

int main()
{
    FILE *fp = fopen("data.txt", "w");
    /* ... */
    fflush(fp);  // Force write to disk now
    fclose(fp);
    return 0;
}
```

- fflush(fp)

```c
Header: <stdio.h>
```

---

## clearerr(fp)     – Clears the EOF and error indicators.<br>ferror(fp)     – Checks for file I/O errors. Returns non-zero if an error occurred

- Within the FILE structure managed by the standard C library (for I/O streams), there is an internal error pointer (flag) that is set when a persistent error occurs during an input/output operation.
- Setting the Flag: When you call an I/O function (e.g., fread(), fwrite(), fgetc()) and that operation encounters an error—for instance, a disk read error—the system sets the internal error flag for that specific stream (FILE \*).
- Effect on Operation: Once the flag is set, most subsequent I/O operations on that stream will immediately fail (or return an error) until the flag is reset. This prevents attempts at further operations on a corrupted stream.
- Resetting: If you determine the error was temporary or you want to reset the stream's state to attempt to continue operations, you use the function clearerr(stream).

```c
0
1
0
```

- Result:

```c
#include <stdio.h>
#include <string.h>
#include <stdbool.h>

int main()
{
    FILE *fp = fopen("data.txt", "r");
    if (fp == NULL)
    {
        printf("Failed to open file.\n");
        return 1;
    }
    bool result = ferror(fp);
    printf("%d\n", result);
    int x = 5;
    fwrite(&x, 1, 4, fp );
    result = ferror(fp);
    clearerr(fp);
    printf("%d\n", result);
    result = ferror(fp);
    printf("%d\n", result);
    fclose(fp);
    return 0;
}
```

- clearerr(fp) / ferror(fp)

```c
Header: <stdio.h>
```

---

## feof() – Checks if the end of the file has been reached. Returns non-zero (true) if EOF is set

```c
#include <stdio.h>
#include <string.h>

int main()
{
        FILE *fp = fopen("data.txt", "r");
        while (!feof(fp))
        {
            int c = fgetc(fp);
            if (c == EOF) break;
            putchar(c);
        }
        fclose(fp);
    return 0;
}
```

- feof(fp)

```c
Header: <stdio.h>
```

```c
#define EOF (-1)
Returned by various functions on end of file condition or error.
Expands to:
(-1)
```

---

## perror() – Prints a human-readable error message related to the last I/O failure

```c
#include <stdio.h>
#include <string.h>

int main()
{
    FILE *fp = fopen("missing.txt", "r");
    if (!fp)
        perror("Error opening file");
    return 0;
}
```

- perror(msg)

```c
Header: <stdio.h>
```

```c
Error opening file: No such file or directory
```

```c
Result(stderr):
```

---

## freopen() – Reopens an existing stream (e.g., redirect stdin or stdout)

```c
#include <stdio.h>
#include <string.h>

int main()
{
    freopen("output.txt", "w", stdout);  // redirect printf() to file
    printf("This will be written to output.txt!\n");
    fclose(stdout);
    return 0;
}
```

- freopen(…)

```c
Header: <stdio.h>
```

```c
Result(stdout):
```

```c
This will be written to output.txt!

```

```c
Result(output.txt):
```

---

## tmpfile() – Creates a temporary file that is automatically deleted when closed or program ends

- On **Unix-like systems** such as Linux and macOS, temporary files are typically placed in the **/tmp** directory. Conversely, on **Windows systems**, the location is defined by environment variables like **%TEMP%** or **%TMP%** for the current user, usually resolving to a path within the user's local application data folder (C:\Users\\[UserName\]\AppData\Local\Temp)
- The function's true value lies in how it manages the file lifecycle. First, it ensures the file is created with a **Unique Name**, effectively preventing naming collisions with other running programs. Second, the file is opened in a robust **Binary Read and Write mode** ("wb+"). Most importantly, the file is **automatically marked for deletion** (or *unlinked*) the moment the associated stream is closed using fclose(), or when the program terminates normally by calling exit(). This automatic cleanup guarantees the file is created in a safe location where the operating system has **write permissions** and ensures the resource **disappears** when no longer needed, making it fundamentally safer and cleaner than manually managing temporary files in the program's executable directory.
- Temporary data
- Result(temp\*):

```c
#include <stdio.h>
#include <string.h>

int main()
{
    FILE *temp = tmpfile();
    fprintf(temp, "Temporary data\n");
    rewind(temp);
    fclose(temp);
    return 0;
}
```

- tmpfile()

```c
Header: <stdio.h>
```

- The location where the tmpfile() function creates a temporary file is **not guaranteed to be the current working directory**; instead, it is dependent on the specific **operating system implementation** and current **environmental settings**. This function consistently utilizes the system's **default temporary directory**.

---

## tmpnam() – Generates a unique temporary filename (does not create the file)

```c
Temporary filename: \s3r4.
```

- Result(temp\*):

```c
#include <stdio.h>
#include <string.h>

int main()
{
    char name[L_tmpnam];
    tmpnam(name);
    printf("Temporary filename: %s\n", name);
    return 0;
}
```

- tmpnam(char\*)

```c
Header: <stdio.h>
```

\#define L\_tmpnam (16)

The maximum size of name (including NUL) that will be put in the user supplied buffer caName for tmpnam. Inferred from the size of the static buffer returned by tmpnam when passed a NULL argument. May actually be smaller.

Expands to:

(16)

---

## rename()    – Changes a file’s name.<br>remove()    – Deletes a file from disk

```c
#include <stdio.h>
#include <string.h>

int main()
{
    FILE *fp = fopen("data.txt", "wt");
    fclose(fp);
    rename("data.txt", "final.txt");
    remove("final.txt");
    return 0;
}
```

- rename(old, new) /remove(name)

```c
Header: <stdio.h>
```

|remove(name)|Deletes file.|remove("old.txt");|
|---|---|---|
|rename(old, new)|Renames file.|rename("a.txt","b.txt");|

---

# Thank you

- Jakub Leszek Pach
- <jpach@mtech.edu>

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
|rand()|Returns pseudo-random number.|x = rand() % 10;|

---

## 8. Diagnostics and Assertions (&lt;assert.h&gt;) Useful for debugging and safety.

|Function / Macro|Description|Example|
|---|---|---|
|assert(expr)|Stops program if condition is false.|assert(ptr != NULL);|
|\_\_FILE\_\_, \_\_LINE\_\_|Preprocessor macros with file and line info.|printf("%s:%d", \_\_FILE\_\_, \_\_LINE\_\_);|

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

## 10. Variable Argument Lists (&lt;stdarg.h&gt;) For functions that accept a variable number of parameters.

|Macro|Description|Example|
|---|---|---|
|va\_start(list, last)|Initializes argument list.|va\_start(args, n);|
|va\_arg(list, type)|Retrieves next argument.|sum += va\_arg(args, int);|
|va\_end(list)|Cleans up argument list.|va\_end(args);|

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

---

## Historia C

- ?

---

## Syllabus - Textbooks

- Brian W. Kernighan, Dennis M. Ritchie. C Programming Language, 2nd Edition. Prentice Hall, 1988
- Seacord, R. C. (2024). Effective C: An Introduction to Professional C Programming. No Starch Press, Inc. (Optional)

![w:251px Amazon.com: C Programming Language, 2nd Edition: 8601410794231: Brian W.  Kernighan, Dennis M. Ritchie: Books](assets/image5.jpeg)

![Picture 4](assets/image6.jpeg)

- Dennis M. Ritchie

<!-- the co-author of this book is the creator of this language!
In the past, textbooks were the primary source of knowledge in higher education. Lectures and labs were just a small supplement to the content found in textbooks. With the advancement of technology, presentations have become the primary source of information for students, and only the most curious students seek additional content in textbooks recommended by professors. -->
