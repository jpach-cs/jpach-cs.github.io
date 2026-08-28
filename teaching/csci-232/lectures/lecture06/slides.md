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

## Lecture 6

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

<!-- _class: compact fit-80 -->

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

<!-- _class: compact fit-70 -->

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

<!-- _class: compact caption-slide -->

# Thank You
