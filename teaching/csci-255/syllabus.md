---
layout: default
title: CSCI 255 — Syllabus
---

[← Back to CSCI 255]({{ '/teaching/csci-112/' | relative_url }})

# CSCI 255: Introduction Embedded Systems



**Montana Technological University** | **Fall 2026**



## Course Information

*   **Instructor:** Dr. J. L. Pach, Ph.D.
*   **Email:** [jpach@mtech.edu](mailto:jpach@mtech.edu)
*   **Office Location:** MUS 103
*   **Office Hours:** Monday, Wednesday, Thursday 08:00 – 09:00 a.m. (Other times by appointment)
*   **Lecture:** Monday & Friday 12:00 – 12:50 p.m. in SE 308
*   **Laboratory:** Monday 02:00 – 04:50 p.m. in ELC 315


## Course Description

This course provides a practical introduction to embedded systems, focusing on the integration of software with physical hardware. Students design and implement systems using programmable processors and external components, learning how digital code interacts with real-world signals.
Topics include basic circuit design, digital input/output, signal generation (including pulse-width modulation), event-driven programming, and concurrent execution. Additional topics include analog signal acquisition using external conversion techniques and serial communication.
The course emphasizes real-world constraints such as power limitations, timing inaccuracies, and operating system overhead, including phenomena such as signal instability (e.g., PWM jitter).
Through a sequence of hands-on laboratory exercises, students develop the ability to design, implement, and debug complete embedded systems involving sensing, actuation, and feedback. The course is platform-agnostic and emphasizes concepts transferable across embedded architectures.



<!--
## Grading Policy
The course grade will be determined by two equally weighted components:

| Component | Weight | Details |
| :--- | :--- | :--- |
| **Lecture Component** | **40%** | Based on two midterm exams (one retake opportunity for each). |
| **Laboratory Component** | **60%** | Evaluated based on Entrance Quiz (30%), Assignments (40%), and Concluding Quiz (30%). |

*Note: Students have exactly 6 days to complete each assignment and submit their solution.*


## Textbooks

1.  **Required:** Brian W. Kernighan, Dennis M. Ritchie. *C Programming Language*, 2nd Edition. Prentice Hall, 1988.
2.  **Optional:** Seacord, R. C. (2024). *Effective C: An Introduction to Professional C Programming*. No Starch Press, Inc.


## Grading

The final course grade will be determined by two equally weighted components:
* Lecture Component: 40%
* Laboratory Component: 60%

The Laboratory Component is evaluated according to the following criteria:
* Entrance Quiz: 30%
* Assignments: 40%
* Brief Concluding Quiz: 30%

Not every laboratory session will necessarily include an entrance quiz or a concluding quiz. When scheduled, these assessments will count toward the corresponding laboratory component.

## Attendance & General Course Policies

### In-Person Format

* This is strictly an in-person course. Regular attendance and active participation are expected.

### Attendance Policy

* Attendance at every class is required.
* Students are allowed up to two unexcused absences during the semester without penalty.
* __Each additional unexcused absence beyond this two-absence allowance will result in a 1 percentage-point deduction from the final course grade.__

### Excused Absences & Emergencies

* Official university-excused absences, university-sanctioned activities, serious personal emergencies, and documented medical circumstances will not count toward the unexcused absence allowance.
* Students should notify the instructor as soon as reasonably possible when an emergency or officially excused absence occurs.

### Makeup Exams

* Makeup exams will only be granted for documented medical or officially recognized reasons.

## Laboratory Rules

### Entrance Quiz

* When an entrance quiz is scheduled, it will consist of three questions.
* A score of at least 2 out of 3 is required to pass.
* A failed entrance quiz may be retaken up to two times during the semester. Only failed entrance quizzes may be retaken.

### Assignments & Deadline

* Students will have six calendar days to complete and submit each assignment.
* The deadline is strict. Once the six-day submission period has closed, the normal submission path will be closed and late or makeup submissions will not be accepted, except where an official University policy, documented emergency, or approved accommodation requires otherwise.
* Students are responsible for submitting their work before the deadline. Students should not wait until the final minutes before the deadline to submit an assignment.

### Brief Concluding Quiz

* When scheduled, the concluding quiz is a short summative assessment covering the material addressed during the laboratory session.


## Code Formatting, Authorship & Declaration

### Code Formatting

* Every submitted source file must begin with exactly four lines of comments containing the required authorship declaration.
* The following template must be used:

  ```c
  // Your Name
  // CSCI 255 Fall 2026
  // Programming Assignment #1
  // I declare that I am the author of this work, take full responsibility for it, and have disclosed any material external assistance.
  ```

### Authorship Requirement

* The four-line declaration is __mandatory__.
* A source file submitted without the required declaration will receive __0 points__.
* If a student submits an assignment before the deadline but accidentally omits the required declaration, the instructor may allow the student to resubmit __the same code with the declaration added__ after the deadline as a correction of an administrative omission.
* This correction is limited strictly to adding the required declaration. No modification, improvement, debugging, or other change to the submitted code is permitted after the original deadline.
* Repeated failure to include the required declaration may be treated as failure to comply with the assignment requirements.


## Academic Integrity, Collaboration & External Resources

Students are encouraged to use appropriate external resources to learn and solve problems. Such resources may include:

* textbooks and other books;
* official programming documentation;
* technical websites and documentation;
* Stack Overflow and similar technical resources;
* ChatGPT, Gemini, GitHub Copilot, and other AI-assisted tools.

__The use of an external resource does not, by itself, constitute academic misconduct.__<br>
However, students remain fully responsible for the work they submit.

### Disclosure of External Assistance

* Students must disclose __material external assistance__ that contributed to their submitted work.
* Such assistance may include, but is not limited to, substantial assistance from another person, technical resources, or generative AI tools.
* The disclosure should be made in an appropriate comment in the source code.

For example:

```c
// I used the C standard library documentation to verify the behavior of strtok().
```

  or:

```c
// I used ChatGPT to help explain pointer arithmetic.
// I wrote, tested, and verified the submitted implementation myself.
```

The purpose of this requirement is not to prohibit the use of external resources. Its purpose is to ensure that the origin of significant assistance is honestly acknowledged.
Students are __not required to document ordinary searches or routine consultation of documentation__ that do not materially contribute to the submitted work.

### Responsibility for Submitted Work

* Regardless of what resources were used during the development process, each student is fully responsible for understanding the work submitted under their name.
* Assignments may be reviewed orally by the instructor.
* During such a review, the instructor may ask the student to:
  * explain specific lines of code;
  * explain how an algorithm works;
  * explain why a particular implementation was chosen;
  * predict what the program will do for a particular input;
  * identify or explain an error;
  * modify part of the submitted code;
  * demonstrate the operation of the submitted program.

The purpose of such a review is to establish that the student understands and is responsible for the submitted work. 
A student's inability to explain substantial portions of submitted work, particularly after reasonable questioning and clarification, may be considered as evidence when determining whether the work was genuinely authored by the student. Such evidence will be evaluated together with the other available evidence in accordance with the Montana Tech Student Code of Conduct.

### Academic Dishonesty
* Submitting another person's work as one's own, submitting content derived directly from generative AI as one's own original work without appropriate acknowledgment, concealing material external assistance, or otherwise violating the University's academic integrity requirements may constitute academic misconduct.
* Academic misconduct may result in a failing or reduced grade for the affected assignment, examination, laboratory, or course, in accordance with University policy.
* Suspected academic misconduct will be handled in accordance with the Montana Tech Student Code of Conduct and may be referred to the appropriate University authority.
* Additional University sanctions may apply depending on the circumstances and the University's determination.


## Declaration of Responsibility

By submitting an assignment, the student declares that:

1. I am the author of the work I am submitting.
2. I have disclosed any material external assistance used in preparing this work.
3. I understand the code and other work that I am submitting.
4. I take full responsibility for the submitted work.
5. I understand that submitting work that is not my own, or concealing material external assistance, may constitute academic misconduct and may be referred to the appropriate University authority.

__The four-line source-file declaration constitutes the student's acknowledgment of these requirements.__

## University Accommodations

* Students who require academic accommodations should work directly with Montana Tech Disability Services and provide the appropriate documentation to the instructor as soon as possible.
* Approved accommodations will be provided in accordance with University policy.


## Student Learning Outcomes

 Upon successful completion of this course, students will demonstrate the ability to:

    R1.  Demonstrate knowledge of program structure and organization, including data types, variable declarations, and initialization.

    R2.   Distinguish between local, global, and static variables, and understand their scope and lifetime within a program.

    R3.  Effectively use unary, binary, and ternary operators in the C programming language.

    R4.  Construct and implement control structures and loops for managing program flow.

    R5.  Define and utilize complex data structures, including structures, unions, and enumerations.

    R6.  Make use of built-in libraries for common programming tasks.

    R7.  Work with pointers, including pointers to variables, labels, and functions.

    R8.  Demonstrate the ability to perform dynamic memory allocation in their programs.

    R9.  Manage file operations, including reading from and writing to files.

    R10. Implement basic error handling mechanisms in their code.



SLO 1 – Problem Solving (ABET 1 – CS/SE)
Students will be able to analyze and solve embedded systems problems by integrating software, hardware, and basic electrical principles.
SLO 2 – Design & Implementation (ABET 2 – CS/SE)
Students will be able to design, implement, and test embedded applications that interact with physical components using GPIO, PWM, and communication interfaces.
SLO 3 – Experimentation & Analysis (ABET 6 – CS / SE)
Students will be able to conduct experiments, collect and interpret data from sensors, and evaluate system behavior under real-world constraints.
SLO 4 – System Constraints & Trade-offs (ABET 2 / SE emphasis)
Students will be able to evaluate trade-offs in embedded systems, including timing limitations, power constraints, and hardware/software interactions.
SLO 5 – Concurrency & Event-Driven Design (ABET 1 / SE)
Students will be able to develop programs that handle asynchronous events using polling, interrupts, or concurrency mechanisms.
SLO 6 – Hardware-Software Integration (ABET 2 / SE strong match)
Students will be able to interface software with external hardware components using standard protocols and electronic circuits.
SLO 7 – Safety & Reliability Awareness (ABET 4 – CS/SE)
Students will be able to recognize and mitigate risks related to hardware damage, incorrect wiring, and improper power usage.
SLO 8 – Teamwork & Lab Practice (ABET 5 – CS/SE)
Students will be able to collaborate effectively in a lab environment, including sharing equipment and troubleshooting systems.
SLO 9 – Self-Learning & Tool Usage (ABET 7 – CS/SE)
Students will be able to learn and apply new tools, libraries, and hardware platforms independently.
SLO 10 – System-Level Thinking (Custom, ale ABET-safe)

Students will be able to reason about complete computing systems, including the interaction between operating systems, hardware timing, and physical signals.
Course supports:
•	ABET CS outcomes: 1, 2, 4, 5, 6
•	ABET SE outcomes: 1, 2, 3, 4, 5, 6, 7



-->