---
marp: true
theme: pach
paginate: true
title: "CSCI 112  Programming with C"
---

# CSCI 112<br><br>Programming with C

- Lecture 9
- Dr. Jakub L. Pach
- Fall 2025

---

![w:277px Graphic 3](assets/image2.png)

---

## Outline

- Review
- Const
- Pointers
- Function arguments<br>

---

# Review

---

## Extended example

```c
#include <stdio.h>
int main()
{
    int x = 5;
    int arr1[7] = {9, 8, 7, 6, 5, 4, 3};
    // Dereferencing the address of x to get its value (same as just x)
    printf("Value at address of %-20s = %d\n", "x", *&x);
    // Dereferencing the array name gives the first element's value (arr1[0])
    printf("Value at address of %-20s = %d\n", "arr1 (array name)", *arr1);


    printf("Value at address of %-20s = %d\n", "arr1 (array name)", *arr1+1 );
    printf("Value at address of %-20s = %d\n", "arr1 (array name)", *(arr1+1) );
}
```

```c
Value at address of x                    = 5
Value at address of arr1 (array name)    = 9
Value at address of arr1 (array name)    = 10
Value at address of arr1 (array name)    = 8

```

- Result:
- Priority!!!

---

## Left-to-right &amp; right-to-left associativity

|Priority||Ass.|
|---|---|---|
|1|()|LR|
|2|++, --|RL|
||\*, &amp;||
||(type)||
|3|\*, /, %|LR|
|4|+, -||
|6|&lt;, &lt;=,||
|7|==, !=||
|14|=|RL|
||+=||
|15|,|LR|

```c
int main()
{
  {
    int x = 1, y = 2;
    x += y = 3 + x * y;
    printf("%d\n", x);
  }
  {
    int x = 1, y = 2;
    x += x = y = 3 + x - y;
    printf("%d\n", x);
  }
}
```

```c
6
4


```

- Result:

```c
x += y = 3 + x * y;			/* 2 */
x += y = 3 + 2;				/* 5 */
x += y = 5;				/*y=5*/
x += 5;					/*x=6*/
```

```c
x += x = y = 3 + x - y; 		/* 4 */
x += x = y = 4 - y;			/* 2 */
x += x = y = 2; 			/*y=2*/
x += x = 2; 				/*x=2*/
x += 2; 					/*x=4*/

```

Left-to-right associativity means that when there are two operators with the same priority, the operator on the left is evaluated first. In right-to-left associativity, the opposite is true.

- LR
- RL

---

## Summary for associativity and \*&amp;

- The associativity of the \* and &amp; operators is right-to-left (R–L), similar to assignment, but unlike arithmetic or logical operations, which we’re more familiar with.
- This means that using them together — like in \*&amp;x — works correctly: first, the address of x is obtained, and then the value stored at that address is retrieved.
- You could say that \*&amp; cancels itself out, and logically that’s true. However, it’s a relatively costly operation: instead of directly accessing the value, the program first computes the address from the symbolic name, and then accesses the value from that location.
- The compiler may optimize this during compilation and simplify it to just x, but relying on such optimizations is considered poor practice. It reflects a lack of foundational understanding — similar to blindly trusting automatic type casting.

---

## The Pre-processor

The C Preprocessor runs before the C program is compiled properly. It is a separate program from the compiler programs and, in theory, could be used on any file not just C source files. Its main uses are macro substitution, file inclusion and conditional compilation.

Each source file will normally have a few preprocessor commands, these are, strictly speaking, not part of the C language itself, though they are associated with the language. The preprocessor commands each start with a # and must either fit on a single source line or must be extended with the use of a - at the end of each line to be continued.

eg.: #include&lt;stdio.h&gt;

---

## The C compiler process has four main phases

- **Preprocessing**: The preprocessor modifies the source code by performing:
  - **Macro substitution**
  - **File inclusion**
  - **Conditional compilation**
- **Compilation**: The compiler translates the preprocessed code into assembly code. This phase includes lexical analysis, parsing, and code generation, along with an optional optimization step.
- **Assembly**: The assembler translates the assembly code into machine code to create an object file.
- **Linking**: The linker combines all object files and libraries into a single executable program.

---

## Preprocessor directives - macro substitution

```c
#define symbolic_name replaced_text
Macros are not terminated with semicolons, unlike regular code statements, making them easily distinguishable.



Writing macro-defined constants in uppercase is a best practice to emphasize their immutable nature. While the compiler won't complain, these values cannot be changed during runtime and are not accessible for debugging.
```

```c
#define PI 3.14159
#define some_text "abcde"

#include <stdio.h>

int main()
{
    printf( "%s\n", some_text );
    printf( "%f\n", PI + 0.5f );
}
```

```c
abcde
3.641590
```

- Result:

```c
#define PI 3.14159
#define some_text "abcde"

#include <stdio.h>

int main()
{
    printf( "%s\n", "abcde" );
    printf( "%f\n", 3.14159 + 0.5f );
}
```

---

## Preprocessor directives - macro substitution

```c
#define symbolic_name replaced_text
```

- Macros are not terminated with semicolons, unlike regular code statements, making them easily distinguishable.

```c
#define square(y) (y * y)
#define merge(left, right) left ## right
#define some_text "abcde"

#include <stdio.h>

int main()
{
    char * word1 = "Hello";
    char * word2 = "world";
    int x = 5;
    printf( "%s\n", some_text );
    printf( "%d\n", square(x) );
    printf( "%s\n", merge(word, 1) );
}
```

```c
abcde
25
Hello
```

- Result:

```c
#include <stdio.h>
int main()
{
    char * word1 = "Hello";
    char * word2 = "world";
    int x = 5;
    printf( "%s\n", "abcde" );
    printf( "%d\n", (x * x) );
    printf( "%s\n", word1 );
}
```

---

## Preprocessor directives - macro substitution

```c
#define symbolic_name replaced_text
```

- Macros are not terminated with semicolons, unlike regular code statements, making them easily distinguishable.

```c
#define min(a, b) ( (a) < (b) ? (a) : (b) )

#include <stdio.h>

int main()
{
    printf("%s\n", min("abc", "cde"));
    printf("%s\n", min("aac", “aab"));

}
```

```c
cde
aab

```

- Result:

```c
#include <stdio.h>
int main()
{
    printf("%s\n", ( ("abc") < ("cde") ? ("abc") : ("cde") ));
    printf("%s\n", ( ("aac") < ("aab") ? ("aac") : ("aab") ));
}
```

- It works because it's a ternary operator!

---

## Conditional compilation

```c
#if (conditional1)
	statement1;
#elif (conditional2)
	statement2;
#else
	statement3;
#endif
```

```c
#include <stdio.h>
#define DEBUG 1
#define n 10

int main()
{
    int arr[n];
    int i;
    for (i = 0; i < n; i++)
    {
        arr[i] = rand() % 100;
        #if (DEBUG)   /* wiersz z if */
            printf("A value of arr[%d] =  %d\n", i, arr[i]);
        #endif
    }

    return 0;
}
```

```c
A value of arr[0] =  41
A value of arr[1] =  67
A value of arr[2] =  34
A value of arr[3] =  0
A value of arr[4] =  69
A value of arr[5] =  24
A value of arr[6] =  78
A value of arr[7] =  58
A value of arr[8] =  62
A value of arr[9] =  64

```

- Result:

---

## Built-in constants in C - examples

\_\_FILE\_\_    name of the file being compiled

\_\_DATE\_\_    file compilation date

\_\_TIME\_\_    file compilation time

```c
#include <stdio.h>

int main()
{
    printf("%s", __TIME__);
    printf("%s", __FILE__);
    printf("%s", __DATE__);
}
```

```c
11:24:35
C:\Users\Jakub\Desktop\CSCI112\main.c
Sep 26 2024
```

- Result:

---

## File inclusion

```c
Using <> (angle brackets)	–	e.g. #include <file_name.h>
Using "" (double quotes)	–	e.g. #include "file_name.h"

```

---

## Summary: How the C Preprocessor Works

- The preprocessor works like a “Find and Replace” tool in a text editor — it searches for specific strings (like constant names) and **replaces them with defined values** before the actual compilation begins. This means you cannot debug constants or change their values during runtime, because the source code has already been transformed — as if you manually replaced every occurrence of the name with its value.
- **Conditional compilation** allows the program to check whether a constant has been defined (#ifdef, #ifndef) and **include or skip parts of the code** accordingly. This is useful for writing code that adapts to different configurations, platforms, or versions.

---

# Buffered input

---

## Fundamental Functions for Input and Output

- Data Output for Screen:
  - putchar\*    -    (put\[ \]char\[acter\]):    Displays a single character on the screen.
  - printf    -    (print\[\]f\[ormatted\]):    Displays a formatted string of characters.
- Data Input from Keyboard:
  - getchar\*    -    (get\[ \]char\[acter\]):    Retrieves a single character from the keyboard.
  - scanf    -    (scan\[ \]f\[ormatted):    Reads a formatted string of characters from the keyboard.
- C doesn't handle input/output on its own. You need a library called &lt;stdio.h&gt;.
- \*You can use putchar and getchar like normal functions,
- but they are not standard C functions but rather preprocessor macros.

<!-- \*#include &lt;stdio.h&gt; -->

---

## Getchar() &amp; scanf()

- Using getche() allows you to read a character from the keyboard **without waiting for the Enter key**. This has consequences: without more advanced logic, the user cannot correct mistakes. For example, pressing Backspace doesn't erase the previous character — it's just another ASCII code. To handle this properly, you'd need to implement logic that detects Backspace and reverts the previous input.
- To simplify user interaction, the system uses an **input buffer**. Keystrokes are stored in this buffer before being passed to the program. This solves some problems, but introduces others: when waiting for Enter to confirm input, remember that Enter is actually **two ASCII characters** — CR (Carriage Return, 13) and LF (Line Feed, 10). As a result, one of these characters may remain in the buffer, causing the next call to getchar() or scanf() to behave incorrectly — it might read leftover input.

---

## Getchar() &amp; scanf()

- To avoid this, you should **clear the input buffer** before reading new data. Since standard functions don’t do this automatically, the simplest solution is to define a macro:

\#define clearBuffer() while (getchar() != '\n’);

- and call clearBuffer() after each keyboard input operation.

---

## Basics of

- The important difference between printf and scanf is that scanf requires its arguments to be location in memory.
- The ampersand operator &amp; is a unary operator that returns the memory address, which is the location in memory where a variable is stored.

```c
int main()
{
  int x = 5;          			/* Declaration of variable x and assigning its value 5 */
  printf("Enter x value : "); 		/* there is no end of line character here! */
  scanf("%d", &x);     			/* To get a pointer (memory address) */
  printf("Value of x = %d\n", x); 	/* we use a & before the variable name p */
}
```

```c
Enter x value : 1
Value of x = 1
```

- Result:

```c
int printf (char format[],  arg1,  arg2 ,...);
```

```c
int scanf  (char format[], *arg1, *arg2 ,...);
```

---

## Basics of

- The important difference between printf and scanf is that scanf requires its arguments to be location in memory.
- The ampersand operator &amp; is a unary operator that returns the memory address, which is the location in memory where a variable is stored.

```c
int main()
{
  int x = 5;          			/* Declaration of variable x and assigning its value 5 */
  printf("Enter x value : "); 		/* there is no end of line character here! */
  scanf("%d", &x);     			/* To get a pointer (memory address) */
  while (getchar() != '\n’);
  printf("Value of x = %d\n", x); 	/* we use a & before the variable name p */
}
```

```c
Enter x value : 1
Value of x = 1
```

- Result:

```c
int printf (char format[],  arg1,  arg2 ,...);
```

```c
int scanf  (char format[], *arg1, *arg2 ,...);
```

---

# Keyword const

---

## const keyword

- We can use const before declaration (and initialization):
  - Array:    Prevents changing the content of the array.
  - Variable:    Prevents changing its value.
  - Pointer:
    - Before the asterisk(\*):    Prevents changing the value it points to.
    - After the asterisk(\*):    Prevents changing the pointer itself.

<!-- (this will be important when we talk about preprocessor constants). -->

---

## const keyword

- const prevents changing the value after its initialization, but it allows debugging.
- In a function definition, const allows control over changing the argument values.
- The compiler ensures the immutability of constants. It will not compile the file if you try to change their value. However, attempting to bypass the restriction (e.g., using a pointer) will always result in incorrect program behavior without informing the programmer.

<!-- (this will be important when we talk about preprocessor constants). -->

---

## Huge problems… undefined behavior

- Do not increment (decrement) a variable in an expression if you need to use the original value of the variable later!

```c
int main()
{
  {
    int x = 1, y;
    y = x + 2 + ++x;
    printf("%d\n", y);
  }
  {
    int x = 1, y;
    y = x + ++x;
    printf("%d\n", y);
  }
}
```

```c
5
4


```

- Result:
- When modifying and using a variable multiple times within the same expression, it may lead to undefined behavior!

---

## printf and scanf format specification

- Optional:
  - Flags    -    modifiers that alter the formatting or scanning behavior.
  - Width    -    specifies the minimum width of the output field <br>        or the maximum number of characters to be scanned.
  - Precision    -    controls the precision of floating-point numbers <br>        or the maximum number of characters to be scanned for strings.
  - Modifier    -    indicates the data type size (e.g., long, short).
- Required:
  - Type    -    specifies the data type of the variable to be formatted or scanned.

```c
Format =  %[flags][width][.precision][modifier]<type>
```

---

## Basic types

|Type &amp; Specifier||Origin|Argument type||Description||
|---|---|---|---|---|---|---|
||||**printf**|**scanf**|**printf**|**scanf**|
|integer|d|decimal|int|int \*|signed decimal notation||
||u|unsigned decimal|int|unsigned int \*|unsigned decimal notation||
||c|character|int|char \*|one unsigned character||
|string|s|string|char \*|char \*|characters from the string are printed until a ‘\0’!|string **of non-white space**; at the end will be added ‘\0’!|
|floating-point number|f|float|float|float \*|single precision floating-point number notation||
||lf|long float <br>(double)|double|double \*|double precision floating-point number notation||

<!-- Każdy lancuch znakowy w C jest o jeden większy od deklarowanej treści, bo na końcu jest jeszcze dopisywany znak końca \0 -->

---

## Width

```c
int main()
{ int x = 5, y = -6; int * z; float f = 3.1234f; /*code*/ }
```

|Data|Type||Description|Example|Result|
|---|---|---|---|---|---|
|Numbers|integer|d|The width value for number (text) representation reserves at least as many characters as are needed to represent that number(text) in ASCII characters (digits). <br>If the width is smaller than the number’s (text’s) representation, the entire number (text) will be displayed. <br>If the width is greater than the number’s (text’s)  representation, extra spaces will be added on the left side.|printf("%1d\n", y);<br>printf("%4d\n", y);|-6<br>   -6|
|||u||||
|||c||printf("%c\n", letter);<br>printf("%1c\n", letter);|a|
||floating-point number|f||printf("%3f\n", fRealNumber);<br>printf("%9f\n", fRealNumber);|3.123400<br> 3.123400|
|||lf||||
|Text|string|s||printf("%3s\n", text);<br>printf("%10s\n", text);|Some Text<br> Some Text|

---

## Precision

```c
int main()
{ int x = 5, y = -6; int * z; float f = 3.1234f; /*code*/ }
```

|Data|Type||Description|Example|Result|
|---|---|---|---|---|---|
|Numbers|integer|d|precision works the same as width — it reserves a minimum field size. If the precision is greater than the ASCII character representation of the number, leading zeros are added to the left. Precision does not truncate the number! It always displays the full value.|printf("%.1d\n", x); <br>printf("%.5d\n", x);|65<br>00065|
|||u||||
|||c||||
||floating-point number|f|precision determines the number of digits after the decimal point that are displayed. If the number has more decimal places than specified by the precision, it will be truncated.|printf("%.6f\n", fRealNumber); <br>printf("%.2f\n", fRealNumber);<br>printf("%.0f\n", fRealNumber);|3.123400<br>3.12<br>3|
|||lf||||
|Text|string|s|precision determines the precise number of characters to be extracted from the string. Any characters beyond the specified precision will be discarded.|printf("%.1s\n", text);<br>printf("%.5s\n", text);<br>printf("%.20s\n", text);|S<br>Some<br>Some Text|

---

## Flags

- \+ : Always display the sign of a number, even if it's positive.
- \- : Left-justify the output within the given field width.
- 0 : Pad the field with zeros instead of spaces.
- \# : Use an alternative form for the conversion specifier.

<!-- **# flag:** Use an alternative form for the conversion specifier. For example, it adds a leading zero for octal numbers or a 0x or 0X prefix for hexadecimal numbers. -->

---

## Modifies

```c
int main()
{ short int x = 65;  int y = -69000;
  float fRealNumber = 3.1234f; double dRealNumber = 3.4e50; /*code*/ }
```

|Data|Type||Description|Example|Result|
|---|---|---|---|---|---|
|Numbers|integer|d|Modifier, h and l specify how many bytes should be formatted as a variable. Therefore, if we use short (h - 2 bytes) on a normal int (long - 32 bit), we will get an incorrect result because printf will take only 16 bits and build a number representation from it.|printf("%0hd\n", x);<br>printf("%0hd\n", y);<br>printf("%0ld\n", x);<br>printf("%0ld\n", y);|65<br>-3464<br>65<br>-69000|
|||u||||
|||c||||
||floating-point number|f|Since there's no such thing as hf (as hf is simply f), the compiler ignores h, and l represents a double. As you can see, there's no lf type, only f with the l modifier.|printf("%0hf\n", fRealNumber);<br>printf("%0lf\n", fRealNumber);<br>printf("%0hf\n", dRealNumber);<br>printf("%0lf\n", dRealNumber);|3.123400<br>3.123400<br>33999999...<br>339999999999999984402842591433794782958910267457536.000000|
|||lf||||
|Text|string|s|None|None|None|

---

## Declaring and initializing arrays

```c
int main()
{
  int a[5];
  /* Declare an integer array named a with 5 elements */
  int b[] = {1, 2, 3, 4};
  /*Declare an integer array named b with 4 elements,
    initialized with values 1, 2, 3, and 4            */
  int c[10] = {9, 8, 7, 6, 5};
  /*Declare an integer array named c with 10 elements,
    the first 5 elements are initialized with values 9, 8, 7, 6, and 5,
    the remaining elements are initialized to 0       		  */
  int d[100] = {0};
  /*Declare an integer array named d with 100 elements, all initialized to 0*/
  int x, y = 2;
  printf("First element (index 0) of array a equals %d.\n", a[0]);
  /*Print the value of the first element of array a(undefined value)*/
  printf("Second(index 1) element of array b equals %d.\n", b[1]);
  /*Print the value of the second element of array b (which is 2)*/
  printf("Second(index 1) element of array b equals %d.\n", *(b+1) );
  /*Print the value of the second element of array b using pointer arithmetic*/
  printf("Sixth(index 5) element of array c equals %d.\n", c[5]);
}
```

```c
First element (index 0) of array a equals 4201200.
Second(index 1) element of array b equals 2.
Second(index 1) element of array b equals 2.
Sixth(index 5) element of array c equals 0.
```

- Result:

---

|Type &amp; Specifier||Origin|Argument type||Description||
|---|---|---|---|---|---|---|
||||**printf**|**scanf**|**printf**|**scanf**|
|integer|d|decimal|int|int \*|signed decimal notation||
||u|unsigned decimal|int|unsigned int \*|unsigned decimal notation||
||c|character|int|char \*|one unsigned character|characters are placed within the indicated memory if the specified width is greater than 1; Without ‘\0’|
||i|integer|int|int \*|signed decimal notation (also accepts octal and hexadecimal)||
||o|octal|int|int \*|octal notation (with leading 0)||
||x, X|hex|int|int \*|hexadecimal notation (with or without leading 0x or 0X)||
|string|s|string|char \*|char \*|characters from the string are printed until a ‘\0’!|string **of non-white space**; at the end will be added ‘\0’|
||\[…\]|specific string|N/A|char \*|N/A|Matches the longest non-empty string input characters from the set between brackets; A ‘\0’ is added.|
||\[^…\]|negated specific string|N/A|char \*|N/A|as above, but only excluding the characters|
|floating-point number|f|float|float|float \*|single precision floating-point number notation||
||lf|long float <br>(double)|double|double \*|double precision floating-point number notation||
||e, E|engineer notation|double|float \*<br>double \*|scientific notation (single or double precision floating-point number)||
||g, G|general floating-point representation|float double|float \*<br>double \*|scientific notation (single or double precision floating-point number) <br>or single or double precision floating-point number||
|pointer|p|pointer|(any)  void \*|N/A|integer value of the pointer|N/A|
|special|n|number of input characters|N/A|int \*|N/A|Writes into the argument the number of characters read so far by this call|
||%|literal %|%|N/A|Prints a literal percent sign (%)|N/A|

<!-- To know something like the back of one's hand. – miec to w malym palcu
To be able to explain something in their sleep – odpowiedziec o 4 and ranem -->

---

# Pointers

---

## Pointers

- Pointers are treated as first-class data types;
- We can create a pointer to **any** data type (also void) using the \* operator between the existing data type and the symbolic name;
- Unary operator &amp; returns memory locations;
- A pointer can reference to anything that has a memory address (anything with a symbolic name), such as:
  - variables,
  - arrays,
  - labels,
  - functions.

---

## Summary - The \* operator works in **three different ways**

- **Binary multiplication operator**

a \* b;  // multiplies a and b

- **Unary dereference operator** – used to access the value stored at a given memory address:

int x = 5;

int \* y =&amp;x;

y = \*ptr + 1;

- **Pointer declaration**

– when used in a declaration, it indicates that the variable is a pointer, not a simple type:

int \* x;  // x is a pointer to an int

This applies to **local variables, global variables, and function parameters** (including arrays).

**Remember**: It’s easy to confuse the **unary dereference operator** \* with the **pointer declaration** \* in a variable definition!

---

## Some examples

```c
int main()
{
  int x = 5, y = 7;
  int * p = &x;
  printf("y equals %d.\n\n",  y );

  printf("&y\t\tequals %d.\n", &y );
  printf("*(&y)\t\tequals %d.\n", *(&y) );
  printf("&(*(&y))\tequals %d.\n", &(*(&y)) );
  printf("&*&y\t\tequals %d.\n", &*&y );
  printf("*&*&y\t\tequals %d.\n\n", *&*&y );

  printf("&x\t\tequals %d.\n", &x );
  printf("p\t\tequals %d.\n", p );
  printf("&p\t\tequals %d.\n", &p );
  printf("*p\t\tequals %d.\n\n", *p );

  return 0;
}
```

```c
y equals 7.

&y              equals 6422292.
*(&y)           equals 7.
&(*(&y))        equals 6422292.
&*&y            equals 6422292.
*&*&y           equals 7.

&x              equals 6422296.
p               equals 6422296.
&p              equals 6422288.
*p              equals 5.

```

- Result:

||Memory Addresses and Values|||
|---|---|---|---|
|||||
||x (6422296)|5||
|||||
||y (6422292)|7||
|||||
||p (6422288)|6422296||
|||||

![Ink 58](assets/image110.png)

![Ink 59](assets/image120.png)

![Ink 60](assets/image130.png)

---

## Consequences

- Each variable declared has a lower address\*. This is due to the computer's memory architecture. The stack grows downward, so when it's empty, the address is at its maximum value (e.g., FFFFFF). Every time a value is pushed onto the stack, the address is decremented by the size of the data type.
- The \* and &amp; operators are right-associative, so parentheses are not strictly necessary.
- The \* and &amp; operators cancel each other out, meaning that \*&amp;y is equivalent to y.
- Arithmetic operations on pointers differ from those on integer types.
- Pointers to pointers are declared using a double asterisk (\*\*), every extra asterisk means another layer of pointers…
- \*Array elements have the opposite effect!

---

# Function arguments

---

## Function arguments Function arguments are always **copies** of our variables, and **not** the same memory areas, a function argument, even though it has the same value, is a completely different variable!

---

## by the Value

- Function arguments are always **copies** of our variables, and **not** the same memory areas, a function argument, even though it has the same value, is a completely different variable!

```c
5
5

```

- Result:

```c
#include <stdio.h>

void byTheValue(int);

void byTheValue(int x)
{
    x++;
    return;
}

int main()
{
    int x = 5;
    printf("%d\n", x);
    byTheValue(x);
    printf("%d\n", x);
  return 0;
}
```

---

## by the Value

- Function arguments are always **copies** of our variables, and **not** the same memory areas, a function argument, even though it has the same value, is a completely different variable!

```c
5
5

```

- Result:

```c
#include <stdio.h>

void byTheValue(int);

void byTheValue(int value)
{
    value++;
    return;
}

int main()
{
    int x = 5;
    printf("%d\n", x);
    byTheValue(x);
    printf("%d\n", x);
  return 0;
}
```

---

## by the Reference

- Function arguments are always **copies** of our variables, and **not** the same memory areas, a function argument, even though it has the same value, is a completely different variable!

```c
5
6

```

- Result:

```c
#include <stdio.h>

void byTheReference(int*);

void byTheReference(int* ref)
{
    (*ref)++;
    return;
}

int main()
{
    int x = 5;
    printf("%d\n", x);
    byTheReference(&x);
    printf("%d\n", x);
  return 0;
}
```

---

# Relations between pointers and arrays

---

## Relations between pointers and arrays

- int a\[10\];

This statement reserves space in memory for 10 integers and creates an 'unchanging address of memory' that points to the beginning of this array.

```c
int main()
{
  int a[] = {1, 2, 3, 4, 5, 6, 7};
  printf("%-4s equals %d.\n", "a", a);
  /*a equals'unchanging address of memory’*/
  return 0;
}
```

```c
a    equals 6422272.


```

- Result:

![Ink 17](assets/image140.png)

![Ink 18](assets/image150.png)

---

## Relations between pointers and arrays

```c
int main()
{
  int a[] = {1, 2, 3, 4, 5, 6, 7};
  printf("%-4s equals %d.\n","a", a);
  printf("%-4s equals %d.\n","&a", &a);
  printf("%-4s equals %d.\n","*a", *a);
  return 0;
}
```

```c
a    equals 6422272.
?
```

- Result:

---

## Relations between pointers and arrays

```c
int main()
{
  int a[] = {1, 2, 3, 4, 5, 6, 7};
  printf("%-4s equals %d.\n","a", a);
  printf("%-4s equals %d.\n","&a", &a);
  printf("%-4s equals %d.\n","*a", *a);
  return 0;
}
```

```c
a    equals 6422272.
&a   equals 6422272.
?
```

- Result:

---

## Relations between pointers and arrays

```c
int main()
{
  int a[] = {1, 2, 3, 4, 5, 6, 7};
  printf("%-4s equals %d.\n","a", a);
  printf("%-4s equals %d.\n","&a", &a);
  printf("%-4s equals %d.\n","*a", *a);
  return 0;
}
```

```c
a    equals 6422272.
&a   equals 6422272.
*a   equals 1.
```

- Result:

---

## Relations between pointers and arrays **So, what does it mean?**

```c
int main()
{
  int x = 5, y = 7, z = 9;
  int * pointer = &y;
  printf("%-4s equals %d.\n", "x", &x);
  printf("%-4s equals %d.\n", "y", &y);
  printf("%-4s equals %d.\n", "z", &z);
  printf("%-4s equals %d.\n", "pointer", pointer);
  printf("%-4s equals %d.\n", "pointer*", *pointer);
  printf("%-4s equals %d.\n", "pointer[1]", pointer[1]);
  return 0;
}
```

```c
x    equals 6422292.
y    equals 6422288.
z    equals 6422284.
pointer equals 6422288.
pointer* equals 7.
pointer[1] equals 5.
```

- Result:

---

## So, what does it mean?

```c
int a[10];

a[i] == *(a+i)		&a[i] == &*(a+i) == a+i
```

When performing arithmetic operations on pointers, the array index is automatically multiplied by the size of the data type pointed to by the pointer.

For example, if the array stores char values, the index is multiplied by 1, and if it stores int values, the index is multiplied by 4 (assuming an int is 4 bytes).

---

## Conclusions

- The expression a\[i\] is transformed by the compiler into the form \*(a+i).
- The square brackets following the symbolic\_name do not provide any information about whether we are referring to an array.
- When performing arithmetic operations on pointers, the array index is automatically multiplied by the size of the data type pointed to by the pointer.

<!-- define s\[n\] na \*(s + n) -->

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

```c
struct Point { int x; int y; }; int main()
{struct Point point = {1,2}, *ppoint = &point;  int arr[] = {1,2}; int x = 5, y =-6; int * z; float f = 3.0f; /*code*/}
```

<!-- perentysys; esiszewitiwy
Use parentheses to override order of evaluation -->

---

## Conclusions

Square brackets are often mistakenly interpreted as an indication that we are working with arrays. However, this is incorrect. Square brackets are actually the highest-priority operator, designed to simplify expressions like \*(a + i) into a\[i\], which is faster. Of course, square brackets also serve a dual purpose: they are used both for array declarations and for accessing array elements.

<!-- define s\[n\] na \*(s + n) -->

---

## const keyword in Array &amp; Pointer

- We can use const before declaration (and initialization):
  - Array: Prevents changing the content of the array.
  - Pointer:
    - Before the asterisk(\*):    Prevents changing the value it points to.
    - After the asterisk(\*):    Prevents changing the pointer itself.
- The compiler ensures the immutability of constants. It will not compile the file if you try to change their value. However, attempting to bypass the restriction (e.g., using a pointer) will always result in incorrect program behavior without informing the programmer.

<!-- (this will be important when we talk about preprocessor constants). -->

---

## const keyword in Pointer

```c
int main()
{
  int x = 5, y = 7, z = 9;
  int const * const pointerX = &x; /* Both the pointer and the pointed-to value are constant */
  /* pointerX = &y; WRONG! */
  /* *pointerX = 1; WRONG! */
  int const *  pointerY = &y; /* The pointed-to value is constant, but the pointer can be reassigned */
  /* *pointerY = 1; WRONG! */
  pointerY = &z;
  int  * const pointerZ = &z; /* The pointer is constant, but the pointed-to value can be changed */
  *pointerZ = 1;
  /* pointerZ = &x; WRONG! */
  printf("x = %d, y = %d, z = %d\n", x, y, z );
  return 0;
}
```

```c
x = 5, y = 7, z = 1


```

- Result:

---

## const keyword in Array

```c
#include <stdio.h>
int main()
{
  int const a[] = {1, 2, 3, 4, 5, 6, 7};
  /* a[1]=a[0]; WRONG! */
  return 0;
}
```

- The most similar thing to the symbolic\_name of an array in C is a pointer with the const keyword placed **after** the asterisk, as this prevents changes to what the pointer points to.
- However, it is important to remember that there is still a small difference. Specifically, the &amp; operator on a static pointer will return the address of the pointer itself, whereas for the symbolic\_name of an array, it will return the address of the first element.

---

## Conclusions

There are no restrictions on passing an array as a function parameter. However, there's a common misconception: when we write int arr\[\], it may seem like the entire array is copied and we get access to an identical copy. This is not true. The square bracket syntax is primarily a hint for the programmer, as the compiler internally treats it as int const \*arr.

```c
1
2
3
4
5
6
7

```

- Result:

```c
#include <stdio.h>
void byTheReference(int arr[], int n);
void byTheReference(int arr[], int n)
{
    for (int i = 0; i < n; i++)
        printf("%d\n", arr[i]);
}
int main()
{
    int a[] = {1, 2, 3, 4, 5, 6, 7};
    byTheReference(a, 7);

    getchar();
    return 0; //return r
}
```

```c
#include <stdio.h>

void byTheReference(int const * arr, int n);
void byTheReference(int const * arr, int n)
{
    for (int i = 0; i < n; i++)
        printf("%d\n", arr[i]);
}
```

<!-- define s\[n\] na \*(s + n) -->

---

# Thank you

- Jakub Leszek Pach
- <jpach@mtech.edu>

---

## Some examples

```c
int main()
{
  int x = 5, y = 7;
  int * p = &x;
  int ** pp = &p;   /* pointer to pointer*/
  y = **pp;
  printf("y equals %d.\n\n",  y );

  printf("&y\t\tequals %d.\n", &y );
  printf("*(&y)\t\tequals %d.\n", *(&y) );
  printf("&(*(&y))\tequals %d.\n", &(*(&y)) );
  printf("&*&y\t\tequals %d.\n", &*&y );
  printf("*&*&y\t\tequals %d.\n\n", *&*&y );

  printf("&x\t\tequals %d.\n", &x );
  printf("p\t\tequals %d.\n", p );
  printf("&p\t\tequals %d.\n", &p );
  printf("*p\t\tequals %d.\n\n", *p );

  printf("pp\t\tequals %d.\n", pp );
  printf("&pp\t\tequals %d.\n", &pp );
  printf("*pp\t\tequals %d.\n", *pp );
  printf("*&*pp\t\tequals %d.\n", *&*pp );
  printf("**pp\t\tequals %d.\n", **pp );
  return 0;
}
```

```c
y equals 5.

&y              equals 6422292.
*(&y)           equals 7.
&(*(&y))        equals 6422292.
&*&y            equals 6422292.
*&*&y           equals 7.

&x              equals 6422296.
p               equals 6422296.
&p              equals 6422288.
*p              equals 5.

pp              equals 6422288.
&pp             equals 6422284.
*pp             equals 6422296.
*&*pp           equals 6422296.
**pp            equals 5.
```

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

## The valid pointer operations are

- Assignment of pointers to the same type,
- Adding or subtracting a pointer and an integer,
- Subtracting or comparing\* two pointers,
- Assigning or comparing to zero (NULL = ‘\0’),
- All other pointer arithmetic is illegal (+, \*, /, &gt;&gt;, &lt;&lt;, etc.).
