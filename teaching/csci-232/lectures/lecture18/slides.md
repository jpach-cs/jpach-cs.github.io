---
marp: true
theme: pach
paginate: true
title: "CSCI 232  Data Structures & Algorithms"
---

<!-- _class: lead -->

# CSCI 232 <br>Data Structures &amp; Algorithms

## Lecture 18
Dr. Jakub L. Pach

---

# Outline

- Syllabus, Textbook, Moodle
- Something about me
- IDE

---

# heap sort

<!-- [Lecture 3: Insertion Sort, Merge Sort (youtube.com)](https://www.youtube.com/watch?v=Kg4bqzAqRBM&t=1493s&ab_channel=MITOpenCourseWare)
[Learn Merge Sort in 13 minutes 🔪 (youtube.com)](https://www.youtube.com/watch?v=3j0SWDX4AtU&t=336s&ab_channel=BroCode) -->

---

# Pseudocode

```text
Algorithm mergeSort (A, l, r)
	Input: An array A with indices 				ranging from 𝑙 to 𝑟 storing n ≥ 			1 integers.
if l < r
m ← ⌊(l+r)/2⌋
mergeSort(A, l, m)
mergeSort(A, m+1, r)
merge(A, l, m, r)
```

```text
merge(A, l, m, r)
	n1 = m - l + 1
	n2 = r - m
let L be a new array of size n1
let R be a new array of size n2
	for i ← 0 to n1 – 1
		L[i] ← A[l + i]
	for j ← 0 to n2 – 1
	   R[j] ← A[m + 1 + j]
		i ← 0, j ← 0, k ← l
	while i < n1 and j < n2
		if L[i] <= R[j]
			A[k] ← L[i]
			i ← i + 1
		else
			A[k] ← R[j]
			j ← j + 1
			k ← k + 1
		while i < n1
			A[k] ← L[i]
			i ← i + 1
		    k ← k + 1
		while j < n2
			A[k] ← R[j]
			j ← j + 1
			k ← k + 1
```

---

# Lecture

- [Lecture 4: Heaps and Heap Sort](https://www.youtube.com/watch?v=B7hVxCmfPtM&t=768s)
- [https://www.youtube.com/watch?v=B7hVxCmfPtM&amp;t=768s](https://www.youtube.com/watch?v=B7hVxCmfPtM&t=768s)

![w:313px Picture 4](assets/image1.png)

![w:651px Picture 6](assets/image2.png)

---

# C

```c
void heapify(int arr[], int n, int i)
{
    int largest = i;         // root
    int left = 2 * i + 1;    // left child
    int right = 2 * i + 2;   // right child
    if (left < n && arr[left] > arr[largest])
        largest = left;


    if (right < n && arr[right] > arr[largest])
        largest = right;


    if (largest != i)
    {
        int temp = arr[i];
        arr[i] = arr[largest];
        arr[largest] = temp;


        heapify(arr, n, largest);
    }
}


```

```c
void heapSort(int arr[], int n)
{
    // Build max heap
    for (int i = n / 2 - 1; i >= 0; i--)
        heapify(arr, n, i);

    // Extract elements one by one
    for (int i = n - 1; i > 0; i--)
    {
        int temp = arr[0];
        arr[0] = arr[i];
        arr[i] = temp;


        heapify(arr, i, 0);
    }
}
```

---

- wyklad z MIT z tego przedmiotu jest super, moze nie ma sensu wszystkiego pisac, ale polaczenie mediany, binarnego sortowania i sortowania przez wstawianie jest meeeega. Abym mail tylko zycia aby to wszystko pieknie opanowac.

<!-- [Lecture 3: Insertion Sort, Merge Sort (youtube.com)](https://www.youtube.com/watch?v=Kg4bqzAqRBM&ab_channel=MITOpenCourseWare)
<https://www.youtube.com/watch?v=Kg4bqzAqRBM&amp;ab_channel=MITOpenCourseWare> 24:59 -->
