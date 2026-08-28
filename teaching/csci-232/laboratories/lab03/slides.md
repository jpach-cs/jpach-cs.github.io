---
marp: true
theme: pach
paginate: true
class: compact
footer: "CSCI 232 | Algorithms & Data Structures | J. L. Pach"
title: "Data Structures & Algorithms"
---

<!-- _class: compact lead -->

# Data Structures &amp; Algorithms

## Lecture 3

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

<!-- _class: compact fit-90 -->

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

<!-- _class: compact fit-80 -->

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

<!-- _class: compact caption-slide -->

# Thank You
