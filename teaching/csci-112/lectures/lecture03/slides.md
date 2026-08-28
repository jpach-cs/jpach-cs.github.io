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

- Lecture 3
- Dr. Jakub L. Pach
- Fall 2025

---

# Outline

- Review
- Operators:
  - Unary, Binary, Ternary
  - Relational & logical
- Statements & expressions
- Block

---

# Review

---

<!-- _class: compact fit-80 -->

# Symbolic names will be used in:

- Variables:    Symbolic names will be used to identify and refer to data stored in variables. This<br>    allows for more meaningful and descriptive code compared to using arbitrary names or <br>    identifiers.
- Arrays:     Symbolic names will be used to identify collections of related data elements. Arrays can be used <br>    to store multiple values of the same data type.
- Functions:    Symbolic names will be used to identify and call functions within the program. This helps in <br>    organizing and structuring the code, making it easier to understand and maintain.
- Labels\*:    Symbolic names will be used to mark specific locations or points within the program code. <br>    These labels can be used for various purposes, such as control flow statements, data references, <br>    or error handling.
- \*In Python we don’t have labels.

---

# Arrays

This statement reserves space in memory for 10 integers and creates an 'unchanging address of memory' that points to the beginning of this array\*. You can use this symbolic name to access individual elements of the array using square brackets and the appropriate index.

The values of array will be undefined, meaning they can hold any random value.

```c
int a[10];
```

\*Array indexing starts from 0.

---

<!-- _class: compact fit-80 -->

# Arrays

- When you specify the size of an array in square brackets, it is created with that exact size.
- If you omit the size but provide initial values, the compiler counts them and creates an array of that size.
- If you specify the size but don't initialize all elements, the remaining ones will have indeterminate, unpredictable values.

```c
<type> symbolic_name[size];
```

```c
<type> symbolic_name[] = {value1, value2, value3};
<type> symbolic_name[size] = {value1, value2};
```

---

# Example of an array

```c
int main()
{
    char string0[12] = "Hello world";
    char string1[]   = "Hello world";
    char string2[12] = { 72, 101, 108 ,108, 111, 32, 87, 111, 114, 108, 100, 0 };
    char string3[]   = { 72, 101, 108 ,108, 111, 32, 87, 111, 114, 108, 100, 0 };
    char string4[12] = { 'H', 'e', 'l' , 'l', 'o', ' ', 'w', 'o', 'r', 'l', 'd', '\0' };
    char string5[]   = { 'H', 'e', 'l' , 'l', 'o', ' ', 'w', 'o', 'r', 'l', 'd', '\0’ };
    char string6[12]   = { 'H', 101, 'l' , 108, 'o', ' ', 'w', 'o', 'r', 'l', 'd’, 0 };
    printf("%s\n", string0);
    printf("%s\n", string1);
    printf("%s\n", string2);
    printf("%s\n", string3);
    printf("%s\n", string4);
    printf("%s\n", string5);
    printf("%s\n", string6);
    return 0;
}
```

Result:

```text
Hello World
Hello World
Hello World
Hello World
Hello World
Hello World
Hello World
```

---

<!-- _class: compact fit-80 -->

# Arrays

- When you specify the size of an array in square brackets, it is created with that exact size.
- If you omit the size but provide initial values, the compiler counts them and creates an array of that size.
- If you specify the size but don't initialize all elements, the remaining ones will have indeterminate, unpredictable values.

```c
<type> symbolic_name[size];
```

```c
<type> symbolic_name[] = {value1, value2, value3};
<type> symbolic_name[size] = {value1, value2};
```

---

# Question: How do we know which letter goes with which number?

```c
int main()
{
  char text[] = { 72, 101, 108 ,108, 111, 32, 87, 111, 114, 108, 100, 10, 13, 0 };
  printf("%s", text);
  return 0;
}
```

Result:

```text
Hello World
```

---

# ASCII Table

American Standard Code for Information Interchange

- is the most common character encoding format for text data in computers and on the Internet. In standard ASCII-encoded data, there are unique values for 128 alphabetic, numeric or special additional characters and control codes.
- \0 equals 0 (NULL)
- \n equals 10, 13 (n\ + \r)
- \t equals 11
- White\_Space equals 32

```text
 Val Char                            Val  Char     Val  Char     Val  Char
---------                            ---------     ---------     ----------
  0  NUL (null)                      32  SPACE     64  @         96  `
  1  SOH (start of heading)          33  !         65  A         97  a
  2  STX (start of text)             34  "         66  B         98  b
  3  ETX (end of text)               35  #         67  C         99  c
  4  EOT (end of transmission)       36  $         68  D        100  d
  5  ENQ (enquiry)                   37  %         69  E        101  e
  6  ACK (acknowledge)               38  &         70  F        102  f
  7  BEL (bell)                      39  '         71  G        103  g
  8  BS  (backspace)                 40  (         72  H        104  h
  9  TAB (horizontal tab)            41  )         73  I        105  i
 10  LF  (NL line feed, new line)    42  *         74  J        106  j
 11  VT  (vertical tab)              43  +         75  K        107  k
 12  FF  (NP form feed, new page)    44  ,         76  L        108  l
 13  CR  (carriage return)           45  -         77  M        109  m
 14  SO  (shift out)                 46  .         78  N        110  n
 15  SI  (shift in)                  47  /         79  O        111  o
 16  DLE (data link escape)          48  0         80  P        112  p
 17  DC1 (device control 1)          49  1         81  Q        113  q
 18  DC2 (device control 2)          50  2         82  R        114  r
 19  DC3 (device control 3)          51  3         83  S        115  s
 20  DC4 (device control 4)          52  4         84  T        116  t
 21  NAK (negative acknowledge)      53  5         85  U        117  u
 22  SYN (synchronous idle)          54  6         86  V        118  v
 23  ETB (end of trans. block)       55  7         87  W        119  w
 24  CAN (cancel)                    56  8         88  X        120  x
 25  EM  (end of medium)             57  9         89  Y        121  y
 26  SUB (substitute)                58  :         90  Z        122  z
 27  ESC (escape)                    59  ;         91  [        123  {
 28  FS  (file separator)            60  <         92  \        124  |
 29  GS  (group separator)           61  =         93  ]        125  }
 30  RS  (record separator)          62  >         94  ^        126  ~
 31  US  (unit separator)            63  ?         95  _        127  DEL
```

<!-- ASCII: abbreviated from American Standard Code for Information Interchange, is a character encoding standard for electronic communication. ASCII codes represent text in computers, telecommunications equipment, and other devices. Because of technical limitations of computer systems at the time it was invented, ASCII has just 128 code points, of which only 95 are printable characters, which severely limited its scope. Modern computer systems have evolved to use Unicode, which has millions of code points, but the first 128 of these are the same as the ASCII set.
'5' has the int value 53 if we write '5'-'0' it evaluates to 53-48, or the int 5 if we write char c = 'B'+32; then c stores 'b' -->

---

# Multi-dimensional arrays

- One dimension:
- Two dimensions:
- Three dimensions:
- etc.

```c
<type> symbolic_name[size];
```

```c
<type> symbolic_name[size1][size2];
```

```c
<type> symbolic_name[size1][size2][size3];
```

---

# Basic operators

|Priority / Operator||Description|Associativity|Example|Result|
|---|---|---|---|---|---|
|1|()|Parentheses|Left-to-right|2 \* (x + y)|-2|
|2|++, --|Prefix & postfix increment and decrement|Right-to-left|++x; x--; x;|6, 6, 5|
||\*, &|Indirection (dereference); Address-of||z = &x; \*z;|6422276; 5|
||(type)|Cast||(int)3.0f|3|
|3|\*, /, %|Multiplication, division, and remainder|Left-to-right|6/2 % 2|1|
|4|+, -|Addition and subtraction||1 + 2; 3 - 1|3, 2|
|6|&lt;, &lt;=, &gt;, &gt;=|For relational operators &lt;, &gt; and ≤, ≥ respectively||x&lt;y; x&lt;=y; x&gt;y; x&gt;=y|1, 1, 0 ,0|
|7|==, !=|For relational = and ≠ respectively||x == y, x != 1|1, 0|
|11|&&|Logical AND||1 && 0|0|
|12|\|\||Logical OR||1 \|\| 0|1|
|14|=|Simple assignment|Right-to-left|x  = y;|-6|
||+=, -=, \*=, /=, %=|Assignment by sum, difference, product, quotient, remainder||x+=1; x-=1; //etc.|6, 5|
|15|,|Comma|Left-to-right|x = 3, y = 1;|3|

```c
int main()
{
	int x = 5, y = -6; int * z; float f = 3.0f; 				/*code*/
}
```

<!-- perentysys; esiszewitiwy
Use parentheses to override order of evaluation -->

---

# Cast

---

# Two words about floating-point representation

Operations on real numbers are recorded with only a certain degree of precision, and therefore there is a very high probability that the result of (a + b – c) will not be the same as (a - c + b) ! This means that using real numbers requires careful consideration.

<!-- but more on that in another course - namely, computer architecture. -->

---

<!-- _class: compact fit-90 -->

# What is Casting?

The process of converting a value of one data type to another.

There are two types of casting:

- Explicit
- Implicit

The purpose:

- To perform arithmetic operations on different data types.
- To assign a value of one type to a variable of another type.
- To access specific parts of a data structure.

---

<!-- _class: compact fit-90 -->

# Explicit Casting

```c
int main()
{
    int   a = 5;
    float b = 8.2f;

    int   c = (int)b + a;
    float d = b + (float)a;

    return 0;
}
```

```text
1
2
3
4
5
6
7
8
9
10
```

- 5
- 8.19999981
- 13.1999998
- 13

If we put a data type in parentheses before a symbolic name (variable), we perform a type cast of that variable to the specified type. When casting a float to an int, the number is truncated, which can **lead to loss of information**. In the opposite case, casting to a wider type is always safe and does not cause data loss, but casting to a narrower type may result in loss of information.

- Manual conversion performed by the programmer using a cast operator.

<!-- The size of a pointer is 4 bytes on 32-bit platforms
asterisk -->

---

<!-- _class: compact fit-70 -->

# Implicit Casting

- Automatic conversion performed by the compiler.
- Automatic casting will always cast to a wider type to never lose information.
- There is no automatic conversion from float to double, this is the only exception.
- Even though expressions in the return statement are always implicitly cast to the function's return type, it is considered good practice to explicitly cast the value to emphasize that this is intentional. If the programmer doesn't perform this explicit cast, the compiler will do it for them, but this is generally considered poor programming style...
- When occurs:
  - When assigning a value of a smaller type to a larger one (e.g. int to float).
  - In arithmetic expressions where different types are mixed.

---

# Unary, Binary, Ternary

---

# Operators

- Operators specify what is to be done to variables (also pointers or labels)
- Operators can be:
  - unary    (e. g. -, ++),
  - binary    (e. g. +, -, \*, /),
  - ternary    (?:)

```c
int main()
{
  int i = 1;
  i = -i;				 /* unary -  						 */
  i++;				 /* unary ++ 						 */
  i = i + 1; i = i - 1;	 /* binary +, - 					 */
  i = i * 1; i = i / 1; 	 /* binary *, / 					 */
  i ? (i > 0) : 1 ; 0;	 /* ternary conditional 				 */
}
```

---

# Basic operators

|Priority / Operator||Description|Associativity|Example|Result|
|---|---|---|---|---|---|
|1|()|Parentheses|Left-to-right|2 \* (x + y)|-2|
|2|++, --|Prefix & postfix increment and decrement|Right-to-left|++x; x--; x;|6, 6, 5|
||\*, &|Indirection (dereference); Address-of||z = &x; \*z;|6422276; 5|
||(type)|Cast||(int)3.0f|3|
|3|\*, /, %|Multiplication, division, and remainder|Left-to-right|6/2 % 2|1|
|4|+, -|Addition and subtraction||1 + 2; 3 - 1|3, 2|
|6|&lt;, &lt;=, &gt;, &gt;=|For relational operators &lt;, &gt; and ≤, ≥ respectively||x&lt;y; x&lt;=y; x&gt;y; x&gt;=y|1, 1, 0 ,0|
|7|==, !=|For relational = and ≠ respectively||x == y, x != 1|1, 0|
|11|&&|Logical AND||1 && 0|0|
|12|\|\||Logical OR||1 \|\| 0|1|
|14|=|Simple assignment|Right-to-left|x  = y;|-6|
||+=, -=, \*=, /=, %=|Assignment by sum, difference, product, quotient, remainder||x+=1; x-=1; //etc.|6, 5|
|15|,|Comma|Left-to-right|x = 3, y = 1;|3|

```c
int main()
{
	int x = 5, y = -6; int * z; float f = 3.0f; 				/*code*/
}
```

<!-- perentysys; esiszewitiwy
Use parentheses to override order of evaluation -->

---

# Basic operators

|Priority / Operator||Description|Associativity|Example|Result|
|---|---|---|---|---|---|
|1|()|Parentheses|Left-to-right|2 \* (x + y)|-2|
|2|++, --|Prefix & postfix increment and decrement|Right-to-left|++x; x--; x;|6, 6, 5|
||\*, &|Indirection (dereference); Address-of||z = &x; \*z;|6422276; 5|
||(type)|Cast||(int)3.0f|3|
|3|\*, /, %|Multiplication, division, and remainder|Left-to-right|6/2 % 2|1|
|4|+, -|Addition and subtraction||1 + 2; 3 - 1|3, 2|
|6|&lt;, &lt;=, &gt;, &gt;=|For relational operators &lt;, &gt; and ≤, ≥ respectively||x&lt;y; x&lt;=y; x&gt;y; x&gt;=y|1, 1, 0 ,0|
|7|==, !=|For relational = and ≠ respectively||x == y, x != 1|1, 0|
|11|&&|Logical AND||1 && 0|0|
|12|\|\||Logical OR||1 \|\| 0|1|
|14|=|Simple assignment|Right-to-left|x  = y;|-6|
||+=, -=, \*=, /=, %=|Assignment by sum, difference, product, quotient, remainder||x+=1; x-=1; //etc.|6, 5|
|15|,|Comma|Left-to-right|x = 3, y = 1;|3|

```c
int main()
{
	int x = 5, y = -6; int * z; float f = 3.0f; 				/*code*/
}
```

<!-- perentysys; esiszewitiwy
Use parentheses to override order of evaluation -->

---

# Basics of mathematics

- From basic mathematics, it is known that multiplication has higher precedence than addition, and this precedence can be changed using parentheses. These rules work exactly the same way in the C language as in mathematics.
- However, because the representation of integers differs from floating-point numbers, as mentioned earlier, when a floating-point number is involved in an operation with an integer, the integer is implicitly cast to a floating-point number.

---

# Basics of mathematics

- Another important point is the division operator /. When used with integers, it performs integer division, meaning that 5 / 3 results in 1. If at least one operand is a floating-point number, the division produces a floating-point result, so 5 / 3 evaluates to approximately 1.6666.
- Finally, there is the modulo operator %, which returns the remainder of integer division. For example, 5 % 2 equals 1.

---

# Example - division

```c
// Declarations
int x = 5, y = 3;
float a = 5.0, b = 3.0;

printf("%s\n", "Integers:");
printf("x = %d\n", x);
printf("y = %d\n", y);

printf("%s\n","Floats:");
printf("a = %f\n", a);
printf("b = %f\n", b);

printf("Integer / Integer:\n");
printf("x / y = %d\n", x / y); // integer division

printf("\nInteger / Float:\n");
printf("x / b = %f\n", x / b); // x promoted to float
printf("x / b with %%d = %d (wrong!)\n", x / b); // incorrect, prints garbage

printf("\nFloat / Integer:\n");
printf("a / y = %f\n", a / y); // y promoted to float

printf("\nFloat / Float:\n");
printf("a / b = %f\n", a / b); // normal float division
```

Result:

```text
Integers:
x = 5
y = 3
Floats:
a = 5.000000
b = 3.000000
Integer / Integer:
x / y = 1

Integer / Float:
x / b = 1.666667
x / b with %d = -1431655765 (wrong!)

Float / Integer:
a / y = 1.666667

Float / Float:
a / b = 1.666667
```

---

# Increment (++) & decrement (--) operator & Assignment by sum

|Priority / Operator||Description|Associativity|Example|Result|
|---|---|---|---|---|---|
|1|()|Parentheses|Left-to-right|2 \* (x + y)|-2|
|2|++, --|Prefix & postfix increment and decrement|Right-to-left|++x; x--; x;|6, 6, 5|
||\*, &|Indirection (dereference); Address-of||z = &x; \*z;|6422276; 5|
||(type)|Cast||(int)3.0f|3|
|3|\*, /, %|Multiplication, division, and remainder|Left-to-right|6/2 % 2|1|
|4|+, -|Addition and subtraction||1 + 2; 3 - 1|3, 2|
|6|&lt;, &lt;=, &gt;, &gt;=|For relational operators &lt;, &gt; and ≤, ≥ respectively||x&lt;y; x&lt;=y; x&gt;y; x&gt;=y|1, 1, 0 ,0|
|7|==, !=|For relational = and ≠ respectively||x == y, x != 1|1, 0|
|11|&&|Logical AND||1 && 0|0|
|12|\|\||Logical OR||1 \|\| 0|1|
|14|=|Simple assignment|Right-to-left|x  = y;|-6|
||+=, -=, \*=, /=, %=|Assignment by sum, difference, product, quotient, remainder||x+=1; x-=1; //etc.|6, 5|
|15|,|Comma|Left-to-right|x = 3, y = 1;|3|

```c
int main()
{
	int x = 5, y = -6; int * z; float f = 3.0f; 				/*code*/
}
```

<!-- perentysys; esiszewitiwy
Use parentheses to override order of evaluation -->

---

<!-- _class: compact fit-90 -->

# Increment (++) & decrement (--) operator & Assignment by sum

- Prefix increment ++ and decrement -- operators increase (decrease) the operand's value first, then use the new value.
- Postfix increment ++ and decrement -- operators use the operand's current value first, then increase (decrease) the operand's value.
- Assignment by sum refers to the process of assigning a value to a variable using the addition operator + or the addition assignment operator += to combine the assigned value with the existing value of the variable.

```c
int main()
{
  int i = 1, j = 2;

  j++;

  i = j++;


  i = ++j;


  i += j;

  i = j = 2 + j;

}
```

```c
int main()
{
  int i = 1, j = 2;

  j = j + 1;

  i = j;
  j = j + 1;

  j = j + 1;
  i = j;

  i = i + j;

  j = 2 + j;
  i = j;
}
```

- \*In Python we don’t have something like that.

<!-- tu skonczylem, poprawilem blad tabilcy c -->

---

# Relational & logical operators

---

# Relational & logical operators &lt;, &lt;=, &gt;, &gt;=, ==, !=, &&, ||

|Priority / Operator||Description|Associativity|Example|Result|
|---|---|---|---|---|---|
|1|()|Parentheses|Left-to-right|2 \* (x + y)|-2|
|2|++, --|Prefix & postfix increment and decrement|Right-to-left|++x; x--; x;|6, 6, 5|
||\*, &|Indirection (dereference); Address-of||z = &x; \*z;|6422276; 5|
||(type)|Cast||(int)3.0f|3|
|3|\*, /, %|Multiplication, division, and remainder|Left-to-right|6/2 % 2|1|
|4|+, -|Addition and subtraction||1 + 2; 3 - 1|3, 2|
|6|&lt;, &lt;=, &gt;, &gt;=|For relational operators &lt;, &gt; and ≤, ≥ respectively||x&lt;y; x&lt;=y; x&gt;y; x&gt;=y|1, 1, 0 ,0|
|7|==, !=|For relational = and ≠ respectively||x == y, x != 1|1, 0|
|11|&&|Logical AND||1 && 0|0|
|12|\|\||Logical OR||1 \|\| 0|1|
|14|=|Simple assignment|Right-to-left|x  = y;|-6|
||+=, -=, \*=, /=, %=|Assignment by sum, difference, product, quotient, remainder||x+=1; x-=1; //etc.|6, 5|
|15|,|Comma|Left-to-right|x = 3, y = 1;|3|

```c
int main()
{
	int x = 5, y = -6; int * z; float f = 3.0f; 				/*code*/
}
```

<!-- Use parentheses to override order of evaluation -->

---

# Relational & logical operators <br>&lt;, &lt;=, &gt;, &gt;=, ==, !=, &&, ||

- Relational and logical operators return 1 for a true condition and 0 for a false condition. The result type of these operators is int (integer).
- In if and while statements, the C language considers the logical value of the conditional expression. This means that any value other than 0 (including positive, negative, characters, pointers, etc.) will be treated as true, while the value 0 will be treated as false.
- The bool type is not a built-in type because it is not essential for basic programming operations. However, to use the bool type, we need to include the &lt;stdbool.h&gt; header file.

```c
#include <stdio.h>
#include <stdbool.h>

int main()
{
  bool is_true  = true;
  bool is_false = false;
  bool result = is_true && is_false;
  printf("%d\n", result);
  result = 3 > 1;
  printf("%d\n", result);
}
```

Result:

```text
0
1
```

---

# Basic operators

|Priority / Operator||Description|Associativity|Example|Result|
|---|---|---|---|---|---|
|1|()|Parentheses|Left-to-right|2 \* (x + y)|-2|
|2|++, --|Prefix & postfix increment and decrement|Right-to-left|++x; x--; x;|6, 6, 5|
||\*, &|Indirection (dereference); Address-of||z = &x; \*z;|6422276; 5|
||(type)|Cast||(int)3.0f|3|
|3|\*, /, %|Multiplication, division, and remainder|Left-to-right|6/2 % 2|1|
|4|+, -|Addition and subtraction||1 + 2; 3 - 1|3, 2|
|6|&lt;, &lt;=, &gt;, &gt;=|For relational operators &lt;, &gt; and ≤, ≥ respectively||x&lt;y; x&lt;=y; x&gt;y; x&gt;=y|1, 1, 0 ,0|
|7|==, !=|For relational = and ≠ respectively||x == y, x != 1|1, 0|
|11|&&|Logical AND||1 && 0|0|
|12|\|\||Logical OR||1 \|\| 0|1|
|14|=|Simple assignment|Right-to-left|x  = y;|-6|
||+=, -=, \*=, /=, %=|Assignment by sum, difference, product, quotient, remainder||x+=1; x-=1; //etc.|6, 5|
|15|,|Comma|Left-to-right|x = 3, y = 1;|3|

```c
int main()
{
	int x = 5, y = -6; int * z; float f = 3.0f; 				/*code*/
}
```

<!-- Use parentheses to override order of evaluation -->

---

# Statements & expressions

---

# C language is a procedural programming language.

- Imperative programming is a programming paradigm that uses **statements to change a program's state**.
- It is like giving the computer instructions step by step on what to do.
- Imperative programming

---

# C language is a procedural programming language.

- Procedural programming is a type of imperative programming that breaks down a program into smaller, independent procedures (functions).
- This makes the program more organized and easier to maintain.
- Imperative programming
- Procedural programming

---

# C language is a procedural programming language.

- Object-oriented programming further extends the concepts of procedural programming by organizing code into objects that encapsulate data and behavior.
- Imperative programming
- Procedural programming
- Object-oriented

---

# Statement & expression

In computer science, a **statement** is a complete instruction that can modify the state of a program, such as assigning a value to a variable, calling a function, or jumping to a different part of the code. Statements do not produce a value on their own.

An **expression**, on the other hand, is a combination of variables, constants, functions, and operators that evaluates to a single value (**The absence of a returned value from a function is also a result**). Expressions can be used within statements to provide values for operations or to control the flow of the program. However, expressions themselves do not directly modify the state of the program.

<!-- [Mitchell, J.](https://en.wikipedia.org/wiki/John_C._Mitchell) (2002). Concepts in Programming Languages. Cambridge: Cambridge University Press, *3.4.1 Statements and Expressions*, p. 26 -->

---

# Null / empty statement;

- A single semicolon ; in C language is a statement called a null statement or empty statement.
- A semicolons ; are used to terminate statements

```c
int main()
{
    ;   									/*  Empty statement    */
	printf("Hello world!\n");			/*  Second statement   */
	printf("Hello"); printf(" world!\n");	/*  3rd & 4th statement in one line */
}
```

<!-- In C programming, a **single line ending with a semicolon** (;) is typically referred to as an **empty statement** or **null statement**. It's a statement that doesn't perform any operation and has no effect on the program's execution. -->

---

# Conclusions

- *In C, a code line is not the same as a statement*
- *An entire program can be written in a single line*
- *As the compiler separates statements with semicolons (;) and not newlines*
- *Therefore, a single line of text (with a newline character) can contain multiple statements.*

---

# Block

---

# Block & complex(compound) statements

- Block can be:
  - substitute for simple statement,
  - defined within a block (Nested blocks),
  - empty {}.
- Variables can be declared inside
- Variables declared inside a block with the same name hide access to variables outside that block
- No semicolon at end of block
- After a code block ends, all variables declared within that block cease to exist and are no longer accessible in the rest of the program

<!-- Moze kiedys dodac “Compiled as a single unit “
Statements which cannot contain other statements are *simple*; those which can contain other statements are *compound*
Simple statements are complete in themselves; these include assignments, subroutine calls, and a few statements which may significantly affect the program flow of control (e.g. goto, return, etc.)
Jak udowodnic ze instrukcje count-controlled loop, condidion – cotrolled loop and if are statement? Zmieniaja stan program to znaczy kolejna linia kodu ktora miala byc a jest inna np. Goto.
Przypisanie jest rownoczesnie statement I -->

---

# Blocks & complex(compound) statements

```c
int main()
{
    char* text = "Hello world\n";
    printf(text);
    {
      char* text = "Bye world\n";
      printf(text);
      {
        char* text = "Aloha world\n";
        printf(text);
      }
    }
    printf(text);
}
```

Result:

```text
Hello world
Bye world
Aloha world
Hello world
```

---

# Statement & expression

- A **statement** can modify the state of a program, such as assigning a value to a variable, calling a function, or jumping to a different part of the code.
- Statements do not produce a value on their own.
- An **expression** is a combination of variables, constants, functions, and operators that evaluates to a single value.
- Expressions themselves do not directly modify the state of the program.

---

# Consequences

|Priority / Operator||Expression|Statement|
|---|---|---|---|
|1|(), \[\]|√|×|
||.|√|×|
||-&gt;|√|×|
|2|++, --|√|√|
||+, -, !, ~ (unary)|√|×|
||\*, & , &&  (unary)|√|×|
||(type), sizeof|√|×|
|3|\*, /, %|√|×|
|4|+, -|√|×|
|5|&lt;&lt;,  &gt;&gt;|√|×|
|6|&lt;, &lt;=, &gt;, &gt;=|√|×|
|7|==, !=|√|×|
|8|&|√|×|
|9|^|√|×|
|10|\||√|×|
|11|&&|√|×|
|12|\|\||√|×|
|13|?:|√|×|
|14|=|√|√|
||+=, -=, \*=, /=, %=|√|√|
||&lt;&lt;=, &gt;&gt;=, &=, ^=, \|=|√|√|
|15|,|√|×|

- In the Python language, there is not a single operator that is both a statement and an expression.
- Increment and decrement operators do not exist at all.
- Assignment is exclusively a statement, as is compound assignment. This has significant consequences.

<!-- Use parentheses to override order of evaluation -->

---

# Consequences

- The underscore \_ in Python (and C#) does not require the declaration of this variable, because it is not a variable, but only an indication to the compiler that this is a conscious rejection of the value returned by a function. It does not change anything - it is just a stylistic trick to improve code readability.
- This makes sense only because assignment in Python is not an expression and does not return a value by itself, but in C it is not like that.

Python:

```python
def sq(n):
    print(n ** 3)
    return n ** 3

_ = sq(3)
```

```python
sq(3)
```

Result:

```text
27
27
```

<!-- Use parentheses to override order of evaluation -->

---

# Consequences

- In the C language, every assignment after assigning a value to a variable (pointer, label), since it is also an expression, will generate a value again, which will be ignored by the compiler at the end
- We can use the underscore \_ discard in C, but you need to declare the variable beforehand. It's a great mechanism that improves the readability of the programmer's intent.

```c
int main()
{
  int x, y, _;
  _ = x = y = 5;
}
```

```c
_ = x = y = 5;
_ = x = (5);
_ = x = 5;
_ = (5);
_ = 5;
(5)
```

<!-- Use parentheses to override order of evaluation -->

---

# Thank you

- Jakub Leszek Pach
- <jpach@mtech.edu>
