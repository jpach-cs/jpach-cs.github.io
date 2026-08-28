---
marp: true
theme: pach
paginate: true
footer: "CSCI 446 | Artificial Intelligence |  J. L. Pach"
backgroundColor: "hsl(150, 36%, 96%)"
title: "CSCI 446"
---

<!-- _class: lead -->

<!-- _paginate: skip -->

# CSCI 446

## Artificial Intelligence

### Lecture: 1

J. L. Pach

---

# Outline:

- Syllabus
- Textbook
- Canvas
- Introduction

---

<!-- _class: caption-slide -->

<!-- _paginate: skip -->

# Syllabus

<!--
## Subtitle
-->

---

# Some basic facts about the course

<div class="columns">

<div class="card">

## Course Name

- Artificial Intelligence (CSCI 446)

## Credit Hours

- 3 credits
- 1.25 hour lecture twice a week

</div>

<div class="card">

## Lecture & Lab

- Tuesday & Thursday

- 09:30 – 10:45 a.m. in NRB 226

</div>

</div>

---

# Syllabus

- Course Description

- Textbooks

- Class Rules

- Grading

- Accommodations & Academic Dishonesty

- Declaration of authorship

<!--
TUTAJ WPISZ TO, CO CHCESZ POWIEDZIEĆ:
- Przywitaj studentów CSCI 446.
- Podkreśl, że IDE to nie tylko edytor, ale cały ekosystem.
- Wspomnij o debuggerze jako narzędziu, które oszczędza godziny pracy.
-->

---

# Course Description

<div class="card justify lh-30">

An introduction to the basic concepts of Artificial Intelligence. Topics to be covered include the history of AI, the problems treated in AI, solution techniques, state spaces, search algorithms and heuristics, expert systems, natural language processing, and robotics.

</div>

---

# …a few words

<div class="card justify">

Instead of trying to define artificial intelligence directly, it may be easier to start with what it is not. AI is a broad field encompassing many methods and approaches, all aimed at building systems that can make decisions, understand language, learn, and solve problems. AI is often mistakenly equated solely with artificial neural networks. However, neural networks are tools used in machine learning (ML), which is just one subfield of AI. The ML 447 course at Montana Tech is dedicated specifically to those topics. Other techniques, such as the Naive Bayes classifier, k-nearest neighbours, image recognition, and pattern analysis, also fall under machine learning or data mining. While they are part of AI, they do not define it entirely.

</div>

---

<div class="card justify lh-10">

# AI 446

## on focuses on the foundations of artificial intelligence:

- logic,
- knowledge representation,
- reasoning,
- planning,
- natural language processing.

These are the core elements that underpin intelligent systems — before we even begin to *teach* them.

</div>

---

# Textbooks

![Book h:100](book.svg)

**Required:** *Russell, S. J., & Norvig, P. (2021). Artificial Intelligence: A Modern Approach (4th ed.).<br>
Pearson.*

**Optional:** *Moroney, L. (2021). AI and Machine Learning for On-Device Development: A Programmer's<br>
Guide. " O'Reilly Media, Inc.*

**Optional:** *Situnayake, D., & Plunkett, J. (2023). AI at the Edge. " O'Reilly Media, Inc.*

---

<div class="justify">

# Grading Breakdown

\*\* The final grade will be calculated based on the following components:

- **Quizzes (25%)**:
  - Entrance Quizzes: Short quizzes (5-10 minutes) may be given at the beginning of some classes to assess understanding of the previous material.
  - Two Major Quizzes: 50-minute quizzes administered throughout the semester. Each student will have one opportunity to retake each quiz at the end of the semester.
- **Assignments (75%)**: Regular, individual assignments will primarily be completed during class time;<br>
The final grade will be calculated as a weighted average of the scores obtained in each component.\*\*

</div>

---

<div class="justify">

# In-Person Format

This is strictly an in-person course. Regular attendance and active participation are expected.

## Attendance Policy

- Attendance at every class is required.
- Students are allowed up to two unexcused absences during the semester without penalty.

**Each additional unexcused absence beyond this two-absence allowance will result in a 1 percentage-point deduction from the final course grade.**

</div>

---

<div class="justify lh-20">

# Excused Absences & Emergencies

- Official university-excused absences, university-sanctioned activities, serious personal emergencies, and documented medical circumstances will not count toward the unexcused absence allowance.
- Students should notify the instructor as soon as reasonably possible when an emergency or officially excused absence occurs.

</div>

---

<div class="justify lh-25">

# Laboratory Rules

## Entrance Quiz

- When an entrance quiz is scheduled, it will consist of three questions.
- A score of at least 2 out of 3 is required to pass.
- A failed entrance quiz may be retaken up to two times during the semester. Only failed entrance quizzes may be retaken.

</div>

---

<div class="justify">

# Assignments & Deadline

- Students will have six calendar days to complete and submit each assignment.
- The deadline is strict. Once the six-day submission period has closed, the normal submission path will be closed and late or makeup submissions will not be accepted, except where an official University policy, documented emergency, or approved accommodation requires otherwise.
- Students are responsible for submitting their work before the deadline. Students should not wait until the final minutes before the deadline to submit an assignment.

## Brief Concluding Quiz

- When scheduled, the concluding quiz is a short summative assessment covering the material addressed during the laboratory session.

</div>

---

<div class="justify">

# Code Formatting, Authorship & Declaration

- Every submitted source file must begin with exactly four lines of comments containing the required authorship declaration.
- The following template must be used:

```c
// Your Name
// CSCI 446 Fall 2026
// Programming Assignment #1
// I declare that I am the author of this work, take full responsibility for it, and have disclosed any material external assistance.
```

</div>

---

<div class="justify">

# Authorship Requirement

- The four-line declaration is **mandatory**.
- A source file submitted without the required declaration will receive **0 points**.
- If a student submits an assignment before the deadline but accidentally omits the required declaration, the instructor may allow the student to resubmit **the same code with the declaration added** after the deadline as a correction of an administrative omission.
- This correction is limited strictly to adding the required declaration. No modification, improvement, debugging, or other change to the submitted code is permitted after the original deadline.
- Repeated failure to include the required declaration may be treated as failure to comply with the assignment requirements.

</div>

---

# Academic Integrity, Collaboration & External Resources

<div class="justify">

Students are encouraged to use appropriate external resources to learn and solve problems. Such resources may include:

- textbooks and other books;
- official programming documentation;
- technical websites and documentation;
- Stack Overflow and similar technical resources;
- ChatGPT, Gemini, GitHub Copilot, and other AI-assisted tools.

**The use of an external resource does not, by itself, constitute academic misconduct.** However, students remain fully responsible for the work they submit.

</div>

---

<div class="justify">

# Disclosure of External Assistance

- Students must disclose **material external assistance** that contributed to their submitted work.
- Such assistance may include, but is not limited to, substantial assistance from another person, technical resources, or generative AI tools.
- The disclosure should be made in an appropriate comment in the source code.

For example:

```
// I used the C standard library documentation to verify the behavior of strtok().
```

or:

```
// I used ChatGPT to help explain pointer arithmetic.
// I wrote, tested, and verified the submitted implementation myself.
```

</div>

---

# Disclosure of External Assistance

<div class="justify lh-30">

The purpose of this requirement is not to prohibit the use of external resources. Its purpose is to ensure that the origin of significant assistance is honestly acknowledged.<br>
Students are **not required to document ordinary searches or routine consultation of documentation** that do not materially contribute to the submitted work.

</div>

---

# Responsibility for Submitted Work

- Regardless of what resources were used during the development process, each student is fully responsible for understanding the work submitted under their name.
- Assignments may be reviewed orally by the instructor.
- During such a review, the instructor may ask the student to:
  - explain specific lines of code, how an algorithm works;
  - explain why a particular implementation was chosen;
  - predict what the program will do for a particular input;
  - identify or explain an error;
  - modify part of the submitted code;
  - demonstrate the operation of the submitted program.

---

<div class="justify lh-20">

# Responsibility for Submitted Work

The purpose of such a review is to establish that the student understands and is responsible for the submitted work.<br>
A student's inability to explain substantial portions of submitted work, particularly after reasonable questioning and clarification, may be considered as evidence when determining whether the work was genuinely authored by the student. Such evidence will be evaluated together with the other available evidence in accordance with the Montana Tech Student Code of Conduct.

</div>

---

# Declaration of Responsibility

By submitting an assignment, the student declares that:

1. I am the author of the work I am submitting.
2. I have disclosed any material external assistance used in preparing this work.
3. I understand the code and other work that I am submitting.
4. I take full responsibility for the submitted work.
5. I understand that submitting work that is not my own, or concealing material external assistance, may constitute academic misconduct and may be referred to the appropriate University authority.

**The four-line source-file declaration constitutes the student's acknowledgment of these requirements.**

---

# University Accommodations

<div class="justify lh-20">

- Students who require academic accommodations should work directly with Montana Tech Disability Services and provide the appropriate documentation to the instructor as soon as possible.
- Approved accommodations will be provided in accordance with University policy.

</div>

---

# Canvas

## Lecture & Laboratory:<br><br>

### (74801) CSCI 446: Artificial Intelligence <br><br><br>

## Check if you are registered for the course and have access to it!

---

# Integrated development environment

![SM](IDE.svg)

---

<!-- _class: caption-slide -->

<!-- _paginate: skip -->

# Thank

## You
