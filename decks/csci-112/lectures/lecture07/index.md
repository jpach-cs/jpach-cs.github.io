---
marp: true
theme: pach
paginate: true
title: "CSCI 112  Programming with C"
---

# CSCI 112<br><br>Programming with C

- Lecture 7
- Dr. Jakub L. Pach
- Fall 2025

---

![Graphic 3](assets/image2.png)

---

## Outline

- Review
- Loop statements
- Functions
- Global &amp; local variables

---

# Review

---

## switch statement

- switch (expression)
- {
- case &lt;constant-expression1&gt;:
- /\* code \*/
- break;
- case &lt;constant-expression2&gt;:
- /\* code \*/
- break;
- default:
- /\* code \*/
- break;
- }
- int main()
- {
-   int x; scanf("%d", &amp;x);
-   printf("%s","a variable x is ");
-   switch (x)   /\* constant-expression \*/
-   {
-     case 1:
-       printf("%s\n","1");
-       break;
-     case 2:
-       printf("%s\n","2");
-       break;
-     default:
-       printf("%s\n","not between 1 and 3");
-       break;
-   }
- }
- 4
- a variable x is not between 1 and 3
- Result:

In C programming, a **constant expression** is an expression that evaluates to a fixed value at compile time, meaning the value is determined during the compilation process rather than during program execution.

---

## switch statement

- int main()
- {
-   int x = getche()-48;
-   printf("%s", "a variable x is ");
-   switch (x)   /\* constant-expression \*/
-   {
-     case 1:
-       printf("%s\n","1");
-       break;
-     case 2:
-       printf("%s\n","2");
-       break;
-   }
- }
- 2
- a variable x is 2
- Result:
- The default block in the switch statement is optional!
- The default block can be used for error handling.
- It's important to note that omitting the default block will cause the program to skip the entire switch statement if the variable takes on a value not defined in the switch statement.

---

## switch statement

- int main()
- {
-   int x = getche()-48;
-   printf("%s", "a variable x is ");
-   switch (x)   /\* constant-expression \*/
-   {
-     case 1:
-     case 2:
-     case 3:
-       printf("%s\n", "between 1 and 3");
-       break;
-     default:
-       printf("%s\n", "not between 1 and 3");
-       break;
-   }
- }
- 2
- a variable x is  1 and 3
- Result:
- To terminate a switch statement, we use the break keyword
- int main()
- {
-   int x = getche()-48;
-   printf("%s", "a variable x is ");
-   switch (x)   /\* constant-expression \*/
-   {
-     case 1:
-       printf("%s", "between");
-     case 2:
-       printf("%s", " 1 and");
-     case 3:
-       printf("%s\n", " 3");
-       break;
-     default:
-       printf("%s\n", "not between 1 and 3");
-       break;
-   }
- }
- OR

<!-- Similar to labels used with goto keyword -->

---

## atof() &amp; atoi() functions

To convert a char array (string) containing an integer number, we can use the atoi() function (ASCII to int), which returns the converted value as an int. Similarly, the atof() function (ASCII to float) converts the char array to a float. After the conversion, arithmetic operations on these numbers become possible. To use these functions, it is necessary to include the &lt;stdlib.h&gt; header.

char floatString\[\] = "3.14159";

char intString\[\] = "255";<br>

float x = atof(floatString);

int y = atoi(intString);<br>

printf("%f", x + y );

- 258.141590
- Result:

---

## atof() &amp; atoi() functions

// Reserve space for a 3-character string + null terminator ('\0')

char stringNumber\[4\] = {'\0','\0','\0','\0'};

// Ask the user for a 3-digit number (with leading zeros if needed)

printf("%s\n", "Give me a 3-digit number. If less than 100, please write 091 etc.");

// Read three characters one by one directly from keyboard (echoed on screen)

stringNumber\[0\] = getche();

stringNumber\[1\] = getche();

stringNumber\[2\] = getche();

// Print a newline for readability

printf("%s", "\n");

// Show the string entered by the user

printf("%s\n", stringNumber);

// Convert the string (ASCII chars) into an integer value

int number = atoi(stringNumber);

int ten = 10;

// Print the integer value increased by 10

printf("%d\n", number + ten);

- 258.141590
- Result:
- Give me a 3-digit number. If less than 100, please write 091 etc.
- 321
- 321
- 331
- Result:

---

## Hex &amp; Octal

- int main()
- {
  - int y;
  - char stringNumber\[4\] = {'\0','\0','\0','\0'};
  - printf("Enter a 3-digit value for y: ");
  - stringNumber\[0\] = getche();
  - stringNumber\[1\] = getche();
  - stringNumber\[2\] = getche();
  - printf("\n");
  - y  = atoi(stringNumber);
  - printf("Value of y in HEX\tis = %X\n", y);
  - printf("Value of y in Octal\tis = %o\n", y);
- }
- Enter a 3-digit value for y: 255
- Value of y in HEX       is = FF
- Value of y in Octal     is = 377
- Result:

---

## goto statement

- goto allows us to jump\* unconditionally to a location identified by a label
- a simple example of Spaghetti Code <br>- Dijkstra, E. W. (1968)
- \*within the same function
- int main()
- {
-   bool is\_true = true;
-   if ( is\_true )
-     goto label1;
-   else
-     goto label2;
- <br>  label1:
-     printf("It was true\n");
-     goto end;
-   label2:
-     printf("It was false\n");
-     goto end;
-   end:
- }
- It was true
- Result:

---

## Ternary conditional operator ?

- If expression1 evaluates to true, the ternary operator returns the value of expression2. Otherwise, it returns the value of expression3.

&lt;expression1&gt; ? &lt;expression2&gt;: &lt;expression3&gt;;

- int main()
- {
-   int i = 1;
-   i = (i &gt; 0) ? 2 : 3;     /\* ternary conditional \*/
-   printf("%d\n", i);
- }
- 2
- Result:

---

# Loop statements

---

## while loop

- while (expression1)
- statement1;

A while loop repeatedly executes statement1 based on the logical outcome of expression1 as long as expression1 evaluates to true.

- a value of i is: 0
- a value of i is: 1
- a value of i is: 2
- Result:
- int main()
- {
-   int i = 0;
-   while ( i &lt; 3 )
-   {
-     printf("a value of i is: %d\n", i);
-     i = i + 1;
-   }
- }
- int main()
- {
-   int i = 0;
-   while ( i &lt; 3 )
-     printf("a value of i is: %d\n", i++);
- }
- OR

---

## while loop

- while (expression1)
- statement1;

A while loop repeatedly executes statement1 based on the logical outcome of expression1 as long as expression1 evaluates to true.

- a value of i is: 0
- a value of i is: 1
- a value of i is: 2
- Result:
- int main()
- {
-   int i = 0;
-   while ( i &lt; 3 )
-   {
-     printf("a value of i is: %d\n", i);
-     i++;
-   }
- }
- int main()
- {
-   int i = 0;
-   while ( i &lt; 3 )
-     printf("a value of i is: %d\n", i++);
- }
- OR

---

## while loop

- a value of i is: 0
- a value of i is: 1
- a value of i is: 2
- Result:
- int main()
- {
-   int i = -1;
-   while ( ++i &lt; 3 )
-     printf("a value of i is: %d\n", i);
- }
- OR
- int main()
- {
-   int i = 0;
-   while ( i &lt; 3 )
-     printf("a value of i is: %d\n", i++);
- }
- int main()
- {
-   int i = 0;
-   while ( i &lt; 3 )
- {
-     printf("a value of i is: %d\n", i);
- i = i + 1;
- }
- }

---

## for loop

- for (expression1; expression2; expression3)
- statement1;
- A for loop repeatedly executes statement1 based on the logical outcome of expression2 as long as expression2 evaluates to true.
- Most commonly expression1 and expression3 are assignments of function calls and expression2 is  a relational expression.
- Any of the three part can be omitted, although the semicolons must be remain. If expression2 is not present, it is taken as permanently true.
- a value of i is: 0
- a value of i is: 1
- a value of i is: 2
- Result:
- int main()
- {
-   for (int i = 0; i &lt; 4; i++ )
-     printf("a value of i is: %d\n", i);
- }

---

## The for loop is equivalent to while loop

- expression1;
- while (expression2)
- {
- statement1;
- expression3;
- }
- for (expression1; expression2; expression3)
- {
- statement1;
- }

---

## “Infinity” loop

- while (true)
- {
- ;
- }
- for (;;)
- {
- ;
- }

---

## do-while loop

- do
- statement1;
- while(expression1)

A do-while loop executes statement1, then checks the logical outcome of expression1. If expression1 evaluates to true, the loop repeats; otherwise, the loop terminates.

- Enter a positive number: -9
- Enter a positive number: 2
- You entered: 2
- Result:
- int main()
- {
-   int number;
- <br>  do
-   {
-       printf("Enter a positive number: ");
-       scanf("%d", &amp;number);
-   }
-   while (number &lt;= 0);
- <br>  printf("You entered: %d\n", number);
- }
- semicolon!

---

## Simulating a do-while loop with while loop

- int main()
- {
-   bool flag = true;
-   while (flag)
-   {
-       printf("This code will execute at least once.\n");
-       if (! (/\* condition \*/) )
-           flag = false;
-   }
- }
- \*In Python we don’t have do\_while.

---

## An example

- Enter a positive number: -9
- Enter a positive number: 2
- You entered: 2
- Result:
- int main()
- {
  - int number;
  - bool flag = true;
  - while (flag)
  - {
  -     printf("Enter a positive number: ");
  -     scanf("%d", &amp;number);
  -     if (! (number &lt;= 0) )
  -         flag = false;
  - }
  - printf("You entered: %d\n", number);
- }

---

## break &amp; continue keywords

- break and continue offer distinct ways to control loop flow.
- break instantly terminates the loop it's in, while continue jumps to the next iteration.
- When nested, break affects only the immediate loop.
- break is also applicable in switch statements to exit a specific case
- int main()
- {
-   for (int i = 1; i &lt;= 10; i++)
-   {
-     if (i == 5)
-       break;          /\* Breaks the loop      \*/
-     printf("%d ", i); /\* when i is equal to 5 \*/
-   }
- }
- 1 2 3 4
- Result:

---

## break &amp; continue keywords

- break and continue offer distinct ways to control loop flow.
- break instantly terminates the loop it's in, while continue jumps to the next iteration.
- When nested, break affects only the immediate loop.
- break is also applicable in switch statements to exit a specific case
- int main()
- {
-   int i = 0;
-   while (i &lt; 10)
-   {
-     i++;
-     if (i % 2 == 0)
-       continue;       /\* Skips the rest of the    \*/
-     printf("%d ", i); /\* iteration when i is even \*/
-   }
- }
- 1 3 5 7 9
- Result:

---

## break &amp; continue keywords

- break and continue offer distinct ways to control loop flow.
- break instantly terminates the loop it's in, while continue jumps to the next iteration.
- When nested, break affects only the immediate loop.
- break is also applicable in switch statements to exit a specific case
- int main()
- {
-   int i;
-   for (int i = 1; i &lt;= 10; i++)
-   {
-     if (i == 5)
-       break;          /\* Breaks the loop      \*/
-     printf("%d ", i); /\* when i is equal to 5 \*/
-   }
- <br>  printf("\n");
- <br>  i = 0;
-   while (i &lt; 10)
-   {
-     i++;
-     if (i % 2 == 0)
-       continue;       /\* Skips the rest of the    \*/
-     printf("%d ", i); /\* iteration when i is even \*/
-   }
- }
- 1 2 3 4
- 1 3 5 7 9
- Result:

---

## goto statement in loops

- goto provides a convenient way to exit from nested blocks
- int main()
- {
-   bool bug = false;
-   for (int i = 0; i &lt; 5; i++)
-   {
-     for (int j = 0; j &lt; 5; j++)
-     {
-       /\* some code \*/
-       /\* ...       \*/
-       if(bug)
-         goto error;
-     }
-   }
-   goto end;
-   error:
-     /\* some code \*/
-     /\* ...       \*/
-     printf("error found");
-   end:
- }
- int main()
- {
-   bool bug = false; int i = 0, j = 0;
-   while ( i &lt; 5)
-   {
-     while ( j &lt; 5)
-     {/\* some code \*/
-      /\* ...       \*/
-       if(bug)
-         goto error;
-       j++;
-     }
-     i++;
-   }
-   goto end;
-   error:
-     /\* some code \*/
-     /\* ...       \*/
-     printf("error found");
-   end:
- }

---

## Summary of the Difference Between for and while Loops

- The statement about using for for a known number of iterations and while for an unknown number is an excellent guideline, but it's not a strict rule. It's more of a best practice for writing clean, readable, and maintainable code.
- In most programming languages, these two loops are technically interchangeable. You can always write a for loop using a while loop (by manually handling the counter variable), and you can often force a while loop into a for structure, though it might look awkward.
- So, while it's possible to use them interchangeably, following the convention makes your code more understandable for yourself and for other developers. It's about choosing the right tool for the job to make your code's purpose immediately clear.

---

# Functions &amp; variables

---

## Prototype &amp; its Function

- In contrast to function implementations, function prototypes are terminated with a semicolon(;)
- A minimal prototype must precede the function definition, and it is standard to list function prototypes alphabetically after preprocessor directives within a file
- return-type function-name (parameter declarations, if any)
- {
- statements;             /\* including declarations \*/
- return expression1;
- }
- return-type function-name (only type of parameter declarations, if any);

---

## Prototype &amp; its Function

- The return type can be any of the data types presented in the previous material, and additionally, void can be used if no value is to be returned.
- The function name is symbolic\_name.
- return-type function-name (parameter declarations, if any)
- {
- statements;             /\* including declarations \*/
- return expression1;
- }
- return-type function-name (only type of parameter declarations, if any);

---

## Main() example

- The main function is the entry point of a C program. When a C program is executed, the main function is called first.
- The main function is an excellent example. The type of value it returns is int, and its symbolic name is main. In this variant, the function doesn't accept any parameters, though another version with argc does exist. The final line, return 0;, instructs the compiler that the function is returning a value of 0.
- \#include &lt;stdio.h&gt;
- <br>int main()
- {
- /\* body\*/
-   return 0;
- }

---

## Exit(0)

One might wonder why it returns zero if we never use this value anywhere. In fact, it isn't truly unused. When the program finishes its execution, control is handed back to the computer's operating system, which can respond to the returned value. A return value of 0 signifies that the program completed successfully, as the programmer intended, without errors. Any other value indicates an abnormal termination or an error.

- \#include &lt;stdio.h&gt;
- <br>int main()
- {
- /\* body\*/
-   return 0;
- }

---

## Functions, return, and Casting

- Regardless of the function's return type, the compiler expects the return keyword followed by a value of the same type as specified in the function's declaration or prototype. Therefore, if a function returns void (nothing), the last line should simply be return;.
- \#include &lt;stdio.h&gt;
- <br>int main()
- {
- /\* body\*/
- }

---

## Functions, return, and Casting

- Similar to **casting**, there is **explicit casting** (consciously performed by the programmer) and **implicit casting** (done automatically by the compiler). If the result of an int expression is assigned to a float variable, implicit casting will occur. Another programmer analyzing this code won't know if this was a mistake or intentional. To avoid this ambiguity, it's a best practice to use explicit casting with parentheses, for example:

float x = (float) (y + z);

- \#include &lt;stdio.h&gt;
- <br>int main()
- {
- /\* body\*/
- }

---

## Functions, return, and Casting

- The return statement works in a similar way. If a programmer omits the return instruction, the compiler will return "some" value (undefined behavior) depending on its settings (usually the value from the processor's ax register). This can lead to undesirable consequences and hard-to-find bugs, since the compiler won't flag them. For this reason, this course requires every function to end with the return keyword and a variable of the function's declared type.
- Finally, it's worth remembering that the terms **procedure**, **method**, and **function** are often used interchangeably. The main difference is that a function, like the main function, is not nested within another structure. In other languages, you can nest functions within other entities, and these are then called methods. A procedure, on the other hand, is the ancestor of a function in assembly language.

---

## Prototype &amp; its Function - myFunction1

- A function prototype must appear **before** its definition.
- A prototype ends with a semicolon.
- If the function does not take any parameters, you can write void in the prototype, but nowadays few people do this, because the compiler does not require it.
- \#include &lt;stdio.h&gt;
- <br>void myFunction1(void);
- <br>void myFunction1()
- {
-   printf("Text from myFuntion1\n");
-   return;
- }
- int main()
- {
-   myFunction1();
-   return 0;
- }
- Text from myFuntion1
- Result:
- Correct exit

---

## Prototype &amp; its Function - myFunction1

- A function prototype must appear **before** its definition.
- A prototype ends with a semicolon.
- If the function does not take any parameters, you can write void in the prototype, but nowadays few people do this, because the compiler does not require it.
- \#include &lt;stdio.h&gt;
- <br>void myFunction1();
- <br>void myFunction1()
- {
-   printf("Text from myFuntion1\n");
-   return;
- }
- int main()
- {
-   myFunction1();
-   return 0;
- }
- Text from myFuntion1
- Result:
- Correct exit

---

## Prototype &amp; its Function – myFunction2

myFunction2 is of type int, so the value it returns is also of type int. Remember that everything inside the parentheses of the function parameters is a **copy** of the value passed to the function. This means that myFunction2 literally declares int n before the first statement of the function and assigns it the value 2 (like int n = 2;).

- \#include &lt;stdio.h&gt;
- <br>int myFunction2(int);
- <br>int myFunction2(int n)
- {
-   n++;
-   printf("incremented n from myFuntion2 equals %d\n", n);
-   return 1;
- }
- int main()
- {
-   int result = myFunction2(2);
-   printf("result of myFuntion2 equals %d\n", result);
-   return 0;
- }
- incremented n from myFuntion2 equals 3
- result of myFuntion2 equals 1
- Result:

---

## Prototype &amp; its Function – myFunction2

As known from the concept of a block, once the body of myFunction2 finishes executing, this local variable n is destroyed — it exists only within the scope of the function. Inside the function, the value of n is incremented by 1, displayed using printf, and the function then returns the value 1. This returned value is assigned to result in main.

- \#include &lt;stdio.h&gt;
- <br>int myFunction2(int);
- <br>int myFunction2(int n)
- {
-   n++;
-   printf("incremented n from myFuntion2 equals %d\n", n);
-   return 1;
- }
- int main()
- {
-   int result = myFunction2(2);
-   printf("result of myFuntion2 equals %d\n", result);
-   return 0;
- }
- incremented n from myFuntion2 equals 3
- result of myFuntion2 equals 1
- Result:

---

## Prototype &amp; its Function – myFunction2

This demonstrates how a function communicates with a variable in main: the parameter n is a local copy, and the function can return a value to the caller.

- \#include &lt;stdio.h&gt;
- <br>int myFunction2(int);
- <br>int myFunction2(int n)
- {
-   n++;
-   printf("incremented n from myFuntion2 equals %d\n", n);
-   return 1;
- }
- int main()
- {
-   int result = myFunction2(2);
-   printf("result of myFuntion2 equals %d\n", result);
-   return 0;
- }
- incremented n from myFuntion2 equals 3
- result of myFuntion2 equals 1
- Result:

---

## Prototype &amp; its Function – myFunction3

- \#include &lt;stdio.h&gt;
- <br>int  myFunction3(void);
- <br>int myFunction3()
- {
-   int n = 2;
-   printf("n from myFuntion3 equals %d\n", n);
-   /\* the compiler will not return an error if     \*/
-   /\* we omit return, and the function will return \*/
-   /\* an unspecified value                         \*/
- }
- int main()
- {
-   int result = myFunction3();
-   printf("result of myFuntion3 equals %d\n", result);
-   return 0;
- }
- n from myFuntion3 equals 2
- result of myFuntion3 equals 27
- Result:

---

## Prototype &amp; its Function

- \#include &lt;stdio.h&gt;
- <br>void myFunction1(void);
- int  myFunction2(int);
- int  myFunction3(void);
- <br>void myFunction1()
- {
-   printf("Text from myFuntion1\n");
-   return;
- }
- int myFunction2(int n)
- {
-   n++;
-   printf("incremented n from myFuntion2 equals %d\n", n);
-   return 1;
- }
- int myFunction3()
- {
-   int n = 2;
-   printf("n from myFuntion3 equals %d\n", n);
-   /\* the compiler will not return an error if     \*/
-   /\* we omit return, and the function will return \*/
-   /\* an unspecified value                         \*/
- }
- int main()
- {
-   myFunction1();
-   int result = myFunction2(2);
-   printf("result of myFuntion2 equals %d\n", result);
-   result = myFunction3();
-   printf("result of myFuntion3 equals %d\n", result);
-   return 0;
- }
- Text from myFuntion1
- incremented n from myFuntion2 equals 3
- result of myFuntion2 equals 1
- n from myFuntion3 equals 2
- result of myFuntion3 equals 27
- Result:
- Correct exit

<!-- Green comment! -->

---

## Variables

- variable scope    –    the region in which a variable is valid;

any variable must be declared before its first use;

- Variables:

– local (automatic)

– global

- local variable    –    is only accessible within the block where it is defined. Once the         block ends, access to the local variable is lost.
- global variable    –    declared outside of functions, is accessible from any point in the         program below its declaration.

---

## global vs local

We don't have direct access to a shadowed variable. The only way to access it is through a pointer.

- \#include &lt;stdio.h&gt;
- int x = 5;                 /\* global x \*/
- <br>void myFunction1(void);<br>void myFunction1()
- {
-   printf("x equals %d that is read by function myFunction\n", x);
- }
- int main()
- {
-   int \* pointerGlobalX = &amp;x;
-   myFunction1();
-   int x = 3;              /\* local x \*/
-   printf("x equals %d that is read by function main\n", x);
-   printf("x equals %d that is read by function main\n", \*pointerGlobalX);
-   return 0;
- }
- x equals 5 that is read by function myFunction
- x equals 3 that is read by function main
- x equals 5 that is read by function main
- Result:

---

## Summary - variable scope

- Global variables are accessible throughout a program, but they can be temporarily hidden by a local variable declared within a nested block, such as a function, for loop, while loop, or even an if statement.
- This is known as "variable shadowing," and within the local variable's scope, any reference to that variable name will refer to the local one. The global variable remains inaccessible until the local variable's block is exited and the local variable is released from memory. At that point, access to the global variable is restored.

---

# Thank you

- Jakub Leszek Pach
- <jpach@mtech.edu>

---

## Declaring and initializing arrays

- int main()
- {
-   int a\[5\];
-   /\* Declare an integer array named a with 5 elements \*/
-   int b\[\] = {1, 2, 3, 4};
-   /\*Declare an integer array named b with 4 elements,
-     initialized with values 1, 2, 3, and 4            \*/
-   int c\[10\] = {9, 8, 7, 6, 5};
-   /\*Declare an integer array named c with 10 elements,
-     the first 5 elements are initialized with values 9, 8, 7, 6, and 5,
-     the remaining elements are initialized to 0                 \*/
-   int d\[100\] = {0};
-   /\*Declare an integer array named d with 100 elements, all initialized to 0\*/
-   int x, y = 2;
-   printf("First element (index 0) of array a equals %d.\n", a\[0\]);
-   /\*Print the value of the first element of array a(undefined value)\*/
-   printf("Second(index 1) element of array b equals %d.\n", b\[1\]);
-   /\*Print the value of the second element of array b (which is 2)\*/
-   printf("Second(index 1) element of array b equals %d.\n", \*(b+1) );
-   /\*Print the value of the second element of array b using pointer arithmetic\*/
-   printf("Sixth(index 5) element of array c equals %d.\n", c\[5\]);
-   /\*Print the value of the sixth element of array c (which is 0)\*/
-   x = b\[0\];   /\*Assign the value of the first element of array b (which is 1) to variable x\*/
-   a\[1\] = y;   /\*Assign the value of variable y (which is 2) to the second element of array a\*/
- }
- First element (index 0) of array a equals 4201200.
- Second(index 1) element of array b equals 2.
- Second(index 1) element of array b equals 2.
- Sixth(index 5) element of array c equals 0.
- Result:

---

## Basics of

- The important difference between printf and scanf is that scanf requires its arguments to be pointers (location in memory) .
- int main()
- {
-   int x = 5;                      /\* Declaration of variable x and assigning its value 5 \*/
-   int \* p;                      /\* Declaration of pointer p \*/
-   p = &amp;x;                       /\* Assigning the address value of the p variable to the pointer p \*/
-   printf("Enter x value : ");         /\* there is no end of line character here! \*/
-   scanf("%d", &amp;x);                 /\* To get a pointer (memory address) \*/
-   printf("Value of x = %d\n", x);     /\* we use a &amp; before the variable name p \*/
-   printf("Enter x value again : ");
-   scanf("%d", p);                     /\*scanf does not work the same as in python, \*/
-   printf("Value of x = %d\n", x);   /\*you have to use printf and scanf separately \*/
- }
- Enter x value : 1
- Value of x = 1
- Enter x value again : 2
- Value of x = 2
- Result:
- int printf (char format\[\],  arg1,  arg2 ,...);
- int scanf  (char format\[\], \*arg1, \*arg2 ,...);
- The ampersand operator &amp; is a unary operator that returns the memory address, which is the location in memory where a variable is stored.

<!-- This line is where the magic happens. It assigns the address of the variable x to the pointer pointer. The &amp; symbol is the "address-of" operator. So, pointer now holds the memory location where the value 5 for x is stored. -->

---

## Notice

Recently, during my lab work, I made a mistake. It wasn't the development environment's fault, but mine. It was related to the scanf function. Because I'm currently working with Python, C, C++, C#, and MATLAB, I mixed up the behavior of the scanf function. You need to know that the scanf function has one drawback: it doesn't clear the buffer of characters entered from the keyboard. This means that after pressing Enter to confirm the data entered from the keyboard, our variable also contains the Enter character, which is that extra line you asked me to use to clear the buffer. To understand its operation, you need to understand today's new material.

---

## Huge problems… undefined behavior

- Do not increment (decrement) a variable in an expression if you need to use the original value of the variable later!
- int main()
- {
-   {
-     int x = 1, y;
-     y = x + 2 + ++x;
-     printf("%d\n", y);
-   }
-   {
-     int x = 1, y;
-     y = x + ++x;
-     printf("%d\n", y);
-   }
- }
- 5
- 4
- Result:
- When modifying and using a variable multiple times within the same expression, it may lead to undefined behavior!

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

- int main()
- {
-   {
-     int x = 1, y = 2;
-     x += y = 3 + x \* y;
-     printf("%d\n", x);
-   }
-   {
-     int x = 1, y = 2;
-     x += x = y = 3 + x - y;
-     printf("%d\n", x);
-   }
- }
- 6
- 4
- Result:
- x += y = 3 + x \* y;            /\* 2 \*/
- x += y = 3 + 2;                /\* 5 \*/
- x += y = 5;                /\*y=5\*/
- x += 5;                    /\*x=6\*/
- x += x = y = 3 + x - y;         /\* 4 \*/
- x += x = y = 4 - y;            /\* 2 \*/
- x += x = y = 2;             /\*y=2\*/
- x += x = 2;                 /\*x=2\*/
- x += 2;                     /\*x=4\*/

Left-to-right associativity means that when there are two operators with the same priority, the operator on the left is evaluated first. In right-to-left associativity, the opposite is true.

- LR
- RL

---

<!-- pptx2marp: slide 52 has no extractable text or images -->

---

## Basics of

- The important difference between printf and scanf is that scanf requires its arguments to be pointers (location in memory) .
- int main()
- {
-   int x = 5;                      /\* Declaration of variable x and assigning its value 5 \*/
-   int \* p;                      /\* Declaration of pointer p \*/
-   p = &amp;x;                       /\* Assigning the address value of the p variable to the pointer p \*/
-   printf("Enter x value : ");         /\* there is no end of line character here! \*/
-   scanf("%d", &amp;x);                 /\* To get a pointer (memory address) \*/
-   printf("Value of x = %d\n", x);     /\* we use a &amp; before the variable name p \*/
-   printf("Enter x value again : ");
-   scanf("%d", p);                     /\*scanf does not work the same as in python, \*/
-   printf("Value of x = %d\n", x);   /\*you have to use printf and scanf separately \*/
- }
- Enter x value : 1
- Value of x = 1
- Enter x value again : 2
- Value of x = 2
- Result:
- int printf (char format\[\],  arg1,  arg2 ,...);
- int scanf  (char format\[\], \*arg1, \*arg2 ,...);
- The ampersand operator &amp; is a unary operator that returns the memory address, which is the location in memory where a variable is stored.

<!-- This line is where the magic happens. It assigns the address of the variable x to the pointer pointer. The &amp; symbol is the "address-of" operator. So, pointer now holds the memory location where the value 5 for x is stored. -->

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

- int main()<br>{ int x = 5, y = -6; int \* z; float f = 3.1234f; /\*code\*/ }

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

- int main()<br>{ int x = 5, y = -6; int \* z; float f = 3.1234f; /\*code\*/ }

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

- int main()<br>{ short int x = 65;  int y = -69000; <br>  float fRealNumber = 3.1234f; double dRealNumber = 3.4e50; /\*code\*/ }

|Data|Type||Description|Example|Result|
|---|---|---|---|---|---|
|Numbers|integer|d|Modifier, h and l specify how many bytes should be formatted as a variable. Therefore, if we use short (h - 2 bytes) on a normal int (long - 32 bit), we will get an incorrect result because printf will take only 16 bits and build a number representation from it.|printf("%0hd\n", x);<br>printf("%0hd\n", y);<br>printf("%0ld\n", x);<br>printf("%0ld\n", y);|65<br>-3464<br>65<br>-69000|
|||u||||
|||c||||
||floating-point number|f|Since there's no such thing as hf (as hf is simply f), the compiler ignores h, and l represents a double. As you can see, there's no lf type, only f with the l modifier.|printf("%0hf\n", fRealNumber);<br>printf("%0lf\n", fRealNumber);<br>printf("%0hf\n", dRealNumber);<br>printf("%0lf\n", dRealNumber);|3.123400<br>3.123400<br>33999999...<br>339999999999999984402842591433794782958910267457536.000000|
|||lf||||
|Text|string|s|None|None|None|

---

## printf and scanf format specification

- Optional:
  - Flags    -    modifiers that alter the formatting or scanning behavior.
  - Width    -    specifies the minimum width of the output field <br>        or the maximum number of characters to be scanned.
  - Precision    -    controls the precision of floating-point numbers <br>        or the maximum number of characters to be scanned for strings.
  - Modifier    -    indicates the data type size (e.g., long, short).
- Required:
  - Type    -    specifies the data type of the variable to be formatted or scanned.

Format =  %\[flags\]\[width\]\[.precision\]\[modifier\]&lt;type&gt;
