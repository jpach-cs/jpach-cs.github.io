---
marp: true
theme: pach
paginate: true
title: "CSCI 112  Programming with C"
---

# CSCI 112<br><br>Programming with C

- Lecture 15
- Dr. Jakub L. Pach
- Fall 2025

---

![Graphic 3](assets/image3.png)

---

## Outline

- Review
- Unions
- Enums
- Bit-fields
- File Input / Output

---

# Review

---

## Project Structure - Modular C Program with Unit Tests

- Separate logic, tests, and headers for clarity.
- Unity is a lightweight, header-based testing framework — ideal for C projects.
- This structure allows easy maintenance and clear organization.
- C project/
- │
- ├── code.c              ← function implementations
- ├── code.h              ← function declarations and globals
- │
- ├── main.c              ← main program entry point
- │
- ├── tests.c             ← unit tests implementation
- ├── tests.h             ← declaration for test runner
- │
- ├── unity.c / unity.h   ← Unity testing framework
- │
- └── Makefile            ← build automation

---

## main.c

//#define clearBuffer() while (getchar() != '\n');

\#include &lt;stdio.h&gt;

\#include &lt;stdlib.h&gt;

\#include &lt;stdbool.h&gt;

\#include &lt;string.h&gt;

\#include "tests.h"

\#include "code.h"

// ----------------- MAIN PROGRAM -----------------

int main(int argc, char \*argv\[\])

{

    int failed\_tests = 0;

    if (argc &gt; 1)

    {

        if (strcmp(argv\[1\], "--test") == 0)

            failed\_tests = run\_unity\_tests();

        else if (strcmp(argv\[1\], "--author") == 0)

            printf(AUTHOR\_NAME);

        else if (strcmp(argv\[1\], "--authorship") == 0)

            printf(AUTHOR\_AUTHORSHIP);

        else if (strcmp(argv\[1\], "--help") == 0)

            printf("\n  --test\...\n\n");

    }

    else

    {

        printf("Wrong parameter. Use --help to see available options.\n");

        return 1;

    }

    //failed\_tests = run\_unity\_tests();

    getchar(); // pause before exit (Windows)

    return failed\_tests; // cmd/powershell: echo $LASTEXITCODE

}

---

## code.h

// code.h

\#ifndef CODE\_H // include guard prevents multiple inclusion

\#define CODE\_H<br>

// comments

extern char \* AUTHOR\_NAME;

extern char \* AUTHOR\_AUTHORSHIP;<br>

// ----------------- DATA STRUCTURES -----------------

// Declaration of a simple test struct<br>

struct TestStruct

{

    int var;

};

// ----------------- GLOBAL VARIABLES -----------------

// Note: use of globals is generally discouraged but okay for small demos

int a;      // test variable 'a'

int \* p;    // pointer used in tests<br><br>

// ----------------- FUNCTION PROTOTYPES -----------------

int multiply(int x, int y);    // multiplies two integers

int addOne(int \* pointer);     // increments value pointed to by pointer<br><br><br>

\#endif

---

## code.c

char \* AUTHOR\_NAME = (char \*) "Jakub Pach";

char \* AUTHOR\_AUTHORSHIP = (char \*) "I acknowledge that I have worked on this assignment independently, except where explicitly noted and referenced. Any collaboration or use of external resources has been properly cited. I am fully aware of the consequences of academic dishonesty and agree to abide by the university's academic integrity policy. I understand the seriousness and implications of plagiarism.";

// --------- FUNCTION IMPLEMENTATIONS ------------

\#include &lt;stdio.h&gt;<br>

int addOne(int \* pointer)

{

    // check pointer validity and positive value

    if(!(\*pointer &gt;= 0))

    {

        fprintf(stderr, "Error: (\*pointer) has to be greater or equal zero!\n");

        return -1;   // special error value

    }

    (\*pointer)++;

    return \*pointer;

}<br>

int multiply(int x, int y)

{

    return x \* y;

}

---

## tests.h

// tests.h

\#ifndef TESTS\_H

\#define TESTS\_H

<br>

// prototype for running all Unity tests

int run\_unity\_tests(void);

<br>

\#endif // TESTS\_H

<br>

---

## tests.c

//#include &lt;assert.h&gt;   // commented out, not needed

\#include "code.h"

\#include "tests.h"

\#include "unity.h"

int result; // global variable for test results

// ----------------- UNITY SETUP / TEARDOWN -----------------

void setUp()

{

    a = 4;

    p = (int\*) malloc(sizeof(int));

    \*p = 5;

    result = 0;

}

void tearDown()

{

    free(p);

    result = 0;

}

// ----------------- TEST FUNCTIONS -----------------

void test\_multiply\_basic()

{

    result = multiply(a, \*p);

    TEST\_ASSERT\_EQUAL(20, result);

}

void test\_multiply\_with\_zero()

{

    \*p = 0;

    result = multiply(a, \*p);

    TEST\_ASSERT\_EQUAL(0, result);

}

void test\_multiply\_negative()

{

    \*p = -3;

    result = multiply(a, \*p);

    TEST\_ASSERT\_EQUAL(-12, result);

}

void test\_addOne\_basic()

{

    result = addOne(p);

    TEST\_ASSERT\_EQUAL(6, result);

}

void test\_addOne\_negative()

{

    \*p = -3;

    result = addOne(p);

    TEST\_ASSERT\_EQUAL(-1, result); // tests proper error handling

}

// ----------------- RUN ALL TESTS -----------------

int run\_unity\_tests(void)

{

    UNITY\_BEGIN();

    RUN\_TEST(test\_multiply\_basic);

    RUN\_TEST(test\_multiply\_with\_zero);

    RUN\_TEST(test\_multiply\_negative);

    RUN\_TEST(test\_addOne\_basic);

    RUN\_TEST(test\_addOne\_negative);

    return UNITY\_END();

}

<br>

---

## code.c and code.h – Functional Module

- code.h declares the interface.
- code.c contains the implementation.

int multiply(int x, int y);    // multiplies two integers

int addOne(int \* pointer);     // increments value pointed to by pointer

int addOne(int \* pointer)

{

    // check pointer validity and positive value

    if(!(\*pointer &gt;= 0))

    {

        fprintf(stderr, "Error: (\*pointer) has to be greater or equal zero!\n");

        return -1;   // special error value

    }

    (\*pointer)++;

    return \*pointer;

}

int multiply(int x, int y)

{

    return x \* y;

}

- addOne() checks input validity → demonstrates defensive programming.Simple, testable logic → perfect for unit testing.
- The Logic Module

---

## main.c – Program Entry Point

- The program supports several command-line arguments.
- --test runs all unit tests.
- The same executable can run in:
  - normal mode (program logic)
  - test mode (verification)
- Demonstrates separation of logic and testing.

int main(int argc, char \*argv\[\])

{

    int failed\_tests = 0;

    if (argc &gt; 1)

    {

        if (strcmp(argv\[1\], "--test") == 0)

            failed\_tests = run\_unity\_tests();

        else if (strcmp(argv\[1\], "--author") == 0)

            printf(AUTHOR\_NAME);

        else if (strcmp(argv\[1\], "--authorship") == 0)

            printf(AUTHOR\_AUTHORSHIP);

        else if (strcmp(argv\[1\], "--help") == 0)

            printf("\n  --test\...\n\n");

    }

    else

    {

        printf("Wrong parameter. Use --help to see available options.\n");

        return 1;

    }

    //failed\_tests = run\_unity\_tests();

    getchar(); // pause before exit (Windows)

    return failed\_tests; // cmd/powershell: echo $LASTEXITCODE

}

- The Main Program and Command Interface

---

## Unit Testing with Unity - Writing Tests with Assertions

- Each test\_\* function verifies one behavior.
- TEST\_ASSERT\_EQUAL(expected, actual) checks correctness.
- Assertion = a condition that must be true for the test to pass.
- Failures are automatically reported by Unity.

void test\_multiply\_basic()

{

    result = multiply(a, \*p);

    TEST\_ASSERT\_EQUAL(20, result);

}

void test\_multiply\_with\_zero()

{

    \*p = 0;

    result = multiply(a, \*p);

    TEST\_ASSERT\_EQUAL(0, result);

}

void test\_multiply\_negative()

{

    \*p = -3;

    result = multiply(a, \*p);

    TEST\_ASSERT\_EQUAL(-12, result);

}

---

## Unit Testing with Unity - Setup and Teardown Functions

- setUp() runs before each test → initializes variables.
- tearDown() runs after each test → cleans up memory.
- Ensures tests run independently and do not affect each other.
- Mimics a controlled test environment.
- Preparing and Cleaning the Test Environment

void setUp()

{

    a = 4;

    p = (int\*) malloc(sizeof(int));

    \*p = 5;

    result = 0;

}

void tearDown()

{

    free(p);

    result = 0;

}

---

## Unit Testing with Unity - Running and Reporting Tests

- Each test is executed via RUN\_TEST().
- Unity reports all results in a readable format.
- Helps trace logical errors quickly and accurately.

void test\_addOne\_basic()

{

    result = addOne(p);

    TEST\_ASSERT\_EQUAL(6, result);

}

void test\_addOne\_negative()

{

    \*p = -3;

    result = addOne(p);

    TEST\_ASSERT\_EQUAL(-1, result); // tests proper error handling

}

// ----------------- RUN ALL TESTS -----------------

int run\_unity\_tests(void)

{

    UNITY\_BEGIN();

    RUN\_TEST(test\_multiply\_basic);

    RUN\_TEST(test\_multiply\_with\_zero);

    RUN\_TEST(test\_multiply\_negative);

    RUN\_TEST(test\_addOne\_basic);

    RUN\_TEST(test\_addOne\_negative);

    return UNITY\_END();

}

<br>

- tests.c:53:test\_multiply\_basic:PASS
- tests.c:54:test\_multiply\_with\_zero:PASS
- tests.c:55:test\_multiply\_negative:PASS
- tests.c:56:test\_addOne\_basic:PASS
- Error: (\*pointer) has to be greater or equal zero!
- tests.c:57:test\_addOne\_negative:PASS
- \-----------------------
- 5 Tests 0 Failures 0 Ignored
- OK
- Result:

---

## Summary and Best Practices

- Why do all these test functions have no parameters and return void? Because their **function signature** must match what Unity expects — the function’s address is passed to the macro: RUN\_TEST(test\_multiply\_basic); inside the run\_unity\_tests() function.
- If all tests run successfully, UNITY\_END() returns the number of **failed tests**.<br>This allows us to conveniently pass that information to the operating system using: return UNITY\_END(); in main.c, since main.c contains:

failed\_tests = run\_unity\_tests();

return failed\_tests;

---

# Unions

---

## An example - unions

- \#include &lt;stdio.h&gt;
- struct Example1
- {
-     char c;
-     int i;
-     short s;
- };
- union Example2
- {
-     short s;
-     char c;
-     int i;
- };<br>int main(int argc, char \*argv\[\])
- {
-     printf( "Size of a struct Example is = %d\n", sizeof(struct Example1) );
-     printf( "Size of a struct Example is = %d\n", sizeof(union Example2) );<br>    struct Example1 example1;
-     printf( "Struct Example1:\n" );
-     printf( "Address of variable c = %d\n", &amp;example1.c );
-     printf( "Address of variable i = %d\n", &amp;example1.i );
-     printf( "Address of variable s = %d\n", &amp;example1.s );
-     union Example2 example2;
-     printf( "Union Example2:\n" );
-     printf( "Address of variable s = %d\n", &amp;example2.s );
-     printf( "Address of variable c = %d\n", &amp;example2.c );
-     printf( "Address of variable i = %d\n", &amp;example2.i );
-     return 0;
- }
- Size of a struct Example is = 12
- Size of a struct Example is = 4
- Struct Example1:
- Address of variable c = 6487828
- Address of variable i = 6487832
- Address of variable s = 6487836
- Union Example2:
- Address of variable s = 6487824
- Address of variable c = 6487824
- Address of variable i = 6487824
- Result:

---

## Unions

- Unions in C are special data types that allow different data types to be stored in the same memory location.
- unions symbolic\_name1
- {
- &lt;statement1&gt;
- }&lt;symbolic\_name2, ...&gt;;
- Syntax:
- Everything that is in angle brackets &lt;&gt; is optional.

---

## An example - unions

- \#include &lt;stdio.h&gt;
- union Example
- {
-     short s;
-     char c;
-     int i;
- };
- <br>int main(int argc, char \*argv\[\])
- {
-     union Example example;
-     printf( "Union Example:\n" );
-     example.s = 5;
-     printf( "The value of \[example.s\] = %d\n", example.s );
-     example.c = 'A';
-     printf( "The value of \[example.c\] = %d\n", example.c );
-     example.i = 63123;
-     printf( "The value of \[example.i\] = %d\n", example.i );
-     /\*but...\*/
-     printf( "The value of \[example.s\] = %d\n", example.s );<br>
-     return 0;
- }
- Union Example:
- The value of \[example.s\] = 5
- The value of \[example.c\] = 65
- The value of \[example.i\] = 63123
- The value of \[example.s\] = -2413
- Result:

Unions in C are a mechanism that allows different data types to be stored in the same memory location, which can be useful in specific situations but requires caution due to potential pitfalls associated with their use.

---

## A summary on unions

Unions in C are special data types that allow different data types to be stored in the same memory location. Unlike structures, where each member has its own dedicated space, all members of a union share the same location. This means that at any given time, only one member of the union can hold a defined value, and changing the value of one member automatically overwrites the values of the others. This makes unions ideal for situations where we need to store different types of data in the same place, but only one of these types is active at any moment. Unions have various applications, from representing variable data types to creating more memory-efficient data structures. However, it’s important to note that improper use of unions can lead to programming errors, such as accessing uninitialized data or violating memory alignment rules

---

# Enums

---

## Enums

- An enum (enumeration) is a user-defined data type in C that consists of a set of named integer constants. These constants are often used to represent a fixed set of values.
- Enum syntax is the same as struct.
- enums symbolic\_name1
- {
- &lt;statement1&gt;
- }&lt;symbolic\_name2, ...&gt;;
- Syntax:
- Everything that is in angle brackets &lt;&gt; is optional.

---

## 1 example

- \#include &lt;stdio.h&gt;
- enum color
- {
-     red,
-     green,
-     blue,
- };
- int main(int argc, char \*argv\[\])
- {
-     printf("The size of \[enum color\] is %d\n", sizeof(enum color)); /\*default as sizeof(int)\*/
- <br>    enum color my\_color = red;
-     printf("The value of my\_color is %d\n", my\_color);
-     int x = green;
-     printf("The value of x is %d\n", x);
- <br>    my\_color = 99;  /\* be careful \*/
-     printf("The value of my\_color is %d\n", my\_color);
- <br>    if(my\_color == red || my\_color == green || my\_color == blue )
-         printf("Proper value\n");
-     else
-         printf("Improper value\n");
-     return 0;
- }
- The size of \[enum color\] is 4
- The value of my\_color is 0
- The value of x is 1
- The value of my\_color is 99
- Improper value
- Result:

These constants are often used to represent a fixed set of values, such as days of the week, colors, or error codes. Enums provide a way to make code more readable and maintainable by using meaningful names instead of raw integer values.

---

## 2 example

- \#include &lt;stdio.h&gt;
- enum color
- {
-     red = 51,
-     green,
-     blue = 91,
-     orange,
- };
- int main(int argc, char \*argv\[\])
- {
-     int array\[red\];
- <br>    printf("The value of red is %d\n", red);
-     printf("The value of green is %d\n", green);
-     printf("The value of blue is %d\n", blue);
-     printf("The value of blue is %d\n", orange);
-     return 0;
- }
- The value of red is 51
- The value of green is 52
- The value of blue is 91
- The value of orange is 92
- Result:

When using elements from a defined enum, we don't need to use the enum's name itself. They are treated by the compiler as integer constants, which means they can be used to define array sizes just like the #define preprocessor directive.

If we don't specify a value for an enumeration field, the default value is 0. The subsequent field will have a value one greater than the previous one. However, if we define a different value for a field, that field will have an individually defined value and the next field will be one more than the last one.

---

## Enums

- An enum (enumeration) is a user-defined data type in C that consists of a set of named integer constants. These constants are often used to represent a fixed set of values.
- Enum syntax is the same as struct.
- enums symbolic\_name1
- {
- &lt;statement1&gt;
- }&lt;symbolic\_name2, ...&gt;;
- Syntax:
- Everything that is in angle brackets &lt;&gt; is optional.

---

## 3 example

- \#include &lt;stdio.h&gt;
- enum color
- {
-     red = 51,
-     green,
-     blue = 91,
-     orange,
- }my\_global\_color, \* my\_pointer\_color;
- <br>enum color my\_global = orange;
- int main(int argc, char \*argv\[\])
- {
-     enum color my\_local\_color = red;
-     printf("The value of my\_local\_color is %d\n", my\_local\_color);
-     my\_pointer\_color = &amp;my\_local\_color;
-     \*my\_pointer\_color = blue;
-     printf("The value of my\_local\_color is %d\n", my\_local\_color);<br>    switch (my\_global)
-     {
-         case red:
-                 printf("red\n");
-                 break;
-         case green:
-                 printf("green\n");
-                 break;
-         case blue:
-                 printf("blue\n");
-                 break;
-         case orange:
-                 printf("orange\n");
-                 break;
-         default:
-                 printf("none\n");
-                 break;
-     }
-     return 0;
- }
- The value of my\_local\_color is 51
- The value of my\_local\_color is 91
- orange
- Result:

Given that enums can also create global variables within their definition (including pointers), it's important to keep this in mind. Enums are often used with switch statements, allowing us to convert numerical values into strings.

---

# Bit-fields

---

## An example

- \#include &lt;stdio.h&gt;
- struct Data
- {
-     unsigned char even\_number : 1;
-     /\* instead of using the char data type,
-        if you use the int data type, it will occupy 4 bytes \*/
-     unsigned char greater\_than\_10 : 1;
-     unsigned char is\_the\_power\_of\_two : 1;
- };
- int main(int argc, char \*argv\[\])
- {
-     printf("The size of Data is %d\n", sizeof(struct Data));
-     struct Data my\_data;
-     int value;
-     printf("Give me a number\n");
-     \_ = scanf("%d", &amp;value);
- <br>    my\_data.even\_number = !(value % 2);
-     my\_data.greater\_than\_10 = ( value &gt; 10 );
-     my\_data.is\_the\_power\_of\_two = value &amp;&amp; !(value &amp; (value - 1));
- <br>    printf("%d %d %d \n", my\_data.even\_number, my\_data.greater\_than\_10, my\_data.is\_the\_power\_of\_two );
-     return 0;
- }
- The size of Data is 1
- Give me a number
- 8
- 1 0 1
- Result1:

A bit-field structure occupies as much space as the largest defined field type, instead of assigning a value '=' to fields, the number of BITS for this flag ':' is specified

- The size of Data is 1
- Give me a number
- 12
- 1 1 0
- Result2:
- The size of Data is 1
- Give me a number
- 11
- 0 1 0
- Result3:

---

# File Input / Output

---

## Introduction to File Access in C

- Why File Access Matters:
  - Storing and retrieving data beyond program execution.
- Types of File Modes:
  - Text Mode:     Reads and writes data as readable characters, char-by-char, line-by-line, etc.
  - Binary Mode:     Reads and writes data as raw bytes, allowing efficient handling of complex data     structures.

---

## Opening and closing files

- Function: fopen()
- Syntax:

FILE \*fopen(const char \*filename, const char \*mode);

- Error Handling:
  - Always check if fopen() returned NULL, indicating failure (e.g., file not found).
- Function: fclose()
- Syntax:

int fclose(\*FILE);

- Error Handling:
  - Always check if fclose() returned NULL, indicating failure (e.g., file not found).
- In the context of file access, the fopen() and fclose() functions serve a role analogous to curly braces {, } in defining a code block. Opening a file with fopen() is akin to entering a new scope of operations on that file, similar to how an opening curly brace signals the beginning of a new block of statements. Conversely, fclose() marks the end of this scope, closing the file and thus concluding the block, much like a closing curly brace.
- While the compiler ensures that code blocks are properly closed, it is the programmer's responsibility to ensure files are closed correctly. An unclosed file is like an unclosed curly brace - it can lead to unexpected errors and hinder further operations.

---

## Opening files

- Function: fopen()
- Syntax:

FILE \*fopen(const char \*filename, const char \*mode);

- Error Handling:
  - Always check if fopen() returned NULL, indicating failure (e.g., file not found).
- file path/file name
- mode

---

## const char \*filename

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

## File Access Modes in C

|Mode|Description|
|---|---|
|r|Opens an existing file for reading only.|
|w|Opens a file for writing. Creates a new file or clears the content of an existing one.|
|a|Opens a file for appending data. Creates the file if it does not already exist.|
|x|Creates the file if it does not already exist. Fails if the file already exists.|
|+|Combined with r, w, a, or x, allows both reading and writing.|

|Type Modifier|Description|
|---|---|
|t|Text mode (default). Treats file as a sequence of characters.|
|b|Binary mode. Treats file as a sequence of bytes with no translation.|

- Access Modes:
- File Types:

<!-- najpierw on bibliotece i EOF i ile wynosi ( stala symboliczna i wartosc wynosi -1 -->

---

## Binary File I/O Functions

- For reading blocks of binary data.
  - Syntax:

int fread(void \*ptr, int size, int count, FILE \*stream);

- For writing blocks of binary data.
  - Syntax:

int fwrite(const void \*ptr, int size, int count, FILE \*stream);

ptr:    Pointer to the data you want to write(read).

size:    Size, in bytes, of each element to be written(read).

count:    Number of elements to write(read), which is the third argument.

stream:    File pointer to the open file where data should be written(read).

---

## An example – Binary file

- \#include &lt;stdio.h&gt;
- int main(int argc, char \*argv\[\])
- {
-     FILE \*file;
-     file =  fopen("binaryFile.bin", "wb");
-     if(file)
-     {
-         int x = 5;
-         \_ =  fwrite(&amp;x, sizeof(x), 1, file);
- <br>        char text\[10\] = "Some text";
-         \_ =  fwrite(text, sizeof(\*text), 10, file);
- <br>        float fnumber = 3.14f;
-         \_ =  fwrite(&amp;fnumber, sizeof(fnumber), 1, file);
-         fclose(file);
-     }
-     else
-         printf("Error");
-     return 0;
- }
- Some text ĂőH@
- binaryFile.bin:
- 15 Some text 3.140000
- Result:
- \#include &lt;stdio.h&gt;
- int main(int argc, char \*argv\[\])
- {
-     FILE \*file;
-     file =  fopen("binaryFile.bin", "rb");
-     if(file)
-     {
-         int x;
-         \_ =  fread(&amp;x, sizeof(x), 1, file);
-         char text\[10\];
-         \_ =  fread(text, sizeof(\*text), 10, file);
- <br>        float fnumber;
-         \_ =  fread(&amp;fnumber, sizeof(fnumber), 1, file);
- <br>        fclose(file);
- <br>        printf("%d %s %f", x, text, fnumber);
-     }
-     else
-         printf("Error");
-     return 0;
- }

---

## fseek() function

- The function fseek() moves the file pointer to a specified location, allowing you to read from or write to a specific part of the file.
- Syntax:

int fseek(FILE \*stream, long offset, int origin);

stream:     A pointer to the FILE object that identifies the file.

offset:     The number of bytes to move the file pointer.

origin:     The starting position for the offset; it can be one of the following constants:

SEEK\_SET:    Start from the beginning of the file (0).

SEEK\_CUR:     Start from the current position of the file pointer (1).

SEEK\_END:     Start from the end of the file(2).

---

## ftell() and rewind() functions

- The function ftell() returns the current file position as a long integer. If an error occurs, it returns -1.
- Syntax:

long ftell(FILE \*stream);

- Unlike fseek() and ftell(), rewind() is simpler to use and is intended to reset the file pointer to the beginning of the file.
- Syntax:

void rewind(FILE \*stream);

---

## 1 example – fseek()

- \#include &lt;stdio.h&gt;
- int main(int argc, char \*argv\[\])
- {
-     FILE \*file;
-     file =  fopen("binaryFile.bin", "rb");
-     if(file)
-     {
  -     /\* Move to the 5th byte from the beginning \*/
  -     fseek(file, 5, SEEK\_SET);
  -     printf("Position after fseek: %ld\n", ftell(file));
  - <br>    /\* Move forward by 10 bytes from the current position \*/
  -     fseek(file, 10, SEEK\_CUR);
  -     printf("Position after another fseek: %ld\n", ftell(file));
  - <br>    /\* Move to the end of the file \*/
  -     fseek(file, 0, SEEK\_END);
  -     printf("Position at the end of file: %ld\n", ftell(file));
  -     fclose(file);
-     }
-     else
-         printf("Error");
-     return 0;
- }
- Position after fseek: 5
- Position after another fseek: 15
- Position at the end of file: 18
- Result:

---

## 2 example – fseek(), ftell()

- \#include &lt;stdio.h&gt;
- int main(int argc, char \*argv\[\])
- {
-     FILE \*file;
-     file =  fopen("binaryFile.bin", "rb");
-     if(file)
-     {
-         int x; int position;<br>        position = ftell(file);
-         printf("The position in file = %d\n", position);<br>        \_ =  fread(&amp;x, sizeof(x), 1, file);
-         position = ftell(file);
-         printf("The position in file = %d\n", position);<br>        char text\[10\];
-         \_ =  fread(text, sizeof(\*text), 10, file);
-         position = ftell(file);
-         printf("The position in file = %d\n", position);
-         float fnumber;
-         \_ =  fread(&amp;fnumber, sizeof(fnumber), 1, file);
-         position = ftell(file);
-         printf("The position in file = %d\n", position);
-         printf("%d %s %f\n", x, text, fnumber);<br>        /\* Move to the 0th byte from the beginning \*/
-         fseek(file, 0, SEEK\_SET);
-         printf("Position after fseek(): %ld\n", ftell(file));<br>        x = 0;
-         \_ =  fread(&amp;x, sizeof(x), 1, file);<br>        printf("%d\n", x);
-         fclose(file);
-     }
-     else
-         printf("Error");
-     return 0;
- }
- The position in file = 0
- The position in file = 4
- The position in file = 14
- The position in file = 18
- 5 Some text 3.140000
- Position after fseek(): 0
- 5
- Result:

---

## Text File I/O Functions

- For reading text from file:
  - fgetc():    Reads a single character from a file.
  - fgets():    Reads a line from a file.
  - fscanf():     Reads formatted input from a file (similar to scanf()).
- For writing text for file:
  - fputc():    Writes a single character to a file.
  - fputs():    Writes a string to a file.
  - fprintf():    Prints formatted output to a file (similar to printf()).

---

## Reading Text from a file

- **int fgetc(FILE \*stream)**
  - **Description**:    Reads a single character from the specified file stream.
  - **Return Type**:    Returns the character read as an unsigned char cast to an int, or EOF on end of file or error.
  - **Example**:     int ch = fgetc(file\_pointer);
- **char \*fgets(char \*str, int n, FILE \*stream)**
  - **Description**:    Reads a line from the file and stores it in the character array str.
  - **Return Type**:    Returns str on success, or NULL on error or when end of file occurs.
  - **Example**:     char \*result = fgets(buffer, sizeof(buffer), file\_pointer);
- **int fscanf(FILE \*stream, const char \*format, ...)**
  - **Description**:    Reads formatted input from a file based on the format string, similar to scanf.
  - **Return Type**:    Returns the number of items successfully read, or EOF if an error or end of file occurs before any items are matched.
  - **Example**:     int read\_count = fscanf(file\_pointer, "%d %f", &amp;int\_var, &amp;float\_var);

---

## Writing Text to a file

- **int fputc(int char, FILE \*stream)**
  - **Description**:    Writes a single character to the specified file stream.
  - **Return Type**:    Returns the written character as an unsigned char cast to an int, or EOF on error.
  - **Example**:     int result = fputc('A', file\_pointer);
- **int fputs(const char \*str, FILE \*stream)**
  - **Description**:    Writes a string to the file.
  - **Return Type**:    Returns a non-negative number on success, or EOF on error.
  - **Example**:     int result = fputs("Hello, World!\n", file\_pointer);
- **int fprintf(FILE \*stream, const char \*format, ...)**
  - **Description**:    Writes formatted output to the specified file stream, similar to printf().
  - **Return Type**:    Returns the number of characters written, or a negative value if an error occurs.
  - **Example**:     int chars\_written = fprintf(file\_pointer, "Integer: %d, Float: %f\n", int\_var, float\_var);

---

# Thank you

- Jakub Leszek Pach
- <jpach@mtech.edu>
