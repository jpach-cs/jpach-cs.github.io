---
marp: true
theme: pach
paginate: true
footer: "CSCI 112 | Programming with C | J. L. Pach"
title: "CSCI 112  Programming with C"
---

<!-- _class: lead -->

# CSCI 112<br><br>Programming with C

- Lecture 15
- Dr. Jakub L. Pach
- Fall 2025

---

# Outline

- Review
- Unions
- Enums
- Bit-fields
- File Input / Output

---

# Review

---

# Project Structure - Modular C Program with Unit Tests

- Separate logic, tests, and headers for clarity.
- Unity is a lightweight, header-based testing framework — ideal for C projects.
- This structure allows easy maintenance and clear organization.

```text
C project/
│
├── code.c              ← function implementations
├── code.h              ← function declarations and globals
│
├── main.c              ← main program entry point
│
├── tests.c             ← unit tests implementation
├── tests.h             ← declaration for test runner
│
├── unity.c / unity.h   ← Unity testing framework
│
└── Makefile            ← build automation
```

---

# main.c

```c
//#define clearBuffer() while (getchar() != '\n');
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include "tests.h"
#include "code.h"
// ----------------- MAIN PROGRAM -----------------
int main(int argc, char *argv[])
{
    int failed_tests = 0;
    if (argc > 1)
    {
        if (strcmp(argv[1], "--test") == 0)
            failed_tests = run_unity_tests();
        else if (strcmp(argv[1], "--author") == 0)
            printf(AUTHOR_NAME);
        else if (strcmp(argv[1], "--authorship") == 0)
            printf(AUTHOR_AUTHORSHIP);
        else if (strcmp(argv[1], "--help") == 0)
            printf("\n  --test\...\n\n");
    }
    else
    {
        printf("Wrong parameter. Use --help to see available options.\n");
        return 1;
    }
    //failed_tests = run_unity_tests();
    getchar(); // pause before exit (Windows)
    return failed_tests; // cmd/powershell: echo $LASTEXITCODE
}
```

---

# code.h

```c
// code.h
#ifndef CODE_H // include guard prevents multiple inclusion
#define CODE_H

// comments
extern char * AUTHOR_NAME;
extern char * AUTHOR_AUTHORSHIP;

// ----------------- DATA STRUCTURES -----------------
// Declaration of a simple test struct

struct TestStruct
{
    int var;
};
// ----------------- GLOBAL VARIABLES -----------------
// Note: use of globals is generally discouraged but okay for small demos
int a;      // test variable 'a'
int * p;    // pointer used in tests


// ----------------- FUNCTION PROTOTYPES -----------------
int multiply(int x, int y);    // multiplies two integers
int addOne(int * pointer);     // increments value pointed to by pointer



#endif


```

---

# code.c

```c
char * AUTHOR_NAME = (char *) "Jakub Pach";
char * AUTHOR_AUTHORSHIP = (char *) "I acknowledge that I have worked on this assignment independently, except where explicitly noted and referenced. Any collaboration or use of external resources has been properly cited. I am fully aware of the consequences of academic dishonesty and agree to abide by the university's academic integrity policy. I understand the seriousness and implications of plagiarism.";

// --------- FUNCTION IMPLEMENTATIONS ------------
#include <stdio.h>

int addOne(int * pointer)
{
    // check pointer validity and positive value
    if(!(*pointer >= 0))
    {
        fprintf(stderr, "Error: (*pointer) has to be greater or equal zero!\n");
        return -1;   // special error value
    }
    (*pointer)++;
    return *pointer;
}

int multiply(int x, int y)
{
    return x * y;
}
```

---

# tests.h

```c
// tests.h
#ifndef TESTS_H
#define TESTS_H


// prototype for running all Unity tests
int run_unity_tests(void);


#endif // TESTS_H


```

---

# tests.c

```c
//#include <assert.h>   // commented out, not needed
#include "code.h"
#include "tests.h"
#include "unity.h"
int result; // global variable for test results
// ----------------- UNITY SETUP / TEARDOWN -----------------
void setUp()
{
    a = 4;
    p = (int*) malloc(sizeof(int));
    *p = 5;
    result = 0;
}
void tearDown()
{
    free(p);
    result = 0;
}
// ----------------- TEST FUNCTIONS -----------------
void test_multiply_basic()
{
    result = multiply(a, *p);
    TEST_ASSERT_EQUAL(20, result);
}
void test_multiply_with_zero()
{
    *p = 0;
    result = multiply(a, *p);
    TEST_ASSERT_EQUAL(0, result);
}
void test_multiply_negative()
{
    *p = -3;
    result = multiply(a, *p);
    TEST_ASSERT_EQUAL(-12, result);
}
```

```c
void test_addOne_basic()
{
    result = addOne(p);
    TEST_ASSERT_EQUAL(6, result);
}
void test_addOne_negative()
{
    *p = -3;
    result = addOne(p);
    TEST_ASSERT_EQUAL(-1, result); // tests proper error handling
}
// ----------------- RUN ALL TESTS -----------------
int run_unity_tests(void)
{
    UNITY_BEGIN();
    RUN_TEST(test_multiply_basic);
    RUN_TEST(test_multiply_with_zero);
    RUN_TEST(test_multiply_negative);
    RUN_TEST(test_addOne_basic);
    RUN_TEST(test_addOne_negative);
    return UNITY_END();
}


```

---

# code.c and code.h – Functional Module

- code.h declares the interface.
- code.c contains the implementation.

```c
int multiply(int x, int y);    // multiplies two integers
int addOne(int * pointer);     // increments value pointed to by pointer
```

```c
int addOne(int * pointer)
{
    // check pointer validity and positive value
    if(!(*pointer >= 0))
    {
        fprintf(stderr, "Error: (*pointer) has to be greater or equal zero!\n");
        return -1;   // special error value
    }
    (*pointer)++;
    return *pointer;
}
int multiply(int x, int y)
{
    return x * y;
}
```

- addOne() checks input validity → demonstrates defensive programming.Simple, testable logic → perfect for unit testing.
- The Logic Module

---

# main.c – Program Entry Point

- The program supports several command-line arguments.
- --test runs all unit tests.
- The same executable can run in:
  - normal mode (program logic)
  - test mode (verification)
- Demonstrates separation of logic and testing.

```c
int main(int argc, char *argv[])
{
    int failed_tests = 0;
    if (argc > 1)
    {
        if (strcmp(argv[1], "--test") == 0)
            failed_tests = run_unity_tests();
        else if (strcmp(argv[1], "--author") == 0)
            printf(AUTHOR_NAME);
        else if (strcmp(argv[1], "--authorship") == 0)
            printf(AUTHOR_AUTHORSHIP);
        else if (strcmp(argv[1], "--help") == 0)
            printf("\n  --test\...\n\n");
    }
    else
    {
        printf("Wrong parameter. Use --help to see available options.\n");
        return 1;
    }
    //failed_tests = run_unity_tests();
    getchar(); // pause before exit (Windows)
    return failed_tests; // cmd/powershell: echo $LASTEXITCODE
}
```

- The Main Program and Command Interface

---

# Unit Testing with Unity - Writing Tests with Assertions

- Each test\_\* function verifies one behavior.
- TEST\_ASSERT\_EQUAL(expected, actual) checks correctness.
- Assertion = a condition that must be true for the test to pass.
- Failures are automatically reported by Unity.

```c
void test_multiply_basic()
{
    result = multiply(a, *p);
    TEST_ASSERT_EQUAL(20, result);
}
void test_multiply_with_zero()
{
    *p = 0;
    result = multiply(a, *p);
    TEST_ASSERT_EQUAL(0, result);
}
void test_multiply_negative()
{
    *p = -3;
    result = multiply(a, *p);
    TEST_ASSERT_EQUAL(-12, result);
}
```

---

# Unit Testing with Unity - Setup and Teardown Functions

- setUp() runs before each test → initializes variables.
- tearDown() runs after each test → cleans up memory.
- Ensures tests run independently and do not affect each other.
- Mimics a controlled test environment.
- Preparing and Cleaning the Test Environment

```c
void setUp()
{
    a = 4;
    p = (int*) malloc(sizeof(int));
    *p = 5;
    result = 0;
}
void tearDown()
{
    free(p);
    result = 0;
}
```

---

# Unit Testing with Unity - Running and Reporting Tests

- Each test is executed via RUN\_TEST().
- Unity reports all results in a readable format.
- Helps trace logical errors quickly and accurately.

```c
void test_addOne_basic()
{
    result = addOne(p);
    TEST_ASSERT_EQUAL(6, result);
}
void test_addOne_negative()
{
    *p = -3;
    result = addOne(p);
    TEST_ASSERT_EQUAL(-1, result); // tests proper error handling
}
// ----------------- RUN ALL TESTS -----------------
int run_unity_tests(void)
{
    UNITY_BEGIN();
    RUN_TEST(test_multiply_basic);
    RUN_TEST(test_multiply_with_zero);
    RUN_TEST(test_multiply_negative);
    RUN_TEST(test_addOne_basic);
    RUN_TEST(test_addOne_negative);
    return UNITY_END();
}


```

Result:

```text
tests.c:53:test_multiply_basic:PASS
tests.c:54:test_multiply_with_zero:PASS
tests.c:55:test_multiply_negative:PASS
tests.c:56:test_addOne_basic:PASS
Error: (*pointer) has to be greater or equal zero!
tests.c:57:test_addOne_negative:PASS

-----------------------
5 Tests 0 Failures 0 Ignored
OK
```

---

<!-- _class: fit-90 -->

# Summary and Best Practices

- Why do all these test functions have no parameters and return void? Because their **function signature** must match what Unity expects — the function’s address is passed to the macro: RUN\_TEST(test\_multiply\_basic); inside the run\_unity\_tests() function.
- If all tests run successfully, UNITY\_END() returns the number of **failed tests**.<br>This allows us to conveniently pass that information to the operating system using: return UNITY\_END(); in main.c, since main.c contains:

```c
failed_tests = run_unity_tests();
return failed_tests;
```

---

# Unions

---

# An example - unions

```c
#include <stdio.h>
struct Example1
{
    char c;
    int i;
    short s;
};
union Example2
{
    short s;
    char c;
    int i;
};
int main(int argc, char *argv[])
{
    printf( "Size of a struct Example is = %d\n", sizeof(struct Example1) );
    printf( "Size of a struct Example is = %d\n", sizeof(union Example2) );
    struct Example1 example1;
    printf( "Struct Example1:\n" );
    printf( "Address of variable c = %d\n", &example1.c );
    printf( "Address of variable i = %d\n", &example1.i );
    printf( "Address of variable s = %d\n", &example1.s );
    union Example2 example2;
    printf( "Union Example2:\n" );
    printf( "Address of variable s = %d\n", &example2.s );
    printf( "Address of variable c = %d\n", &example2.c );
    printf( "Address of variable i = %d\n", &example2.i );
    return 0;
}
```

Result:

```text
Size of a struct Example is = 12
Size of a struct Example is = 4
Struct Example1:
Address of variable c = 6487828
Address of variable i = 6487832
Address of variable s = 6487836
Union Example2:
Address of variable s = 6487824
Address of variable c = 6487824
Address of variable i = 6487824
```

---

# Unions

- Unions in C are special data types that allow different data types to be stored in the same memory location.

Syntax:

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

Result:

```text
Union Example:
The value of [example.s] = 5
The value of [example.c] = 65
The value of [example.i] = 63123
The value of [example.s] = -2413
```

Unions in C are a mechanism that allows different data types to be stored in the same memory location, which can be useful in specific situations but requires caution due to potential pitfalls associated with their use.

---

<!-- _class: fit-90 -->

# A summary on unions:

Unions in C are special data types that allow different data types to be stored in the same memory location. Unlike structures, where each member has its own dedicated space, all members of a union share the same location. This means that at any given time, only one member of the union can hold a defined value, and changing the value of one member automatically overwrites the values of the others. This makes unions ideal for situations where we need to store different types of data in the same place, but only one of these types is active at any moment. Unions have various applications, from representing variable data types to creating more memory-efficient data structures. However, it’s important to note that improper use of unions can lead to programming errors, such as accessing uninitialized data or violating memory alignment rules

---

# Enums

---

# Enums

- An enum (enumeration) is a user-defined data type in C that consists of a set of named integer constants. These constants are often used to represent a fixed set of values.
- Enum syntax is the same as struct.

Syntax:

```c
enums symbolic_name1
{
	<statement1>
}<symbolic_name2, ...>;
```

- Everything that is in angle brackets &lt;&gt; is optional.

---

<!-- _class: fit-80 -->

# 1 example

```c
#include <stdio.h>
enum color
{
    red,
    green,
    blue,
};


int main(int argc, char *argv[])
{
    printf("The size of [enum color] is %d\n", sizeof(enum color)); /*default as sizeof(int)*/

    enum color my_color = red;
    printf("The value of my_color is %d\n", my_color);

    int x = green;
    printf("The value of x is %d\n", x);

    my_color = 99;  /* be careful */
    printf("The value of my_color is %d\n", my_color);

    if(my_color == red || my_color == green || my_color == blue )
        printf("Proper value\n");
    else
        printf("Improper value\n");
    return 0;
}
```

Result:

```text
The size of [enum color] is 4
The value of my_color is 0
The value of x is 1
The value of my_color is 99
Improper value

```

These constants are often used to represent a fixed set of values, such as days of the week, colors, or error codes. Enums provide a way to make code more readable and maintainable by using meaningful names instead of raw integer values.

---

<!-- _class: fit-80 -->

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

Result:

```text
The value of red is 51
The value of green is 52
The value of blue is 91
The value of orange is 92

```

When using elements from a defined enum, we don't need to use the enum's name itself. They are treated by the compiler as integer constants, which means they can be used to define array sizes just like the #define preprocessor directive.

If we don't specify a value for an enumeration field, the default value is 0. The subsequent field will have a value one greater than the previous one. However, if we define a different value for a field, that field will have an individually defined value and the next field will be one more than the last one.

---

# Enums

- An enum (enumeration) is a user-defined data type in C that consists of a set of named integer constants. These constants are often used to represent a fixed set of values.
- Enum syntax is the same as struct.

Syntax:

```c
enums symbolic_name1
{
	<statement1>
}<symbolic_name2, ...>;
```

- Everything that is in angle brackets &lt;&gt; is optional.

---

<!-- _class: fit-90 -->

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

Result:

```text
The value of my_local_color is 51
The value of my_local_color is 91
orange

```

Given that enums can also create global variables within their definition (including pointers), it's important to keep this in mind. Enums are often used with switch statements, allowing us to convert numerical values into strings.

---

# Bit-fields

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

Result1:

```text
The size of Data is 1
Give me a number
8
1 0 1
```

A bit-field structure occupies as much space as the largest defined field type, instead of assigning a value '=' to fields, the number of BITS for this flag ':' is specified

Result2:

```text
The size of Data is 1
Give me a number
12
1 1 0
```

Result3:

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

<!-- _class: fit-50 -->

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

```text
file path/file name
```

- mode

---

<!-- _class: fit-60 -->

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

Access Modes:

|Mode|Description|
|---|---|
|r|Opens an existing file for reading only.|
|w|Opens a file for writing. Creates a new file or clears the content of an existing one.|
|a|Opens a file for appending data. Creates the file if it does not already exist.|
|x|Creates the file if it does not already exist. Fails if the file already exists.|
|+|Combined with r, w, a, or x, allows both reading and writing.|

File Types:

|Type Modifier|Description|
|---|---|
|t|Text mode (default). Treats file as a sequence of characters.|
|b|Binary mode. Treats file as a sequence of bytes with no translation.|

<!-- najpierw on bibliotece i EOF i ile wynosi ( stala symboliczna i wartosc wynosi -1 -->

---

# Thank you

- Jakub Leszek Pach
- <jpach@mtech.edu>
