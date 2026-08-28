---
marp: true
theme: pach
paginate: true
class: compact
footer: "CSCI 112 | Programming with C | J. L. Pach"
title: "CSCI 112  Programming with C"
---

<!-- _class: compact lead -->

# CSCI 112<br><br>Programming with C

- Lecture 16
- Dr. Jakub L. Pach
- Fall 2025

---

# Outline

- Review
- File Input / Output
- Lists

---

# Review

---

# Unions

- Unions in C are special data types that allow different data types to be stored in the same memory location.

**Syntax:**

```c
unions symbolic_name1
{
	<statement1>
}<symbolic_name2, ...>;
```

- Everything that is in angle brackets &lt;&gt; is optional.

---

# An example - unions

```c
#include <stdio.h>
union Example
{
    short s;
    char c;
    int i;
};

int main(int argc, char *argv[])
{
    union Example example;
    printf( "Union Example:\n" );

    example.s = 5;
    printf( "The value of [example.s] = %d\n", example.s );
    example.c = 'A';
    printf( "The value of [example.c] = %d\n", example.c );
    example.i = 63123;
    printf( "The value of [example.i] = %d\n", example.i );
    /*but...*/
    printf( "The value of [example.s] = %d\n", example.s );

    return 0;
}
```

**Result:**

```text
Union Example:
The value of [example.s] = 5
The value of [example.c] = 65
The value of [example.i] = 63123
The value of [example.s] = -2413
```

Unions in C are a mechanism that allows different data types to be stored in the same memory location, which can be useful in specific situations but requires caution due to potential pitfalls associated with their use.

---

# Enums

- An enum (enumeration) is a user-defined data type in C that consists of a set of named integer constants. These constants are often used to represent a fixed set of values.
- Enum syntax is the same as struct.

**Syntax:**

```c
enums symbolic_name1
{
	<statement1>
}<symbolic_name2, ...>;
```

- Everything that is in angle brackets &lt;&gt; is optional.

---

<!-- _class: compact fit-80 -->

# 2 example

```c
#include <stdio.h>
enum color
{
    red = 51,
    green,
    blue = 91,
    orange,
};

int main(int argc, char *argv[])
{
    int array[red];

    printf("The value of red is %d\n", red);
    printf("The value of green is %d\n", green);
    printf("The value of blue is %d\n", blue);
    printf("The value of blue is %d\n", orange);
    return 0;
}
```

**Result:**

```text
The value of red is 51
The value of green is 52
The value of blue is 91
The value of orange is 92
```

When using elements from a defined enum, we don't need to use the enum's name itself. They are treated by the compiler as integer constants, which means they can be used to define array sizes just like the #define preprocessor directive.

If we don't specify a value for an enumeration field, the default value is 0. The subsequent field will have a value one greater than the previous one. However, if we define a different value for a field, that field will have an individually defined value and the next field will be one more than the last one.

---

<!-- _class: compact fit-90 -->

# 3 example

```c
#include <stdio.h>
enum color
{
    red = 51,
    green,
    blue = 91,
    orange,
}my_global_color, * my_pointer_color;

enum color my_global = orange;
int main(int argc, char *argv[])
{
    enum color my_local_color = red;
    printf("The value of my_local_color is %d\n", my_local_color);
    my_pointer_color = &my_local_color;
    *my_pointer_color = blue;
    printf("The value of my_local_color is %d\n", my_local_color);
    switch (my_global)
    {
        case red:
                printf("red\n");
                break;
        case green:
                printf("green\n");
                break;
        case blue:
                printf("blue\n");
                break;
        case orange:
                printf("orange\n");
                break;
        default:
                printf("none\n");
                break;
    }
    return 0;
}
```

**Result:**

```text
The value of my_local_color is 51
The value of my_local_color is 91
orange
```

Given that enums can also create global variables within their definition (including pointers), it's important to keep this in mind. Enums are often used with switch statements, allowing us to convert numerical values into strings.

---

# An example

```c
#include <stdio.h>
struct Data
{
    unsigned char even_number : 1;
    /* instead of using the char data type,
       if you use the int data type, it will occupy 4 bytes */
    unsigned char greater_than_10 : 1;
    unsigned char is_the_power_of_two : 1;
};
int main(int argc, char *argv[])
{
    printf("The size of Data is %d\n", sizeof(struct Data));

    struct Data my_data;
    int value;
    printf("Give me a number\n");
    _ = scanf("%d", &value);

    my_data.even_number = !(value % 2);
    my_data.greater_than_10 = ( value > 10 );
    my_data.is_the_power_of_two = value && !(value & (value - 1));

    printf("%d %d %d \n", my_data.even_number, my_data.greater_than_10, my_data.is_the_power_of_two );
    return 0;
}
```

**Result1:**

```text
The size of Data is 1
Give me a number
8
1 0 1
```

A bit-field structure occupies as much space as the largest defined field type, instead of assigning a value '=' to fields, the number of BITS for this flag ':' is specified

**Result2:**

```text
The size of Data is 1
Give me a number
12
1 1 0
```

**Result3:**

```text
The size of Data is 1
Give me a number
11
0 1 0
```

---

# File Input / Output

---

# Introduction to File Access in C

- Why File Access Matters:
  - Storing and retrieving data beyond program execution.
- Types of File Modes:
  - Text Mode:     Reads and writes data as readable characters, char-by-char, line-by-line, etc.
  - Binary Mode:     Reads and writes data as raw bytes, allowing efficient handling of complex data     structures.

---

<!-- _class: compact fit-50 -->

# Opening and closing files

```text
Function: fopen()
Syntax:
	FILE *fopen(const char *filename, const char *mode);
Error Handling:
    Always check if fopen() returned NULL, indicating failure (e.g., file not found).
Function: fclose()
Syntax:
	int fclose(*FILE);
Error Handling:
    Always check if fclose() returned NULL, indicating failure (e.g., file not found).
```

- In the context of file access, the fopen() and fclose() functions serve a role analogous to curly braces {, } in defining a code block. Opening a file with fopen() is akin to entering a new scope of operations on that file, similar to how an opening curly brace signals the beginning of a new block of statements. Conversely, fclose() marks the end of this scope, closing the file and thus concluding the block, much like a closing curly brace.
- While the compiler ensures that code blocks are properly closed, it is the programmer's responsibility to ensure files are closed correctly. An unclosed file is like an unclosed curly brace - it can lead to unexpected errors and hinder further operations.

---

# Opening files

```text
Function: fopen()
Syntax:
	FILE *fopen(const char *filename, const char *mode);
Error Handling:
Always check if fopen() returned NULL, indicating failure (e.g., file not found).
```

- file path/file name
- mode

---

<!-- _class: compact fit-60 -->

# const char \*filename

- The const char \*filename argument in the fopen() function can specify three types of file locations:
- File Name Only:
  - When only the file name is provided, fopen() attempts to open the file in the same directory as the currently executing program.
  - Example: fopen("data.txt", "rt") will try to open the file "data.txt" in the directory where the program is located.
- Relative Path:
  - A relative path specifies the location of the file relative to the current working directory.
  - Example: fopen("data/results.txt", "wt")\* will try to open the file "results.txt" in a subdirectory named "data" within the current working directory.
- Absolute Path:
  - An absolute path provides the complete path to the file, starting from the root directory of the file system.
  - Example: fopen("/home/user/documents/project/data.txt", "at") will open the file "data.txt" in the specified directory, regardless of the current working directory.
- \*Platform-specific path separators: The specific character used to separate directories in a path (e.g., / in Unix-like systems, \ \ in Windows) depends on the operating system.

---

# File Access Modes in C

**Access Modes:**

|Mode|Description|
|---|---|
|r|Opens an existing file for reading only.|
|w|Opens a file for writing. Creates a new file or clears the content of an existing one.|
|a|Opens a file for appending data. Creates the file if it does not already exist.|
|x|Creates the file if it does not already exist. Fails if the file already exists.|
|+|Combined with r, w, a, or x, allows both reading and writing.|

**File Types:**

|Type Modifier|Description|
|---|---|
|t|Text mode (default). Treats file as a sequence of characters.|
|b|Binary mode. Treats file as a sequence of bytes with no translation.|

<!-- najpierw on bibliotece i EOF i ile wynosi ( stala symboliczna i wartosc wynosi -1 -->

---

# Binary File I/O Functions

```text
For reading blocks of binary data.
    Syntax:
int fread(void *ptr, int size, int count, FILE *stream);
For writing blocks of binary data.
    Syntax:
int fwrite(const void *ptr, int size, int count, FILE *stream);
```

ptr:    Pointer to the data you want to write(read).

size:    Size, in bytes, of each element to be written(read).

count:    Number of elements to write(read), which is the third argument.

stream:    File pointer to the open file where data should be written(read).

---

# An example – Binary file

```c
#include <stdio.h>
int main(int argc, char *argv[])
{
    FILE *file;
    file =  fopen("binaryFile.bin", "wb");
    if(file)
    {
        int x = 5;
        _ =  fwrite(&x, sizeof(x), 1, file);

        char text[10] = "Some text";
        _ =  fwrite(text, sizeof(*text), 10, file);

        float fnumber = 3.14f;
        _ =  fwrite(&fnumber, sizeof(fnumber), 1, file);
        fclose(file);
    }
    else
        printf("Error");
    return 0;
}
```

**binaryFile.bin:**

```text
   Some text ĂőH@
```

**Result:**

```text
15 Some text 3.140000
```

```c
#include <stdio.h>
int main(int argc, char *argv[])
{
    FILE *file;
    file =  fopen("binaryFile.bin", "rb");
    if(file)
    {
        int x;
        _ =  fread(&x, sizeof(x), 1, file);

        char text[10];
        _ =  fread(text, sizeof(*text), 10, file);

        float fnumber;
        _ =  fread(&fnumber, sizeof(fnumber), 1, file);

        fclose(file);

        printf("%d %s %f", x, text, fnumber);
    }
    else
        printf("Error");
    return 0;
}
```

---

<!-- _class: compact fit-90 -->

# fseek() function

```text
The function fseek() moves the file pointer to a specified location, allowing you to read from or write to a specific part of the file.
Syntax:
int fseek(FILE *stream, long offset, int origin);
```

stream:     A pointer to the FILE object that identifies the file.

offset:     The number of bytes to move the file pointer.

origin:     The starting position for the offset; it can be one of the following constants:

SEEK\_SET:    Start from the beginning of the file (0).

SEEK\_CUR:     Start from the current position of the file pointer (1).

SEEK\_END:     Start from the end of the file(2).

---

<!-- _class: compact fit-90 -->

# ftell() and rewind() functions

```text
The function ftell() returns the current file position as a long integer. If an error occurs, it returns -1.
Syntax:
long ftell(FILE *stream);
```

- Unlike fseek() and ftell(), rewind() is simpler to use and is intended to reset the file pointer to the beginning of the file.
**Syntax:**

```c
void rewind(FILE *stream);
```

---

# 1 example – fseek()

```c
#include <stdio.h>
int main(int argc, char *argv[])
{
    FILE *file;
    file =  fopen("binaryFile.bin", "rb");
    if(file)
    {
        /* Move to the 5th byte from the beginning */
        fseek(file, 5, SEEK_SET);
        printf("Position after fseek: %ld\n", ftell(file));

    /* Move forward by 10 bytes from the current position */
        fseek(file, 10, SEEK_CUR);
        printf("Position after another fseek: %ld\n", ftell(file));

    /* Move to the end of the file */
        fseek(file, 0, SEEK_END);
        printf("Position at the end of file: %ld\n", ftell(file));
        fclose(file);
    }
    else
        printf("Error");
    return 0;
}
```

**Result:**

```text
Position after fseek: 5
Position after another fseek: 15
Position at the end of file: 18
```

---

# 2 example – fseek(), ftell()

```c
#include <stdio.h>
int main(int argc, char *argv[])
{
    FILE *file;
    file =  fopen("binaryFile.bin", "rb");
    if(file)
    {
        int x; int position;
        position = ftell(file);
        printf("The position in file = %d\n", position);
        _ =  fread(&x, sizeof(x), 1, file);
        position = ftell(file);
        printf("The position in file = %d\n", position);
        char text[10];
        _ =  fread(text, sizeof(*text), 10, file);
        position = ftell(file);
        printf("The position in file = %d\n", position);
        float fnumber;
        _ =  fread(&fnumber, sizeof(fnumber), 1, file);
        position = ftell(file);
        printf("The position in file = %d\n", position);
        printf("%d %s %f\n", x, text, fnumber);
        /* Move to the 0th byte from the beginning */
        fseek(file, 0, SEEK_SET);
        printf("Position after fseek(): %ld\n", ftell(file));
        x = 0;
        _ =  fread(&x, sizeof(x), 1, file);
        printf("%d\n", x);
        fclose(file);
    }
    else
        printf("Error");
    return 0;
}
```

**Result:**

```text
The position in file = 0
The position in file = 4
The position in file = 14
The position in file = 18
5 Some text 3.140000
Position after fseek(): 0
5
```

---

# Text File I/O Functions

```text
For reading text from file:
    fgetc():	Reads a single character from a file.
    fgets():	Reads a line from a file.
    fscanf(): 	Reads formatted input from a file (similar to scanf()).
For writing text for file:
    fputc():	Writes a single character to a file.
    fputs():	Writes a string to a file.
    fprintf():	Prints formatted output to a file (similar to printf()).
```

---

# Reading Text from a file

```text
int fgetc(FILE *stream)
    Description:	Reads a single character from the specified file stream.
    Return Type:	Returns the character read as an unsigned char cast to an int, or EOF on end of file or error.
    Example: 	int ch = fgetc(file_pointer);
char *fgets(char *str, int n, FILE *stream)
    Description:	Reads a line from the file and stores it in the character array str.
    Return Type:	Returns str on success, or NULL on error or when end of file occurs.
    Example:	 char *result = fgets(buffer, sizeof(buffer), file_pointer);
int fscanf(FILE *stream, const char *format, ...)
    Description:	Reads formatted input from a file based on the format string, similar to scanf.
    Return Type:	Returns the number of items successfully read, or EOF if an error or end of file occurs before any items are matched.
    Example: 	int read_count = fscanf(file_pointer, "%d %f", &int_var, &float_var);
```

---

# Writing Text to a file

```text
int fputc(int char, FILE *stream)
Description:	Writes a single character to the specified file stream.
Return Type:	Returns the written character as an unsigned char cast to an int, or EOF on error.
Example: 	int result = fputc('A', file_pointer);
int fputs(const char *str, FILE *stream)
Description:	Writes a string to the file.
Return Type:	Returns a non-negative number on success, or EOF on error.
Example: 	int result = fputs("Hello, World!\n", file_pointer);
int fprintf(FILE *stream, const char *format, ...)
Description:	Writes formatted output to the specified file stream, similar to printf().
Return Type:	Returns the number of characters written, or a negative value if an error occurs.
Example: 	int chars_written = fprintf(file_pointer, "Integer: %d, Float: %f\n", int_var, float_var);
```

---

# Lists

---

<!-- _class: compact fit-90 -->

# Introduction to Linked Lists

Let’s talk about **arrays**. Imagine we have an array designed to store a list of products that a customer wants to buy in an online store. By default, the array has a size of 20, because people usually buy only a few products.

Of course, an edge case must eventually happen — a customer tries to add the **21st product**. What should the program do if the array has only 20 elements?<br>It cannot simply “add” the 21st element after the allocated memory.

**Why not?** Because, as you know, **static memory (on the stack)** is reserved one variable after another — like:

```c
int x, y;
```

---

# Introduction to Linked Lists

These memory slots are fixed and continuous. Besides, even if we decided to use **dynamic memory allocation**, we still face a problem: to insert the 21st element, we would need to:

- Create a new array with size larger than the previous one (for example, +1),
- Copy all elements from the old array,
- Add the new element, and
- Free the old memory (if it was dynamically allocated).

Now, what if our customer wants to add yet another product? As you can see, this approach is **extremely inefficient**.

---

<!-- _class: compact fit-90 -->

# Introduction to Linked Lists

Arrays have a **fixed size**, so one common workaround is to increase the array not by 1, but by a fraction of its current size — for example, by half. However, the same problem still occurs: the larger the array becomes, the more expensive it is to:

- declare a new array,
- allocate new memory,
- and copy all existing elements.

So we can ask: *Is there another way to store data whose size changes during program execution, without copying everything from scratch each time?* Yes, there is.

---

# Introduction to Linked Lists

The answer actually appeared on this slide already — but as a word in everyday language, not yet as a data structure: we are talking about a list.

Defining a Node: Let’s imagine a data structure that has **two fields**:

This structure can store:

- an integer value (value),
- a pointer to another structure of the same type (nextPtr).

```c
typedef struct
{
    int value;
    struct Node *nextPtr;
} Node;
```

---

# Creating and Linking Nodes

Now, let’s create an independent pointer to the first element:

I prefer the naming convention headPtr rather than head, because it clearly emphasizes that headPtr does not allocate memory or create a node. It only points to an existing one — just like this analogy:

```c
typedef struct
{
    int value;
    struct Node *nextPtr;
} Node;
```

```c
Node *headPtr;
```

```c
int x = 5;
int *xPtr = &x;   // xPtr does not create a new variable; it only points to x
```

---

# Creating and Linking Nodes

Through xPtr, we can modify x itself, for example:

The same idea applies to headPtr. Let’s create our first node:

Now let’s create a second node:

We can now **connect** our elements into a list:

```c
int x = 5;
int *xPtr = &x;   // xPtr does not create a new variable; it only points to x
```

```c
*xPtr = 2;
```

```c
Node node_1;
node_1.value = 5;          // or shorter: Node node_1 = {5, NULL};
node_1.nextPtr = NULL;     // currently, our node does not point to anything
```

```c
Node node_2 = {7, NULL};
```

```c
headPtr = &node_1;       // same idea as with &x
node_1.nextPtr = &node_2;
```

```c
typedef struct
{
    int value;
    struct Node *nextPtr;
} Node;
```

---

# Traversing the List

Now we can move through the list using the pointer headPtr and read the elements just like we did with an array. For an array, we might do:

For our list, we can do:

```c
for (int i = 0; i < n; i++)
    printf("%d\n", arr[i]);
```

```c
for (Node *current = headPtr; current != NULL; current = current->nextPtr)
    printf("%d\n", current->value);
//Node *current = headPtr;  a copy of the pointer to the first element
```

---

<!-- _class: compact fit-80 -->

# What Happens in the Loop

- Let’s explain what happens here:
- We start by assigning the first element to current.
- The loop continues **as long as** current is not NULL.
- Each iteration assigns current to current-&gt;nextPtr, i.e., moves to the next element.
- The last element of the list has its nextPtr set to NULL, so when we reach it, the condition fails and the loop stops.
- We must use the **arrow operator (-&gt;)** instead of the dot (.) because we are accessing fields of a structure **through a pointer**. For example, these are equivalent:

```text
current->value
(*current).value
```

---

# Why We Use current Instead of headPtr

- *Why didn’t we use headPtr directly in the loop?*
- Because if we overwrite headPtr, we lose access to the previous elements. That’s why headPtr is usually reserved as a reference to the head of the list, used primarily for reading or accessing the start of the list.
- We use current as a temporary pointer to safely traverse the list.

---

# Stack vs Heap

- So far, we created our elements on the stack. However, later, when we learn about dynamic memory allocation using malloc() and free(), we will create lists on the heap instead of the stack so that their elements can persist even after the function that created them ends.
- The headPtr always points to the beginning of the list,<br>so we never modify it inside the loop — otherwise, we would lose the list entirely.<br>Instead, we use its copy (current) to move through the elements safely.

---

# Thank you

- Jakub Leszek Pach
- <jpach@mtech.edu>
