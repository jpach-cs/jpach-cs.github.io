---
marp: true
theme: pach
paginate: true
title: "CSCI 232  Data Structures & Algorithms"
---

# CSCI 232 <br>Data Structures &amp; Algorithms

*Lecture 19*

- Dr. Jakub L. Pach

---

## Outline

- Syllabus, Textbook, Moodle
- Something about me
- IDE

---

# **Analyzing Algorithm Complexity by Example**

<!-- [Lecture 3: Insertion Sort, Merge Sort (youtube.com)](https://www.youtube.com/watch?v=Kg4bqzAqRBM&t=1493s&ab_channel=MITOpenCourseWare)
[Learn Merge Sort in 13 minutes 🔪 (youtube.com)](https://www.youtube.com/watch?v=3j0SWDX4AtU&t=336s&ab_channel=BroCode) -->

---

## Analyzing Algorithm Complexity

- Review of Time Complexity
- Asymptotic Notation
- Primitive Operations

<!-- Today we’ll review how to analyze algorithms — not just theoretically, but by *counting primitive operations* and expressing the result using asymptotic notation.<br>You already know Big-O, Theta, and Omega — now let’s strengthen intuition by going through simple C examples step by step. -->

---

## Primitive Operations

|Symbol|Description|
|---|---|
|c₁|Assigning a value to a variable|
|c₂|Calling a function|
|c₃|Performing an arithmetic operation|
|c₄|Comparing two numbers|
|c₅|Indexing into an array|
|c₆|Following an object reference|
|c₇|Returning from a function|

<!-- Each of these represents one *basic operation*. When we analyze time complexity, we count how many of these are executed as a function of the input size n. -->

---

## Algorithm 1: Constant Time

- \- T(n) = c₁ + 2c₃ + c₇
- \- O(1), Θ(1), Ω(1)

int sumThree(int a, int b, int c)

{

    int result = a + b + c;

    return result;

}

|S.|Description|
|---|---|
|c₁|Assigning a value to a variable|
|c₂|Calling a function|
|c₃|Performing an arithmetic operation|
|c₄|Comparing two numbers|
|c₅|Indexing into an array|
|c₆|Following an object reference|
|c₇|Returning from a function|

<!-- &gt; This is the simplest possible case — the algorithm doesn’t depend on input size.
&gt; No loops, no recursion. The runtime is constant regardless of \`n\`. -->

---

## Algorithm 2: Linear Time

int sumArray(int A\[\], int n)

{

    int sum = 0;

    for (int i = 0; i &lt; n; i++)

    {

        sum += A\[i\];

    }

    return sum;

}

- T(n)=c1​+c1​+(n+1)c4​+n(c1​+c3​)+n(c1​+c3​+c5​)+c7 =
- T(n)=(3n+3)c​+2nc​+nc​+(n+1)c​+c​​= 7nc\*5c = 7n + 5
- \- \*O(1), Θ(1), Ω(1)

|S.|Description|
|---|---|
|c₁|Assigning a value to a variable|
|c₂|Calling a function|
|c₃|Performing an arithmetic operation|
|c₄|Comparing two numbers|
|c₅|Indexing into an array|
|c₆|Following an object reference|
|c₇|Returning from a function|

|Step|Description|Count|
|---|---|---|
|int sum = 0;|Initialization|c₁|
|int i = 0;|Loop initialization|c₁|
|i &lt; n|Loop condition|(n + 1) × c₄|
|i++|Increment (assignment + addition)|n × (c₁ + c₃)|
|sum += A\[i\];|Array access + addition + assignment|n × (c₅ + c₃ + c₁)|
|return sum;|Return statement|c₇|

<!-- Each iteration does a few simple operations — comparison, indexing, and addition.<br>Because the loop runs n times, the total time grows linearly. -->

---

## Algorithm 3: Quadratic Time

void printPairs(int A\[\], int n)

{

    for (int i = 0; i &lt; n; i++)

    {

        for (int j = 0; j &lt; n; j++)

        {

            printf("%d, %d\n", A\[i\], A\[j\]);

        }

    }

}

T(n)=c1​+(n+1)c4​+n(c1​+c3​)+n\[c1​+(n+1)c4​+n(c1​+c3​)+ n(c2+2(c5))\]

... T(n)=n2(2c5​+c2​+c3​+c4​)+n(c1​+c4​+c3​+c1​)+(c1​+c4​)

|S.|Description|
|---|---|
|c₁|Assigning a value to a variable|
|c₂|Calling a function|
|c₃|Performing an arithmetic operation|
|c₄|Comparing two numbers|
|c₅|Indexing into an array|
|c₆|Following an object reference|
|c₇|Returning from a function|

|Step|Description|Count|
|---|---|---|
|int sum = 0;|Initialization|c₁|
|int i = 0;|Loop initialization|c₁|
|i &lt; n|Loop condition|(n + 1) × c₄|
|i++|Increment (assignment + addition)|n × (c₁ + c₃)|
|sum += A\[i\];|Array access + addition + assignment|n × (c₅ + c₃ + c₁)|
|return sum;|Return statement|c₇|

<!-- Each iteration does a few simple operations — comparison, indexing, and addition.<br>Because the loop runs n times, the total time grows linearly. -->

---

## Algorithm 4: Logarithmic Time

int binarySearch(int A\[\], int n, int key)

{

    int left = 0, right = n - 1;

    while (left &lt;= right)

    {

        int mid = (left + right) / 2;

        if (A\[mid\] == key)

            return mid;

        else

            if (A\[mid\] &lt; key)

                left = mid + 1;

            else

                right = mid - 1;

    }

    return -1;

}

T(n)=(2c1​+c3​)+(k+1)c4​+k\[(c1​+2c3​)+(c5​+c4​)+(c5​+c4​+c1​+c3​)\]+c7​

|S.|Description|
|---|---|
|c₁|Assigning a value to a variable|
|c₂|Calling a function|
|c₃|Performing an arithmetic operation|
|c₄|Comparing two numbers|
|c₅|Indexing into an array|
|c₆|Following an object reference|
|c₇|Returning from a function|

|Step|Description|Cost|
|---|---|---|
|1|Initialize left = 0|c₁|
|2|Initialize right = n - 1|c₁ + c₃|
|3|Compare left &lt;= right|c₄|
|4|Compute mid = (left + right) / 2|c₁ + 2c₃|
|5|Compare A\[mid\] == key|c₅ + c₄|
|6|Compare A\[mid\] &lt; key|c₅ + c₄|
|7|Update left = mid + 1 or right = mid - 1|c₁ + c₃|
|8|Return value|c₇|

<!-- Binary search is one of the best examples of a logarithmic-time algorithm.<br>We start with two indices — left and right — and repeatedly cut the search interval in half.<br>Each iteration performs a constant number of primitive operations: a few comparisons, arithmetic operations, and assignments.<br>Because the number of iterations grows as log₂(n), the total time complexity is Θ(log n).
Notice how the structure of the algorithm guarantees efficiency — we don’t scan every element, just a small subset that keeps shrinking -->

---

## Algorithm 5: Linearithmic Time

void mergeSort(int arr\[\], int left, int right)

{

    if (left &lt; right)

    {

        int mid = (left + right) / 2;

        mergeSort(arr, left, mid);

        mergeSort(arr, mid + 1, right);

        merge(arr, left, mid, right);

    }

}

|S.|Description|
|---|---|
|c₁|Assigning a value to a variable|
|c₂|Calling a function|
|c₃|Performing an arithmetic operation|
|c₄|Comparing two numbers|
|c₅|Indexing into an array|
|c₆|Following an object reference|
|c₇|Returning from a function|

- \- Recurrence: T(n) = 2T(n/2) + O(n)
- \- Solved by Master Theorem → T(n) = O(n log n)
- \- \*\*O(n log n), Θ(n log n), Ω(n)\*\*

<!-- Merge sort splits the problem in half recursively and then merges.
The splitting gives you log(n) levels of recursion, and at each level you process all \`n\` elements — n × log n total.
**1️⃣ Operacje prymitywne w mergeSort**
**A. Warunek if (left &lt; right)**
Porównanie dwóch liczb → **c4**
Wartość zwracana zależy od wyniku porównania
**B. Obliczenie mid = (left + right) / 2**
Dodawanie → **c3**
Dzielenie → **c3**
Przypisanie do zmiennej → **c1**<br>**Razem:** c1 + 2c3
**C. Wywołanie rekurencyjne mergeSort(arr, left, mid)**
Koszt zależy od rozmiaru podtablicy → **T(n/2)**
**D. Wywołanie rekurencyjne mergeSort(arr, mid+1, right)**
Koszt zależy od rozmiaru podtablicy → **T(n/2)**
Przypisanie mid+1 → c1 + c3
**E. Wywołanie merge(arr, left, mid, right)**
Załóżmy, że funkcja merge porównuje i kopiuje elementy → **Θ(n)**
W szczegółach: w merge jest **pętla po wszystkich elementach od left do right**, więc liczba operacji prymitywnych to około **c \* (right-left+1) = c \* n**
<br>
**2️⃣ Rekurencyjna zależność czasowa**
Dla tablicy długości n:
Dwa wywołania rekurencyjne na połowie tablicy
Merge, które łączy dwie połowy, kosztuje **Θ(n)**
<br>
**3️⃣ Rozpisanie operacji prymitywnych (przybliżenie)**
if (left &lt; right) → c4
mid = (left + right)/2 → c1 + 2c3
mergeSort(arr, left, mid) → T(n/2)
mergeSort(arr, mid+1, right) → T(n/2) + c1 + c3 (przy mid+1)
merge(arr, left, mid, right) → c \* n
<br>
**4️⃣ Rozwiązanie rekurencji (Master Theorem)**
a = 2, b = 2, f(n) = cn
Sprawdzenie: f(n) = Θ(n), n^{log\_b a} = n^{log\_2 2} = n
Master Theorem → T(n) = Θ(n log n)
<br>
**5️⃣ Podsumowanie złożoności**
RodzajWartość**Best case**Θ(n log n)**Average case**Θ(n log n)**Worst case**Θ(n log n) -->

---

## Algorithm 6: Exponential Time

int fib(int n)

{

    if (n &lt;= 1) return n;

    return fib(n - 1) + fib(n - 2);

}

|S.|Description|
|---|---|
|c₁|Assigning a value to a variable|
|c₂|Calling a function|
|c₃|Performing an arithmetic operation|
|c₄|Comparing two numbers|
|c₅|Indexing into an array|
|c₆|Following an object reference|
|c₇|Returning from a function|

- Recurrence: T(n) = T(n–1) + T(n–2) + O(1)
- Grows exponentially: O(2ⁿ)
- O(2ⁿ), Θ(2ⁿ), Ω(2ⁿ)

<!-- This is the classic example of an inefficient recursive algorithm.<br>Each call creates two more calls — the total work doubles roughly each time.<br>Great for illustrating why complexity matters.
**Operacje prymitywne**
**A. Warunek if (n &lt;= 1)**
Porównanie → **c4**
Przypisanie zwracanej wartości → **c1**
**B. Wywołania rekurencyjne fib(n-1) i fib(n-2)**
Obliczenie n-1 → **c3** (odejmowanie)
Obliczenie n-2 → **c3**
Wywołanie fib(n-1) → **T(n-1)**
Wywołanie fib(n-2) → **T(n-2)**
**C. Dodawanie wyników fib(n-1) + fib(n-2)**
Operacja arytmetyczna → **c3**
Zwrócenie wyniku → **c7**
<br>
**2️⃣ Rekurencyjna zależność czasowa**
gdzie **c** = suma operacji prymitywnych w aktualnym wywołaniu (porównanie, odejmowanie, dodawanie, zwrócenie wartości).
<br>
**3️⃣ Złożoność czasowa**
Rekurencja jest klasyczna dla Fibonacciego: **eksploduje wykładniczo**
Dokładnie:
Złożoność wynika z tego, że każde wywołanie generuje dwa kolejne wywołania, a wiele podproblemów jest liczone wielokrotnie.
<br>
**4️⃣ Operacje prymitywne przybliżone**
Na poziomie pojedynczego wywołania:
OperacjaLiczbaPorównanie n &lt;= 11 (c4)Odejmowanie n-11 (c3)Odejmowanie n-21 (c3)Wywołania rekurencyjneT(n-1), T(n-2)Dodawanie wyników1 (c3)Zwrócenie wyniku1 (c7)
Łącznie: **c = 1 c4 + 3 c3 + 1 c7** na jednym wywołaniu, plus koszt rekurencji. -->

---

## Comparing Growth Rates

|Complexity|Example Algorithm|Growth|
|---|---|---|
|O(1)|Constant operations|Flat|
|O(log n)|Binary search|Very slow growth|
|O(n)|Summation, linear scan|Linear|
|O(n log n)|Merge sort|Moderate growth|
|O(n²)|Nested loops|Rapid growth|
|O(2ⁿ)|Recursive Fibonacci|Explosive|

---

## Pseudocode

- **Algorithm** mergeSort (A, l, r)
- **Input**: An array *A* with indices                 ranging from 𝑙 to 𝑟 storing *n* ≥             1 integers.
  - **if** l &lt; r
    - m ← ⌊(l+r)/2⌋
    - mergeSort(A, l, m)
    - mergeSort(A, m+1, r)
    - merge(A, l, m, r)
- merge(A, l, m, r)
- n1 = m - l + 1
- n2 = r - m
- let L be a new array of size n1
- let R be a new array of size n2
- **for** i ← 0 to n1 – 1
- L\[i\] ← A\[l + i\]
- **for** j ← 0 to n2 – 1
- R\[j\] ← A\[m + 1 + j\]
- i ← 0, j ← 0, k ← l
- **while** i &lt; n1 and j &lt; n2
- **if** L\[i\] &lt;= R\[j\]
- A\[k\] ← L\[i\]
- i ← i + 1
- **else**
- A\[k\] ← R\[j\]
- j ← j + 1
- k ← k + 1
- **while** i &lt; n1
- A\[k\] ← L\[i\]
- i ← i + 1
- k ← k + 1
- **while** j &lt; n2
- A\[k\] ← R\[j\]
- j ← j + 1
- k ← k + 1

---

<!-- pptx2marp: slide 14 has no extractable text or images -->
