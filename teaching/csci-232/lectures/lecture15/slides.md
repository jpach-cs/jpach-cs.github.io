---
marp: true
theme: pach
paginate: true
class: compact
footer: "CSCI 232 | Algorithms & Data Structures | J. L. Pach"
title: "CSCI 232  Data Structures & Algorithms"
---

<!-- _class: compact lead -->

# CSCI 232 <br>Data Structures &amp; Algorithms

## Lecture 15

Dr. Jakub L. Pach

---

# Analyzing algorithms

---

# arrayMax

- To summarize, the number of primitive operations t(n) (or  T(n)) executed by algorithm arrayMax is at least:

```text
Algorithm arrayMax(A, n):
	Input: An array A storing n ≥ 1 integers.
	Output: The maximum element in A.
	currentMax ← A[0]
	for i ← 1 to n - 1 do
    	if currentMax < A[i] then
        	currentMax ← A[i]
	return currentMax
```

- and at most:
- The best case (t(n) = 5n) occurs when A\[0\] is the maximum element, so that variable currentMax is never reassigned. The worst case (t(n) = 7n-2) occurs when the elements are sorted in increasing order, so that variable currentMax is reassigned at each iteration of the for loop.

![w:630px TextBox 4](assets/image14.png)

![w:587px TextBox 18](assets/image15.png)

<!-- why is n? because conditional will be one more times than everything else
normalnie jest n+1 -->

---

# recursiveMax

- from **recurrence equation** to **closed form**

![w:478px TextBox 4](assets/image27.png)

![w:435px TextBox 9](assets/image28.png)

---

<!-- _class: compact fit-90 -->

# Asymptotic notation

![w:1125px Content Placeholder 2](assets/image2.png)

---

<!-- _class: compact fit-90 -->

# The O(n) "big-oh" notation

- Let f(n) and g(n) be functions mapping nonnegative integers to real numbers. We say that f(n) is O(g(n) if there is a real constant c &gt; 0 and an integer constant n0 ≥ 1 such that f(n) ≤ c\*g(n) for every integer n ≥ n0. This definition is often pronounced as "f(n) is big-Oh of g(n)" or "f(n) is order g(n)".
- **Example:**
- 7n-4 is O(n).
- Proof: We need a real constant c &gt; 0 and an integer constant n0 ≥ 1 such that 7n-2 ≤ c\*n for every integer n ≥ n0. It is easy to see that a possible choice is c=7 and n0 = 1, but there are other possibilities as well.

<!-- ≥≤ -->

---

# Example

![w:1223px Picture 4](assets/image3.png)

![w:347px Picture 5](assets/image4.png)

![w:85px TextBox 7](assets/image5.png)

---

# Example

![w:347px Picture 7](assets/image4.png)

![w:236px TextBox 2](assets/image6.png)

![w:239px TextBox 3](assets/image7.png)

![w:128px TextBox 6](assets/image8.png)

---

# Example

- The big-Oh notation allows us to say that a function of n is "less than or equal to" another function (by the inequality "≤" in the definition), up to a constant factor (by the constant c in the definition) and in the asymptotic sense as n grows toward infinity (by the statement "n ≥ n0" in the definition).
- The big-Oh notation is used widely to characterize running times and space bounds of algorithm in terms of a parameter, n , which represents the "size" of the problem. For example, if we are interested in finding the largest element in an array of integers ( arrayMax given ), it would be most natural to let n denote the number of elements of the array. For example, we can write the following precise statement on the running time of algorithm arrayMax.

<!-- ≥≤ -->

---

# Theorem

![w:1189px Content Placeholder 4](assets/image9.png)

---

# Example

![w:588px Picture 3](assets/image10.png)

![w:818px Picture 7](assets/image11.png)

---

# Example

![w:1099px Picture 4](assets/image12.png)

---

# Example

![w:749px Picture 3](assets/image13.png)

![w:1012px Picture 6](assets/image16.png)

---

# Theorem – 8 rules!

![w:1092px Content Placeholder 6](assets/image17.png)

---

<!-- _class: compact long-title -->

# Analogy between the asymptotic comparison of two functions *f* and *g* and the comparison of two real numbers *a* and *b*

![w:511px Picture 6](assets/image18.png)

---

# 1/8 rule.

![w:1020px Picture 4](assets/image19.png)

![TextBox 5](assets/image20.png)

![TextBox 8](assets/image21.png)

![TextBox 19](assets/image22.png)

![TextBox 20](assets/image23.png)

---

# 2/8 rule.

![w:1006px Picture 3](assets/image24.png)

![TextBox 7](assets/image25.png)

![TextBox 8](assets/image26.png)

![TextBox 10](assets/image29.png)

![TextBox 14](assets/image30.png)

---

# 3/8 rule.

![w:1025px Picture 4](assets/image31.png)

![TextBox 10](assets/image32.png)

![TextBox 11](assets/image33.png)

![TextBox 7](assets/image34.png)

![TextBox 9](assets/image35.png)

---

# 4/8 rule.

![w:1057px Picture 4](assets/image36.png)

![TextBox 10](assets/image37.png)

![TextBox 11](assets/image38.png)

![TextBox 9](assets/image39.png)

---

# 5/8 rule.

![w:1139px Picture 4](assets/image40.png)

![w:179px TextBox 9](assets/image41.png)

---

# 6/8 rule.

![w:1141px Picture 6](assets/image42.png)

---

# 7/8 rule.

![w:1138px Picture 4](assets/image43.png)

---

# 8/8 rule.

![w:1151px Picture 4](assets/image44.png)

---

# Terminology for classes of functions.

![w:774px Content Placeholder 4](assets/image45.png)

---

# Using the big-Oh notation

![w:1110px Content Placeholder 4](assets/image46.png)

---

<!-- _class: compact caption-slide -->

# Thank You
