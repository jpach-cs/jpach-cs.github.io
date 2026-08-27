---
marp: true
theme: pach
paginate: true
title: "CSCI 112  Programming with C"
---

<!-- _class: lead -->

# CSCI 112<br><br>Programming with C

- Lecture 5
- Dr. Jakub L. Pach
- Fall 2025

---

![w:277px Graphic 3](assets/image2.png)

---

# Outline

- Review
- Control Flow – If statement
- printf

---

# Review

---

# Accessing Array Elements

- tab\[index\] is used both to read and write values.
- Array indices in C start from 0.
- Make sure the index is within the declared size (here 0–2).
- Each element in the array is stored contiguously in memory.

```c
#include <stdio.h>
int main()
{
    // Declare an array of 3 integers
    int tab[3];
    // Store values into the array
    tab[0] = 5;   // put 5 into the first element
    tab[1] = 10;  // put 10 into the second element
    tab[2] = 15;  // put 15 into the third element
    // Retrieve values from the array
    int x = tab[0];  // read the first element into variable x
    int y = tab[1];  // read the second element into variable y
    // Display the values
    printf("x = %d\n", tab[0]);  // prints 5
    printf("y = %d\n", tab[1]);  // prints 10
    return 0;
}
```

Result:

```text
x = 5
y = 10
```

---

# Logical vs Bitwise Operators

```c
unsigned int x = 6;             // 00000000 00000000 00000000 0000 0110 (binary)
unsigned int y = 3;             // 00000000 00000000 00000000 0000 0011 (binary)
//Bitwise AND, OR, NOT, XOR
// AND &
printf("%u\n", x & y);          // (00000000 00000000 00000000 0000 0010) = 2
// OR  |
printf("%u\n", x | y);          // (00000000 00000000 00000000 0000 0111)  = 7
// NOT ~ (flips all bits)
printf("%u\n", ~x);             // (11111111 11111111 11111111 1111 1001) = 4 294 967 289
// XOR ^
printf("%u\n", x ^ y);          // (00000000 00000000 00000000 0000 0101) = 5
//Logical AND, OR, NOT, XOR
// AND &
printf("%d\n", x && y);         // (00000000 00000000 00000000 0000 0001) = 1 (true)
// OR  |
printf("%d\n", x || y);         // (00000000 00000000 00000000 0000 0001) = 1 (true)
// NOT !
printf("%d\n", !x);             // (00000000 00000000 00000000 0000 0000) = 0 (false)
// XOR doesn't exist but =  (a || b) && !(a && b);
printf("%d\n", (x || y) && !(x && y));
                                // (00000000 00000000 00000000 0000 0000) = 0 (false)

printf("%d\n", -1 && -2);       // (00000000 00000000 00000000 0000 0001) = 1 (true)
```

Result:

```text
2
7
4294967289
5
1
1
0
0
1
```

---

# Operator Sizeof()

The sizeof operator returns the size of a type(requires parentheses) or variable in bytes.

- It is a unary operator, just like a cast, and has the same precedence level.
- It is easy to mistake sizeof for a function, but it is not — it is evaluated at compile time.

```c
    long long x;
    printf("%d\n", sizeof(x));
    printf("%d\n", sizeof x );
    printf("%d\n", sizeof(long long));
    short y;
    printf("%d\n", sizeof(y));
    printf("%d\n", sizeof y );
    printf("%d\n", sizeof(short) );
    float z;
    printf("%d\n", sizeof(z));
    printf("%d\n", sizeof z );
    printf("%d\n", sizeof(float) );
```

Result:

```text
8
8
8
2
2
2
4
4
4
```

---

# limits.h & float.h

```c
printf("CHAR_MIN           = %d\n", CHAR_MIN);
printf("CHAR_MAX           = %d\n", CHAR_MAX);
printf("UCHAR_MAX          = %u\n", UCHAR_MAX);
// short
printf("SHRT_MIN           = %d\n", SHRT_MIN);
printf("SHRT_MAX           = %d\n", SHRT_MAX);
printf("USHRT_MAX          = %u\n", USHRT_MAX);
// int
printf("INT_MIN            = %d\n", INT_MIN);
printf("INT_MAX            = %d\n", INT_MAX);
printf("UINT_MAX           = %u\n", UINT_MAX);
//float
printf("FLT_SMALLEST       = %e\n", FLT_MIN);
printf("FLT_MIN            = %f\n", -FLT_MAX);
printf("FLT_MAX            = %f\n", FLT_MAX);
printf("FLT_MAX            = %e\n", FLT_MAX);
```

Result:

```text
CHAR_MIN           = -128
CHAR_MAX           = 127
UCHAR_MAX          = 255
SHRT_MIN           = -32768
SHRT_MAX           = 32767
USHRT_MAX          = 65535
INT_MIN            = -2147483648
INT_MAX            = 2147483647
UINT_MAX           = 4294967295
FLT_SMALLEST       = 1.175494e-038
FLT_MIN            =
-340282346638528859811704183484516925440.000000
FLT_MAX            =
 340282346638528859811704183484516925440.000000
FLT_MAX            = 3.402823e+038
```

---

# putchar() & getche() without '\n'

```c
int putchar(int);
putchar(c) puts the character c on the standard output.
it returns the character printed or EOF on error(-1).
int getche(void);
returns the next character from standard input.
it returns EOF on error.
```

```c
int main()
{
    char character;
    character = getche();   // Read a single key from the keyboard and immediately display it (echo)
    putchar(character);     // Display the value of 'character' using putchar (prints the same key again)

    character = getche();   // Read another single key (char is enough, automatic casting occurs)
    putchar(character);     // Display the second key pressed
}
```

Result:

```text
aaBB
```

---

# putchar() & getche()

```c
int putchar(int);
putchar(c) puts the character c on the standard output.
it returns the character printed or EOF on error(-1).
int getche(void);
returns the next character from standard input.
it returns EOF on error.
```

```c
int main()
{
    char character;
    character = getche();   // Read a single key from the keyboard and immediately display it (echo)
    printf("%s", "\n");     // Print newline (CRLF) to move to the next line for clarity
    putchar(character);     // Display the value of 'character' using putchar (prints the same key again)
    printf("%s", "\n");     // Print another newline to separate outputs


    character = getche();   // Read another single key (char is enough, automatic casting occurs)
    printf("%s", "\n");     // Print newline to move to next line
    putchar(character);     // Display the second key pressed
    printf("%s", "\n");     // Final newline for clean output
}
```

Result:

```text
a
a
B
B
```

---

# Basics of

- The format requires a string enclosed in double quotes ("&lt;string&gt;").
- If we want to display the contents of our variables, such as int types, we must use the % symbol followed by the type. This allows displaying a value from memory interpreted as the given type and after we must provide the name of the variable that will be read. Each instance of %&lt;type&gt; will allow us to display the contents of one variable.

```c
int main()
{
  int x = 5;
  int y = 7;
  printf ("%s\n", "Hello world\n");
  printf("%d\n", x);
  printf("Value of x = %d, and value of y = %d\n", x, y);
  printf("%d %d\n", x, y, x, x);
}
```

Result:

```text
Hello world
5
Value of x = 5, and value of y = 7
5 7
```

```c
int printf (char format[], arg1, arg2 ,...);
```

<!-- While printf resembles Python's print function, and Python can utilize C-style formatting, the reverse is not true. This concept can be illustrated by the relationship between a square and a rectangle. -->

---

# Control Flow

---

# if-else statement

```text
expression1 is non-zero ⇒ statement1
expression1 could be series of expressions
Block can be substitute for simple_statement
else is optional

```

```c
if (expression1)
	single_statement1
else
	single_statement2
```

---

# if-else statement

```c
int main()
{
    int x = 5;
    if( x > 1 )
          printf("%s\n", "a variable x is greater than 1");
}
```

- Why is an if-else statement considered a statement when it doesn't change anything on its own?
- It's not true that it doesn't change the PC, but to explain that we need to understand ternary operator and labels.

Result:

```text
a variable x is greater than 1
```

---

# if-else statement

- With optional else

```c
int main()
{
    int x = 5;
    if( x > 1 )
          printf("%s\n", "a variable x is greater than 1");
    else
          printf("%s\n", "a variable x is NOT greater than 1");
}
```

Result:

```text
a variable x is greater than 1
```

---

# if-else statement

```c
int main()
{
    int x = 0;
    if( x > 1 )
    {
      printf("%s", "a variable x");
      printf("%s\n"," is greater than 1");
    }
    else
    {
      printf("%s", "a variable x");
      printf("%s\n"," is not greater than 1");
    }
}
```

Result:

```text
a variable x is not greater than 1
```

---

# nested if-else statement

```c
int main()
{
  int x = 1;

  if(x == 0)
  ;
  else if(x == 1)
  ;
  else if(x > 2)
  ;
  else
  ;
}
```

```c
int main()
{int x = 1;
  if(x == 0)
  {

  }
  else
  if(x == 1)
  {

  }
  else
  if(x > 2)
  {

  }
  else
  {

  }
}
```

Since an if statement following its condition in parentheses (the expression that, if it evaluates to a non-zero value, executes the subsequent code block) is considered a statement itself, it's important to note that another if statement can be placed after either the code block of the first if or its else block (if present).

---

```c
if(x == 0)
{

}
else
if(x == 1)
{

}
else
if(x > 2)
{

}
else
{

}
```

```c
int main()
{
int x; scanf("%d", &x);
printf("%s","a variable x is ");

if(x == 0)
{
  printf("%s\n","0");
}
else
{
  if(x == 1)
  {
        printf("%s\n","1");
  }
  else
  {
    if(x > 1 && x < 5)
    {
        printf("%s\n","between 2 and 4");
    }
    else
    {
      printf("%s\n","not between 0 and 4");
    }
  }
}
}

```

```c
int main()
{
  int x = 1; scanf("%d", &x);
  printf("%s","a variable x is ");

  if(x > 0)
    if(x < 5)
      printf("%s\n", "between 1 and 4");

}
```

---

```c
printf(char format[],  arg1,  arg2 ,...)
scanf (char format[], *arg1, *arg2 ,...)
```

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

# Basic types

|Type & Specifier||Origin|Argument type||Description||
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

# Basic types

|Type & Specifier||Origin|Argument type|Example|Result|
|---|---|---|---|---|---|
|integer|d|decimal|int|printf("%d\n", x);<br>    printf("%d\n", y);|65<br>-6|
||u|unsigned decimal|int|printf("%u\n", x);<br>    printf("%u\n", y);|65<br>4294967290|
||c|character|int|printf("%c\n", letter);<br>    printf("%c\n", x);<br>    printf("%d\n", letter);|a<br>A<br>97|
|string|s|string|char \*|printf("%s\n", text);|Some Text|
|floating-point number|f|float|float|printf("%f\n", fRealNumber);<br>    printf("%f\n", dRealNumber);|3.000000<br>33999999999999998856806021345479952957440.000000|
||lf|long float <br>(double)|double|fRealNumber = dRealNumber; <br>    printf("%lf\n", fRealNumber);<br>    printf("%lf\n", dRealNumber);|inf<br>33999999999999998856806021345479952957440.000000|

```c
int main()
{
  unsigned int x = 65;  int y = -6; char letter ='a'; char * text = "Some Text";
  float fRealNumber = 3.0f; double dRealNumber = 3.4e40;
}
```

---

# Conclusions

- *Remember that* signed *and* unsigned integers *are represented differently in computer memory. Using the wrong* format specifier *can lead to incorrect results (e.g., using* %d *for an* unsigned int*).*
- *A* char *is essentially a one-byte* integer*. Therefore, you can treat a* char *variable as either an ASCII character or a small* integer*.*
- *The* float *data type has a smaller range than* double*. Assigning a* double *value to a* float *variable can result in data loss if the value is too large or too small to be represented accurately*
- *The* lf *specifier is used for* double *values, as* d *is already reserved for decimal(*integer*).* <br>*It's important to remember this distinction.*

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

# Precision

```c
int main()
{ int x = 5, y = -6; int * z; float f = 3.1234f; /*code*/ }
```

|Data|Type||Description|Example|Result|
|---|---|---|---|---|---|
|Numbers|integer|d|Figure out what's happening by looking at the examples.|printf("%.1d\n", x); <br>printf("%.5d\n", x);|65<br>00065|
|||u||||
|||c||||
||floating-point number|f||printf("%.6f\n", fRealNumber); <br>printf("%.2f\n", fRealNumber);<br>printf("%.0f\n", fRealNumber);|3.123400<br>3.12<br>3|
|||lf||||
|Text|string|s||printf("%.1s\n", text);<br>printf("%.5s\n", text);<br>printf("%.20s\n", text);|S<br>Some<br>Some Text|

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

# Flags

- \+ : Always display the sign of a number, even if it's positive.
- \- : Left-justify the output within the given field width.
- 0 : Pad the field with zeros instead of spaces.
- \# : Use an alternative form for the conversion specifier.

<!-- **# flag:** Use an alternative form for the conversion specifier. For example, it adds a leading zero for octal numbers or a 0x or 0X prefix for hexadecimal numbers. -->

---

# Flag "+"

```c
int main()
{unsigned int x = 65, y = -6; int * z; float f = 3.1234f; /*code*/ }
```

|Data|Type||Description|Example|Result|
|---|---|---|---|---|---|
|Numbers|integer|d|Always display the sign of a number, even if it's positive.|printf("%+d\n", x);<br>printf("%+d\n", y);|+65<br>-6|
|||u||||
|||c||||
||floating-point number|f||printf("%+f\n", fRealNumber);|+3.123400|
|||lf||||
|Text|string|s|None|None|None|

---

# Flag "-"

```c
int main()
{unsigned int x = 65, y = -6; int * z; float f = 3.1234f; /*code*/ }
```

|Data|Type||Description|Example|Result|
|---|---|---|---|---|---|
|Numbers|integer|d|Left-justify the output within the given field width.|printf("%7d", x);<br>printf("\_next\n");<br>printf("%-7d", x);<br>printf("\_next\n");|65\_next<br>65     \_next|
|||u||||
|||c||||
||floating-point number|f||printf("%13f", fRealNumber); printf("\_next\n");<br>printf("%-13f", fRealNumber);<br>printf("\_next\n");|3.123400\_next<br>3.123400     \_next|
|||lf||||
|Text|string|s||printf("%20s", text);    printf("\_next\n");<br>printf("%-20s", text);<br>printf("\_next\n");|Some Text\_next<br>Some Text           \_next|

<!-- To understand recursion, you must first understand recursion -->

---

# Flag "0"

```c
int main()
{unsigned int x = 65, y = -6; int * z; float f = 3.1234f; /*code*/ }
```

|Data|Type||Description|Example|Result|
|---|---|---|---|---|---|
|Numbers|integer|d|Pad the field with zeros instead of spaces.|printf("%07d\n", x);|0000065\_next|
|||u||||
|||c||||
||floating-point number|f||printf("%013f\n", fRealNumber);|000003.123400\_next|
|||lf||||
|Text|string|s||printf("%020s", text);|00000000000Some Text|

<!-- To understand recursion, you must first understand recursion -->

---

# Flag "#"

- To understand recursion, you must first understand recursion.
- This will be explained in the future, because...

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

# Modifies

```c
int main()
{ short int x = 65;  int y = -69000;
  float fRealNumber = 3.1234f; double dRealNumber = 3.4e50; /*code*/ }
```

|Data|Type||Description|Example|Result|
|---|---|---|---|---|---|
|Numbers|integer|d|Modifier, h and l specify how many bytes should be formatted as a variable. Therefore, if we use short (h - 1 bit) on a normal int (long - 32 bit), we will get an incorrect result because printf will take only 16 bits and build a number representation from it.|printf("%0hd\n", x);<br>printf("%0hd\n", y);<br>printf("%0ld\n", x);<br>printf("%0ld\n", y);|65<br>-3464<br>65<br>-69000|
|||u||||
|||c||||
||floating-point number|f|Since there's no such thing as hf (as hf is simply f), the compiler ignores h, and l represents a double. As you can see, there's no lf type, only f with the l modifier.|printf("%0hf\n", fRealNumber);<br>printf("%0lf\n", fRealNumber);<br>printf("%0hf\n", dRealNumber);<br>printf("%0lf\n", dRealNumber);|3.123400<br>3.123400<br>33999999...<br>339999999999999984402842591433794782958910267457536.000000|
|||lf||||
|Text|string|s|None|None|None|

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

# Do you think it is all?

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

# Thank you

- Jakub Leszek Pach
- <jpach@mtech.edu>

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
  /*Print the value of the sixth element of array c (which is 0)*/
  x = b[0];   /*Assign the value of the first element of array b (which is 1) to variable x*/
  a[1] = y;   /*Assign the value of variable y (which is 2) to the second element of array a*/
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

# Basics of

- The important difference between printf and scanf is that scanf requires its arguments to be pointers (location in memory) .

```c
int main()
{
  int x = 5;          			/* Declaration of variable x and assigning its value 5 */
  int * p;      				/* Declaration of pointer p */
  p = &x;       				/* Assigning the address value of the p variable to the pointer p */
  printf("Enter x value : "); 		/* there is no end of line character here! */
  scanf("%d", &x);     			/* To get a pointer (memory address) */
  printf("Value of x = %d\n", x); 	/* we use a & before the variable name p */
  printf("Enter x value again : ");
  scanf("%d", p);             		/*scanf does not work the same as in python, */
  printf("Value of x = %d\n", x);   /*you have to use printf and scanf separately */
}
```

Result:

```text
Enter x value : 1
Value of x = 1
Enter x value again : 2
Value of x = 2
```

```c
int printf (char format[],  arg1,  arg2 ,...);
```

```c
int scanf  (char format[], *arg1, *arg2 ,...);
```

- The ampersand operator & is a unary operator that returns the memory address, which is the location in memory where a variable is stored.

<!-- This line is where the magic happens. It assigns the address of the variable x to the pointer pointer. The & symbol is the "address-of" operator. So, pointer now holds the memory location where the value 5 for x is stored. -->

---

# Notice

Recently, during my lab work, I made a mistake. It wasn't the development environment's fault, but mine. It was related to the scanf function. Because I'm currently working with Python, C, C++, C#, and MATLAB, I mixed up the behavior of the scanf function. You need to know that the scanf function has one drawback: it doesn't clear the buffer of characters entered from the keyboard. This means that after pressing Enter to confirm the data entered from the keyboard, our variable also contains the Enter character, which is that extra line you asked me to use to clear the buffer. To understand its operation, you need to understand today's new material.
