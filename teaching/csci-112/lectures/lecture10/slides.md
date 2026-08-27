---
marp: true
theme: pach
paginate: true
title: "CSCI 112  Programming with C"
---

<!-- _class: lead -->

# CSCI 112<br><br>Programming with C

- Lecture 10
- Dr. Jakub L. Pach
- Fall 2025

---

![w:277px Graphic 3](assets/image2.png)

---

# Outline

- Review
- Pointer operations
- scanf

---

# Review

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

Result:

```text
cde
aab

```

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

# Basics of

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

Result:

```text
Enter x value : 1
Value of x = 1
```

```c
int printf (char format[],  arg1,  arg2 ,...);
```

```c
int scanf  (char format[], *arg1, *arg2 ,...);
```

---

# const keyword

- We can use const before declaration (and initialization):
  - Array:    Prevents changing the content of the array.
  - Variable:    Prevents changing its value.
  - Pointer:
    - Before the asterisk(\*):    Prevents changing the value it points to.
    - After the asterisk(\*):    Prevents changing the pointer itself.

<!-- (this will be important when we talk about preprocessor constants). -->

---

# const keyword

- const prevents changing the value after its initialization, but it allows debugging.
- In a function definition, const allows control over changing the argument values.
- The compiler ensures the immutability of constants. It will not compile the file if you try to change their value. However, attempting to bypass the restriction (e.g., using a pointer) will always result in incorrect program behavior without informing the programmer.

<!-- (this will be important when we talk about preprocessor constants). -->

---

# Declaring and initializing arrays

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

Result:

```text
First element (index 0) of array a equals 4201200.
Second(index 1) element of array b equals 2.
Second(index 1) element of array b equals 2.
Sixth(index 5) element of array c equals 0.
```

---

# Summary - The \* operator works in **three different ways**

- **Binary multiplication operator**

```c
a * b;  // multiplies a and b
```

- **Unary dereference operator** – used to access the value stored at a given memory address:

```c
int x = 5;
int * y =&x;
y = *ptr + 1;
```

- **Pointer declaration**

– when used in a declaration, it indicates that the variable is a pointer, not a simple type:

```c
int * x;  // x is a pointer to an int
```

This applies to **local variables, global variables, and function parameters** (including arrays).

**Remember**: It’s easy to confuse the **unary dereference operator** \* with the **pointer declaration** \* in a variable definition!

---

# Some examples

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

Result:

```text
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

# Consequences

- Each variable declared has a lower address\*. This is due to the computer's memory architecture. The stack grows downward, so when it's empty, the address is at its maximum value (e.g., FFFFFF). Every time a value is pushed onto the stack, the address is decremented by the size of the data type.
- The \* and &amp; operators are right-associative, so parentheses are not strictly necessary.
- The \* and &amp; operators cancel each other out, meaning that \*&amp;y is equivalent to y.
- Arithmetic operations on pointers differ from those on integer types.
- Pointers to pointers are declared using a double asterisk (\*\*), every extra asterisk means another layer of pointers…
- \*Array elements have the opposite effect!

---

# Function arguments

Function arguments are always **copies** of our variables, and **not** the same memory areas, a function argument, even though it has the same value, is a completely different variable!

---

# by the Value

- Function arguments are always **copies** of our variables, and **not** the same memory areas, a function argument, even though it has the same value, is a completely different variable!

Result:

```text
5
5

```

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

# by the Reference

- Function arguments are always **copies** of our variables, and **not** the same memory areas, a function argument, even though it has the same value, is a completely different variable!

Result:

```text
5
6

```

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

**So, what does it mean?**

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

Result:

```text
x    equals 6422292.
y    equals 6422288.
z    equals 6422284.
pointer equals 6422288.
pointer* equals 7.
pointer[1] equals 5.
```

---

# So, what does it mean?

```c
int a[10];

a[i] == *(a+i)		&a[i] == &*(a+i) == a+i
```

When performing arithmetic operations on pointers, the array index is automatically multiplied by the size of the data type pointed to by the pointer.

For example, if the array stores char values, the index is multiplied by 1, and if it stores int values, the index is multiplied by 4 (assuming an int is 4 bytes).

---

# Conclusions

- The expression a\[i\] is transformed by the compiler into the form \*(a+i).
- The square brackets following the symbolic\_name do not provide any information about whether we are referring to an array.
- When performing arithmetic operations on pointers, the array index is automatically multiplied by the size of the data type pointed to by the pointer.

<!-- define s\[n\] na \*(s + n) -->

---

# const keyword in Array &amp; Pointer

- We can use const before declaration (and initialization):
  - Array: Prevents changing the content of the array.
  - Pointer:
    - Before the asterisk(\*):    Prevents changing the value it points to.
    - After the asterisk(\*):    Prevents changing the pointer itself.
- The compiler ensures the immutability of constants. It will not compile the file if you try to change their value. However, attempting to bypass the restriction (e.g., using a pointer) will always result in incorrect program behavior without informing the programmer.

<!-- (this will be important when we talk about preprocessor constants). -->

---

# const keyword in Pointer

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

Result:

```text
x = 5, y = 7, z = 1


```

---

# const keyword in Array

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

# Conclusions

There are no restrictions on passing an array as a function parameter. However, there's a common misconception: when we write int arr\[\], it may seem like the entire array is copied and we get access to an identical copy. This is not true. The square bracket syntax is primarily a hint for the programmer, as the compiler internally treats it as int const \*arr.

Result:

```text
1
2
3
4
5
6
7

```

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

# Pointer operations

---

# The valid pointer operations are

- Assignment of pointers to the same type,
- Adding or subtracting a pointer and an integer,
- Subtracting or comparing\* two pointers,
- Assigning or comparing to zero (NULL = ‘\0’),
- All other pointer arithmetic is illegal (+, \*, /, &gt;&gt;, &lt;&lt;, etc.).

---

# Subtracting two pointers

The result of subtracting two pointers is the difference in their array indices, not the actual difference in their memory locations

```c
#include <stdio.h>

int strlen(char * string)
{
  char *pointer = string;
  while(*pointer != '\0') /* or NULL or 0 or FALSE */
    pointer++;
  return pointer - string;
}

int main()
{
  char * text = "Hello world!";
  printf("Length of [%s] equals %d\n", text, strlen(text));
  return 0;
}
```

Result:

```text
Length of [Hello world!] equals 12


```

---

# Comparing two pointers

Comparing pointers to strings in C can be significantly optimized, especially when there's a high probability that two strings are identical and point to the same memory location

```c
#include <stdio.h>

int main()
{
  char *str1 = "Hello";
  char *str2 = str1;

  if (str1 == str2)
        printf("Str1 and str2 point to the same string\n");
  else
  { // If addresses are different, then compare the content
    if (strcmp(str1, str2) == 0)
        printf("Str1 and str2 have the same content\n");
    else
        printf("Str1 and str2 are different\n");
  }
  return 0;
}
```

Result:

```text
Str1 and str2 point to the same string


```

<!-- Jesli mamy dwa element tej samej tablicy, i chcemy znalezc element srodkowy tej tablicy mozemy odjac od siebie adresy I uzyskamy od tego element srodkowy -->

---

# Comparing two pointers

- Array elements are pushed onto the stack in reverse order to ensure that element addresses increase.
- If we compare two elements of an array using two pointers, and we don't know which one is closer to the beginning and which one is closer to the end, the one with the higher address value will be closer to the end, and the one with the lower address value will be closer to the beginning of the array.

```c
#include <stdio.h>
int main()
{
  int x = 5, y = 7, z = 9;
  int b[]= { 1, 2, 3, 4 };
  char text[] = "hello";
  char *l1 = &text[2] , *l2 = &text[3];

  printf("%d.\n", &x);
  printf("%d.\n", &y);
  printf("%d.\n\n", &z);

  printf("%d.\n", &b[3]);
  printf("%d.\n", &b[2]);
  printf("%d.\n", &b[1]);
  printf("%d.\n\n", &b[0]);

  printf("%d.\n", &text[3]);
  printf("%d.\n", &text[2]);
  printf("%d.\n", &text[1]);
  printf("%d.\n\n", &text[0]);

  if(l1 < l2)
    printf("l1 is closer to the beginning\n");
  else
    printf("l2 is closer to the beginning\n");
  return 0;
}
```

Result:

```text
6422292.
6422288.
6422284.

6422280.
6422276.
6422272.
6422268.

6422265.
6422264.
6422263.
6422262.

l1 is closer to the beginning
```

<!-- Jesli mamy dwa element tej samej tablicy, i chcemy znalezc element srodkowy tej tablicy mozemy odjac od siebie adresy I uzyskamy od tego element srodkowy -->

---

# Assigning or comparing to zero (NULL = ‘\0’)

Trying to use a null pointer will crash the program.

```c
#include <stdio.h>
int main()
{
  char * a[10] = {NULL};

  a[0] = "Words";
  a[1] = "of";
  a[2] = "different";
  a[3] = "lengths";

  int i;
  for ( i = 0; i < 10; i++ )
    if(a[i])
      printf("%s ", a[i]);
  return 0;
}
```

Result:

```text
Words of different lengths

```

---

# scanf

---

# printf and scanf format specification

- Optional:
  - Flags    -    modifiers that alter the formatting or scanning behavior.
  - Width    -    specifies the minimum width of the output field <br>        or the maximum number of characters to be scanned.
  - Precision    -    controls the precision of floating-point numbers <br>        or the maximum number of characters to be scanned for strings.
  - Modifier    -    indicates the data type size (e.g., long, short).
- Required:
  - Type    -    specifies the data type of the variable to be formatted or scanned.

```text
Format =  %[flags][width][.precision][modifier]<type>
```

---

# Basic types

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

# Width

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

# Precision

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

# Flags

- \+ : Always display the sign of a number, even if it's positive.
- \- : Left-justify the output within the given field width.
- 0 : Pad the field with zeros instead of spaces.
- \# : Use an alternative form for the conversion specifier.

<!-- **# flag:** Use an alternative form for the conversion specifier. For example, it adds a leading zero for octal numbers or a 0x or 0X prefix for hexadecimal numbers. -->

---

# Modifies

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

# Scanf -Basic Types and Width Specifier

```c
#include <stdio.h>
#define clearBuffer() while (getchar() != '\n');

int main()
{
    int age;
    char firstInitial;
    float weight;
    printf("1. Basic Reads and Width:\n");
    // %2d - Limits the read to the first 2 digits. If the user enters "255", only 25 is read.
    printf("Enter Age (2 digits max, e.g., 35): ");
    scanf("%2d", &age);
    clearBuffer();
    // %c - Reads a single character.
    // NOTE: The space before %c is CRITICAL! It instructs scanf to skip leading whitespace,
    // including any leftover '\n' from the previous input.
    printf("Enter First Initial: ");
    scanf(" %c", &firstInitial);
    clearBuffer();
    // %f - Reads a floating-point number.
    printf("Enter Weight (e.g., 75.5): ");
    scanf("%f", &weight);
    clearBuffer();
    printf("Results: Age: %d, Initial: %c, Weight: %.1f\n", age, firstInitial, weight);
}
```

Result:

```text
1. Basic Reads and Width:
Enter Age (2 digits max, e.g., 35): 2222222
Enter First Initial: a
Enter Weight (e.g., 75.5): 76.2
Results: Age: 22, Initial: a, Weight: 76.2
```

- This exercise focuses on the fundamental type specifiers (%d, %c, %f) and introduces the **width** modifier (%2d).

<!-- Jesli mamy dwa element tej samej tablicy, i chcemy znalezc element srodkowy tej tablicy mozemy odjac od siebie adresy I uzyskamy od tego element srodkowy -->

---

# Scanf -Length Modifiers (h and l)

```c
#include <stdio.h>
#define clearBuffer() while (getchar() != '\n');

int main()
{
    int age;
    char firstInitial;
    float weight;
    printf("1. Basic Reads and Width:\n");
    // %2d - Limits the read to the first 2 digits. If the user enters "255", only 25 is read.
    printf("Enter Age (2 digits max, e.g., 35): ");
    scanf("%2d", &age);
    clearBuffer();
    // %c - Reads a single character.
    // NOTE: The space before %c is CRITICAL! It instructs scanf to skip leading whitespace,
    // including any leftover '\n' from the previous input.
    printf("Enter First Initial: ");
    scanf(" %c", &firstInitial);
    clearBuffer();
    // %f - Reads a floating-point number.
    printf("Enter Weight (e.g., 75.5): ");
    scanf("%f", &weight);
    clearBuffer();
    printf("Results: Age: %d, Initial: %c, Weight: %.1f\n", age, firstInitial, weight);
}
```

Result:

```text
2. Length Modifiers (long/short):
Enter a small integer (short): 25
Enter a large integer (long): 66000

Results: Short: 25, Long: 66000
```

Result:

```text
2. Length Modifiers (long/short):
Enter a small integer (short): 67 000
Enter a large integer (long): 1

Results: Short: 67, Long: 1
```

- This exercise demonstrates the length modifiers for integers: **h** (for short) and **l** (for long). These are essential for matching the format specifier to the variable type.

<!-- Jesli mamy dwa element tej samej tablicy, i chcemy znalezc element srodkowy tej tablicy mozemy odjac od siebie adresy I uzyskamy od tego element srodkowy -->

---

# Scanf - Common Errors 1 and Pitfalls

```c
#include <stdio.h>
#define clearBuffer() while (getchar() != '\n');

int main()
{
    printf("\n3. ERROR: Using '\\n' in the scanf format string.\n");
    printf("Enter a value (You will have to press Enter a second time):\n");

    // BAD PRACTICE: scanf("%d\n", &val);
    scanf("%d\n", &val);

    // The program hangs here, waiting for more non-whitespace input to satisfy the '\n' specifier.
    printf("Thank you. The value read is: %d\n", val);
}
```

- A frequent beginner mistake is adding \n to the format string, confusing it with printf. **Never use \n in a scanf format string!** It forces the program to wait for non-whitespace input, confusing the user.

<!-- Jesli mamy dwa element tej samej tablicy, i chcemy znalezc element srodkowy tej tablicy mozemy odjac od siebie adresy I uzyskamy od tego element srodkowy -->

---

# Scanf - Common Errors 2 and Pitfalls

```c
#include <stdio.h>
#define clearBuffer() while (getchar() != '\n');

int main()
{
    int num;
    char character;
    printf("\n4. ERROR: Demonstrating the Buffer Problem (No clearBuffer()).\n");
    printf("Enter a number: ");
    scanf("%d", &num);
    // NO clearBuffer() -> The '\n' from the Enter key remains in the buffer.
    printf("Enter a character (watch what happens): ");
    // This scanf("%c") immediately reads the leftover '\n' as the intended character.
    scanf("%c", &character);

    printf("\nResult: The character read was: '%c' (It should have been your input, but was the newline)\n", character);


}
```

- This highlights why **clearBuffer()** is necessary, especially before reading a character (%c).

<!-- Jesli mamy dwa element tej samej tablicy, i chcemy znalezc element srodkowy tej tablicy mozemy odjac od siebie adresy I uzyskamy od tego element srodkowy -->

---

# Scanf - Best Practice: Reading Multiple Variables

```c
#include <stdio.h>
#define clearBuffer() while (getchar() != '\n');

int main()
{
    int day, month, year;
    printf("\n5. BEST PRACTICE: Reading multiple variables with one scanf call.\n");
    printf("Enter the date in DD MM YYYY format (separated by spaces/Enter): ");

    // scanf automatically skips whitespace between %d specifiers.
    // The user can type: 15 [space] 12 [Enter] 2023 [Enter]
    scanf("%d %d %d", &day, &month, &year);
    clearBuffer(); // Clear the buffer only once at the end.
    printf("\nResult: Date: %d-%d-%d\n", year, month, day);

}
```

Result:

```text
5. BEST PRACTICE: Reading multiple variables with one scanf call.
Enter the date in DD MM YYYY format (separated by spaces/Enter): 2 08 1988

Result: Date: 1988-8-2
```

<!-- Jesli mamy dwa element tej samej tablicy, i chcemy znalezc element srodkowy tej tablicy mozemy odjac od siebie adresy I uzyskamy od tego element srodkowy -->

---

# Scanf - Summary of Best Practices

- Always use &amp;: Remember that scanf requires the address of the variable (&amp;variable) to store the new value.
- Use clearBuffer(): Call the macro AFTER EVERY scanf call, unless you are reading multiple numeric variables in one go.
- No \n in Format String: Never include the newline character (\n) in the scanf format string.
- Whitespace before %c: When reading a single character after reading anything else, use a space: scanf(" %c", ...) to explicitly skip any lingering whitespace.
- Check Return Value: For robust code, always check the value returned by scanf (the count of items successfully read) to validate user input.

<!-- Jesli mamy dwa element tej samej tablicy, i chcemy znalezc element srodkowy tej tablicy mozemy odjac od siebie adresy I uzyskamy od tego element srodkowy -->

---

# Thank you

- Jakub Leszek Pach
- <jpach@mtech.edu>

---

# Some examples

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

Result:

```text
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
