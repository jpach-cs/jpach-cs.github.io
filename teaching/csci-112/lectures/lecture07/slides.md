---
marp: true
theme: pach
paginate: true
footer: "CSCI 112 | Programming with C | J. L. Pach"
title: "CSCI 112  Programming with C"
---

<!-- _class: lead -->

# CSCI 112<br><br>Programming with C

- Lecture 7
- Dr. Jakub L. Pach
- Fall 2025

---

# Outline

- Review
- Loop statements
- Functions
- Global & local variables

---

# Review

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

# Loop statements

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
    i = i + 1;
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

# while loop

```c
int main()
{
  int i = -1;
  while ( ++i < 3 )
    printf("a value of i is: %d\n", i);
}
```

Result:

```text
a value of i is: 0
a value of i is: 1
a value of i is: 2
```

OR

```c
int main()
{
  int i = 0;
  while ( i < 3 )
    printf("a value of i is: %d\n", i++);
}
```

```c
int main()
{
  int i = 0;
  while ( i < 3 )
  {
    printf("a value of i is: %d\n", i);
    i = i + 1;
  }
}
```

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

# do-while loop

```c
do
  statement1;
while(expression1)
```

A do-while loop executes statement1, then checks the logical outcome of expression1. If expression1 evaluates to true, the loop repeats; otherwise, the loop terminates.

```c
int main()
{
  int number;

  do
  {
      printf("Enter a positive number: ");
      scanf("%d", &number);
  }
  while (number <= 0);

  printf("You entered: %d\n", number);
}
```

Result:

```text
Enter a positive number: -9
Enter a positive number: 2
You entered: 2
```

- semicolon!

---

# Simulating a do-while loop with while loop

```c
int main()
{
  bool flag = true;
  while (flag)
  {
      printf("This code will execute at least once.\n");
      if (! (/* condition */) )
          flag = false;
  }
}
```

- \*In Python we don’t have do\_while.

---

# An example

```c
int main()
{
    int number;
    bool flag = true;
    while (flag)
    {
        printf("Enter a positive number: ");
        scanf("%d", &number);
        if (! (number <= 0) )
            flag = false;
    }
    printf("You entered: %d\n", number);
}
```

Result:

```text
Enter a positive number: -9
Enter a positive number: 2
You entered: 2
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

<!-- _class: fit-90 -->

# Summary of the Difference Between for and while Loops

- The statement about using for for a known number of iterations and while for an unknown number is an excellent guideline, but it's not a strict rule. It's more of a best practice for writing clean, readable, and maintainable code.
- In most programming languages, these two loops are technically interchangeable. You can always write a for loop using a while loop (by manually handling the counter variable), and you can often force a while loop into a for structure, though it might look awkward.
- So, while it's possible to use them interchangeably, following the convention makes your code more understandable for yourself and for other developers. It's about choosing the right tool for the job to make your code's purpose immediately clear.

---

# Functions & variables

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

# Main() example

- The main function is the entry point of a C program. When a C program is executed, the main function is called first.
- The main function is an excellent example. The type of value it returns is int, and its symbolic name is main. In this variant, the function doesn't accept any parameters, though another version with argc does exist. The final line, return 0;, instructs the compiler that the function is returning a value of 0.

```c
#include <stdio.h>

int main()
{
	/* body*/
  return 0;
}
```

---

# Exit(0)

One might wonder why it returns zero if we never use this value anywhere. In fact, it isn't truly unused. When the program finishes its execution, control is handed back to the computer's operating system, which can respond to the returned value. A return value of 0 signifies that the program completed successfully, as the programmer intended, without errors. Any other value indicates an abnormal termination or an error.

```c
#include <stdio.h>

int main()
{
	/* body*/
  return 0;
}
```

---

# Functions, return, and Casting

- Regardless of the function's return type, the compiler expects the return keyword followed by a value of the same type as specified in the function's declaration or prototype. Therefore, if a function returns void (nothing), the last line should simply be return;.

```c
#include <stdio.h>

int main()
{
	/* body*/
}
```

---

# Functions, return, and Casting

- Similar to **casting**, there is **explicit casting** (consciously performed by the programmer) and **implicit casting** (done automatically by the compiler). If the result of an int expression is assigned to a float variable, implicit casting will occur. Another programmer analyzing this code won't know if this was a mistake or intentional. To avoid this ambiguity, it's a best practice to use explicit casting with parentheses, for example:

```c
float x = (float) (y + z);
```

```c
#include <stdio.h>

int main()
{
	/* body*/
}
```

---

<!-- _class: fit-80 -->

# Functions, return, and Casting

- The return statement works in a similar way. If a programmer omits the return instruction, the compiler will return "some" value (undefined behavior) depending on its settings (usually the value from the processor's ax register). This can lead to undesirable consequences and hard-to-find bugs, since the compiler won't flag them. For this reason, this course requires every function to end with the return keyword and a variable of the function's declared type.
- Finally, it's worth remembering that the terms **procedure**, **method**, and **function** are often used interchangeably. The main difference is that a function, like the main function, is not nested within another structure. In other languages, you can nest functions within other entities, and these are then called methods. A procedure, on the other hand, is the ancestor of a function in assembly language.

---

<!-- _class: fit-90 -->

# Prototype & its Function - myFunction1

- A function prototype must appear **before** its definition.
- A prototype ends with a semicolon.
- If the function does not take any parameters, you can write void in the prototype, but nowadays few people do this, because the compiler does not require it.

```c
#include <stdio.h>

void myFunction1(void);

void myFunction1()
{
  printf("Text from myFuntion1\n");
  return;
}
int main()
{
  myFunction1();
  return 0;
}

```

Result:

```text
Text from myFuntion1
```

- Correct exit

---

<!-- _class: fit-90 -->

# Prototype & its Function - myFunction1

- A function prototype must appear **before** its definition.
- A prototype ends with a semicolon.
- If the function does not take any parameters, you can write void in the prototype, but nowadays few people do this, because the compiler does not require it.

```c
#include <stdio.h>

void myFunction1();

void myFunction1()
{
  printf("Text from myFuntion1\n");
  return;
}
int main()
{
  myFunction1();
  return 0;
}

```

Result:

```text
Text from myFuntion1
```

- Correct exit

---

<!-- _class: fit-80 -->

# Prototype & its Function – myFunction2

myFunction2 is of type int, so the value it returns is also of type int. Remember that everything inside the parentheses of the function parameters is a **copy** of the value passed to the function. This means that myFunction2 literally declares int n before the first statement of the function and assigns it the value 2 (like int n = 2;).

```c
#include <stdio.h>

int myFunction2(int);

int myFunction2(int n)
{
  n++;
  printf("incremented n from myFuntion2 equals %d\n", n);
  return 1;
}
int main()
{
  int result = myFunction2(2);
  printf("result of myFuntion2 equals %d\n", result);
  return 0;
}
```

Result:

```text
incremented n from myFuntion2 equals 3
result of myFuntion2 equals 1
```

---

<!-- _class: fit-80 -->

# Prototype & its Function – myFunction2

As known from the concept of a block, once the body of myFunction2 finishes executing, this local variable n is destroyed — it exists only within the scope of the function. Inside the function, the value of n is incremented by 1, displayed using printf, and the function then returns the value 1. This returned value is assigned to result in main.

```c
#include <stdio.h>

int myFunction2(int);

int myFunction2(int n)
{
  n++;
  printf("incremented n from myFuntion2 equals %d\n", n);
  return 1;
}
int main()
{
  int result = myFunction2(2);
  printf("result of myFuntion2 equals %d\n", result);
  return 0;
}
```

Result:

```text
incremented n from myFuntion2 equals 3
result of myFuntion2 equals 1
```

---

# Prototype & its Function – myFunction2

This demonstrates how a function communicates with a variable in main: the parameter n is a local copy, and the function can return a value to the caller.

```c
#include <stdio.h>

int myFunction2(int);

int myFunction2(int n)
{
  n++;
  printf("incremented n from myFuntion2 equals %d\n", n);
  return 1;
}
int main()
{
  int result = myFunction2(2);
  printf("result of myFuntion2 equals %d\n", result);
  return 0;
}
```

Result:

```text
incremented n from myFuntion2 equals 3
result of myFuntion2 equals 1
```

---

# Prototype & its Function – myFunction3

```c
#include <stdio.h>

int  myFunction3(void);

int myFunction3()
{
  int n = 2;
  printf("n from myFuntion3 equals %d\n", n);
  /* the compiler will not return an error if     */
  /* we omit return, and the function will return */
  /* an unspecified value                         */
}
int main()
{
  int result = myFunction3();
  printf("result of myFuntion3 equals %d\n", result);
  return 0;
}
```

Result:

```text
n from myFuntion3 equals 2
result of myFuntion3 equals 27
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

- local variable    –    is only accessible within the block where it is defined. Once the         block ends, access to the local variable is lost.
- global variable    –    declared outside of functions, is accessible from any point in the         program below its declaration.

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

# Thank you

- Jakub Leszek Pach
- <jpach@mtech.edu>
