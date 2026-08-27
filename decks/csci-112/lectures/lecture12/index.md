---
marp: true
theme: pach
paginate: true
title: "CSCI 112  Programming with C"
---

# CSCI 112<br><br>Programming with C

- Lecture 12
- Dr. Jakub L. Pach
- Fall 2025

---

![Graphic 3](assets/image2.png)

---

## Outline

- Review
- &gt;&gt; &amp; &lt;&lt;
- Typedef
- Function pointer
- Structures
- Padding

---

# Review

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

## Source code &amp; header files

To improve code readability, C allows for the separation of functions, data structures, and global variables into separate files. This makes the code more clear and easier to maintain.

- header file:

(with a .h extension) contains prototypes of functions, global variables, and structures that are used in multiple source files, providing a way to share information

- source code file:

(with a .c extension) contains the actual implementation of the program's logic, such as function definitions and variable declarations.

To make functions defined in other files visible in a file, it is sufficient to include the header file using #include "name\_of\_header.h". There is no need to include files with the .c extension.

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

---

# Bitwise left shift &amp; right shift

---

|Priority / Operator||Description|Associativity|Example|Result|
|---|---|---|---|---|---|
|1|(), \[\]|Parentheses; Array subscript|Left-to-right|arr\[0\] \* (x + y)|1|
||.|Structure and union member access||point.x|1|
||-&gt;|Structure and union member access through pointer||ppoint-&gt;x|1|
|2|++, --|Prefix &amp; postfix increment and decrement|Right-to-left|++x; x--; x;|6, 6, 5|
||+, -, !, ~|(Unary) plus and minus; Logical NOT and bitwise NOT||y =-y; y =+y; !x; ~;x|6, -6,0, -6|
||\*, &amp; , &amp;&amp;|Indirection (dereference); Address-of; Address-of labels||z = &amp;x; \*z;|6422276; 5|
||(type), sizeof|Cast, Size-of||(int)3.0f; sizeof(x);|3, 4|
|3|\*, /, %|Multiplication, division, and remainder|Left-to-right|6/2 % 2|1|
|4|+, -|Addition and subtraction||1 + 2; 3 - 1|3, 2|
|5|&lt;&lt;,  &gt;&gt;|Bitwise left shift and right shift||4 &lt;&lt; 1; 4 &gt;&gt; 2|8, 1|
|6|&lt;, &lt;=, &gt;, &gt;=|For relational operators &lt;, &gt; and ≤, ≥ respectively||x&lt;y; x&lt;=y; x&gt;y; x&gt;=y|1, 1, 0 ,0|
|7|==, !=|For relational = and ≠ respectively||x == y, x != 1|1, 0|
|8|&amp;|Bitwise AND||7 &amp; 3|3|
|9|^|Bitwise XOR (exclusive or)||255 ^ 0|255|
|10|\||Bitwise OR (inclusive or)||7 \| 3|7|
|11|&amp;&amp;|Logical AND||1 &amp;&amp; 0|0|
|12|\|\||Logical OR||1 \|\| 0|1|
|13|?:|Ternary conditional|Right-to-left|x  = (x &gt; y) ? y : x;|-6|
|14|=|Simple assignment||x  = y;|-6|
||+=, -=, \*=, /=, %=|Assignment by sum, difference, product, quotient, remainder||x+=1; x-=1; //etc.|6, 5|
||&lt;&lt;=, &gt;&gt;=, &amp;=, ^=, \|=|Assignment by bitwise left shift, right shift, AND, XOR, OR||3&lt;&lt;=1, 8&gt;&gt;=2 //etc.|6, 2|
|15|,|Comma|Left-to-right|x = 3, y = 1;|3|

- struct Point { int x; int y; }; int main()<br>{struct Point point = {1,2}, \*ppoint = &amp;point;  int arr\[\] = {1,2}; int x = 5, y =-6; int \* z; float f = 3.0f; /\*code\*/}

<!-- perentysys; esiszewitiwy
Use parentheses to override order of evaluation -->

---

## Bitwise AND, OR, XOR

- a | b = 13
- a &amp; b = 4
- a ^ b = 9
- Result:
- int main()
- {
-     int a = 4;
-     int b = 13;
-     int result = a | b;
-     printf("a | b = %d\n", result);
-     result = a &amp; b;
-     printf("a &amp; b = %d\n", result);
-     result = a ^ b;
-     printf("a ^ b = %d\n", result);
- }
- How does work?

---

## Example

|Index|7|6|5|4|3|2|1|0|Result|
|---|---|---|---|---|---|---|---|---|---|
|Value 2^Idx|128|64|32|16|8|4|2|1||
|a|0|0|0|0|0|1|0|0|4|
|b|0|0|0|0|1|1|0|1|13|
|a \| b (or )||||||||||
|a &amp; b (and)||||||||||
|a ^ b (xor)||||||||||

---

## Example

|Index|7|6|5|4|3|2|1|0|Result|
|---|---|---|---|---|---|---|---|---|---|
|Value 2^Idx|128|64|32|16|8|4|2|1||
|a|0|0|0|0|0|1|0|0|4|
|b|0|0|0|0|1|1|0|1|13|
|a \| b (or )|0|0|0|0|1|1|0|1|13|
|a &amp; b (and)||||||||||
|a ^ b (xor)||||||||||

---

## Example

|Index|7|6|5|4|3|2|1|0|Result|
|---|---|---|---|---|---|---|---|---|---|
|Value 2^Idx|128|64|32|16|8|4|2|1||
|a|0|0|0|0|0|1|0|0|4|
|b|0|0|0|0|1|1|0|1|13|
|a \| b (or )|0|0|0|0|1|1|0|1|13|
|a &amp; b (and)|0|0|0|0|0|1|0|0|4|
|a ^ b (xor)||||||||||

---

## Example

|Index|7|6|5|4|3|2|1|0|Result|
|---|---|---|---|---|---|---|---|---|---|
|Value 2Index|128|64|32|16|8|4|2|1||
|a|0|0|0|0|0|1|0|0|4|
|b|0|0|0|0|1|1|0|1|13|
|a \| b (or )|0|0|0|0|1|1|0|1|13|
|a &amp; b (and)|0|0|0|0|0|1|0|0|4|
|a ^ b (xor)|0|0|0|0|1|0|0|1|9|

---

|Priority / Operator||Description|Associativity|Example|Result|
|---|---|---|---|---|---|
|1|(), \[\]|Parentheses; Array subscript|Left-to-right|arr\[0\] \* (x + y)|1|
||.|Structure and union member access||point.x|1|
||-&gt;|Structure and union member access through pointer||ppoint-&gt;x|1|
|2|++, --|Prefix &amp; postfix increment and decrement|Right-to-left|++x; x--; x;|6, 6, 5|
||+, -, !, ~|(Unary) plus and minus; Logical NOT and bitwise NOT||y =-y; y =+y; !x; ~;x|6, -6,0, -6|
||\*, &amp; , &amp;&amp;|Indirection (dereference); Address-of; Address-of labels||z = &amp;x; \*z;|6422276; 5|
||(type), sizeof|Cast, Size-of||(int)3.0f; sizeof(x);|3, 4|
|3|\*, /, %|Multiplication, division, and remainder|Left-to-right|6/2 % 2|1|
|4|+, -|Addition and subtraction||1 + 2; 3 - 1|3, 2|
|5|&lt;&lt;,  &gt;&gt;|Bitwise left shift and right shift||4 &lt;&lt; 1; 4 &gt;&gt; 2|8, 1|
|6|&lt;, &lt;=, &gt;, &gt;=|For relational operators &lt;, &gt; and ≤, ≥ respectively||x&lt;y; x&lt;=y; x&gt;y; x&gt;=y|1, 1, 0 ,0|
|7|==, !=|For relational = and ≠ respectively||x == y, x != 1|1, 0|
|8|&amp;|Bitwise AND||7 &amp; 3|3|
|9|^|Bitwise XOR (exclusive or)||255 ^ 0|255|
|10|\||Bitwise OR (inclusive or)||7 \| 3|7|
|11|&amp;&amp;|Logical AND||1 &amp;&amp; 0|0|
|12|\|\||Logical OR||1 \|\| 0|1|
|13|?:|Ternary conditional|Right-to-left|x  = (x &gt; y) ? y : x;|-6|
|14|=|Simple assignment||x  = y;|-6|
||+=, -=, \*=, /=, %=|Assignment by sum, difference, product, quotient, remainder||x+=1; x-=1; //etc.|6, 5|
||&lt;&lt;=, &gt;&gt;=, &amp;=, ^=, \|=|Assignment by bitwise left shift, right shift, AND, XOR, OR||3&lt;&lt;=1, 8&gt;&gt;=2 //etc.|6, 2|
|15|,|Comma|Left-to-right|x = 3, y = 1;|3|

- struct Point { int x; int y; }; int main()<br>{struct Point point = {1,2}, \*ppoint = &amp;point;  int arr\[\] = {1,2}; int x = 5, y =-6; int \* z; float f = 3.0f; /\*code\*/}

<!-- perentysys; esiszewitiwy
Use parentheses to override order of evaluation -->

---

## Bitwise left shift(&lt;&lt;) and right shift(&gt;&gt;)

- a &gt;&gt; b = ?
- a &lt;&lt; b = ?
- Result:
- int main()
- {
-     int a = 4;
-     int b = 2;
-     int result = a &gt;&gt; b;
-     printf("a &gt;&gt; b = %d\n", result);
-     result = a &lt;&lt; b;
-     printf("a &lt;&lt; b = %d\n", result);
- }
- How does work?

---

## Example

|Index|7|6|5|4|3|2|1|0|Result|
|---|---|---|---|---|---|---|---|---|---|
|Value 2^Idx|128|64|32|16|8|4|2|1||
|a|0|0|0|0|0|1|0|0|4|
|b|0|0|0|0|0|0|1|0|2|
|a &gt;&gt; b||||||||||
|a &lt;&lt; b||||||||||

---

## Example

|Index|7|6|5|4|3|2|1|0|Result|
|---|---|---|---|---|---|---|---|---|---|
|Value 2^Idx|128|64|32|16|8|4|2|1||
|a|0|0|0|0|0|1|0|0|4|
|b|0|0|0|0|0|0|1|0|2|
|a &gt;&gt; b|0|0|0|0|0|0|0|1|1|
|a &lt;&lt; b||||||||||

---

## Example

|Index|7|6|5|4|3|2|1|0|Result|
|---|---|---|---|---|---|---|---|---|---|
|Value 2^Idx|128|64|32|16|8|4|2|1||
|a|0|0|0|0|0|1|0|0|4|
|b|0|0|0|0|0|0|1|0|2|
|a &gt;&gt; b|0|0|0|0|0|0|0|1|1|
|a &lt;&lt; b|0|0|0|1|0|0|0|0|16|

---

## Bitwise left shift(&lt;&lt;) and right shift(&gt;&gt;)

- a &gt;&gt; b = 1
- a &lt;&lt; b = 16
- Result:
- int main()
- {
-     int a = 4;
-     int b = 2;
-     int result = a &gt;&gt; b;
-     printf("a &gt;&gt; b = %d\n", result);
-     result = a &lt;&lt; b;
-     printf("a &lt;&lt; b = %d\n", result);
- }

---

## Bitwise Left Shift &amp; Right Shift - summary

- The left shift &lt;&lt; moves all bits in a number to the left by a specified number of positions.→ Each shift left multiplies the value by 2.
- The right shift &gt;&gt; moves all bits to the right by a specified number of positions.→ Each shift right divides the value by 2 (for unsigned types).
- **Applications**:
  - Fast multiplication or division by powers of two
  - Bit masking and flag operations
  - Extracting or packing bits into specific positions
  - Embedded systems, hardware control, and data compression
- Can be combined in **expressions** with arithmetic, logical, and assignment operators: x = (a &lt;&lt; 3) | (b &amp; 0x0F);
- Shifting beyond the bit width of the type → undefined behavior,
- Right shift of signed values may perform arithmetic or logical shift depending on the compiler.

---

# typedef keyword

---

## typedef keyword

- C provides a facility called typedef for creating new data type names.
- typedef can be used with functions and structs etc.

Syntax:

typedef &lt;type&gt; Symbolic\_name

- \#include &lt;stdio.h&gt;
- typedef char \* String;
- typedef char Letter;
- int strCmp( String one, String two )
- {
-     int i;
-     for (i = 0; one\[i\] != '\0' &amp;&amp; two\[i\] != '\0'; i++)
-         if(one\[i\] &gt; two\[i\])
-             return 1;
-         else if(one\[i\] &lt; two\[i\])
-             return -1;
-     return 0;
- }
- int main(int argc, char \*argv\[\])
- {
-     String text1 = "Some text\n"; /\* read only! \*/
-     String text2 = "Some text\n";
-     printf( "%d", strCmp(text1, text2) );
-     Letter letter = 'A';
-     printf( "%c", letter );
-     return 0;
- }
- 0A
- Result:

---

# Function pointer

---

## Foreword - signature of function

Although the concept of a signature officially emerged in the context of methods in C++, it can be argued that functions in C have their own signatures, meaning a unique identifier composed of:

- Function name: Each function has a unique name used to call it.
- Parameter list: The set of arguments that a function takes, along with their types and order, is crucial for its operation.
- Return type: The data type that a function returns upon completion is also an essential part of its definition.

---

## Function pointer

- int (\*operation)(int, int);

*Function pointers are used to store the memory address of a function. For a function pointer to be correctly used, the signature of the function it points to must exactly match the signature of the pointer itself. This means the return type and the list of arguments (including their types and order) must be identical.*

- return-type function-name (only type of parameter declarations, if any);
- return-type (\*function-name-pointer) (only type of parameter declarations, if any);

---

## Function pointer

- \#include &lt;stdio.h&gt;
- int add(int, int); /\* Function prototypes (declarations)\*/
- int subtract(int, int);
- <br>int add(int a, int b) /\* Function definitions \*/
- {
-   return a + b;
- }
- int subtract(int a, int b)
- {
-   return a - b;
- }
- int main()
- {
-   int x = 5, y = 3;
-   int (\*operation)(int, int);    /\* Declare a function pointer that can point to functions  \*/
-                                            /\* taking two integers and returning an integer  \*/
-   operation = add;               /\* Assign the address of the 'add' function to the pointer \*/
-   int result = operation(x, y); /\* Call the function through the pointer \*/
-   printf("Result of addition: %d\n", result);
-   operation = subtract;
-   result = operation(x, y);
-   printf("Result of subtraction: %d\n", result);
- <br>  return 0;
- }
- Result of addition: 8
- Result of subtraction: 2
- Result:

---

## Function pointer with typdef

- \#include &lt;stdio.h&gt;
- int add(int, int);
- int subtract(int, int);
- <br>int add(int a, int b)
- {
-   return a + b;
- }
- int subtract(int a, int b)
- {
-   return a - b;
- }
- int main()
- {
-   int x = 5, y = 3;
-   int (\*peration)(int,int);
-   operation = add;
-   int result = operation(x, y);
-   printf("Result of addition: %d\n", result);
-   operation = subtract;
-   result = operation(x, y);
-   printf("Result of subtraction: %d\n", result);
- <br>  return 0;
- }
- Result of addition: 8
- Result of subtraction: 2
- Result:
- \#include &lt;stdio.h&gt;
- int add(int, int);
- int subtract(int, int);
- <br>int add(int a, int b)
- {
-   return a + b;
- }
- int subtract(int a, int b)
- {
-   return a - b;
- }

typedef int (\*Operation)(int,int);

- int main()
- {
-   int x = 5, y = 3;
-   Operation operation = add;
-   int result = operation(x, y);
-   printf("Result of addition: %d\n", result);
-   operation = subtract;
-   result = operation(x, y);
-   printf("Result of subtraction: %d\n", result);
- <br>  return 0;
- }
- When you use **typedef** with the syntax for a function pointer, you are not creating any pointer.
- You are simply defining <br>a type alias, which means this type does not exist in main until you actually declare <br>a variable of that type!!!

---

# Structures

---

## Structures

- Structures are user-defined data types that group together variables of different data types.
- A structure is a collection of one or more variables, possibly of different types, grouped together under single symbolic\_name for convenient handling.
- struct symbolic\_name1
- {
- &lt;statement1&gt;
- }&lt;symbolic\_name2, ...&gt;;
- Syntax:
- Everything that is in angle brackets &lt;&gt; is optional.

---

## An example

- \#include &lt;stdio.h&gt;
- struct MyStruct
- {
-     int value;
- }\*p, s; /\* like struct MyStruct  \* sPointer; struct MyStruct myStructure;\*/
- <br>struct MyStruct  \* sPointer; /\* global pointer \*/
- struct MyStruct myStructure; /\* global variable \*/
- <br>struct MyStruct function( struct MyStruct temp )
- {
-     temp.value += 5;
-     return temp;
- }
- int main(int argc, char \*argv\[\])
- {
-     struct MyStruct localStruct; /\* local variable \*/
-     localStruct.value = 1;
-     struct MyStruct \* localStructPointer; /\* local pointer \*/
-     localStructPointer = &amp;localStruct;
-     printf( "%d\n", localStruct.value );
-     localStructPointer-&gt;value = 2;
-     printf( "%d\n", localStructPointer-&gt;value );
-     printf( "%d\n", (\*localStructPointer).value ); /\*Equivalent to the previous line\*/
-     p = &amp; s;
-     (\*p).value = 2;
-     printf( "%d\n", s.value );
-     printf( "%d\n", p-&gt;value );
- <br>    printf( "%d\n", myStructure.value );
-     myStructure = function( \*localStructPointer );
-     printf( "%d\n", myStructure.value );
-     return 0;
- }
- 1
- 2
- 2
- 2
- 2
- 0
- 7
- Result:

To access members of a structure, we use the dot operator. When accessing a member through a pointer, we must use the dereferencing operator (\*) followed by the member access operator (.), enclosed in parentheses: (\*symbolic\_name).field. Alternatively, we can use the arrow operator (-&gt;), which is equivalent to symbolic\_name-&gt;field.

---

|Priority / Operator||Description|Associativity|Example|Result|
|---|---|---|---|---|---|
|1|(), \[\]|Parentheses; Array subscript|Left-to-right|arr\[0\] \* (x + y)|1|
||.|Structure and union member access||point.x|1|
||-&gt;|Structure and union member access through pointer||ppoint-&gt;x|1|
|2|++, --|Prefix &amp; postfix increment and decrement|Right-to-left|++x; x--; x;|6, 6, 5|
||+, -, !, ~|(Unary) plus and minus; Logical NOT and bitwise NOT||y =-y; y =+y; !x; ~;x|6, -6,0, -6|
||\*, &amp; , &amp;&amp;|Indirection (dereference); Address-of; Address-of labels||z = &amp;x; \*z;|6422276; 5|
||(type), sizeof|Cast, Size-of||(int)3.0f; sizeof(x);|3, 4|
|3|\*, /, %|Multiplication, division, and remainder|Left-to-right|6/2 % 2|1|
|4|+, -|Addition and subtraction||1 + 2; 3 - 1|3, 2|
|5|&lt;&lt;,  &gt;&gt;|Bitwise left shift and right shift||4 &lt;&lt; 1; 4 &gt;&gt; 2|8, 1|
|6|&lt;, &lt;=, &gt;, &gt;=|For relational operators &lt;, &gt; and ≤, ≥ respectively||x&lt;y; x&lt;=y; x&gt;y; x&gt;=y|1, 1, 0 ,0|
|7|==, !=|For relational = and ≠ respectively||x == y, x != 1|1, 0|
|8|&amp;|Bitwise AND||7 &amp; 3|3|
|9|^|Bitwise XOR (exclusive or)||255 ^ 0|255|
|10|\||Bitwise OR (inclusive or)||7 \| 3|7|
|11|&amp;&amp;|Logical AND||1 &amp;&amp; 0|0|
|12|\|\||Logical OR||1 \|\| 0|1|
|13|?:|Ternary conditional|Right-to-left|x  = (x &gt; y) ? y : x;|-6|
|14|=|Simple assignment||x  = y;|-6|
||+=, -=, \*=, /=, %=|Assignment by sum, difference, product, quotient, remainder||x+=1; x-=1; //etc.|6, 5|
||&lt;&lt;=, &gt;&gt;=, &amp;=, ^=, \|=|Assignment by bitwise left shift, right shift, AND, XOR, OR||3&lt;&lt;=1, 8&gt;&gt;=2 //etc.|6, 2|
|15|,|Comma|Left-to-right|x = 3, y = 1;|3|

- struct Point { int x; int y; }; int main()<br>{struct Point point = {1,2}, \*ppoint = &amp;point;  int arr\[\] = {1,2}; int x = 5, y =-6; int \* z; float f = 3.0f; /\*code\*/}

<!-- perentysys; esiszewitiwy
Use parentheses to override order of evaluation -->

---

|Priority / Operator||Description|Associativity|Example|Result|
|---|---|---|---|---|---|
|1|(), \[\]|Parentheses; Array subscript|Left-to-right|arr\[0\] \* (x + y)|1|
||.|Structure and union member access||point.x|1|
||-&gt;|Structure and union member access through pointer||ppoint-&gt;x|1|
|2|++, --|Prefix &amp; postfix increment and decrement|Right-to-left|++x; x--; x;|6, 6, 5|
||+, -, !, ~|(Unary) plus and minus; Logical NOT and bitwise NOT||y =-y; y =+y; !x; ~;x|6, -6,0, -6|
||\*, &amp; , &amp;&amp;|Indirection (dereference); Address-of; Address-of labels||z = &amp;x; \*z;|6422276; 5|
||(type), sizeof|Cast, Size-of||(int)3.0f; sizeof(x);|3, 4|
|3|\*, /, %|Multiplication, division, and remainder|Left-to-right|6/2 % 2|1|
|4|+, -|Addition and subtraction||1 + 2; 3 - 1|3, 2|
|5|&lt;&lt;,  &gt;&gt;|Bitwise left shift and right shift||4 &lt;&lt; 1; 4 &gt;&gt; 2|8, 1|
|6|&lt;, &lt;=, &gt;, &gt;=|For relational operators &lt;, &gt; and ≤, ≥ respectively||x&lt;y; x&lt;=y; x&gt;y; x&gt;=y|1, 1, 0 ,0|
|7|==, !=|For relational = and ≠ respectively||x == y, x != 1|1, 0|
|8|&amp;|Bitwise AND||7 &amp; 3|3|
|9|^|Bitwise XOR (exclusive or)||255 ^ 0|255|
|10|\||Bitwise OR (inclusive or)||7 \| 3|7|
|11|&amp;&amp;|Logical AND||1 &amp;&amp; 0|0|
|12|\|\||Logical OR||1 \|\| 0|1|
|13|?:|Ternary conditional|Right-to-left|x  = (x &gt; y) ? y : x;|-6|
|14|=|Simple assignment||x  = y;|-6|
||+=, -=, \*=, /=, %=|Assignment by sum, difference, product, quotient, remainder||x+=1; x-=1; //etc.|6, 5|
||&lt;&lt;=, &gt;&gt;=, &amp;=, ^=, \|=|Assignment by bitwise left shift, right shift, AND, XOR, OR||3&lt;&lt;=1, 8&gt;&gt;=2 //etc.|6, 2|
|15|,|Comma|Left-to-right|x = 3, y = 1;|3|

- struct Point { int x; int y; }; int main()<br>{struct Point point = {1,2}, \*ppoint = &amp;point;  int arr\[\] = {1,2}; int x = 5, y =-6; int \* z; float f = 3.0f; /\*code\*/}

<!-- perentysys; esiszewitiwy
Use parentheses to override order of evaluation -->

---

## A summary

- Structures are user-defined data types that group together variables of different data types. They provide a way to create custom data types tailored to specific needs.
- **Components:** Structures consist of members (or fields), which can be of different data types.
- **Member access:**
  - **Direct:** To access members of a structure directly, use the dot operator (.).
  - **Indirect (through a pointer):** To access members through a pointer, use either:
    - the dereferencing operator (\*) followed by the member access operator (.), enclosed in parentheses: (\*pointer).member,
    - the arrow operator (-&gt;): pointer-&gt;member.
- **Pointers to structures:** You can create pointers to structures, similar to other data types. This allows dynamic memory allocation for structures and passing them as function arguments.
- **Global vs. local variables:** Structures can be declared as global variables (accessible from anywhere in the program) or local variables (accessible only within a specific block of code). You can also create pointers to structures for more flexible memory management.

---

## typedef &amp; struct

Normally, when we define a struct, we can also declare global variables or pointers immediately after the closing brace:

- The variables p1 and ptr are global objects of this structure type.

We can also **omit the structure tag name** to make it **anonymous**, preventing multiple instances from being created:

- Here, config is the **only instance** of this unnamed structure type.

struct Point

{

    int x, y;

} p1, \*ptr;

struct

{

    int id;

    float value;

} config;

---

## typedef &amp; struct

Alternatively, we can use **typedef** to create an **alias** for a structure type:

- Now we can declare variables as Point p1; — no need for the keyword struct.
- The name after the definition (Point) is a type alias, not a variable.
- This alias does not prevent creating multiple instances — it simply simplifies the syntax.

typedef struct

{

    int x, y;

} Point;

Point symbolic\_name;

---

## typedef &amp; struct - Summary

|Form|Description|Example|
|---|---|---|
|struct Tag { ... } var;|Defines type + creates variable|struct Point {int x; int y;} p;|
|struct { ... } var;|Anonymous struct, single instance|struct {int x;} s;|
|typedef struct { ... } Alias;|Creates a reusable type alias|typedef struct {int x;} Point;|

---

# Padding

---

## Padding

- **What is padding in structures?**
  - Padding is extra space (or "padding") that a compiler adds to a structure to align its members on specific memory addresses. This alignment is often done to improve memory access performance, especially for data types like integers and floating-point numbers.
- **Why do compilers add padding?**
  - **Performance:**
    - Most processors are optimized to access memory in chunks (like 4 or 8 bytes). Aligning data on these boundaries can significantly speed up memory access.
  - **Hardware architecture:**
    - Different hardware architectures have specific alignment requirements.

---

## An example - padding

- \#include &lt;stdio.h&gt;
- struct Example1
- {
-     char c;
-     int i;
-     short s;
- };
- struct Example2
- {
-     short s;
-     char c;
-     int i;
- };<br>int main(int argc, char \*argv\[\])
- {
-     printf( "Size of a struct Example is = %d\n", sizeof(struct Example1) );
-     printf( "Size of a struct Example is = %d\n", sizeof(struct Example2) );<br>    struct Example1 example1;
-     printf( "Struct Example1:\n" );
-     printf( "Address of variable c = %d\n", &amp;example1.c );
-     printf( "Address of variable i = %d\n", &amp;example1.i );
-     printf( "Address of variable s = %d\n", &amp;example1.s );
-     struct Example2 example2;
-     printf( "Struct Example2:\n" );
-     printf( "Address of variable s = %d\n", &amp;example2.s );
-     printf( "Address of variable c = %d\n", &amp;example2.c );
-     printf( "Address of variable i = %d\n", &amp;example2.i );
-     return 0;
- }
- Size of a struct Example is = 12
- Size of a struct Example is = 8
- Struct Example1:
- Address of variable c = 6487828
- Address of variable i = 6487832
- Address of variable s = 6487836
- Struct Example2:
- Address of variable s = 6487820
- Address of variable c = 6487822
- Address of variable i = 6487824
- Result:

---

## A summary on padding

- Even though memory was scarce when the C language was invented and every byte was precious, processors were even slower. Every machine instruction that could be saved while maintaining program functionality sped up the program. Therefore, the padding mechanism is a compromise between memory efficiency and program speed. Instead of calculating the memory address and saving one byte, it was better to perform a simple shift trick to make the variable addresses multiples of two. This is because, instead of multiplying (which is a relatively expensive operation for a processor), a bitwise shift can be used, which is extremely cheap. Thus, padding allows for an increase in the required space for storing a structure, but significantly speeds up access to structure members.
- Another important point is that the sizeof() operator does not return the minimum size of the structure, but the actual size after taking into account the padding mechanism. To counteract memory waste, you can change the order of variable declarations in the structure as shown in the example.

---

# Thank you

- Jakub Leszek Pach
- <jpach@mtech.edu>
