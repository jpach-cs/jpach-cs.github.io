---
marp: true
theme: pach
paginate: true
footer: "CSCI 232 | Algorithms & Data Structures | J. L. Pach"
title: "CSCI 232  Data Structures & Algorithms"
---

<!-- _class: lead -->

# CSCI 232 <br>Data Structures &amp; Algorithms

## Lecture 17

Dr. Jakub L. Pach

---

# Merge sort

<!-- [Lecture 3: Insertion Sort, Merge Sort (youtube.com)](https://www.youtube.com/watch?v=Kg4bqzAqRBM&t=1493s&ab_channel=MITOpenCourseWare)
[Learn Merge Sort in 13 minutes 🔪 (youtube.com)](https://www.youtube.com/watch?v=3j0SWDX4AtU&t=336s&ab_channel=BroCode) -->

---

<!-- _class: fit-90 -->

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

<!-- _class: fit-90 -->

# C

```c
// Function to merge two halves of the array
void merge(int arr[], int left, int mid, int right)
{
    int i, j, k;
    int n1 = mid - left + 1;
    int n2 = right - mid;

    // Create temp arrays
    int* L = (int*) malloc(n1 * sizeof(int));
    int* R = (int*) malloc(n2 * sizeof(int));

    for (i = 0; i < n1; i++)     // Copy data to temp arrays
        L[i] = arr[left + i];
    for (j = 0; j < n2; j++)
        R[j] = arr[mid + 1 + j];

    // Merge the temp arrays back into arr
    i = 0; j = 0;// Initial index of the first / second ssubarray
    k = left; // Initial index of the merged subarray
    while (i < n1 && j < n2)
    {
        if (L[i] <= R[j])
        {
            arr[k] = L[i];
            i++;
        }
        else
        {
            arr[k] = R[j];
            j++;
        }
        k++;
    }
    while (i < n1)
    { // Copy the remaining elements of L[]
        arr[k] = L[i];
        i++;
        k++;
    }
    while (j < n2)
    { // Copy the remaining elements of R[]
        arr[k] = R[j];
        j++;
        k++;
    }
    free(L);     // Free the allocated memory
    free(R);
}
```

```c
void mergeSort(int arr[], int left, int right)
{  // Function to implement merge sort
    if (left < right)
    {
        int mid = left + (right - left) / 2;

        // Sort first and second halves
        mergeSort(arr, left, mid);
        mergeSort(arr, mid + 1, right);

        // Merge the sorted halves
        merge(arr, left, mid, right);
    }
}
```
