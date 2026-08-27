---
marp: true
theme: pach
paginate: true
title: "CSCI 112  Programming with C"
---

# CSCI 112<br><br>Programming with C

- Lecture 11
- Dr. Jakub L. Pach
- Fall 2025

---

![Graphic 3](assets/image2.png)

---

## Outline

- Review
- Command-Line Arguments
- Breaking down code into files
- Keywords
  - extern
  - static
- Compiler
- Makefile

---

# Review

---

## Subtracting two pointers

The result of subtracting two pointers is the difference in their array indices, not the actual difference in their memory locations

- \#include &lt;stdio.h&gt;
- int strlen(char \* string)
- {
-   char \*pointer = string;
-   while(\*pointer != '\0') /\* or NULL or 0 or FALSE \*/
-     pointer++;
-   return pointer - string;
- }
- int main()
- {
-   char \* text = "Hello world!";
-   printf("Length of \[%s\] equals %d\n", text, strlen(text));
-   return 0;
- }
- Length of \[Hello world!\] equals 12
- Result:

---

## Comparing two pointers

Comparing pointers to strings in C can be significantly optimized, especially when there's a high probability that two strings are identical and point to the same memory location

- \#include &lt;stdio.h&gt;
- int main()
- {
-   char \*str1 = "Hello";
-   char \*str2 = str1;
-   if (str1 == str2)
-         printf("Str1 and str2 point to the same string\n");
-   else
-   { // If addresses are different, then compare the content
-     if (strcmp(str1, str2) == 0)
-         printf("Str1 and str2 have the same content\n");
-     else
-         printf("Str1 and str2 are different\n");
-   }
-   return 0;
- }
- Str1 and str2 point to the same string
- Result:

<!-- Jesli mamy dwa element tej samej tablicy, i chcemy znalezc element srodkowy tej tablicy mozemy odjac od siebie adresy I uzyskamy od tego element srodkowy -->

---

## Comparing two pointers

- Array elements are pushed onto the stack in reverse order to ensure that element addresses increase.
- If we compare two elements of an array using two pointers, and we don't know which one is closer to the beginning and which one is closer to the end, the one with the higher address value will be closer to the end, and the one with the lower address value will be closer to the beginning of the array.
- \#include &lt;stdio.h&gt;
- int main()
- {
-   int x = 5, y = 7, z = 9;
-   int b\[\]= { 1, 2, 3, 4 };
-   char text\[\] = "hello";
-   char \*l1 = &amp;text\[2\] , \*l2 = &amp;text\[3\];
- <br>  printf("%d.\n", &amp;x);
-   printf("%d.\n", &amp;y);
-   printf("%d.\n\n", &amp;z);
-   printf("%d.\n", &amp;b\[3\]);
-   printf("%d.\n", &amp;b\[2\]);
-   printf("%d.\n", &amp;b\[1\]);
-   printf("%d.\n\n", &amp;b\[0\]);
- <br>  printf("%d.\n", &amp;text\[3\]);
-   printf("%d.\n", &amp;text\[2\]);
-   printf("%d.\n", &amp;text\[1\]);
-   printf("%d.\n\n", &amp;text\[0\]);
- <br>  if(l1 &lt; l2)
-     printf("l1 is closer to the beginning\n");
-   else
-     printf("l2 is closer to the beginning\n");
-   return 0;
- }
- 6422292\.
- 6422288\.
- 6422284\.
- 6422280\.
- 6422276\.
- 6422272\.
- 6422268\.
- 6422265\.
- 6422264\.
- 6422263\.
- 6422262\.
- l1 is closer to the beginning
- Result:

<!-- Jesli mamy dwa element tej samej tablicy, i chcemy znalezc element srodkowy tej tablicy mozemy odjac od siebie adresy I uzyskamy od tego element srodkowy -->

---

## Assigning or comparing to zero (NULL = ‘\0’)

Trying to use a null pointer will crash the program.

- \#include &lt;stdio.h&gt;
- int main()
- {
-   char \* a\[10\] = {NULL};
- <br>  a\[0\] = "Words";
-   a\[1\] = "of";
-   a\[2\] = "different";
-   a\[3\] = "lengths";
- <br>  int i;
-   for ( i = 0; i &lt; 10; i++ )
-     if(a\[i\])
-       printf("%s ", a\[i\]);
-   return 0;
- }
- Words of different lengths
- Result:

---

## Scanf -Basic Types and Width Specifier

- \#include &lt;stdio.h&gt;

\#define clearBuffer() while (getchar() != '\n');

- int main()
- {

    int age;

    char firstInitial;

    float weight;

    printf("1. Basic Reads and Width:\n");

    // %2d - Limits the read to the first 2 digits. If the user enters "255", only 25 is read.

    printf("Enter Age (2 digits max, e.g., 35): ");

    scanf("%2d", &amp;age);

    clearBuffer();

    // %c - Reads a single character.

    // NOTE: The space before %c is CRITICAL! It instructs scanf to skip leading whitespace,

    // including any leftover '\n' from the previous input.

    printf("Enter First Initial: ");

    scanf(" %c", &amp;firstInitial);

    clearBuffer();

    // %f - Reads a floating-point number.

    printf("Enter Weight (e.g., 75.5): ");

    scanf("%f", &amp;weight);

    clearBuffer();

    printf("Results: Age: %d, Initial: %c, Weight: %.1f\n", age, firstInitial, weight);

- }
- 1\. Basic Reads and Width:
- Enter Age (2 digits max, e.g., 35): 2222222
- Enter First Initial: a
- Enter Weight (e.g., 75.5): 76.2
- Results: Age: 22, Initial: a, Weight: 76.2
- Result:
- This exercise focuses on the fundamental type specifiers (%d, %c, %f) and introduces the **width** modifier (%2d).

<!-- Jesli mamy dwa element tej samej tablicy, i chcemy znalezc element srodkowy tej tablicy mozemy odjac od siebie adresy I uzyskamy od tego element srodkowy -->

---

## Scanf -Length Modifiers (h and l)

- \#include &lt;stdio.h&gt;

\#define clearBuffer() while (getchar() != '\n');

- int main()
- {

    int age;

    char firstInitial;

    float weight;

    printf("1. Basic Reads and Width:\n");

    // %2d - Limits the read to the first 2 digits. If the user enters "255", only 25 is read.

    printf("Enter Age (2 digits max, e.g., 35): ");

    scanf("%2d", &amp;age);

    clearBuffer();

    // %c - Reads a single character.

    // NOTE: The space before %c is CRITICAL! It instructs scanf to skip leading whitespace,

    // including any leftover '\n' from the previous input.

    printf("Enter First Initial: ");

    scanf(" %c", &amp;firstInitial);

    clearBuffer();

    // %f - Reads a floating-point number.

    printf("Enter Weight (e.g., 75.5): ");

    scanf("%f", &amp;weight);

    clearBuffer();

    printf("Results: Age: %d, Initial: %c, Weight: %.1f\n", age, firstInitial, weight);

- }
- 2\. Length Modifiers (long/short):
- Enter a small integer (short): 25
- Enter a large integer (long): 66000
- Results: Short: 25, Long: 66000
- Result:
- 2\. Length Modifiers (long/short):
- Enter a small integer (short): 67 000
- Enter a large integer (long): 1
- Results: Short: 67, Long: 1
- Result:
- This exercise demonstrates the length modifiers for integers: **h** (for short) and **l** (for long). These are essential for matching the format specifier to the variable type.

<!-- Jesli mamy dwa element tej samej tablicy, i chcemy znalezc element srodkowy tej tablicy mozemy odjac od siebie adresy I uzyskamy od tego element srodkowy -->

---

## Scanf - Common Errors 1 and Pitfalls

- \#include &lt;stdio.h&gt;

\#define clearBuffer() while (getchar() != '\n');

- int main()
- {

    printf("\n3. ERROR: Using '\\n' in the scanf format string.\n");

    printf("Enter a value (You will have to press Enter a second time):\n");

    // BAD PRACTICE: scanf("%d\n", &amp;val);

    scanf("%d\n", &amp;val);

    // The program hangs here, waiting for more non-whitespace input to satisfy the '\n' specifier.

    printf("Thank you. The value read is: %d\n", val);

- }
- A frequent beginner mistake is adding \n to the format string, confusing it with printf. **Never use \n in a scanf format string!** It forces the program to wait for non-whitespace input, confusing the user.

<!-- Jesli mamy dwa element tej samej tablicy, i chcemy znalezc element srodkowy tej tablicy mozemy odjac od siebie adresy I uzyskamy od tego element srodkowy -->

---

## Scanf - Common Errors 2 and Pitfalls

- \#include &lt;stdio.h&gt;

\#define clearBuffer() while (getchar() != '\n');

- int main()
- {

    int num;

    char character;

    printf("\n4. ERROR: Demonstrating the Buffer Problem (No clearBuffer()).\n");

    printf("Enter a number: ");

    scanf("%d", &amp;num);

    // NO clearBuffer() -&gt; The '\n' from the Enter key remains in the buffer.

    printf("Enter a character (watch what happens): ");

    // This scanf("%c") immediately reads the leftover '\n' as the intended character.

    scanf("%c", &amp;character);

    printf("\nResult: The character read was: '%c' (It should have been your input, but was the newline)\n", character);

<br>

- }
- This highlights why **clearBuffer()** is necessary, especially before reading a character (%c).

<!-- Jesli mamy dwa element tej samej tablicy, i chcemy znalezc element srodkowy tej tablicy mozemy odjac od siebie adresy I uzyskamy od tego element srodkowy -->

---

## Scanf - Best Practice: Reading Multiple Variables

- \#include &lt;stdio.h&gt;

\#define clearBuffer() while (getchar() != '\n');

- int main()
- {

    int day, month, year;

    printf("\n5. BEST PRACTICE: Reading multiple variables with one scanf call.\n");

    printf("Enter the date in DD MM YYYY format (separated by spaces/Enter): ");

    // scanf automatically skips whitespace between %d specifiers.

    // The user can type: 15 \[space\] 12 \[Enter\] 2023 \[Enter\]

    scanf("%d %d %d", &amp;day, &amp;month, &amp;year);

    clearBuffer(); // Clear the buffer only once at the end.

    printf("\nResult: Date: %d-%d-%d\n", year, month, day);

- }
- 5\. BEST PRACTICE: Reading multiple variables with one scanf call.
- Enter the date in DD MM YYYY format (separated by spaces/Enter): 2 08 1988
- Result: Date: 1988-8-2
- Result:

<!-- Jesli mamy dwa element tej samej tablicy, i chcemy znalezc element srodkowy tej tablicy mozemy odjac od siebie adresy I uzyskamy od tego element srodkowy -->

---

## Scanf - Summary of Best Practices

- Always use &amp;: Remember that scanf requires the address of the variable (&amp;variable) to store the new value.
- Use clearBuffer(): Call the macro AFTER EVERY scanf call, unless you are reading multiple numeric variables in one go.
- No \n in Format String: Never include the newline character (\n) in the scanf format string.
- Whitespace before %c: When reading a single character after reading anything else, use a space: <br>scanf(" %c", ...) to explicitly skip any lingering whitespace.
- Check Return Value: For robust code, always check the value returned by scanf (the count of items successfully read) to validate user input.

<!-- Jesli mamy dwa element tej samej tablicy, i chcemy znalezc element srodkowy tej tablicy mozemy odjac od siebie adresy I uzyskamy od tego element srodkowy -->

---

# Command-Line Arguments

---

## Review

Trying to use a null pointer will crash the program.

- \#include &lt;stdio.h&gt;
- int main()
- {
-   char \* a\[10\] = {NULL};
- <br>  a\[0\] = "Words";
-   a\[1\] = "of";
-   a\[2\] = "different";
-   a\[3\] = "lengths";
- <br>  int i;
-   for ( i = 0; i &lt; 10; i++ )
-     if(a\[i\])
-       printf("%s ", a\[i\]);
-   return 0;
- }
- Words of different lengths
- Result:

---

## Command-Line Arguments

Command-line arguments are values passed to a program when it is executed from the terminal/command prompt. Allows users to provide input to the program without the need for user interaction during execution.

- argc:    Argument count, the number of command-line arguments passed <br>    (including the program's name).
- argv\[\]:    Argument vector, an array of strings (character pointers) representing the     arguments.

Syntax:    int main(int argc, char \*argv\[\])

---

## Command-Line Arguments

- Command-line arguments start after a whitespace character, such as a space (ASCII 32), and are treated as strings. Each word separated by a space is considered a separate argument.
- However, if you want to pass an argument that contains spaces as a single string, you need to enclose it in quotes.

argc:    Always greater than or equal to 1 (the first argument is the program’s name).

- argv\[\]:
  - argv\[0\]: The name of the program.
  - argv\[1\] to argv\[argc-1\]: The actual arguments passed by the user.

---

## Examples

- \#include &lt;stdio.h&gt;
- int main(int argc, char \*argv\[\])
- {
-     if(argc &gt; 1)
-         printf("%s\n", argv\[1\] );
-     return 0;
- }
- C:\...\C&gt;main.exe text
- text
- one argument
- \#include &lt;stdio.h&gt;
- int main(int argc, char \*argv\[\])
- {
-     if(argc &gt; 2)
-     {
-         printf("%s\n", argv\[1\] );
-         printf("%s\n", argv\[2\] );
-     }
-     return 0;
- }
- C:\...\C&gt;main.exe text1 text2
- text1
- text2
- two arguments
- \#include &lt;stdio.h&gt;
- int main(int argc, char \*argv\[\])
- {
-     if(argc &gt; 1)
-         printf("%s\n", argv\[1\] );
-     return 0;
- }
- C:\...\C&gt;main.exe "text1 text2"
- text1 text2
- one argument
- consisting of several words

---

## Examples

- \#include &lt;stdio.h&gt;
- int main(int argc, char \*argv\[\])
- {
-     int i;
-     for (i = 1; i &lt; argc; i++)
-         printf("Argument %d: %s\n", i, argv\[i\]);
-     return 0;
- }
- C:\...\C&gt;main.exe text1 text2
- Argument 1: tex1
- Argument 2: text2
- \#include &lt;stdio.h&gt;
- \#include &lt;stdlib.h&gt;
- int main(int argc, char \*argv\[\])
- {
-     if (argc == 3)
-     {
-         int num1 = atoi(argv\[1\]);
-         int num2 = atoi(argv\[2\]);
-         int sum = num1 + num2;
-         printf("Sum: %d\n", sum);
-     }
-     return 0;
- }
- C:\...\C&gt;main.exe 1 2
- Sum: 3
- The name of the atoi() function is an acronym for ASCII to int. This function converts a string into an integer.
- To use it, the #include &lt;stdlib.h&gt; header must be imported.

---

# Breaking down code into files

---

## Source code &amp; header files

To improve code readability, C allows for the separation of functions, data structures, and global variables into separate files. This makes the code more clear and easier to maintain.

- header file:

(with a .h extension) contains prototypes of functions, global variables, and structures that are used in multiple source files, providing a way to share information

- source code file:

(with a .c extension) contains the actual implementation of the program's logic, such as function definitions and variable declarations.

To make functions defined in other files visible in a file, it is sufficient to include the header file using #include "name\_of\_header.h". There is no need to include files with the .c extension.

---

## Source code &amp; header files

- Function prototypes serve a dual purpose.
  - They ensure consistency between a function's declaration and its definition. This allows the compiler to verify the compatibility of return types and arguments, preventing hard-to-find errors that often occur when prototypes are omitted.
  - Prototypes are typically placed in separate header files(.h) , especially in larger projects consisting of multiple files. This division enables better code organization.
- The C compiler does not strictly require function prototypes or header files. It's possible to create a new file, write a function, add it to the project, and access it from main.c However, in our course, we require the creation of at least one header file containing prototypes for all functions that will be implemented in other files and included in the entire program.

---

## Example

- All files are in the same folder
- It's worth noting that header file names and implementation file names don't have to be identical, although this convention is often used to improve project readability
- <br>int sum(int, int);
- int difference(int, int);

\#include "funs.h"

- int sum(int a, int b)
- {
-   return a + b;
- }
- int difference(int a, int b)
- {
-   return a - b;
- }
- \#include &lt;stdio.h&gt;
- \#include "funs.h"
- int main()
- {
-  int x = 5, y = 3;
-  printf("Sum of %d and %d equals %d\n", x, y, sum(x, y));
-  return 0;
- }
- File: funs.h
- File: funs.c
- File: main.c
- Sum of 5 and 3 equals 8
- Result:

---

## Review - preprocessor directive - #ifndef

- Checks if a macro is not defined.
- \#include &lt;stdio.h&gt;
- <br>#ifndef MAX\_SIZE
- \#define MAX\_SIZE 100
- \#endif
- <br>int main()
- {
-     printf("MAX\_SIZE is %d\n", MAX\_SIZE);
-     return 0;
- }
- MAX\_SIZE is 100
- Result:

---

## Example

Every source file that includes a header will have its contents inserted during compilation. If multiple files include the same header that contains definitions, the linker will report multiple definition errors because the same code is compiled more than once. To prevent this, header files should use include guards (#ifndef, #define, #endif)

- <br>int sum(int, int);
- int difference(int, int);
- File: funs.h
- \#include &lt;stdio.h&gt;
- <br>#ifndef MAX\_SIZE
- \#define MAX\_SIZE 100
- \#endif
- <br>int main()
- {
-     printf("MAX\_SIZE is %d\n", MAX\_SIZE);
-     return 0;
- }

//func.h

\#ifndef FUNC\_H

\#define FUNC\_H

  int sum(int, int);

  int difference(int, int);

\#endif

---

## Summary

*Of all the directives regarding compilation and makefiles, the* #ifndef *directive seems to be the most commonly used, as it prevents the same file from being included more than once in the final output. As can easily be seen, many different files can use the same library.*

---

## Example

- All files are in the same folder
- It's worth noting that header file names and implementation file names don't have to be identical, although this convention is often used to improve project readability

//func.h

\#ifndef FUNC\_H

\#define FUNC\_H

  int sum(int, int);

  int difference(int, int);

\#endif

\#include "funs.h"

- int sum(int a, int b)
- {
-   return a + b;
- }
- int difference(int a, int b)
- {
-   return a - b;
- }
- \#include &lt;stdio.h&gt;
- \#include "funs.h"
- int main()
- {
-  int x = 5, y = 3;
-  printf("Sum of %d and %d equals %d\n", x, y, sum(x, y));
-  return 0;
- }
- File: funs.h
- File: funs.c
- File: main.c
- Sum of 5 and 3 equals 8
- Result:

---

## extern keyword

- In a single code block, we cannot declare two variables with the same name.
- An inner block allows us to declare a variable with the same name inside it, which shadows the variable from the outer block but doesn't destroy it. After the inner block ends, we can access the first variable again.
- Similarly, we cannot declare and initialize the same global variable in two different files.
- If we declare a global variable in one file, to make it visible in another file, we use the extern keyword before the declaration in the second file. In this way, we can access the variable from the other file.

---

## extern keyword

//func.h

\#ifndef FUNC\_H

\#define FUNC\_H

  int sum(int, int);

  int difference(int, int);

\#endif

\#include "funs.h"

- extern int x, y;
- int sum()
- {
-   return x + y;
- }
- int difference()
- {
-   return x - y;
- }
- \#include &lt;stdio.h&gt;
- \#include "funs.h“
- int x = 5, y = 3;
- int main()
- {
-  printf("Sum of %d and %d equals %d\n", x, y, sum());
-  return 0;
- }
- File: funs.h
- File: funs.c
- File: main.c
- Sum of 5 and 3 equals 8
- Result:

---

# Is this the way to hide a variable from one file to another?

---

## static keyword

//func.h

\#ifndef FUNC\_H

\#define FUNC\_H

  int sum(int, int);

  int difference(int, int);

\#endif

\#include "funs.h"

- static int x = 4, y = 2;
- int sum()
- {
-   return x + y;
- }
- int difference()
- {
-   return x - y;
- }
- \#include &lt;stdio.h&gt;
- \#include "funs.h“
- static int x = 5, y = 3;
- int main()
- {
-  printf("Sum of %d and %d equals %d\n", x, y, sum());
-  return 0;
- }
- File: funs.h
- File: funs.c
- File: main.c
- Sum of 5 and 3 equals 6
- Result:

---

## static keyword

- static keyword has two meanings, depending on where the static variable\* is declared:
- Outside a function, static variables only visible within that file, not globally
- Inside a function, static variables:
  - are still local to that function :
  - are initialized only during program initialization\*
  - do not get reinitialized with each function call
- \*    The keyword static can be placed before a function's implementation to restrict its     accessibility to the current file.
- \*    Static variables are initialized with a default value according to their type, unlike automatic     variables.

---

## static keyword

- \#include &lt;stdio.h&gt;
- void ticketSale(void);
- int main()
- {
-   ticketSale();
-   ticketSale();
-   ticketSale();
-   return 0;
- }
- void ticketSale()
- {
-   static int x = 0; /\* initialization at the beginning \*/
-   x++;    /\*of the program, not during block execution \*/
-   printf("There are currently %d tickets sold.\n", x);
- }
- There are currently 1 tickets sold.
- There are currently 1 tickets sold.
- There are currently 1 tickets sold.
- Result:
- \#include &lt;stdio.h&gt;
- void ticketSale(void);
- int main()
- {
-   ticketSale();
-   ticketSale();
-   ticketSale();
-   return 0;
- }
- void ticketSale()
- {
-   int x = 0;
-   x++;
-   printf("There are currently %d tickets sold.\n", x);
- }
- There are currently 1 tickets sold.
- There are currently 2 tickets sold.
- There are currently 3 tickets sold.
- Result:

---

# Compiler

---

## How does a C program executes?

- C/C++ code
- Preprocessing
- Compiler
- Assembler
- Linker
- Loader

This is the source code you have written in the C/C++ programming language. It forms the basis of your program.

During this stage, the preprocessor processes your source code. It includes header files (e.g., stdio.h, math.h) using directives like #include and expands macros defined with #define. The output of this stage is the preprocessed source code.

The compiler takes the preprocessed source code and translates it into assembly code. This assembly code is a low-level representation of your program that is specific to the target architecture.

The assembler converts the assembly code **into object code**. Object code is a machine-readable format that contains instructions and data.

The linker combines the object code with other necessary libraries (e.g., standard C library) to create the final executable program. This process resolves external references and creates a complete program that can be run.

The loader loads the executable program into memory (RAM) so that it can be executed by the CPU. The running program is often referred to as a process.

These steps are essential for transforming your C code into an executable program that can be run on a computer.

---

## Compilers

- GCC – GNU Compiler Collection
- Microsoft Compiler C/C++
- …

C files are regular text files (txt), differing only by their extension, as they are plain text files in which each byte (depending on the encoding - ASCII) is represented as an element of the ASCII table.

---

## A summary

*Although GNU is primarily associated with Unix-like systems, the ideas of free software and open source have allowed GNU tools, such as GCC, to be ported to other platforms, including Windows.*

*As a result, Windows developers can use the same tools as developers working on other systems, which contributes to the unification of the development environment.*

---

## Example 1 - main.c

- Create a new folder,
- create a file named main.c inside it and fill it with the simplest possible code.

// main.c

\#include&lt;stdio.h&gt;

int main()

{

  printf("%s\n", "Hello, world!");

  return 0;

}

---

## Process of compilation

- Compile main.c into an object file main.o:
- Link the object file main.o into an executable main.exe:

gcc -g -Wall -std=c99 -pedantic -c main.c -o main.o

\# 1) Compile main.c into an object file main.o (no linking).

\#    Includes debug symbols (-g), enables most warnings (-Wall), uses the C99 standard (-std=c99),

\#    and enforces strict standard conformance (-pedantic).

gcc -g main.o -o main.exe

\# 2) Link the object file into an executable named main.exe.

---

## How does a C program executes?

- C code
- Preprocessing
- Compiler
- Assembler
- Linker
- Loader

This is the source code you have written in the C programming language. It forms the basis of your program.

During this stage, the preprocessor processes your source code. It includes header files (e.g., stdio.h, math.h) using directives like #include and expands macros defined with #define. The output of this stage is the preprocessed source code.

The compiler takes the preprocessed source code and translates it into assembly code. This assembly code is a low-level representation of your program that is specific to the target architecture.

The assembler converts the assembly code **into object code**. Object code is a machine-readable format that contains instructions and data.

The linker combines the object code with other necessary libraries (e.g., standard C library) to create the final executable program. This process resolves external references and creates a complete program that can be run.

The loader loads the executable program into memory (RAM) so that it can be executed by the CPU. The running program is often referred to as a process.

These steps are essential for transforming your C code into an executable program that can be run on a computer.

---

## Process of compilation

- Compile and link in one step (from main.c directly to main.exe):

gcc -g -Wall -std=c99 -pedantic main.c -o main.exe

\# 3) Compile and link in one step: from main.c directly to main.exe,

\#    with the same diagnostic/standard flags as in step 1.

---

## How does a C program executes?

- C code
- Preprocessing
- Compiler
- Assembler
- Linker
- Loader

This is the source code you have written in the C programming language. It forms the basis of your program.

During this stage, the preprocessor processes your source code. It includes header files (e.g., stdio.h, math.h) using directives like #include and expands macros defined with #define. The output of this stage is the preprocessed source code.

The compiler takes the preprocessed source code and translates it into assembly code. This assembly code is a low-level representation of your program that is specific to the target architecture.

The assembler converts the assembly code **into object code**. Object code is a machine-readable format that contains instructions and data.

The linker combines the object code with other necessary libraries (e.g., standard C library) to create the final executable program. This process resolves external references and creates a complete program that can be run.

The loader loads the executable program into memory (RAM) so that it can be executed by the CPU. The running program is often referred to as a process.

These steps are essential for transforming your C code into an executable program that can be run on a computer.

---

## About flags

- The -g flag tells the compiler to include debugging information in the output. Without it, setting breakpoints in the compiled file would not be possible. This flag should be disabled in the final compilation of the application after the development process is complete.
- The flags -Wall, -std, and -pedantic are compiler-specific and only necessary during the creation of object files. The -c and -o flags indicate source and object files, respectively.
- Therefore, if the compilation process is split into two stages — compilation and linking — only the -g flag should be repeated during linking.

---

# Makefile

---

## Introduction to Makefile

- What is a Makefile?
  - A Makefile is a script(program) used by the mingw32-make build automation tool to compile and link programs.
  - It defines a set of rules to determine which files need to be compiled, how to compile them, and in what order.
  - This is especially helpful for large projects where multiple source files depend on each other.
- A Makefile consists of:
  - **Targets**:    Names of the file(s) to be created, usually executable files.
  - **Dependencies**:    Files that must be compiled or checked before the target can be built.
  - **Commands**:    The shell commands executed to compile the dependencies and create the target.

---

## Introduction to Makefile

Syntax Example:

TARGET: DEPENDENCIES

\[TAB\] command

- TARGET:    The file to generate (e.g., main.exe).
- DEPENDENCIES:    Source files or other targets that the current target depends on.
- command:    Shell command (preceded by a tab) to execute.

---

## An example of makefile

CC = gcc

CFLAGS = -g -Wall -Wextra -std=c99 -pedantic

OBJS = main.o unity.o

TARGET = main.exe<br>

.PHONY: all clean

all: $(TARGET)<br>

$(TARGET): $(OBJS)

    $(CC) $(OBJS) -o $(TARGET)<br>

main.o: main.c unity.h

    $(CC) $(CFLAGS) -c main.c -o main.o<br>

unity.o: unity.c unity.h

    $(CC) $(CFLAGS) -c unity.c -o unity.o<br>

clean:

    del /f \*.o $(TARGET)  # Windows

Key Components:

- Variables: Reusable values like CC (compiler) and CFLAGS (compiler flags).
- Targets: Specifies what file(s) to create (e.g., main.exe).
- Commands: Actual shell commands that run <br>(must be preceded by a tab).
- Phony Targets: Non-file targets like clean, used to remove build files (rm in Linux, del in Windows).

---

# Thank you

- Jakub Leszek Pach
- <jpach@mtech.edu>

---

## Some examples

- int main()
- {
-   int x = 5, y = 7;
-   int \* p = &amp;x;
-   int \*\* pp = &amp;p;   /\* pointer to pointer\*/
-   y = \*\*pp;
-   printf("y equals %d.\n\n",  y );
- <br>  printf("&amp;y\t\tequals %d.\n", &amp;y );
-   printf("\*(&amp;y)\t\tequals %d.\n", \*(&amp;y) );
-   printf("&amp;(\*(&amp;y))\tequals %d.\n", &amp;(\*(&amp;y)) );
-   printf("&amp;\*&amp;y\t\tequals %d.\n", &amp;\*&amp;y );
-   printf("\*&amp;\*&amp;y\t\tequals %d.\n\n", \*&amp;\*&amp;y );
- <br>  printf("&amp;x\t\tequals %d.\n", &amp;x );
-   printf("p\t\tequals %d.\n", p );
-   printf("&amp;p\t\tequals %d.\n", &amp;p );
-   printf("\*p\t\tequals %d.\n\n", \*p );
- <br>  printf("pp\t\tequals %d.\n", pp );
-   printf("&amp;pp\t\tequals %d.\n", &amp;pp );
-   printf("\*pp\t\tequals %d.\n", \*pp );
-   printf("\*&amp;\*pp\t\tequals %d.\n", \*&amp;\*pp );
-   printf("\*\*pp\t\tequals %d.\n", \*\*pp );
-   return 0; <br>}
- y equals 5.
- &amp;y              equals 6422292.
- \*(&amp;y)           equals 7.
- &amp;(\*(&amp;y))        equals 6422292.
- &amp;\*&amp;y            equals 6422292.
- \*&amp;\*&amp;y           equals 7.
- &amp;x              equals 6422296.
- p               equals 6422296.
- &amp;p              equals 6422288.
- \*p              equals 5.
- pp              equals 6422288.
- &amp;pp             equals 6422284.
- \*pp             equals 6422296.
- \*&amp;\*pp           equals 6422296.
- \*\*pp            equals 5.
- Result:

||Memory Addresses and Values|||
|---|---|---|---|
|||||
||x (6422296)|5||
|||||
||y (6422292)|5||
|||||
||p (6422288)|6422296||
|||||
||pp (6422284)|6422288||
|||||

![Ink 54](assets/image4.png)

![Ink 55](assets/image5.png)

![Ink 56](assets/image6.png)

![Ink 58](assets/image7.png)

![Ink 59](assets/image8.png)

![Ink 60](assets/image9.png)
