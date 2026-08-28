---
marp: true
theme: pach
paginate: true
class: compact
footer: "ESOF 322 | Software Engineering | J. L. Pach"
title: "Chapter 5 – System Modeling"
---

<!-- _class: compact lead -->

# Chapter 5 – System Modeling

---

# Topics covered

- Context models
- Interaction models
- Structural models
- Behavioral models
- Model-driven
  - engineering
  - architecture

---

<!-- _class: compact fit-90 -->

# Types of System Modeling

- Visual Modeling (Graphical Modeling)

Describing a system using diagrams, typically in UML (Unified Modeling Language). Examples:

- Use Case Diagram
- Class Diagram
- Activity Diagram
- State, Component, and Sequence Diagrams, etc.

**Purpose:** To facilitate communication between stakeholders, developers, and designers through a clear, visual language that everyone can understand.

- Formal Modeling

Describing a system using mathematical notation, such as logic, sets, equations, or automata. Examples:

- Formal specifications using languages like Z, VDM, B, or Alloy
- Models suitable for formal verification (e.g., safety-critical systems, communication protocols)

**Purpose:** To ensure precision, support proof of system properties, and enable verification of safety, consistency, and correctness.

- System Modeling
- Visual Modeling (Graphical Modeling)
- Formal Modeling

---

# System modeling

- System modeling is the process of developing abstract models of a system, with each model presenting a different view or perspective of that system.
- System modeling has now come to mean representing a system using some kind of graphical notation, which is now almost always based on notations in the Unified Modeling Language (UML).
- System modelling helps the analyst to understand the functionality of the system and models are used to communicate with customers.

---

# Existing and planned system models

- Models of the existing system are used during requirements engineering. They help clarify what the existing system does and can be used as a basis for discussing its strengths and weaknesses. These then lead to requirements for the new system.
- Models of the new system are used during requirements engineering to help explain the proposed requirements to other system stakeholders. Engineers use these models to discuss design proposals and to document the system for implementation.
- In a model-driven engineering process, it is possible to generate a complete or partial system implementation from the system model.

---

# System perspectives

- An external perspective, where you model the context or environment of the system.
- An interaction perspective, where you model the interactions between a system and its environment, or between the components of a system.
- A structural perspective, where you model the organization of a system or the structure of the data that is processed by the system.
- A behavioral perspective, where you model the dynamic behavior of the system and how it responds to events.

---

# UML diagram types

- Activity diagrams, which show the activities involved in a process or in data processing .
- Use case diagrams, which show the interactions between a system and its environment.
- Sequence diagrams, which show interactions between actors and the system and between system components.
- Class diagrams, which show the object classes in the system and the associations between these classes.
- State diagrams, which show how the system reacts to internal and external events.

---

# Use of graphical models

- As a means of facilitating discussion about an existing or proposed system
  - Incomplete and incorrect models are OK as their role is to support discussion.
- As a way of documenting an existing system
  - Models should be an accurate representation of the system but need not be complete.
- As a detailed system description that can be used to generate a system implementation
  - Models have to be both correct and complete.

<!-- As a way to stimulate and focus discussion about an existing or proposed system. The purpose of the model is to stimulate and focus discussion among the software engineers involved in developing the system. The models may be incomplete (as long as they cover the key points of the discussion), and they may use the modeling notation informally. This is how models are normally used in agile modeling (Ambler and Jeffries 2002).
As a way of documenting an existing system. When models are used as docu mentation, they do not have to be complete, as you may only need to use models to document some parts of a system. However, these models have to be correct— they should use the notation correctly and be an accurate description of the system.
As a detailed system description that can be used to generate a system implementation. Where models are used as part of a model-based development process, the system models have to be both complete and correct. They are used as a basis for generating the source code of the system, and you therefore have to be very careful not to confuse similar symbols, such as stick and block arrow heads, that may have different meanings. -->

---

# The Unified Modeling Language (UML)

The Unified Modeling Language (UML) is a set of 13 different diagram types that may be used to model soft ware systems. It emerged from work in the 1990s on object-oriented modeling, where similar object-oriented notations were integrated to create the UML. A major revision (UML 2) was finalized in 2004. The UML is universally accepted as the standard approach for developing models of software systems. Variants, such as SysML, have been proposed for more general system modeling.

<http://software-engineering-book.com/web/uml/>

---

# Brief Overview of UML Evolution

The current official version of UML is UML 2.5.1, which was formally adopted in December 2017. This specification remains the latest widely recognized and stable version endorsed by the Object Management Group (OMG).

UML 2.5.1 simplifies and consolidates earlier subparts (Superstructure, Infrastructure, Diagram Interchange, OCL).

Brief Overview of UML Evolution

- UML 2.5 was released in June 2015, introduced a simplified,
- UML 2.5.1 followed in December 2017, as a minor revision refining semantics and fixing issues of the 2.5 release,
- Since then, UML 2.5.1 remains the current standard, with no newer major release yet.

---

# From The author

In this chapter, I use diagrams defined in the Unified Modeling Language (UML), which has become a standard language for object-oriented modeling. The UML has 13 diagram types and so supports the creation of many different types of system model. However, a survey showed that most users of the UML thought that five diagram types could represent the essentials of a system. I therefore concentrate on these five UML diagram types here:

- **Activity diagrams**, which show the activities involved in a process or in data processing.
- **Use case diagrams**, which show the interactions between a system and its environment.
- **Sequence diagrams**, which show interactions between actors and the system and between system components.
- **Class diagrams**, which show the object classes in the system and the associations between these classes.
- **State diagrams**, which show how the system reacts to internal and external events.

---

- Context models
  - **Activity diagrams**, which show the activities involved in a process or in data processing.
- Interaction models
  - **Use case diagrams**, which show the interactions between a system and its environment.
  - **Sequence diagrams**, which show interactions between actors and the system and between system components.
  - \*communication diagram / alternatywa
- Structural models
  - **Class diagrams**, which show the object classes in the system and the associations between these classes.
- Behavioral models
  - **State diagrams**, which show how the system reacts to internal and external events.

?Model-driven engineering

<!-- **Przykład ścieżki poznawczej studenta:**
**Zaczynamy** od kontekstu (Context Diagram) → wiemy, *co otacza system*.
**Potem** patrzymy na proces (Activity Diagram) → wiemy, *jak przebiega procedura*.
**Następnie** skupiamy się na interakcjach (Use Case, Sequence) → wiemy, *kto co robi i w jakiej kolejności*.
**Na końcu** patrzymy w głąb systemu (Class Diagram) → wiemy, *z czego się składa system i jakie ma dane*. -->

---

# Context models

---

# Context models

- Context models are used to illustrate the operational context of a system - they show what lies outside the system boundaries.
- Social and organisational concerns may affect the decision on where to position system boundaries.
- Architectural models show the system and its relationship with other systems.

---

# System boundaries

- System boundaries are established to define what is inside and what is outside the system.
  - They show other systems that are used or depend on the system being developed.
- The position of the system boundary has a profound effect on the system requirements.
- Defining a system boundary is a political judgment
  - There may be pressures to develop system boundaries that increase / decrease the influence or workload of different parts of an organization.

---

# The context of the Mentcare system

![w:790px 5.1 Mentcare context.eps](assets/image2.emf)
<!-- pptx2marp: image2.emf is a EMF file; many browsers cannot render it inline. Re-export from PowerPoint as PNG/SVG if this slide looks blank. -->

- double angle brackets - chevrons - «...»

---

# The context of the Mentcare system

![w:790px 5.1 Mentcare context.eps](assets/image2.emf)
<!-- pptx2marp: image2.emf is a EMF file; many browsers cannot render it inline. Re-export from PowerPoint as PNG/SVG if this slide looks blank. -->

- double angle brackets - chevrons - «...»

<!-- **chevrons)** «...» -->

---

# Process perspective

- Context models simply show the other systems in the environment, not how the system being developed is used in that environment.
- Process models reveal how the system being developed is used in broader business processes.
- UML activity diagrams may be used to define business process models.

---

# Process model of involuntary detention

![w:1166px 5.2 Detention Process.eps](assets/image3.emf)
<!-- pptx2marp: image3.emf is a EMF file; many browsers cannot render it inline. Re-export from PowerPoint as PNG/SVG if this slide looks blank. -->

<!-- Arrows represent the flow of work from one activity to another, and a solid bar indicates activity coordination.
When the flow from more than one activity leads to a solid bar, then all of these activities must be complete before progress is possible.
When the flow from a solid bar leads to a number of activities, these may be executed in parallel.
Therefore, in that Figure, the activities to inform social care and the patient’s next of kin, as well as to update the detention register, may be concurrent.
Arrows may be annotated with guards (in square brackets) that specify when that flow is followed. In that Figure, you can see guards showing the flows for patients who are dangerous and not dangerous to society. Patients who are dangerous to society must be detained in a secure facility.
However, patients who are suicidal and are a danger to themselves may be admitted to an appropriate ward in a hospital, where they can be kept under close supervision. -->

---

# Interaction models

---

# Interaction models

- Modeling user interaction is important as it helps to identify user requirements.
- Modeling system-to-system interaction highlights the communication problems that may arise.
- Modeling component interaction helps us understand if a proposed system structure is likely to deliver the required system performance and dependability.
- Use case diagrams and sequence diagrams may be used for interaction modeling.

---

# Use case modeling

- Use cases were developed originally to support requirements elicitation and now incorporated into the UML.
- Each use case represents a discrete task that involves external interaction with a system.
- Actors in a use case may be people or other systems.
- Represented diagramatically to provide an overview of the use case and in a more detailed textual form.

---

# Transfer-data use case

- A use case in the Mentcare system

![w:1048px 5.3 UseCase.eps](assets/image4.emf)
<!-- pptx2marp: image4.emf is a EMF file; many browsers cannot render it inline. Re-export from PowerPoint as PNG/SVG if this slide looks blank. -->

<!-- Figure 5.3 shows a use case from the Mentcare system that represents the task of uploading data from the Mentcare system to a more general patient record system. This more general system maintains summary data about a patient rather than data about each consultation, which is recorded in the Mentcare system. Notice that there are two actors in this use case—the operator who is transferring the data and the patient record system. The stick figure notation was originally devel oped to cover human interaction, but it is also used to represent other external sys tems and hardware. Formally, use case diagrams should use lines without arrows as arrows in the UML indicate the direction of flow of messages. Obviously, in a use case, messages pass in both directions. However, the arrows in Figure 5.3 are used informally to indicate that the medical receptionist initiates the transaction and data is transferred to the patient record system. -->

---

# Tabular description of the ‘Transfer data’ use-case

|**MHC-PMS: Transfer data**||
|---|---|
|Actors|Medical receptionist, patient records system (PRS)|
|Description|A receptionist may transfer data from the Mentcase system to a general patient record database that is maintained by a health authority. The information transferred may either be updated personal information (address, phone number, etc.) or a summary of the patient’s diagnosis and treatment.|
|Data|Patient’s personal information, treatment summary|
|Stimulus / Request\*|User command issued by medical receptionist|
|Response|Confirmation that PRS has been updated|
|Comments|The receptionist must have appropriate security permissions to access the patient information and the PRS.|

<!-- Composite use case diagrams show a number of different use cases. Sometimes it is possible to include all possible interactions within a system in a single composite use case diagram. However, this may be impossible because of the number of use cases. In such cases, you may develop several diagrams, each of which shows related use cases. -->

---

# Use cases in the Mentcare system involving the role ‘Medical Receptionist’

![w:623px 5.5 RecepUseCases.eps](assets/image5.emf)
<!-- pptx2marp: image5.emf is a EMF file; many browsers cannot render it inline. Re-export from PowerPoint as PNG/SVG if this slide looks blank. -->

<!-- For example, Figure 5.5 shows all of the use cases in the Mentcare system in which the actor “Medical Receptionist” is involved. Each of these should be accompanied by a more detailed description. The UML includes a number of constructs for sharing all or part of a use case in other use case diagrams. While these constructs can sometimes be helpful for system designers, Author say: “my experience is that many people, especially end-users, find them difficult to understand.” For this reason, these constructs are not described here. -->

---

# Sequence diagrams

- Sequence diagrams are part of the UML and are used to model the interactions between the actors and the objects within a system.
- A sequence diagram shows the sequence of interactions that take place during a particular use case or use case instance.
- The objects and actors involved are listed along the top of the diagram, with a dotted line drawn vertically from these.
- Interactions between objects are indicated by annotated arrows.

---

# Sequence diagram for View patient information

![w:868px 5.6 ViewInfo Seq Diag.eps](assets/image6.emf)
<!-- pptx2marp: image6.emf is a EMF file; many browsers cannot render it inline. Re-export from PowerPoint as PNG/SVG if this slide looks blank. -->

<!-- This diagram models the interactions involved in the View patient information use case, where a medical receptionist can see some patient information. The objects and actors involved are listed along the top of the diagram, with a dotted line drawn vertically from these. Annotated arrows indicate interactions between objects. The rectangle on the dotted lines indicates the lifeline of the object concerned (i.e., the time that object instance is involved in the computation). You read the sequence of interactions from top to bottom. The annotations on the arrows indicate the calls to the objects, their parameters, and the return values. This example also shows the notation used to denote alternatives. A box named alt is used with the conditions indicated in square brackets, with alternative interaction options separated by a dotted line. You can read this Figure as follows:
The medical receptionist triggers the ViewInfo method in an instance P of the PatientInfo object class, supplying the patient’s identifier, PID to identify the required information. P is a user interface object, which is displayed as a form showing patient information.
The instance P calls the database to return the information required, supplying the receptionist’s identifier to allow security checking. (At this stage, it is not important where the receptionist’s UID comes from.)
The database checks with an authorization system that the receptionist is authorized for this action.
If authorized, the patient information is returned and is displayed on a form on the user’s screen. If authorization fails, then an error message is returned. The box denoted by “alt” in the top-left corner is a choice box indicating that one of the contained interactions will be executed. The condition that selects the choice is shown in square brackets. -->

---

# Sequence diagram for Transfer Data

![w:838px 5.7 Transfer Data.eps](assets/image7.emf)
<!-- pptx2marp: image7.emf is a EMF file; many browsers cannot render it inline. Re-export from PowerPoint as PNG/SVG if this slide looks blank. -->

<!-- that Figure is a further example of a sequence diagram from the same system that illustrates two additional features. These are the direct communication between the actors in the system and the creation of objects as part of a sequence of operations. In this example, an object of type Summary is created to hold the summary data that is to be uploaded to a national PRS (patient records system). You can read this diagram as follows:
The receptionist logs on to the PRS.
Two options are available (as shown in the “alt” box). These allow the direct transfer of updated patient information from the Mentcare database to the PRS and the transfer of summary health data from the Mentcare database to the PRS.
In each case, the receptionist’s permissions are checked using the authorization system.
Personal information may be transferred directly from the user interface object to the PRS. Alternatively, a summary record may be created from the database, and that record is then transferred.
On completion of the transfer, the PRS issues a status message and the user logs off.
Unless you are using sequence diagrams for code generation or detailed docu mentation, you don’t have to include every interaction in these diagrams. If you develop system models early in the development process to support requirements engineering and high-level design, there will be many interactions that depend on implementation decisions. For example, in Figure 5.7 the decision on how to get the user identifier to check authorization is one that can be delayed. In an implementation, this might involve interacting with a User object. As this is not important at this stage, you do not need to include it in the sequence diagram. -->

---

- **Static (Structure) models** – show the structure of the system at rest:
  - Class diagram
  - Component diagram
  - Package diagram
  - Deployment diagram
  - Composite Structure diagram
- **Dynamic (behavioral) models** – show the behavior of the system during execution:
  - Sequence diagram
  - Communication diagram
  - Activity diagram
  - State Machine diagram

---

# Structural models

- Structural models of software display the organization of a system in terms of the components that make up that system and their relationships.
- Structural models may be static models, which show the structure of the system design, or dynamic models, which show the organization of the system when it is executing.
- You create structural models of a system when you are discussing and designing the system architecture.

---

# Class diagrams

- Class diagrams are used when developing an object-oriented system model to show the classes in a system and the associations between these classes.
- An object class can be thought of as a general definition of one kind of system object.
- An association is a link between classes that indicates that there is some relationship between these classes.
- When you are developing models during the early stages of the software engineering process, objects represent something in the real world, such as a patient, a prescription, doctor, etc.

---

# UML classes and association

![w:744px 5.8 ClassAssoc.eps](assets/image8.emf)
<!-- pptx2marp: image8.emf is a EMF file; many browsers cannot render it inline. Re-export from PowerPoint as PNG/SVG if this slide looks blank. -->

<!-- Class diagrams in the UML can be expressed at different levels of detail. When you are developing a model, the first stage is usually to look at the world, identify the essential objects, and represent these as classes.
The simplest way of writing these diagrams is to write the class name in a box. You can also note the existence of an association by drawing a line between classes.
For example, in that Figure is a simple class diagram showing two classes, Patient and Patient Record, with an association between them. -->

---

# Classes and associations in the MHC-PMS

![w:935px 5.9 MHCPMS-classes.eps](assets/image9.emf)
<!-- pptx2marp: image9.emf is a EMF file; many browsers cannot render it inline. Re-export from PowerPoint as PNG/SVG if this slide looks blank. -->

<!-- At this stage, you do not need to say what the association is.
Figure 5.9 develops the simple class diagram in Figure 5.8 to show that objects of class Patient are also involved in relationships with a number of other classes. In this example, I show that you can name associations to give the reader an indication of the type of relationship that exists.
Figures 5.8 and 5.9, shows an important feature of class diagrams—the ability to show how many objects are involved in the association.
In Figure 5.8 each end of the association is annotated with a 1, meaning that there is a 1:1 relationship between objects of these classes. That is, each patient has exactly one record, and each record maintains information about exactly one patient. As you can see from Figure 5.9, other multiplicities are possible. You can define that an exact number of objects are involved (e.g., 1..4) or, by using a \*, indicate that there are an indefinite number of objects involved in the association. For example, the (1..\*) multiplicity in Figure 5.9 on the relationship between Patient and Condition shows that a patient may suffer from several conditions and that the same condition may be associated with several patients.
At this level of detail, class diagrams look like semantic data models. Semantic data models are used in database design. They show the data entities, their associated attributes, and the relations between these entities. The UML does not include a diagram type for database modeling, as it models data using objects and their relationships. However, you can use the UML to represent a seman tic data model. You can think of entities in a semantic data model as simplified object classes (they have no operations), attributes as object class attributes, and rela tions as named associations between object classes. -->

---

# The Consultation class

![w:372px 5.10 Consultation Class.eps](assets/image10.emf)
<!-- pptx2marp: image10.emf is a EMF file; many browsers cannot render it inline. Re-export from PowerPoint as PNG/SVG if this slide looks blank. -->

<!-- In the UML, you show attributes and operations by extending the simple rectangle that represents a class. I illustrate this in that Figure that shows an object representing a consultation between doctor and patient:
The name of the object class is in the top section.
The class attributes are in the middle section. This includes the attribute names and, optionally, their types. I don’t show the types in Figure 5.10.
The operations (called methods in Java and other OO programming languages) associated with the object class are in the lower section of the rectangle. I show some but not all operations in Figure 5.10
In the example shown in Figure 5.10, it is assumed that doctors record voice notes that are transcribed later to record details of the consultation. To prescribe medication, the doctor involved must use the Prescribe method to generate an electronic prescription. -->

---

# Generalization

- Generalization is an everyday technique that we use to manage complexity.
- Rather than learn the detailed characteristics of every entity that we experience, we place these entities in more general classes (animals, cars, houses, etc.) and learn the characteristics of these classes.
- This allows us to infer that different members of these classes have some common characteristics e.g. squirrels and rats are rodents.

---

# Generalization

- In modeling systems, it is often useful to examine the classes in a system to see if there is scope for generalization. If changes are proposed, then you do not have to look at all classes in the system to see if they are affected by the change.
- In object-oriented languages, such as Java (C#, C++, Python, etc.), generalization is implemented using the class inheritance mechanisms built into the language.
- In a generalization, the attributes and operations associated with higher-level classes are also associated with the lower-level classes.
- The lower-level classes are subclasses inherit the attributes and operations from their superclasses. These lower-level classes then add more specific attributes and operations.

---

# A generalization hierarchy

![w:629px 5.11 GeneralizationHierarchy.eps](assets/image11.emf)
<!-- pptx2marp: image11.emf is a EMF file; many browsers cannot render it inline. Re-export from PowerPoint as PNG/SVG if this slide looks blank. -->

<!-- The generalization is shown as an arrowhead pointing up to the more general class. This indicates that general practitioners and hospital doctors can be generalized as doctors and that there are three types of Hospital Doctor: those who have just graduated from medical school and have to be supervised (Trainee Doctor); those who can work unsupervised as part of a consultant’s team (Registered Doctor); and consultants, who are senior doctors with full decision making responsibilities.
In a generalization, the attributes and operations associated with higher-level classes are also associated with the lower-level classes. The lower-level classes are subclasses that inherit the attributes and operations from their superclasses. These lower-level classes then add more specific attributes and operations. -->

---

# A generalization hierarchy with added detail

![w:641px 5.12 GeneralisationDetail.eps](assets/image12.emf)
<!-- pptx2marp: image12.emf is a EMF file; many browsers cannot render it inline. Re-export from PowerPoint as PNG/SVG if this slide looks blank. -->

---

# Object class aggregation models

- An aggregation model shows how classes that are collections are composed of other classes.
- Aggregation models are similar to the part-of relationship in semantic data models.

---

# The aggregation association

![w:588px 5.13 Aggregation.eps](assets/image13.emf)
<!-- pptx2marp: image13.emf is a EMF file; many browsers cannot render it inline. Re-export from PowerPoint as PNG/SVG if this slide looks blank. -->

<!-- That Figure shows that a patient record is an aggregate of Patient and an indefinite number of Consultations. That is, the record maintains personal patient information as well as an individual record for each consultation with a doctor. -->

---

<!-- _class: compact fit-80 -->

# Data flow diagrams

Data-flow diagrams (DFDs) are system models that show a functional perspective where each transformation represents a single function or process. DFDs are used to show how data flows through a sequence of process ing steps. For example, a processing step could be the filtering of duplicate records in a customer database. The data is transformed at each step before moving on to the next stage. These processing steps or transformations represent software processes or functions, where data-flow diagrams are used to document a software design. Activity diagrams in the UML may be used to represent DFDs.

<http://software-engineering-book.com/web/dfds>

---

# Behavioral models

---

# Behavioral models

- Behavioral models are models of the dynamic behavior of a system as it is executing. They show what happens or what is supposed to happen when a system responds to a stimulus from its environment.
- You can think of these stimuli as being of two types:
  - Data Some data arrives that has to be processed by the system.
  - Events Some event happens that triggers system processing. Events may have associated data, although this is not always the case.

---

# Data-driven modeling

- Many business systems are data-processing systems that are primarily driven by data. They are controlled by the data input to the system, with relatively little external event processing.
- Data-driven models show the sequence of actions involved in processing input data and generating an associated output.
- They are particularly useful during the analysis of requirements as they can be used to show end-to-end processing in a system.

---

# An activity model of the insulin pump’s operation

![w:1010px 5.14 PumpDFD.eps](assets/image14.emf)
<!-- pptx2marp: image14.emf is a EMF file; many browsers cannot render it inline. Re-export from PowerPoint as PNG/SVG if this slide looks blank. -->

- **the activity diagram type**
- We can see the processing steps, represented as activities (rounded rectangles), and the data flowing between these steps, represented as objects (rectangles).

<!-- Data-driven models were among the first graphical software models. In the 1970s, structured design methods used data-flow diagrams (DFDs) as a way to illustrate the processing steps in a system.
Data-flow models are useful because tracking and documenting how data associated with a particular process moves through the system help analysts and designers understand what is going on in the process.
DFDs are simple and intuitive and so are more accessible to stakeholders than some other types of model. It is usually possible to explain them to potential system users who can then participate in validating the model.
Data-flow diagrams can be represented in the UML using the activity diagram type, described in Section 5.1. Figure 5.14 is a simple activity diagram that shows the chain of processing involved in the insulin pump software. You can see the processing steps, represented as activities (rounded rectangles), and the data flowing between these steps, represented as objects (rectangles). -->

---

# An activity model of the insulin pump’s operation

Key Takeaways:

- Rounded rectangles (Activities) represent actions (methods/functions) or logical steps in a process, but they do not necessarily correspond 1:1 to methods(functions) in code. They describe what happens in each phase of the system’s behavior.
- Rectangles (Object Nodes) represent input/output data – such as structures (struct, class, dict, record) or objects passed between activities.

![w:470px 5.14 PumpDFD.eps](assets/image14.emf)
<!-- pptx2marp: image14.emf is a EMF file; many browsers cannot render it inline. Re-export from PowerPoint as PNG/SVG if this slide looks blank. -->

<!-- Data-driven models were among the first graphical software models. In the 1970s, structured design methods used data-flow diagrams (DFDs) as a way to illustrate the processing steps in a system.
Data-flow models are useful because tracking and documenting how data associated with a particular process moves through the system help analysts and designers understand what is going on in the process.
DFDs are simple and intuitive and so are more accessible to stakeholders than some other types of model. It is usually possible to explain them to potential system users who can then participate in validating the model.
Data-flow diagrams can be represented in the UML using the activity diagram type, described in Section 5.1. Figure 5.14 is a simple activity diagram that shows the chain of processing involved in the insulin pump software. You can see the processing steps, represented as activities (rounded rectangles), and the data flowing between these steps, represented as objects (rectangles). -->

---

# Order processing

**UML sequence diagrams**

![w:1035px 5.15 OrderSeq.eps](assets/image15.emf)
<!-- pptx2marp: image15.emf is a EMF file; many browsers cannot render it inline. Re-export from PowerPoint as PNG/SVG if this slide looks blank. -->

---

# Event-driven modeling

- Real-time systems are often event-driven, with minimal data processing. For example, a landline phone switching system responds to events such as ‘receiver off hook’ by generating a dial tone.
- Event-driven modeling shows how a system responds to external and internal events.
- It is based on the assumption that a system has a finite number of states and that events (stimuli) may cause a transition from one state to another.

---

# State machine models

- These model the behaviour of the system in response to external and internal events.
- They show the system’s responses to stimuli so are often used for modelling real-time systems.
- State machine models show system states as nodes and events as arcs between these nodes. When an event occurs, the system moves from one state to another.
- Statecharts are an integral part of the UML and are used to represent state machine models.

---

# State diagram of a microwave oven

![w:992px 5.16 MWOvenStateDiag.eps](assets/image16.emf)
<!-- pptx2marp: image16.emf is a EMF file; many browsers cannot render it inline. Re-export from PowerPoint as PNG/SVG if this slide looks blank. -->

<!-- I use an example of control software for a very simple microwave oven to illustrate event-driven modeling. Real microwave ovens are much more complex than this system, but the simplified system is easier to understand. This simple oven has a switch to select full or half power, a numeric keypad to input the cooking time, a start/stop button, and an alphanumeric display.
I have assumed that the sequence of actions in using the microwave is as follows:
Select the power level (either half power or full power).
Input the cooking time using a numeric keypad.
Press Start and the food is cooked for the given time
For safety reasons, the oven should not operate when the door is open, and, on completion of cooking, a buzzer is sounded. The oven has a simple display that is used to display various alerts and warning messages.
In UML state diagrams, rounded rectangles represent system states.
They may include a brief description (following “do”) of the actions taken in that state.
The labeled arrows represent stimuli that force a transition from one state to another. You can indicate start and end states using filled circles, as in activity diagrams.
From that Figure, you can see that the system starts in a waiting state and responds initially to either the full-power or the half-power button.
Users can change their minds after selecting one of these and may press the other button. The time is set and, if the door is closed, the Start button is enabled.
Pushing this button starts the oven operation, and cooking takes place for the specified time. This is the end of the cooking cycle, and the system returns to the waiting state. The problem with state-based modeling is that the number of possible states increases rapidly. For large system models, therefore, you need to hide detail in the models.
One way to do this is by using the notion of a “superstate” that encapsulates a number of separate states.
This superstate looks like a single state on a high-level model but is then expanded to show more detail on a separate diagram. -->

---

# Microwave oven operation

![w:707px 5.18 Operate-state-mc.eps](assets/image17.emf)
<!-- pptx2marp: image17.emf is a EMF file; many browsers cannot render it inline. Re-export from PowerPoint as PNG/SVG if this slide looks blank. -->

<!-- One way to do this is by using the notion of a “superstate” that encapsulates a number of separate states. This is a superstate that can be expanded, as shown in that Figure.
The Operation state includes a number of substates. It shows that operation starts with a status check and that if any problems are discovered an alarm is indicated and operation is disabled.
Cooking involves running the microwave generator for the specified time; on completion, a buzzer is sounded. If the door is opened during operation, the system moves to the disabled state, as shown in that Figure. State models of a system provide an overview of event processing, but you normally have to extend this with a more detailed description of the stimuli and the system states.
You may use a table to list the states and events that stimulate state transitions along with a description of each state and event in next slide. -->

---

# States and stimuli for the microwave oven (a)

|**State**|**Description**|
|---|---|
|Waiting|The oven is waiting for input. The display shows the current time.|
|Half power|The oven power is set to 300 watts. The display shows ‘Half power’.|
|Full power|The oven power is set to 600 watts. The display shows ‘Full power’.|
|Set time|The cooking time is set to the user’s input value. The display shows the cooking time selected and is updated as the time is set.|
|Disabled|Oven operation is disabled for safety. Interior oven light is on. Display shows ‘Not ready’.|
|Enabled|Oven operation is enabled. Interior oven light is off. Display shows ‘Ready to cook’.|
|Operation|Oven in operation. Interior oven light is on. Display shows the timer countdown. On completion of cooking, the buzzer is sounded for five seconds. Oven light is on. Display shows ‘Cooking complete’ while buzzer is sounding.|

|**Stimulus**|**Description**|
|---|---|
|Half power|The user has pressed the half-power button.|
|Full power|The user has pressed the full-power button.|
|Timer|The user has pressed one of the timer buttons.|
|Number|The user has pressed a numeric key.|
|Door open|The oven door switch is not closed.|
|Door closed|The oven door switch is closed.|
|Start|The user has pressed the Start button.|
|Cancel|The user has pressed the Cancel button.|

<!-- That Figure shows a tabular description of each state and how the stimuli that force state transitions are generated. -->

---

# States and stimuli for the microwave oven (a)

|**State**|**Description**|
|---|---|
|Waiting|The oven is waiting for input. The display shows the current time.|
|Half power|The oven power is set to 300 watts. The display shows ‘Half power’.|
|Full power|The oven power is set to 600 watts. The display shows ‘Full power’.|
|Set time|The cooking time is set to the user’s input value. The display shows the cooking time selected and is updated as the time is set.|
|Disabled|Oven operation is disabled for safety. Interior oven light is on. Display shows ‘Not ready’.|
|Enabled|Oven operation is enabled. Interior oven light is off. Display shows ‘Ready to cook’.|
|Operation|Oven in operation. Interior oven light is on. Display shows the timer countdown. On completion of cooking, the buzzer is sounded for five seconds. Oven light is on. Display shows ‘Cooking complete’ while buzzer is sounding.|

---

# States and stimuli for the microwave oven (b)

|**Stimulus**|**Description**|
|---|---|
|Half power|The user has pressed the half-power button.|
|Full power|The user has pressed the full-power button.|
|Timer|The user has pressed one of the timer buttons.|
|Number|The user has pressed a numeric key.|
|Door open|The oven door switch is not closed.|
|Door closed|The oven door switch is closed.|
|Start|The user has pressed the Start button.|
|Cancel|The user has pressed the Cancel button.|

---

# Model-driven architecture

---

<!-- _class: compact fit-90 -->

# Model driven architecture

- Model-driven architecture (MDA) was the precursor of more general model-driven engineering
- MDA is a model-focused approach to software design and implementation that uses a subset of UML models to describe a system.
- Models at different levels of abstraction are created. From a high-level, platform independent model, it is possible, in principle, to generate a working program without manual intervention.

---

<!-- _class: compact fit-90 -->

# but...

*...it is possible, in principle, to generate a working program without manual intervention...*

This means that from a model (e.g., UML, SysML, or another abstract system description), it's possible to automatically generate source code that:

- compiles without errors (meaning it's a "working" program in a technical sense),
- has a correctly defined structure (e.g., classes, interfaces, methods, dependencies, etc., are generated in accordance with the model),
- but **does not contain the operational logic** — meaning "nothing happens" because the implementation details, such as method bodies, algorithms, etc., are missing.

---

<!-- _class: compact fit-90 -->

# Types of model

- A computation independent model (CIM)
  - These model the important domain abstractions used in a system. CIMs are sometimes called domain models.
- A platform independent model (PIM)
  - These model the operation of the system without reference to its implementation. The PIM is usually described using UML models that show the static system structure and how it responds to external and internal events.
- Platform specific models (PSM)
  - These are transformations of the platform-independent model with a separate PSM for each application platform. In principle, there may be layers of PSM, with each layer adding some platform-specific detail.
- CIM
- PIM
- PSM

<!-- Model-based engineering allows engineers to think about systems at a high level of abstraction, without concern for the details of their implementation. This reduces the likelihood of errors, speeds up the design and implementation process, and allows for the creation of reusable, platform-independent application models. By using powerful tools, system implementations can be generated for different platforms from the same model. Therefore, to adapt the system to some new plat form technology, you write a model translator for that platform. When this is available, all platform-independent models can then be rapidly re-hosted on the new platform. Fundamental to MDA is the notion that transformations between models can be defined and applied automatically by software tools -->

---

# MDA transformations

![w:950px 5.19 MDA-Transformations.eps](assets/image18.emf)
<!-- pptx2marp: image18.emf is a EMF file; many browsers cannot render it inline. Re-export from PowerPoint as PNG/SVG if this slide looks blank. -->

<!-- This diagram also shows a final level of automatic transformation where a transformation is applied to the PSM to generate the executable code that will run on the designated software platform. Therefore, in principle at least, executable software can be generated from a high-level system model. In practice, completely automated translation of models to code is rarely possi ble. The translation of high-level CIM to PIM models remains a research problem, and for production systems, human intervention, illustrated using a stick figure in Figure 5.19, is normally required. A particularly difficult problem for automated model transformation is the need to link the concepts used in different CIMS. For example, the concept of a role in a security CIM that includes role-driven access control may have to be mapped onto the concept of a staff member in a hospital CIM. Only a person who understands both security and the hospital environment can make this mapping.
The translation of platform-independent to platform-specific models is a simpler technical problem. Commercial tools and open-source tools (Koegel 2012) are avail able that provide translators from PIMS to common platforms such as Java and J2EE. These use an extensive library of platform-specific rules and patterns to convert a PIM to a PSM. There may be several PSMs for each PIM in the system. If a software system is intended to run on different platforms (e.g., J2EE and .NET), then, in principle, you only have to maintain a single PIM. The PSMs for each platform are automatically generated (Figure 5.20). -->

---

# Multiple platform-specific models

![w:996px 5.20 Multiple PSMs.eps](assets/image19.emf)
<!-- pptx2marp: image19.emf is a EMF file; many browsers cannot render it inline. Re-export from PowerPoint as PNG/SVG if this slide looks blank. -->

<!-- Although MDA support tools include platform-specific translators, these sometimes only offer partial support for translating PIMS to PSMs. The execution environment for a system is more than the standard execution platform, such as J2EE or Java. It also includes other application systems, specific application libraries that may be created for a company, external services, and user interface libraries. These vary from one company to another, so off-the-shelf tool support is not available that takes these into account. Therefore, when MDA is introduced into an organization, special-purpose translators may have to be created to make use of the facilities available in the local environment. This is one reason why many companies have been reluctant to take on model-driven approaches to development. They do not want to develop or maintain their own tools or to rely on small software companies, who may go out of business, for tool development. Without these specialist tools, model-based development requires additional manual coding which reduces the cost-effectiveness of this approach. -->

---

# Executable UML

The fundamental notion behind model-driven engineering is that completely automated transformation of models to code should be possible. To achieve this, you have to be able to construct graphical models with clearly defined meanings that can be compiled to executable code. You also need a way of adding information to graphical models about the ways in which the operations defined in the model are implemented. This is possible using a subset of UML 2, called Executable UML or xUML (Mellor and Balcer 2002).

<http://software-engineering-book.com/web/xuml/>

---

# Agile methods and MDA

- The developers of MDA claim that it is intended to support an iterative approach to development and so can be used within agile methods.
- The notion of extensive up-front modeling contradicts the fundamental ideas in the agile manifesto and I suspect that few agile developers feel comfortable with model-driven engineering.
- If transformations can be completely automated and a complete program generated from a PIM, then, in principle, MDA could be used in an agile development process as no separate coding would be required.

---

# Adoption of MDA

- A range of factors has limited the adoption of MDE/MDA
- Specialized tool support is required to convert models from one level to another
- There is limited tool availability and organizations may require tool adaptation and customisation to their environment
- For the long-lifetime systems developed using MDA, companies are reluctant to develop their own tools or rely on small companies that may go out of business

---

# Adoption of MDA

- Models are a good way of facilitating discussions about a software design. Howeverthe abstractions that are useful for discussions may not be the right abstractions for implementation.
- For most complex systems, implementation is not the major problem – requirements engineering, security and dependability, integration with legacy systems and testing are all more significant.

---

# Adoption of MDA

- The arguments for platform-independence are only valid for large, long-lifetime systems. For software products and information systems, the savings from the use of MDA are likely to be outweighed by the costs of its introduction and tooling.
- The widespread adoption of agile methods over the same period that MDA was evolving has diverted attention away from model-driven approaches.

---

# Model-driven engineering

---

# Model-driven engineering

- Model-driven engineering (MDE) is an approach to software development where models rather than programs are the principal outputs of the development process.
- The programs that execute on a hardware/software platform are then generated automatically from the models.
- Proponents of MDE argue that this raises the level of abstraction in software engineering so that engineers no longer have to be concerned with programming language details or the specifics of execution platforms.

---

# Usage of model-driven engineering

- Model-driven engineering is still at an early stage of development, and it is unclear whether or not it will have a significant effect on software engineering practice.
- Pros
  - Allows systems to be considered at higher levels of abstraction
  - Generating code automatically means that it is cheaper to adapt systems to new platforms.
- Cons
  - Models for abstraction and not necessarily right for implementation.
  - Savings from generating code may be outweighed by the costs of developing translators for new platforms.

---

# Key points

- A model is an abstract view of a system that ignores system details. Complementary system models can be developed to show the system’s context, interactions, structure and behavior.
- Context models show how a system that is being modeled is positioned in an environment with other systems and processes.
- Use case diagrams and sequence diagrams are used to describe the interactions between users and systems in the system being designed. Use cases describe interactions between a system and external actors; sequence diagrams add more information to these by showing interactions between system objects.
- Structural models show the organization and architecture of a system. Class diagrams are used to define the static structure of classes in a system and their associations.

---

# Key points

- Behavioral models are used to describe the dynamic behavior of an executing system. This behavior can be modeled from the perspective of the data processed by the system, or by the events that stimulate responses from a system.
- Activity diagrams may be used to model the processing of data, where each activity represents one process step.
- State diagrams are used to model a system’s behavior in response to internal or external events.
- Model-driven engineering is an approach to software development in which a system is represented as a set of models that can be automatically transformed to executable code.
