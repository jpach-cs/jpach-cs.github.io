---
marp: true
theme: pach
paginate: true
footer: "CSCI 112 | Programming with C | J. L. Pach"
title: "CSCI 112  Programming with C"
---

<!-- _class: lead -->

# CSCI 112<br><br>Programming with C

- Lecture 6
- Dr. Jakub L. Pach
- Fall 2025

---

<!-- _class: fit-90 -->

# Outline

- Review
- Printing / scanning a number as ASCII
- printf:
  - complex examples
  - Hex & octal
- Switch statement
- goto statement
- Ternary conditional operator

---

# Review

---

<!-- _class: fit-90 -->

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

# Printing / scanning a number as ASCII

---

# Printing a number as ASCII

```c
int number = 123;
printf("%d\n", number);
// On the screen, we'll display the integer 123 as a sequence of ASCII characters.
// The ASCII codes for the digits are: '1' = 49, '2' = 50, '3' = 51.
// To do this manually, we first need to isolate each digit.
int units, tens, hundreds;
units = number % 10;      // units = 3
number = number / 10;     // number = 12
tens = number % 10;       // tens = 2
hundreds = number / 10;   // hundreds = 1
// Now, we convert each integer digit to its ASCII character equivalent.
// The ASCII value for the character '0' is 48.
// By adding 48 to each digit, we get the correct ASCII code.
printf("%c%c%c\n", hundreds + 48, tens + 48, units + 48);
```

Result:

```text
123
123
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

---

# Printing a number as ASCII

When we display text on a console, anywhere on a computer, we must remember that everything we see is represented by ASCII characters. Each character has its own decimal value from the ASCII table. When we see the number 123 on the screen, it is not an integer but its textual representation. These are the ASCII characters '1' (which has a decimal value of 49), '2' (with a value of 50), and '3' (with a value of 51). The process of displaying a decimal number on the screen via a function like printf is performed automatically, following a similar algorithm to the one shown.

---

# Scanning a number as ASCII

```c
int units, tens, hundreds, number;
// Read a character from the keyboard immediately without waiting for 'Enter'.
// The ASCII value of the character is stored in the 'hundreds' variable.
hundreds = getche();
// Read the second character (the tens digit) from the keyboard.
tens = getche();
// Read the third character (the units digit) from the keyboard.
units = getche();
// Print a new line to move the cursor to the next line on the console.
printf("%s", "\n");
// Convert the ASCII characters into a single integer number.
// We subtract 48 (the ASCII value of '0') from each character's ASCII value to get its
// corresponding integer value.
// The hundreds digit is multiplied by 100, the tens digit by 10, and the units digit by 1.
// These values are then summed to form the final integer.
number = (hundreds - 48) * 100 + (tens - 48) * 10 + (units - 48);
// Print the final integer number to the console using the %d format specifier.
printf("%d\n", number);
```

---

# Scanning a number as ASCII

Scanning a number as ASCII is the process of converting a sequence of characters representing a number into its numerical value in a computer's memory. This is the reverse process of printing and is crucial for programs that need to accept numerical input from a user.

---

# atof() & atoi() functions

To convert a char array (string) containing an integer number, we can use the atoi() function (ASCII to int), which returns the converted value as an int. Similarly, the atof() function (ASCII to float) converts the char array to a float. After the conversion, arithmetic operations on these numbers become possible. To use these functions, it is necessary to include the &lt;stdlib.h&gt; header.

```c
char floatString[] = "3.14159";
char intString[] = "255";

float x = atof(floatString);
int y = atoi(intString);

printf("%f", x + y );
```

Result:

```text
258.141590
```

---

# What will you see?

```c
int main()
{
  char text[] = { 72, 101, 108 ,108, 111, 32, 87, 111, 114, 108, 100, 10, 13, 0 };
  printf("%s", text);
}
```

Result:

```text
Hello World
```

```c
int main()
{
  char text[] = { 72, 101, 0 ,108, 111, 32, 87, 111, 114, 108, 100, 10, 13, 0 };
  printf("%s", text);
}
```

Result:

?

---

# What will you see?

The printf function does not read a character array from the first to the last element we reserved, but instead it continues until it encounters the special null-terminator character '\0'. This convention comes from older languages such as Assembly. The same rule applies to most functions that operate on strings (character arrays) in C. For example, when we create a character array like: char arr[] = "Hello"; we provided 5 ASCII characters, but the actual length of the array is 6. The compiler automatically appends one extra byte at the end to store the terminating '\0'. Thanks to this, functions like printf know where the string ends.

```c
int main()
{
  char text[] = { 72, 101, 0 ,108, 111, 32, 87, 111, 114, 108, 100, 10, 13, 0 };
  printf("%s", text);
}
```

Result:

```text
He
```

---

# atof() & atoi() functions

```c
// Reserve space for a 3-character string + null terminator ('\0')
char stringNumber[4] = {'\0','\0','\0','\0'};
// Ask the user for a 3-digit number (with leading zeros if needed)
printf("%s\n", "Give me a 3-digit number. If less than 100, please write 091 etc.");
// Read three characters one by one directly from keyboard (echoed on screen)
stringNumber[0] = getche();
stringNumber[1] = getche();
stringNumber[2] = getche();
// Print a newline for readability
printf("%s", "\n");
// Show the string entered by the user
printf("%s\n", stringNumber);
// Convert the string (ASCII chars) into an integer value
int number = atoi(stringNumber);
int ten = 10;
// Print the integer value increased by 10
printf("%d\n", number + ten);
```

Result:

```text
258.141590
```

Result:

```text
Give me a 3-digit number. If less than 100, please write 091 etc.
321
321
331
```

---

# complex examples of printf

---

# complex examples of printf

```c
int main()
{
    // 1. Right-justify with a width of 10, displaying an integer
    printf("%10d\n", 123);  // Output: "       123" (7 spaces before 123)
    // 2. Left-justify with a width of 10, displaying a floating-point number
    printf("%-10f\n", 123.456);  // Output: "123.456000 " (with 3 spaces after)
    // 3. Pad with leading zeros, width of 8 for an integer
    printf("%08d\n", 123);  // Output: "00000123" (padded with zeros)
    // 4. Floating-point with 2 decimal places, right-justified, width of 8
    printf("%8.2f\n", 123.456);  // Output: "  123.46" (2 spaces before the number)
    // 5. Displaying an integer with the '+' flag to show the sign
    printf("%+d\n", 123);  // Output: "+123"
    printf("%+d\n", -123); // Output: "-123"
    // 6. Using a width specifier for strings, right-justified
    printf("%10s\n", "hello");  // Output: "     hello" (5 spaces before)
    // 7. Using width and precision with strings
    printf("%10.3s\n", "hello");  // Output: "       hel" (cut to 3 chars, 7 spaces)
    // 8. Display a floating-point number in scientific notation
    printf("%12.3e\n", 123456.789);  // Output: " 1.235e+05" (total width of 12)
    // 9. Using the 'l' modifier for long integers
    printf("%ld\n", 1234567890L);  // Output: "1234567890"
    // 10. Hexadecimal integer with leading '0x', width of 10, left-justified
    printf("%-#10x\n", 255);  // Output: "0xff      " (3 spaces after)
}
```

Result:

```text
       123
123.456000
00000123
  123.46
+123
-123
     hello
       hel
  1.235e+005
1234567890
0xff
```

<!-- This line is where the magic happens. It assigns the address of the variable x to the pointer pointer. The & symbol is the "address-of" operator. So, pointer now holds the memory location where the value 5 for x is stored. -->

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

# Hex & Octal

```c
int main()
{
    int y;
    char stringNumber[4] = {'\0','\0','\0','\0'};
    printf("Enter a 3-digit value for y: ");
    stringNumber[0] = getche();
    stringNumber[1] = getche();
    stringNumber[2] = getche();
    printf("\n");
    y  = atoi(stringNumber);
    printf("Value of y in HEX is = %x\n", y);
    printf("Value of y in Octal is = %o\n", y);
}
```

Result:

```text
Enter a 3-digit value for y: 255
Value of y in HEX is = ff
Value of y in Octal is = 377
```

- Is it possible to nicely format the result display?

---

# Hex & Octal

```c
int main()
{
    int y;
    char stringNumber[4] = {'\0','\0','\0','\0'};
    printf("Enter a 3-digit value for y: ");
    stringNumber[0] = getche();
    stringNumber[1] = getche();
    stringNumber[2] = getche();
    printf("\n");
    y  = atoi(stringNumber);
    printf("Value of y in HEX\tis = %x\n", y);
    printf("Value of y in Octal\tis = %o\n", y);
}
```

Result:

```text
Enter a 3-digit value for y: 255
Value of y in HEX       is = ff
Value of y in Octal     is = 377
```

- Is it possible to get uppercase letters in Hex?

---

# Hex & Octal

```c
int main()
{
    int y;
    char stringNumber[4] = {'\0','\0','\0','\0'};
    printf("Enter a 3-digit value for y: ");
    stringNumber[0] = getche();
    stringNumber[1] = getche();
    stringNumber[2] = getche();
    printf("\n");
    y  = atoi(stringNumber);
    printf("Value of y in HEX\tis = %X\n", y);
    printf("Value of y in Octal\tis = %o\n", y);
}
```

Result:

```text
Enter a 3-digit value for y: 255
Value of y in HEX       is = FF
Value of y in Octal     is = 377
```

---

# Switch statement

---

# switch statement

```c
switch (expression)
{
 case <constant-expression1>:
 /* code */
  break;

 case <constant-expression2>:
 /* code */
  break;

 default:
 /* code */
  break;
}
```

```c
int main()
{
  int x; scanf("%d", &x);
  printf("%s","a variable x is ");
  switch (x)   /* constant-expression */
  {
    case 1:
      printf("%s\n","1");
      break;
    case 2:
      printf("%s\n","2");
      break;
    default:
      printf("%s\n","not between 1 and 3");
      break;
  }
}
```

Result:

```text
4
a variable x is not between 1 and 3
```

In C programming, a **constant expression** is an expression that evaluates to a fixed value at compile time, meaning the value is determined during the compilation process rather than during program execution.

---

# switch statement

```c
int main()
{
  int x = getche()-48;
  printf("%s", "a variable x is ");
  switch (x)   /* constant-expression */
  {
    case 1:
      printf("%s\n","1");
      break;
    case 2:
      printf("%s\n","2");
      break;
  }
}
```

Result:

```text
2
a variable x is 2
```

- The default block in the switch statement is optional!
- The default block can be used for error handling.
- It's important to note that omitting the default block will cause the program to skip the entire switch statement if the variable takes on a value not defined in the switch statement.

---

# switch statement

```c
int main()
{
  int x = getche()-48;
  printf("%s", "a variable x is ");
  switch (x)   /* constant-expression */
  {
    case 1:
    case 2:
    case 3:
      printf("%s\n", "between 1 and 3");
      break;
    default:
      printf("%s\n", "not between 1 and 3");
      break;
  }
}
```

Result:

```text
2
a variable x is  1 and 3
```

- To terminate a switch statement, we use the break keyword

```c
int main()
{
  int x = getche()-48;
  printf("%s", "a variable x is ");
  switch (x)   /* constant-expression */
  {
    case 1:
      printf("%s", "between");
    case 2:
      printf("%s", " 1 and");
    case 3:
      printf("%s\n", " 3");
      break;
    default:
      printf("%s\n", "not between 1 and 3");
      break;
  }
}
```

OR

<!-- Similar to labels used with goto keyword -->

---

# Difference between switch & if-else

- if statements:
  - Dynamic Conditions: if statements allow for dynamic conditions that can change during program execution. These conditions can involve complex expressions, function calls, and even user input.
- switch statements:
  - Static Values: switch statements are primarily designed for evaluating expressions against a set of predefined, static values. These values are typically determined before program execution.

---

# goto statement

---

# goto statement

- goto allows us to jump\* unconditionally to a location identified by a label
- a simple example of Spaghetti Code <br>- Dijkstra, E. W. (1968)
- \*within the same function

```c
int main()
{
  bool is_true = true;
  if ( is_true )
    goto label1;
  else
    goto label2;

  label1:
    printf("It was true\n");
    goto end;
  label2:
    printf("It was false\n");
    goto end;
  end:
}
```

Result:

```text
It was true
```

---

# Ternary conditional operator

---

# Ternary conditional operator ?:

- If expression1 evaluates to true, the ternary operator returns the value of expression2. Otherwise, it returns the value of expression3.

```c
<expression1> ? <expression2>: <expression3>;
```

```c
int main()
{
  int i = 1;
  i = (i > 0) ? 2 : 3;	 /* ternary conditional */
  printf("%d\n", i);
}
```

Result:

```text
2
```

---

# If-else statement

```c
int main()		/* Program Counter =01;		PC++; “goto” new PC	 	*/
{				/* Program Counter =02;		PC++; “goto” new PC	 	*/
 if ( x > 0 )		/* if x>0 then PC = 04 otherwise PC = 10; “goto” new PC	*/
  {				/* Program Counter =04;		PC++; “goto” new PC		*/
   ;				/* Program Counter =04;		PC++; “goto” new PC 		*/
   ;				/* Program Counter =04;		PC++; “goto” new PC		*/
   ;				/* Program Counter =04;		PC++; “goto” new PC		*/
  }				/* Program Counter =15; 	  “goto” new PC	 		*/
  else			/* 												*/
  {				/* Program Counter =10;		PC++; “goto” new PC		*/
   ; 			/* Program Counter =11;		PC++; “goto” new PC		*/
   ;				/* Program Counter =12;		PC++; “goto” new PC		*/
   ;				/* Program Counter =13;		PC++; “goto” new PC		*/
  }				/* Program Counter =15; 	  “goto” new PC	 		*/
}				/* Program Counter =15;		PC++; “goto” new PC		*/
```

```text
Line 01
Line 02
Line 03
Line 04
Line 05
Line 06
Line 07
Line 08
Line 09
Line 10
Line 11
Line 12
Line 13
Line 14
Line 15
```

<!-- This is a answer why if statement change state in your computer, because PC may change -->

---

# Is there a way to simulate an if statement without using it?

---

# magic...

```c
int main()
{
	int x = 10;
     int * label_pointer;
     label_pointer = ( x > 0 ) ? &&label_greater: &&label_lower; / equals 08 or 12 */;
     goto *label_pointer;

     label_greater:
      printf("%s\n","a variable x is greater than 0");
      goto end_label;

     label_lower:
      printf("%s\n","a variable x is lower than 0");
      goto end_label;

     end_label:
      ;
}
```

```text
Line 01
Line 02
Line 03
Line 04
Line 05
Line 06
Line 07
Line 08
Line 09
Line 10
Line 11
Line 12
Line 13
Line 14
Line 15
Line 16
Line 17
Line 18
```

---

# Thank you

- Jakub Leszek Pach
- <jpach@mtech.edu>
