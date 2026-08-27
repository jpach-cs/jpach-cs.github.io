---
marp: true
theme: pach
paginate: true
title: "Data Structures & Algorithms"
---

<!-- _class: lead -->

# Data Structures &amp; Algorithms

## Lecture 6
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

- Stack
- Queue
- Working with code

---

# Stack (LIFO – Last In, First Out)

---

# Stack (LIFO – Last In, First Out)

- Last element pushed is the first to be popped.
- Operations:
  - push(x) → add to the top
  - pop() → remove from the top

```text
Stack (LIFO):

   +-----+
   |  D  | <- Top (newest element)
   +-----+
   |  C  |
   +-----+
   |  B  |
   +-----+
   |  A  | <- Bottom (oldest element)
   +-----+

push(E) => E goes on top
pop()   => removes D from the top
```

---

# Queue (FIFO – First In, First Out)

---

# Queue (FIFO – First In, First Out)

- First element enqueued is the first to be dequeued.
- Operations:
  - enqueue(x) → add to the rear
  - dequeue() → remove from the front

```text
Queue (FIFO):

Front -> +-----+     +-----+     +-----+     +-----+ <- Rear
         |  A  | --> |  B  | --> |  C  | --> |  D  |
         +-----+     +-----+     +-----+     +-----+

enqueue(E) => E goes to the rear
dequeue()  => removes A from the front
```

---

# Stack &amp; Queue

The difference between a stack and a queue is not in the underlying structure—they both work on linked lists—but in the way elements are added and removed.

- In a stack, elements are inserted at the front and also removed from the front (LIFO).
- In a queue, elements are inserted at the rear but removed from the front (FIFO).

|**Structure**|**Insert**|**Remove**|**Rule**|
|---|---|---|---|
|**Stack**|Top|Top|Last In, First Out|
|**Queue**|Rear|Front|First In, First Out|

---

# working with code

---

# Questions?

---

<!-- _class: caption-slide -->

# Thank You
