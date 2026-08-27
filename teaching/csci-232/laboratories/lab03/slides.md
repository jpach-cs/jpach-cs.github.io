---
marp: true
theme: pach
paginate: true
title: "Data Structures & Algorithms"
---

<!-- _class: lead -->

# Data Structures &amp; Algorithms

## Lecture 3
---

# In 136, we covered

- Objects and classes, Abstract Data Types – lots of coverage.  I required class and header files in most assignments
- Time and Space complexity – a discussion was included in each exercise.  Good coverage of constant time, linear, n2, n3, with loops and nested loops.  Didn’t do any of the math.
- Arrays and 2D arrays, and “2D” vectors, along with Big-O and execution time tests with larger structures.  Students had a LOT of coverage
- Linked List and Sorted Linked List – students had to write their own class/header files and driver for each
- Stack and Queue – students were given .h files, had to write the class and member functions and driver
- Maze using stack and queue in Python – students were given classes, had to write DFS and BFS with much assistance and examples
- Lecture coverage of memory allocation, memory usage, static variables, compilation, memory leaks, dangling pointers, comparison of C and C++, binary search, examples of object-oriented programming and ADT’s in C++, Python, Java
- Parameter passing, command line arguments, scope – good coverage
- Pointers – medium coverage, mostly with parameter passing.  We didn’t use them in any useful way.
- Recursion – weak coverage
- Visual Studio – all the time

---

# Today’s Agenda

- Review
  - Relations between pointers and arrays
- List Basics

---

# Function arguments

Function arguments are always **copies** of our variables, and **not** the same memory areas, a function argument, even though it has the same value, is a completely different variable!

---

# by the Value

Function arguments are always **copies** of our variables, and **not** the same memory areas, a function argument, even though it has the same value, is a completely different variable!

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

Function arguments are always **copies** of our variables, and **not** the same memory areas, a function argument, even though it has the same value, is a completely different variable!

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

Result:

```text
5
6

```

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

|Memory Addresses and Values||
|---|---|
|x (6422296)|5|
|y (6422292)|5|
|p (6422288)|6422296|
|pp (6422284)|6422288|

![Ink 54](assets/image80.png)

![Ink 55](assets/image90.png)

![Ink 56](assets/image100.png)

![Ink 58](assets/image110.png)

![Ink 59](assets/image120.png)

![Ink 60](assets/image130.png)

---

# Relations between pointers and arrays

---

# Relations between pointers and arrays

This statement reserves space in memory for 10 integers and creates an 'unchanging address of memory' that points to the beginning of this array.

```c
int a[10];
```

```c
int main()
{
  int a[] = {1, 2, 3, 4, 5, 6, 7};
  printf("%-4s equals %d.\n", "a", a);
  /*a equals'unchanging address of memory’*/
  return 0;
}
```

Result:

```text
a    equals 6422272.


```

![Ink 17](assets/image140.png)

![Ink 18](assets/image150.png)

---

# Relations between pointers and arrays

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

Result:

```text
a    equals 6422272.
?
```

---

# Relations between pointers and arrays

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

Result:

```text
a    equals 6422272.
&a   equals 6422272.
?
```

---

# Relations between pointers and arrays

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

Result:

```text
a    equals 6422272.
&a   equals 6422272.
*a   equals 1.
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

When performing arithmetic operations on pointers, the array index is automatically multiplied by the size of the data type pointed to by the pointer.

For example, if the array stores char values, the index is multiplied by 1, and if it stores int values, the index is multiplied by 4 (assuming an int is 4 bytes).

```c
int a[10];

a[i] == *(a+i)		&a[i] == &*(a+i) == a+i
```

---

# Conclusions

- The expression a\[i\] is transformed by the compiler into the form \*(a+i).
- The square brackets following the symbolic\_name do not provide any information about whether we are referring to an array.
- When performing arithmetic operations on pointers, the array index is automatically multiplied by the size of the data type pointed to by the pointer.

<!-- define s\[n\] na \*(s + n) -->

---

# crème de la crème

```c
int main()
{
    unsigned int x = 0x41424344; // Store a 32-bit integer with ASCII-like hex values
    char *p = (char*) &x;          // Cast the address of x to a char pointer
    printf("x = 0x%X\n", x);
    // Using p[i] does not mean we have an array.
    // In C, p[i] is just shorthand for *(p + i),
    // which means "take the value at address p plus i bytes."
    // Since p is a char*, each step moves by 1 byte.
    // The actual output depends on system endianness:
    // - Little-endian: p[0] = 'D', p[1] = 'C', p[2] = 'B', p[3] = 'A'
    // - Big-endian:    p[0] = 'A', p[1] = 'B', p[2] = 'C', p[3] = 'D'
    printf("p[0] = %c\n", p[0]);
    printf("p[1] = %c\n", p[1]);
    printf("p[2] = %c\n", p[2]);
    printf("p[3] = %c\n", p[3]);
    return 0;
}
```

Result:

```text
x = 0x41424344
p[0] = D
p[1] = C
p[2] = B
p[3] = A
```

---

# List Basics

---

# Code file

<!-- //#define clearBuffer() while (getchar() != '\n');
#include &lt;stdio.h&gt;
#include &lt;stdbool.h&gt;
#include &lt;stdlib.h&gt;
// tests
#include "unity.h"
#include &lt;assert.h&gt;
<br>// Unity requires these functions (they can be left empty if not used)
void setUp(void) {}
void tearDown(void) {}
<br>// - - - - - - - - - - - - - - - - -  STRUCTURE DEFINITION - - - - - - - - - - - - - - - - -
// Each node contains a value and a pointer to the next node (dynamic memory)
struct Node
{
int value;
struct Node \*nextPtr;
};
<br>// - - - - - - - - - - - - - - - - -  HELPER FUNCTIONS - - - - - - - - - - - - - - - - -
<br>// Print all elements of the list starting from head
void printList(struct Node \*listHeadPtr)
{
unsigned index = 0;
if (!listHeadPtr) // empty list
{
printf("This list is empty!\n");
return;
}
<br>    while (listHeadPtr)
{
printf("index: %u, value = %d\n", index, listHeadPtr-&gt;value);
index++;
listHeadPtr = listHeadPtr-&gt;nextPtr;
}
}
<br>// - - - - - - - - - - - - - - - - -  STACK-BASED DEMO - - - - - - - - - - - - - - - - -
<br>// Example of building a list using stack variables (no malloc)
void demoWithStack()
{
struct Node first;
struct Node second;
struct Node third;
struct Node fourth;
<br>    // Assign values
first.value  = 5;
second.value = 4;
third.value  = 3;
fourth.value = 2;
<br>    // Link nodes together
first.nextPtr  = &amp;second;
second.nextPtr = &amp;third;
third.nextPtr  = &amp;fourth;
fourth.nextPtr = NULL;
<br>    printf("%s\n\n", "Printing static list");
printList(&amp;first); // pass address of head node
}
<br>// - - - - - - - - - - - - - - - - -  DYNAMIC MEMORY DEMO - - - - - - - - - - - - - - - - -
<br>// Allocate memory for a new dynamic node
struct Node \* CreateDynamicNode(int value, struct Node \*nextPtr)
{
struct Node \*nodePtr = (struct Node \*) malloc(sizeof(struct Node));
if (!nodePtr)
{
printf("Memory allocation failed!\n");
return NULL;
}
nodePtr-&gt;value = value;
nodePtr-&gt;nextPtr = nextPtr;
return nodePtr;
}
<br>// Add a dynamic node to the end of the list
// Returns updated head pointer (useful if head was NULL)
struct Node \* AddDynamicNode2List(struct Node \*listHeadPtr, struct Node \*newNodePtr)
{
if (!newNodePtr)
{
printf("New node does not exist!\n");
return listHeadPtr;
}
<br>    if (listHeadPtr == NULL)
return newNodePtr; // new node becomes head
<br>    struct Node \*currentPtr = listHeadPtr;
while (currentPtr-&gt;nextPtr != NULL)
{
currentPtr = currentPtr-&gt;nextPtr;
}
currentPtr-&gt;nextPtr = newNodePtr;
return listHeadPtr;
}
<br>// Delete entire dynamic list
// After deletion, caller should set head pointer to NULL
struct Node \* DeleteDynamicList(struct Node \*listHeadPtr)
{
struct Node \*currentPtr = listHeadPtr;
struct Node \*nextPtr;
<br>    while (currentPtr != NULL)
{
nextPtr = currentPtr-&gt;nextPtr;
free(currentPtr);
currentPtr = nextPtr;
}
return NULL;
}
<br>// - - - - - - - - - - - - - - - - -  DEMO FUNCTION - - - - - - - - - - - - - - - - -
<br>void demoWithDynamicMemory()
{
struct Node \*headPtr = NULL; // initially empty
struct Node \*newNodePtr;
<br>    newNodePtr = CreateDynamicNode(66, NULL); // node 1
headPtr = AddDynamicNode2List(headPtr, newNodePtr);
<br>    newNodePtr = CreateDynamicNode(65, NULL); // node 2
headPtr = AddDynamicNode2List(headPtr, newNodePtr);
<br>    newNodePtr = CreateDynamicNode(64, NULL); // node 3
headPtr = AddDynamicNode2List(headPtr, newNodePtr);
<br>    printf("%s\n\n", "Printing dynamic list");
printList(headPtr);
<br><br>    // Free memory
headPtr = DeleteDynamicList(headPtr);
}
<br>// - - - - - - - - - - - - - - - - -  MAIN PROGRAM - - - - - - - - - - - - - - - - -
<br>int main()
{
// Demo with stack-based list
demoWithStack();
<br>    // Demo with dynamic memory list
demoWithDynamicMemory();
<br>    getchar(); // pause before exit (Windows)
return 0;
} -->

---

# Questions?

---

<!-- _class: caption-slide -->

# Thank You

---

# unit tests

---

# What are Unit Tests

Unit tests are automated checks of small parts of a program (such as functions or procedures) to verify that they work correctly. The idea is to test whether a given function returns the correct result for specific input values.

- Why use unit tests?
  - You catch bugs faster.
  - You don’t have to manually test your code every time.
  - You gain confidence that changes in the code don’t break other parts (this is called regression prevention).

---

# Exit code / return code / status code

- The program returned exit code 0, which means it ran successfully.
- A non-zero exit code usually indicates an error or failure.

---

# assert()

- In structurally or imperatively oriented programming, function names are typically nouns — for example, sum(), pow(), or strlen().
- In object-oriented programming, we create instances of objects represented by nouns, but the methods invoked on those objects are usually verbs, describing actions performed on the instance — for example, trash.clean().
- In the C language, the function assert() is an exception. Unlike typical function names, it is a verb, reflecting the programmer’s intention to assert — to strongly claim — that a certain condition holds true. Conceptually, it’s as if the programmer is saying: “I assert that x equals 1” assert(x==1);

---

# assert()

- The original intent behind assert() was to allow developers to write code like:

```c
sum(a, b);

assert(a > 0);
```

- These statements were meant to halt program execution if the condition was not met. In short, they served as additional safeguards to help speed up debugging.
- Over time, most programming languages adopted dedicated unit testing frameworks — even C, thanks to the Unity library. Unity was designed with a plan-driven approach in mind, enabling developers to write tests before implementing the actual code.

---

***I assert that x equals 1.***
