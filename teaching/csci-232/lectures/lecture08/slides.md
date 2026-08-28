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

## Lecture 8

---

# Today’s Agenda

- Doubly Linked Lists
- Insertion sort

---

# Doubly Linked Lists

---

<!-- _class: compact fit-80 -->

# Introduction to Doubly Linked Lists

A **Doubly Linked List (DLL)** is a linear data structure where each element (node) contains three fields:

- **Data:** The actual value stored in the node.
- **Next Pointer (NextPtr):** A pointer to the next node in the sequence.
- **Previous Pointer (PrevPtr):** A pointer to the preceding node in the sequence.

Unlike a **Singly Linked List**, which can only be traversed forward, the DLL allows traversal in both directions—forward from the head and backward from the tail.

---

<!-- _class: compact fit-70 -->

# Key Advantages of the Doubly Linked List

The addition of the PrevPtr dramatically increases the flexibility and efficiency of certain operations:

|**Feature**|**Benefit**|**Efficiency Gain**|
|---|---|---|
|Bidirectional Traversal|Allows moving backward from any node or starting from the tail.|Essential for complex algorithms.|
|Efficient Deletion|To delete a node, you only need a pointer to *that node*. You can easily access its preceding node via PrevPtr.|Deletion complexity is **O(1)** (after finding the node), as you don't need to traverse from the head to find the predecessor.|
|Simplified Implementation|Operations like **inserting before a node** or **deleting the last element** are much simpler and cleaner to implement compared to their singly linked list counterparts.|Reduced code complexity and fewer edge cases.|

---

<!-- _class: compact fit-60 -->

# DLL as LIFO (Stack) and FIFO (Queue)

The DLL's ability to efficiently handle insertions at both the head and the tail makes it a perfect foundation for implementing the two primary abstract data types:

This dual efficiency **drastically streamlines the implementation of various data processing structures and algorithms** that rely on quick insertions and deletions, making the DLL highly versatile.

|ADT (Abstract Data Type)|Operation|DLL Implementation|Efficiency|
|---|---|---|---|
|**Stack (LIFO)**|**Push** (add) and **Pop** (remove)|Operations are performed exclusively at the **Head**.|**O(1)**|
|**Queue (FIFO)**|**Enqueue** (add) at the **Tail** and **Dequeue** (remove) at the **Head**.|Both operations are direct (no traversal needed).|**O(1)**|

---

<!-- _class: compact fit-80 -->

# The Trade-Off: Increased Memory Consumption

The primary drawback of the Doubly Linked List is its memory overhead:

**In summary:** The DLL sacrifices memory space for significant gains in time efficiency and implementation simplicity for many common list operations.

|Metric|Doubly Linked List|Singly Linked List|Trade-Off|
|---|---|---|---|
|**Pointers per Node**|**Two** (NextPtr and PrevPtr)|**One** (NextPtr)|DLL requires **double the memory** for pointers compared to a Singly Linked List.|
|**Memory Consumption**|Higher|Lower|This memory increase can be significant in applications with a large number of nodes, making the DLL less desirable when memory is strictly limited.|

---

# Insertion sort

---

<!-- _class: compact fit-50 -->

# Insertion sort

Insertion Sort is a simple, stable sorting algorithm that builds the final sorted array (or list) one item at a time. It is highly intuitive and often compared to how a person might sort a hand of playing cards.

The Mechanism:

- The array is conceptually divided into a sorted portion (initially containing only the first element) and an unsorted portion.
- The algorithm iteratively takes the next element from the unsorted part.
- It then inserts this element into its correct position within the already sorted part.
- This process involves shifting all elements greater than the current element one position to the right to create a space for the insertion.

---

# Insertion sort

```c
void insertionSort(int arr[], int n)
{
    int i, key, j;
    for (i = 1; i < n; i++)
    {
        key = arr[i];
        j = i - 1;
        while (j >= 0 && arr[j] > key)
        {
            arr[j + 1] = arr[j];
            j = j - 1;
        }
        arr[j + 1] = key;
    }
}
```

```text
Algorithm insertionSort (A, n):
	Input: An array A storing n ≥ 1 integers.
	for i ← 1 to n - 1 do
    	key ← A[i]
    	j ← j – 1
    	while j ≥ 0 and A[j] > key do
    		A[j + 1] ← A[j]
    		j ← j – 1
    	A[j + 1] ← key
```

---

# Insertion sort - Strengths and Weaknesses

- Poor Scalability: The primary weakness is its O(n^2 ) complexity for large, unsorted lists. This makes it impractical for sorting large volumes of data compared to O(nlogn) algorithms.
- High Number of Shifts: In the worst case, every insertion requires a large number of shifts to make space for the new element, making it slower than other O(n^2 ) algorithms like Selection Sort (which minimizes swaps).
- Typical Use Cases:
  - **Small Arrays**: Used efficiently to sort small arrays where n^2  overhead is negligible.
  - **Nearly Sorted Data**: Ideal for maintaining the sorted order of **a dynamic list where new elements are frequently inserted**.

---

# Questions?

---

<!-- _class: compact caption-slide -->

# Thank You
