---
marp: true
theme: pach
paginate: true
footer: "CSCI 112 | Programming with C | J. L. Pach"
title: "CSCI 112  Programming with C"
---

<!-- _class: lead -->

# CSCI 112<br><br>Programming with C

- Lecture 8
- Dr. Jakub L. Pach
- Fall 2025

---

# Outline

- Review
- Operators
  - & address-of
  - \* Indirection (dereference)
- Left-to-right & right-to-left associativity
- Preprocessor
- Buffered input

---

# Review

---

# while loop

```c
while (expression1)
	statement1;
```

A while loop repeatedly executes statement1 based on the logical outcome of expression1 as long as expression1 evaluates to true.

```c
int main()
{
  int i = 0;
  while ( i < 3 )
  {
    printf("a value of i is: %d\n", i);
    i++;
  }
}
```

Result:

```text
a value of i is: 0
a value of i is: 1
a value of i is: 2
```

```c
int main()
{
  int i = 0;
  while ( i < 3 )
    printf("a value of i is: %d\n", i++);
}
```

OR

---

<!-- _class: fit-70 -->

# for loop

```c
for (expression1; expression2; expression3)
	statement1;
```

- A for loop repeatedly executes statement1 based on the logical outcome of expression2 as long as expression2 evaluates to true.
- Most commonly expression1 and expression3 are assignments of function calls and expression2 is  a relational expression.
- Any of the three part can be omitted, although the semicolons must be remain. If expression2 is not present, it is taken as permanently true.

```c
int main()
{
  for (int i = 0; i < 4; i++ )
    printf("a value of i is: %d\n", i);
}
```

Result:

```text
a value of i is: 0
a value of i is: 1
a value of i is: 2
```

---

# The for loop is equivalent to while loop

```c
expression1;
while (expression2)
{
	statement1;
	expression3;
}
```

```c
for (expression1; expression2; expression3)
{
	statement1;
}
```

---

# “Infinity” loop

```c
while (true)
{
	;
}
```

```c
for (;;)
{
	;
}
```

---

# break & continue keywords

- break and continue offer distinct ways to control loop flow.
- break instantly terminates the loop it's in, while continue jumps to the next iteration.
- When nested, break affects only the immediate loop.
- break is also applicable in switch statements to exit a specific case

```c
int main()
{
  for (int i = 1; i <= 10; i++)
  {
    if (i == 5)
      break;          /* Breaks the loop      */
    printf("%d ", i); /* when i is equal to 5 */
  }
}
```

Result:

```text
1 2 3 4
```

---

# break & continue keywords

- break and continue offer distinct ways to control loop flow.
- break instantly terminates the loop it's in, while continue jumps to the next iteration.
- When nested, break affects only the immediate loop.
- break is also applicable in switch statements to exit a specific case

```c
int main()
{
  int i = 0;
  while (i < 10)
  {
    i++;
    if (i % 2 == 0)
      continue;       /* Skips the rest of the    */
    printf("%d ", i); /* iteration when i is even */
  }
}
```

Result:

```text
1 3 5 7 9
```

---

# goto statement in loops

- goto provides a convenient way to exit from nested blocks

```c
int main()
{
  bool bug = false;

  for (int i = 0; i < 5; i++)
  {
    for (int j = 0; j < 5; j++)
    {
      /* some code */
      /* ...       */
      if(bug)
        goto error;
    }
  }
  goto end;
  error:
    /* some code */
    /* ...       */
    printf("error found");
  end:
}
```

```c
int main()
{
  bool bug = false; int i = 0, j = 0;
  while ( i < 5)
  {
    while ( j < 5)
    {/* some code */
     /* ...       */
      if(bug)
        goto error;
      j++;
    }
    i++;
  }
  goto end;
  error:
    /* some code */
    /* ...       */
    printf("error found");
  end:
}
```

---

# Prototype & its Function

- In contrast to function implementations, function prototypes are terminated with a semicolon(;)
- A minimal prototype must precede the function definition, and it is standard to list function prototypes alphabetically after preprocessor directives within a file

```c
return-type function-name (parameter declarations, if any)
{
	statements; 			/* including declarations */
	return expression1;
}
```

```c
return-type function-name (only type of parameter declarations, if any);
```

---

# Prototype & its Function

- The return type can be any of the data types presented in the previous material, and additionally, void can be used if no value is to be returned.
- The function name is symbolic\_name.

```c
return-type function-name (parameter declarations, if any)
{
	statements; 			/* including declarations */
	return expression1;
}
```

```c
return-type function-name (only type of parameter declarations, if any);
```

---

# Prototype & its Function

```c
#include <stdio.h>

void myFunction1(void);
int  myFunction2(int);
int  myFunction3(void);

void myFunction1()
{
  printf("Text from myFuntion1\n");
  return;
}
int myFunction2(int n)
{
  n++;
  printf("incremented n from myFuntion2 equals %d\n", n);
  return 1;
}
int myFunction3()
{
  int n = 2;
  printf("n from myFuntion3 equals %d\n", n);
  /* the compiler will not return an error if     */
  /* we omit return, and the function will return */
  /* an unspecified value                         */
}
```

```c
int main()
{
  myFunction1();
  int result = myFunction2(2);
  printf("result of myFuntion2 equals %d\n", result);
  result = myFunction3();
  printf("result of myFuntion3 equals %d\n", result);
  return 0;
}
```

Result:

```text
Text from myFuntion1
incremented n from myFuntion2 equals 3
result of myFuntion2 equals 1
n from myFuntion3 equals 2
result of myFuntion3 equals 27
```

- Correct exit

<!-- Green comment! -->

---

# Variables

- variable scope    –    the region in which a variable is valid;

any variable must be declared before its first use;

- Variables:

– local (automatic)

– global

local variable    –    is only accessible within the block where it is defined. Once the         block ends, access to the local variable is lost.

global variable    –    declared outside of functions, is accessible from any point in the         program below its declaration.

---

# global vs local

We don't have direct access to a shadowed variable. The only way to access it is through a pointer.

```c
#include <stdio.h>
int x = 5; 				/* global x */

void myFunction1(void);
void myFunction1()
{
  printf("x equals %d that is read by function myFunction\n", x);
}
int main()
{
  int * pointerGlobalX = &x;
  myFunction1();
  int x = 3;  			/* local x */
  printf("x equals %d that is read by function main\n", x);
  printf("x equals %d that is read by function main\n", *pointerGlobalX);
  return 0;
}
```

Result:

```text
x equals 5 that is read by function myFunction
x equals 3 that is read by function main
x equals 5 that is read by function main
```

---

<!-- _class: fit-90 -->

# Summary - variable scope

- Global variables are accessible throughout a program, but they can be temporarily hidden by a local variable declared within a nested block, such as a function, for loop, while loop, or even an if statement.
- This is known as "variable shadowing," and within the local variable's scope, any reference to that variable name will refer to the local one. The global variable remains inaccessible until the local variable's block is exited and the local variable is released from memory. At that point, access to the global variable is restored.

---

# Operator & address-of

---

|Priority / Operator||Description|Associativity|Example|Result|
|---|---|---|---|---|---|
|1|(), \[\]|Parentheses; Array subscript|Left-to-right|arr\[0\] \* (x + y)|1|
||.|Structure and union member access||point.x|1|
||-&gt;|Structure and union member access through pointer||ppoint-&gt;x|1|
|2|++, --|Prefix & postfix increment and decrement|Right-to-left|++x; x--; x;|6, 6, 5|
||+, -, !, ~|(Unary) plus and minus; Logical NOT and bitwise NOT||y =-y; y =+y; !x; ~;x|6, -6,0, -6|
||\*, & , &&|Indirection (dereference); Address-of; Address-of labels||z = &x; \*z;|6422276; 5|
||(type), sizeof|Cast, Size-of||(int)3.0f; sizeof(x);|3, 4|
|3|\*, /, %|Multiplication, division, and remainder|Left-to-right|6/2 % 2|1|
|4|+, -|Addition and subtraction||1 + 2; 3 - 1|3, 2|
|5|&lt;&lt;,  &gt;&gt;|Bitwise left shift and right shift||4 &lt;&lt; 1; 4 &gt;&gt; 2|8, 1|
|6|&lt;, &lt;=, &gt;, &gt;=|For relational operators &lt;, &gt; and ≤, ≥ respectively||x&lt;y; x&lt;=y; x&gt;y; x&gt;=y|1, 1, 0 ,0|
|7|==, !=|For relational = and ≠ respectively||x == y, x != 1|1, 0|
|8|&|Bitwise AND||7 & 3|3|
|9|^|Bitwise XOR (exclusive or)||255 ^ 0|255|
|10|\||Bitwise OR (inclusive or)||7 \| 3|7|
|11|&&|Logical AND||1 && 0|0|
|12|\|\||Logical OR||1 \|\| 0|1|
|13|?:|Ternary conditional|Right-to-left|x  = (x &gt; y) ? y : x;|-6|
|14|=|Simple assignment||x  = y;|-6|
||+=, -=, \*=, /=, %=|Assignment by sum, difference, product, quotient, remainder||x+=1; x-=1; //etc.|6, 5|
||&lt;&lt;=, &gt;&gt;=, &=, ^=, \|=|Assignment by bitwise left shift, right shift, AND, XOR, OR||3&lt;&lt;=1, 8&gt;&gt;=2 //etc.|6, 2|
|15|,|Comma|Left-to-right|x = 3, y = 1;|3|

```c
struct Point { int x; int y; }; int main()
{struct Point point = {1,2}, *ppoint = &point;  int arr[] = {1,2}; int x = 5, y =-6; int * z; float f = 3.0f; /*code*/}
```

<!-- perentysys; esiszewitiwy
Use parentheses to override order of evaluation -->

---

|Priority / Operator||Description|Associativity|Example|Result|
|---|---|---|---|---|---|
|1|(), \[\]|Parentheses; Array subscript|Left-to-right|arr\[0\] \* (x + y)|1|
||.|Structure and union member access||point.x|1|
||-&gt;|Structure and union member access through pointer||ppoint-&gt;x|1|
|2|++, --|Prefix & postfix increment and decrement|Right-to-left|++x; x--; x;|6, 6, 5|
||+, -, !, ~|(Unary) plus and minus; Logical NOT and bitwise NOT||y =-y; y =+y; !x; ~;x|6, -6,0, -6|
||\*, & , &&|Indirection (dereference); **Address-of; Address-of labels**||z = &x; \*z;|6422276; 5|
||(type), sizeof|Cast, Size-of||(int)3.0f; sizeof(x);|3, 4|
|3|\*, /, %|Multiplication, division, and remainder|Left-to-right|6/2 % 2|1|
|4|+, -|Addition and subtraction||1 + 2; 3 - 1|3, 2|
|5|&lt;&lt;,  &gt;&gt;|Bitwise left shift and right shift||4 &lt;&lt; 1; 4 &gt;&gt; 2|8, 1|
|6|&lt;, &lt;=, &gt;, &gt;=|For relational operators &lt;, &gt; and ≤, ≥ respectively||x&lt;y; x&lt;=y; x&gt;y; x&gt;=y|1, 1, 0 ,0|
|7|==, !=|For relational = and ≠ respectively||x == y, x != 1|1, 0|
|8|&|Bitwise AND||7 & 3|3|
|9|^|Bitwise XOR (exclusive or)||255 ^ 0|255|
|10|\||Bitwise OR (inclusive or)||7 \| 3|7|
|11|&&|Logical AND||1 && 0|0|
|12|\|\||Logical OR||1 \|\| 0|1|
|13|?:|Ternary conditional|Right-to-left|x  = (x &gt; y) ? y : x;|-6|
|14|=|Simple assignment||x  = y;|-6|
||+=, -=, \*=, /=, %=|Assignment by sum, difference, product, quotient, remainder||x+=1; x-=1; //etc.|6, 5|
||&lt;&lt;=, &gt;&gt;=, &=, ^=, \|=|Assignment by bitwise left shift, right shift, AND, XOR, OR||3&lt;&lt;=1, 8&gt;&gt;=2 //etc.|6, 2|
|15|,|Comma|Left-to-right|x = 3, y = 1;|3|

```c
struct Point { int x; int y; }; int main()
{struct Point point = {1,2}, *ppoint = &point;  int arr[] = {1,2}; int x = 5, y =-6; int * z; float f = 3.0f; /*code*/}
```

<!-- perentysys; esiszewitiwy
Use parentheses to override order of evaluation -->

---

# What is an address?

- Address is an identifier <br>(symbolic name) of location
- **A place to locate what we refer to**
- **Address of University:**
- 1300 W Park St, Butte, MT 59701

![w:600px Montana Tech | TeenLife](assets/image4.jpeg)

---

# Every symbolic name…

Every symbolic name — whether for a variable, array, function, or label — refers to a specific memory location. Once assigned (declared/initialized), the content at that memory location can change, but the address itself remains fixed for the lifetime of that entity. For example, a variable declared within a block will always occupy the same memory address until the block ends.

```c
#include <stdio.h>
int main()
{
    int y = 5;
    printf("Address of %-10s= %d\n", "y", &y);
    int x = 2;
    y++;
    printf("Address of %-10s= %d\n", "y", &y);
}
```

Result:

```text
Address of y       = 6487800
Address of y       = 6487800
```

---

# Extended example

Warning…

Should be %p

```c
#include <stdio.h>
int myFunction(){return 0;}
int main()
{
    int x;
    int arr1[7] = {1, 2, 3, 4, 5, 6, 7};
    label1: x = 5;                                                 // statement, not a declaration
    printf("Address of %-20s= %d\n", "x", &x);                     // address of local variable x
    printf("Address of %-20s= %d\n", "arr1 (array name)", arr1);   // address of first element of array
    printf("Address of %-20s= %d\n", "arr1 (array itself)", &arr1);// address of the whole array (the same!)
    printf("Address of %-20s= %d\n", "function myFunction", &myFunction); // address of function
    printf("Address of %-20s= %d\n", "label1:", &&label1);         // address of label
}
```

Result:

```text
Address of x                   = 6487836
Address of arr1 (array name)   = 6487808
Address of arr1 (array itself) = 6487808
Address of function myFunction = 4199493
Address of label1:             = 4199573
```

```c
int myFunction()
{
    return 0;
}
```

---

# Extended example - description

- When a variable, a symbolic name, is declared, it is allocated a static location in RAM. Its value can be changed, but for its entire lifetime, it cannot be deleted or moved. It will always refer to the same specific memory cell. For example, with int x = 5;, we can change its value later, like x = 3;, but the address &x will always point to the same memory location.
- The same principle applies to arrays. That is why we must initialize an array in a single line, like int arr1\[7\] = {1, 2, 3, 4, 5, 6, 7};.

---

<!-- _class: fit-90 -->

# Extended example - description

- We cannot declare and then initialize it on separate lines, such as:

```c
int arr1[7];
arr1[7] = {1, 2, 3, 4, 5, 6, 7}; // This is invalid
```

- The first line is a shorthand for the compiler. The compiler, before the code is actually executed, performs a loop-like operation to initialize the array, assigning each value to its corresponding memory location. Because of this, initialization cannot be split into two separate steps.

---

# Extended example - description

- The symbolic name of an array represents a fixed memory address — specifically, the location where the array begins in memory. You can think of it as a label that always refers to the same starting point of the array.
- This address is read-only: once the array is declared, you cannot change where it begins. The name of the array and the address of its first element are essentially the same in expressions. Because the array name itself stands for a memory location, you can't reassign it to refer to a different place in memory.

---

# Extended example

Warning…

Should be %p

```c
#include <stdio.h>
int myFunction(){return 0;}
int main()
{
    int x;
    int arr1[7] = {1, 2, 3, 4, 5, 6, 7};
    label1: x = 5;                                                 // statement, not a declaration
    printf("Address of %-20s= %d\n", "x", &x);                     // address of local variable x
    printf("Address of %-20s= %d\n", "arr1 (array name)", arr1);   // address of first element of array
    printf("Address of %-20s= %d\n", "arr1 (array itself)", &arr1);// address of the whole array (the same!)
    printf("Address of %-20s= %d\n", "function myFunction", &myFunction); // address of function
    printf("Address of %-20s= %d\n", "label1:", &&label1);         // address of label
}
```

Result:

```text
Address of x                   = 6487836
Address of arr1 (array name)   = 6487808
Address of arr1 (array itself) = 6487808
Address of function myFunction = 4199493
Address of label1:             = 4199573
```

---

# Extended example

Warning…

Should be %p

```c
#include <stdio.h>
int myFunction(){return 0;}
int main()
{
    int x;
    int arr1[7] = {1, 2, 3, 4, 5, 6, 7};
    label1: x = 5;                                                  // statement, not a declaration
    printf("Address of %-20s= %d\n", "x", &x);                     // address of local variable x
    printf("Address of %-20s= %p\n", "arr1 (array name)", arr1);   // address of first element of array
    printf("Address of %-20s= %08x\n", "arr1 (array itself)", &arr1);// address of the whole array (the same!)
    printf("Address of %-20s= %d\n", "function myFunction", &myFunction); // address of function
    printf("Address of %-20s= %d\n", "label1:", &&label1);         // address of label
}
```

Result:

```text
Address of x                   = 6487836
Address of arr1 (array name)   = 0062ff00
Address of arr1 (array itself) = 0062ff00
Address of function myFunction = 4199493
Address of label1:             = 4199573
```

---

# Extended example

```c
#include <stdio.h>
int myFunction(){return 0;}
int main()
{
    int x;
    int arr1[7] = {1, 2, 3, 4, 5, 6, 7};
    label1: x = 5;                                                  // statement, not a declaration
    printf("Address of %-20s= %p\n", "x", &x);                     // address of local variable x
    printf("Address of %-20s= %p\n", "arr1 (array name)", arr1);   // address of first element of array
    printf("Address of %-20s= %p\n", "arr1 (array itself)", &arr1);// address of the whole array (the same!)
    printf("Address of %-20s= %p\n", "function myFunction", &myFunction); // address of function
    printf("Address of %-20s= %p\n", "label1:", &&label1);         // address of label
}
```

Result:

```text
Address of x                   = 0062ff1c
Address of arr1 (array name)   = 0062ff00
Address of arr1 (array itself) = 0062ff00
Address of function myFunction = 00401445
Address of label1:             = 00401495
```

---

|Type & Specifier||Origin|Argument type||Description||
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

<!-- _class: fit-90 -->

# Extended example - description

- When printf receives an address using the & operator, it prints the address of a 32-bit <br>(or platform-dependent) integer. To display addresses correctly without compiler warnings, the %p format specifier should be used, which is specifically designed for pointer values.
- Once a variable is declared within a block, the compiler has already reserved a specific memory location for it. Redeclaring the same variable name in the same scope is illegal because that memory is already allocated and associated with the original symbolic name. It would cause a compile-time error.

---

# Operator & address-of

- The single ampersand symbol, &, is a unary operator used to get the **memory address** of a variable. Think of it as asking, "Where in the computer's memory is this variable physically located?"
- When you use & before a variable's name (symbolic name), the operator returns the exact location of that variable in memory. This location is just a number that tells you where the variable's data is stored.

---

# Operator \* Indirection (dereference)

---

<!-- _class: fit-90 -->

# Operator \* Indirection (dereference)

- The asterisk symbol, \*, is a unary operator used to access the actual value stored at a specific location in memory. Think of it as asking, "What is stored at this address?"
- When you use \* before something that represents a memory location — for example, a result you got using the & operator — the \* operator lets you look inside that location and see the value stored there.
- This operation **only** makes semantic sense when applied to variables and arrays — that is, to objects that occupy space in memory and hold meaningful data. It does not apply to labels, which are used for program control flow and do not have a retrievable memory location, nor to functions, which are executed rather than accessed for stored values.

---

# Extended example

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

Result:

```text
Value at address of x                    = 5
Value at address of arr1 (array name)    = 9
Value at address of arr1 (array name)    = 10
Value at address of arr1 (array name)    = 8
```

- Priority!!!

---

|Priority / Operator||Description|Associativity|Example|Result|
|---|---|---|---|---|---|
|1|(), \[\]|Parentheses; Array subscript|Left-to-right|arr\[0\] \* (x + y)|1|
||.|Structure and union member access||point.x|1|
||-&gt;|Structure and union member access through pointer||ppoint-&gt;x|1|
|2|++, --|Prefix & postfix increment and decrement|Right-to-left|++x; x--; x;|6, 6, 5|
||+, -, !, ~|(Unary) plus and minus; Logical NOT and bitwise NOT||y =-y; y =+y; !x; ~;x|6, -6,0, -6|
||\*, & , &&|Indirection (dereference); Address-of; Address-of labels||z = &x; \*z;|6422276; 5|
||(type), sizeof|Cast, Size-of||(int)3.0f; sizeof(x);|3, 4|
|3|\*, /, %|Multiplication, division, and remainder|Left-to-right|6/2 % 2|1|
|4|+, -|Addition and subtraction||1 + 2; 3 - 1|3, 2|
|5|&lt;&lt;,  &gt;&gt;|Bitwise left shift and right shift||4 &lt;&lt; 1; 4 &gt;&gt; 2|8, 1|
|6|&lt;, &lt;=, &gt;, &gt;=|For relational operators &lt;, &gt; and ≤, ≥ respectively||x&lt;y; x&lt;=y; x&gt;y; x&gt;=y|1, 1, 0 ,0|
|7|==, !=|For relational = and ≠ respectively||x == y, x != 1|1, 0|
|8|&|Bitwise AND||7 & 3|3|
|9|^|Bitwise XOR (exclusive or)||255 ^ 0|255|
|10|\||Bitwise OR (inclusive or)||7 \| 3|7|
|11|&&|Logical AND||1 && 0|0|
|12|\|\||Logical OR||1 \|\| 0|1|
|13|?:|Ternary conditional|Right-to-left|x  = (x &gt; y) ? y : x;|-6|
|14|=|Simple assignment||x  = y;|-6|
||+=, -=, \*=, /=, %=|Assignment by sum, difference, product, quotient, remainder||x+=1; x-=1; //etc.|6, 5|
||&lt;&lt;=, &gt;&gt;=, &=, ^=, \|=|Assignment by bitwise left shift, right shift, AND, XOR, OR||3&lt;&lt;=1, 8&gt;&gt;=2 //etc.|6, 2|
|15|,|Comma|Left-to-right|x = 3, y = 1;|3|

```c
struct Point { int x; int y; }; int main()
{struct Point point = {1,2}, *ppoint = &point;  int arr[] = {1,2}; int x = 5, y =-6; int * z; float f = 3.0f; /*code*/}
```

<!-- perentysys; esiszewitiwy
Use parentheses to override order of evaluation -->

---

# Left-to-right & right-to-left associativity

---

# Left-to-right & right-to-left associativity

|Priority||Ass.|
|---|---|---|
|1|()|LR|
|2|++, --|RL|
||\*, &||
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

Result:

```text
6
4
```

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

<!-- _class: fit-70 -->

# Summary for associativity and \*&

- The associativity of the \* and & operators is right-to-left (R–L), similar to assignment, but unlike arithmetic or logical operations, which we’re more familiar with.
- This means that using them together — like in \*&x — works correctly: first, the address of x is obtained, and then the value stored at that address is retrieved.
- You could say that \*& cancels itself out, and logically that’s true. However, it’s a relatively costly operation: instead of directly accessing the value, the program first computes the address from the symbolic name, and then accesses the value from that location.
- The compiler may optimize this during compilation and simplify it to just x, but relying on such optimizations is considered poor practice. It reflects a lack of foundational understanding — similar to blindly trusting automatic type casting.

---

# Preprocessor

---

# Hello World

- Code
- Preprocessor

```c
#include <stdio.h>


int main()
{
	printf("Hello world\n");
	return 0;
}
```

---

<!-- _class: fit-90 -->

# The Pre-processor

The C Preprocessor runs before the C program is compiled properly. It is a separate program from the compiler programs and, in theory, could be used on any file not just C source files. Its main uses are macro substitution, file inclusion and conditional compilation.

Each source file will normally have a few preprocessor commands, these are, strictly speaking, not part of the C language itself, though they are associated with the language. The preprocessor commands each start with a # and must either fit on a single source line or must be extended with the use of a - at the end of each line to be continued.

eg.: #include&lt;stdio.h&gt;

---

<!-- _class: fit-80 -->

# The C compiler process has four main phases

- **Preprocessing**: The preprocessor modifies the source code by performing:
  - **Macro substitution**
  - **File inclusion**
  - **Conditional compilation**
- **Compilation**: The compiler translates the preprocessed code into assembly code. This phase includes lexical analysis, parsing, and code generation, along with an optional optimization step.
- **Assembly**: The assembler translates the assembly code into machine code to create an object file.
- **Linking**: The linker combines all object files and libraries into a single executable program.

---

# Macro

---

<!-- _class: fit-70 -->

# Preprocessor directives - macro substitution

- A macro is a symbolic name that represents a sequence of tokens. It's like creating a shorthand that expands to a longer expression whenever it's encountered in the code.
- Macros allow us to define constants whose values cannot be changed during program execution.
- Macros can be used to conditionally compile parts of the code, for example, depending on whether a certain definition exists.
- Macros are generally faster than functions but are less safe. Therefore, they should be used with caution.
- Since macros are substituted before the program runs, they cannot be debugged directly.

```c
#define symbolic_name replaced_text
```

---

<!-- _class: fit-70 -->

# Preprocessor directives - macro substitution

```c
#define symbolic_name replaced_text
```

Macros are not terminated with semicolons, unlike regular code statements, making them easily distinguishable.

Writing macro-defined constants in uppercase is a best practice to emphasize their immutable nature. While the compiler won't complain, these values cannot be changed during runtime and are not accessible for debugging.

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
#define PI 3.14159
#define some_text "abcde"

#include <stdio.h>

int main()
{
    printf( "%s\n", "abcde" );
    printf( "%f\n", 3.14159 + 0.5f );
}
```

Result:

```text
abcde
3.641590
```

---

# Preprocessor directives - macro substitution

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

Result:

```text
abcde
25
Hello
```

---

# Preprocessor directives - macro substitution

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
#include <stdio.h>
int main()
{
    printf("%s\n", ( ("abc") < ("cde") ? ("abc") : ("cde") ));
    printf("%s\n", ( ("aac") < ("aab") ? ("aac") : ("aab") ));
}
```

Result:

```text
cde
aab
```

- It works because it's a ternary operator!

---

# Conditional compilation

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

Result:

```text
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

---

# Built-in constants in C - examples

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

Result:

```text
11:24:35
C:\Users\Jakub\Desktop\CSCI112\main.c
Sep 26 2024
```

---

# File inclusion

```text
Using <> (angle brackets)	–	e.g. #include <file_name.h>
Using "" (double quotes)	–	e.g. #include "file_name.h"

```

---

# File inclusion - &lt;&gt; (angle brackets)

- Using Standard library search:
  - When you use angle brackets, the compiler searches for the file in the standard system directories where the compiler expects to find header files for the standard C library.
- System-wide:
  - This is commonly used to include standard library (build-in) headers like &lt;stdio.h&gt;, &lt;time.h&gt;, etc.

---

<!-- _class: fit-70 -->

# File inclusion - "" (double quotes)

- Local search:
  - When you use double quotes around a filename in an #include directive, the compiler first searches for the file in the same directory as the current file.
- Project-specific:
  - This is useful for including header files that are specific to your current project and are located in the same directory or a subdirectory.

---

<!-- _class: fit-80 -->

# Summary: How the C Preprocessor Works

- The preprocessor works like a “Find and Replace” tool in a text editor — it searches for specific strings (like constant names) and **replaces them with defined values** before the actual compilation begins. This means you cannot debug constants or change their values during runtime, because the source code has already been transformed — as if you manually replaced every occurrence of the name with its value.
- **Conditional compilation** allows the program to check whether a constant has been defined (#ifdef, #ifndef) and **include or skip parts of the code** accordingly. This is useful for writing code that adapts to different configurations, platforms, or versions.

---

# Buffered input

---

# Fundamental Functions for Input and Output

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

<!-- _class: fit-80 -->

# Getchar() & scanf()

- Using getche() allows you to read a character from the keyboard **without waiting for the Enter key**. This has consequences: without more advanced logic, the user cannot correct mistakes. For example, pressing Backspace doesn't erase the previous character — it's just another ASCII code. To handle this properly, you'd need to implement logic that detects Backspace and reverts the previous input.
- To simplify user interaction, the system uses an **input buffer**. Keystrokes are stored in this buffer before being passed to the program. This solves some problems, but introduces others: when waiting for Enter to confirm input, remember that Enter is actually **two ASCII characters** — CR (Carriage Return, 13) and LF (Line Feed, 10). As a result, one of these characters may remain in the buffer, causing the next call to getchar() or scanf() to behave incorrectly — it might read leftover input.

---

# Getchar() & scanf()

- To avoid this, you should **clear the input buffer** before reading new data. Since standard functions don’t do this automatically, the simplest solution is to define a macro:

```c
#define clearBuffer() while (getchar() != '\n’);
```

- and call clearBuffer() after each keyboard input operation.

---

# Thank you

- Jakub Leszek Pach
- <jpach@mtech.edu>
