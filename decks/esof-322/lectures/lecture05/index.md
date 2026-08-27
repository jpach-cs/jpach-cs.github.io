---
marp: true
theme: pach
paginate: true
title: "Software Engineering"
---

# Software Engineering

*Lecture 5*

---

## Today’s Agenda

Unit test

Engine Unity for C

Forking on GitHub

Working with code

---

# unit

*tests*

---

## What are Unit Tests

Unit tests are automated checks of small parts of a program (such as functions or procedures) to verify that they work correctly. The idea is to test whether a given function returns the correct result for specific input values.

- Why use unit tests?
  - You catch bugs faster.
  - You don’t have to manually test your code every time.
  - You gain confidence that changes in the code don’t break other parts (this is called regression prevention).

---

## Introduction to Unity Test in C

When we write programs, we need a way to check if our code works correctly. There are two common tools for this in C:

- Assertions (assert)
- Unit testing frameworks (like Unity Test)

---

## What is an assert?

- Assert() is a built-in tool in C. (#include &lt;assert.h&gt;)
- It is mainly used by the programmer while writing code to check if assumptions are correct.
- If the condition in assert is false, the program immediately stops (crashes). Example:
- Good for debugging, **but not suitable for automated testing**, because once it fails, the program cannot continue.

\#include &lt;assert.h&gt;<br>int divide(int a, int b)

{

    assert(b != 0);  // program will stop if b == 0

    return a / b;

}

---

## Word – 'assert'

- In structurally or imperatively oriented programming, function names are typically nouns — for example, sum(), pow(), or strlen().
- In object-oriented programming, we create instances of objects represented by nouns, but the methods invoked on those objects are usually verbs, describing actions performed on the instance — for example, trash.clean().
- In the C language, the function assert() is an exception. Unlike typical function names, it is a verb, reflecting the programmer’s intention to assert — to strongly claim — that a certain condition holds true.

Conceptually, it’s as if the programmer is saying: “I assert that x equals 1”     assert(x==1);

---

## Word – 'assert'

- The original intent behind assert() was to allow developers to write code like:

sum(a, b);

assert(a &gt; 0);

- These statements were meant to halt program execution if the condition was not met. In short, they served as additional safeguards to help speed up debugging.
- Over time, **most programming languages adopted dedicated unit testing frameworks** — even C, thanks to the Unity library. Unity was designed with **a plan-driven** approach in mind, enabling developers to write tests before implementing the actual code.

---

## Exit code / return code / status code

- The program returned exit code 0, which means it ran successfully.
- A non-zero exit code usually indicates an error or failure.

int main(int argc, char \*argv\[\])

{

    return 0; // cmd/powershell:  echo $LASTEXITCODE

}

- C:&gt;main.exe
- C:&gt;echo $LASTEXITCODE
- 0
- C:&gt;

---

## What is Unity Test?

- Unity Test is a unit testing framework for C.
- It allows us to test functions in a safe and controlled way.
- Unlike assert, Unity Test does not stop the program when a test fails. Instead, it records the failure and continues with other tests.
- This way we get a summary of all passed and failed tests at the end. Example test with Unity:

\#include "unity.h"

void test\_addition(void)

{

    TEST\_ASSERT\_EQUAL(4, 2 + 2);  // this will pass

    TEST\_ASSERT\_EQUAL(5, 2 + 2);  // this will fail, but program continues

}

---

## The difference: assert vs. Unity Test

- Assert() → for the programmer, during development, to catch bugs early.
- Unity Test → for systematic testing of finished functions, with clear reports.

---

## Error handling in C

- C has no exceptions (like in Java or Python).
- Instead, functions use special return values to signal errors:
  - Functions returning int often use -1 to mean “something went wrong.”
  - Functions returning pointers use NULL to mean “failure.”
  - At the program level, the exit code follows the same rule:
  - 0 = success
  - non-zero = error

int findElement(int arr\[\], int size, int target)

{

    for(int i = 0; i &lt; size; i++)

    {

        if(arr\[i\] == target)

            return i;  // found, return index

    }

    return -1;  // not found → error

}

---

## Summary

- Use assert inside your code while developing → catches programmer mistakes early.
- Use Unity Test to run proper unit tests on your functions.
- Handle errors with special return values (-1 for int, NULL for pointers), so tests can check failures without crashing the program.

---

## Introduction to Unity Test Framework in C

Unity is a lightweight testing framework for the C language. It allows us to write **unit tests** that check whether our functions work as expected.

When using Unity, every test file usually has three important parts:

- **setUp()** – a function that runs before each test. You can use it to prepare data or reset variables.
- **tearDown()** – a function that runs after each test. You can use it to clean up resources.
- **UNITY\_BEGIN(); RUN\_TEST(...); return UNITY\_END();** – this is the main pattern for starting Unity, running all tests, and reporting the results.

---

## Common Unity Assertions

Assertions are the heart of testing. They compare the expected result with the actual result and tell us if the test passed or failed. Some of the most common are:

- TEST\_ASSERT\_EQUAL(expected, actual)
  - – check if two integers are the same.
- TEST\_ASSERT\_NULL(ptr) / TEST\_ASSERT\_NOT\_NULL(ptr)
  - – check if a pointer is NULL or not.
- TEST\_ASSERT\_TRUE(condition) / TEST\_ASSERT\_FALSE(condition)
  - – check if a condition is true or false.
- TEST\_ASSERT\_FLOAT\_WITHIN(delta, expected, actual)
  - – check if two floating-point numbers are equal within a tolerance.
- TEST\_ASSERT\_EQUAL\_STRING(expected, actual)
  - – check if two strings are equal.
- TEST\_ASSERT\_GREATER\_THAN(threshold, actual)
  - – custom/extended check if a value is greater than a threshold.

---

## Common Unity Assertions

- TEST\_ASSERT\_EQUAL(expected, actual)
  - – check if two integers are the same.
- TEST\_ASSERT\_NULL(ptr) / TEST\_ASSERT\_NOT\_NULL(ptr)
  - – check if a pointer is NULL or not.
- TEST\_ASSERT\_TRUE(condition) / TEST\_ASSERT\_FALSE(condition)
  - – check if a condition is true or false.

---

## Common Unity Assertions

- TEST\_ASSERT\_FLOAT\_WITHIN(delta, expected, actual)
  - – check if two floating-point numbers are equal within a tolerance.
- TEST\_ASSERT\_EQUAL\_STRING(expected, actual)
  - – check if two strings are equal.
- TEST\_ASSERT\_GREATER\_THAN(threshold, actual)
  - – custom/extended check if a value is greater than a threshold.

---

## Understanding setUp() and tearDown()

In Unity, the function setUp() is always called before each test. You use it to prepare the environment: initialize variables, reset arrays, or allocate memory.

The function tearDown() is always called after each test. At first, this may look unnecessary. In modern languages with a garbage collector (like Java or Python), developers rarely think about memory allocation and cleanup, so they might wonder: “Why do I need tearDown() if setUp() can just reset the data again?”

The answer is that in C and C++ we often use dynamic memory. If a test uses malloc() (or new in C++), we must free that memory after the test, otherwise we create memory leaks. That’s why tearDown() is important—it ensures that all resources used by a test are properly released, no matter if the test passed or failed.

So the pattern is:

- setUp() → prepare everything a test needs.
- tearDown() → clean up, especially for dynamic memory.

This makes every test independent, safe, and repeatable.

---

## An Introduction to Forking on GitHub

Let's break down the fundamentals of forking on GitHub. This is one of the most important concepts for collaborating on open-source projects.

- What is Forking?

**Forking** is the process of creating a **personal copy** of a public repository on your own GitHub account. It's like making a private duplicate of someone else's project. This gives you a safe sandbox to experiment, make your own changes, and work on new features without altering the original code.

---

## An Introduction to Forking on GitHub

- Cloning the Repository to Your Computer

Once you have your copy (the fork), the next step is to bring it down to your local machine. This process is called cloning. You use the git clone command for this.

- How to do it:
- Navigate to your newly created fork on GitHub.
- Click the green &lt;&gt; Code button and copy the URL.
- Open your terminal (or Git Bash) on your computer.
- Type the command, pasting the URL you copied: git clone \[copied\_url\]
- Press Enter. The repository will be downloaded to your computer, and you can start working in your code editor.

---

## An Introduction to Forking on GitHub

- Working on Your Code and Pushing Changes

Now that you have the repository on your local machine, you can make changes, add files, and so on. When you're finished, you need to push your changes back to GitHub. Remember, you're pushing the changes to your copy (the fork), not the original repository.

The steps are as follows:

- Open your terminal in the repository folder.
- Commit your changes (commit):
- Push the changes to GitHub (push):
- git add .
- git commit -m "Brief description of my changes"
- git push origin main

---

## An Introduction to Forking on GitHub

- Summary

In short, the process looks like this:

The steps are as follows:

- Fork the original repository to create your own copy on GitHub.
- Clone that copy to work locally on your computer.
- Push your changes from your local computer back to your fork on GitHub.

---

# working

*with code*

---

## Working with code

- <https://github.com/jpach-cs/C_tests>

---

# Thank

*You!*
