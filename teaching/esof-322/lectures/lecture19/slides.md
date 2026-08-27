---
marp: true
theme: pach
paginate: true
footer: "ESOF 322 | Software Engineering | J. L. Pach"
title: "Software Engineering"
---

<!-- _class: lead -->

# Software Engineering

## Lecture 19

---

# Today’s Agenda

Software Security

---

# Software Security

---

# 1) Design Principle: "Never Trust the Client"

The most crucial rule: **never assume the client is honest.** Where possible, all critical logic and core data must reside on an **authoritative server (etc. Diablo IV)**. If your application or game operates offline, you must implement local detection, auditing, and anti-tamper mechanisms.

---

# 2) Methods for Detecting and Preventing Memory Manipulation (Client-Side)

- Redundant Value Copies (Mirroring)
- Store critical values in multiple memory locations (e.g., v, v\_copy1, v\_copy2) and compare them cyclically.

**Pro:** Simple, low overhead.

**Con:** Sophisticated attackers can identify and modify all redundant copies simultaneously.

---

# Etymology: The Canary in the Coal Mine

The name ***canary*** refers to a historical method of warning used in coal mines:

- **The Practice**: Miners would take small birds, such as canaries, with them underground.
- **Danger Detection**: Canaries are much more sensitive than humans to toxic gases (like carbon monoxide and methane), which are odorless and lethal.
- **The Warning**: If the level of dangerous gases rose, the canary would perish first. This immediately signaled to the miners that they had to evacuate the mine before the gas reached life-threatening concentrations for humans.

---

<!-- _class: fit-80 -->

# Canary - Transfer to Computer Science

In computer science, especially in the field of memory security, the **"Canary Value"** serves an identical role:

- **The Purpose:** The value is placed in a strategic, yet **vulnerable location** (e.g., on the stack, or adjacent to critical data).
- **The Mechanism:** If an attacker attempts to overwrite a buffer or violate data integrity using exploits (like buffer overflow or memory manipulation via Cheat Engine), the attack **corrupts the canary first** or leads to its incorrect verification.
- **The Alert:** Before using the sensitive data, the application **checks the state of the canary**. If the canary is damaged, it signals that the environment has been compromised (attacked), and the application can safely **react** (e.g., terminate, reset the data) before malicious code is executed or fraudulent data is used.

---

# 2) Methods for Detecting and Preventing Memory Manipulation (Client-Side)

B. Sentry/Canary Values

Place a "sentry" (e.g., a 32-bit random token) adjacent to or associated with every critical data structure. If the sentry value is corrupted or does not match a verified state -&gt; a memory modification is detected.

*Note: This is often used to protect against* ***stack buffer overflows*** *(Stack Canaries).* In the data integrity context, it protects variable integrity.

---

# 2) Methods for Detecting and Preventing Memory Manipulation (Client-Side)

C. Checksums / CRC / Fast Hash

Calculate a quick checksum (like **CRC32** or **xxHash**) for a block of data, store the checksum separately, and periodically verify the block's integrity.

*Note:* **Fast**, but relatively **easy to bypass** if the attacker understands the algorithm and has access to the updated checksum value.

---

# 2) Methods for Detecting and Preventing Memory Manipulation (Client-Side)

D. Monotonic Counters / Versioning (Missing in original, but critical)

Maintain a **counter** that is incremented with every legitimate data update (e.g., item count, score). If the system detects a "rollback" or an impossible change (e.g., item count suddenly decreasing or skipping an incremental state), unauthorized modification is suspected.

---

# 2) Methods for Detecting and Preventing Memory Manipulation (Client-Side)

E. Obfuscation &amp; Anti-Debug Techniques

Making code analysis difficult for reverse engineers through **obfuscation** (e.g., control-flow flattening, symbol stripping) and implementing simple **debugger detection** checks (e.g., checking for the presence of specific debugger APIs or suspicious module names).

---

<!-- _class: fit-80 -->

# 3) Performance and Practical Trade-offs

Continuous, full verification is often too computationally expensive and introduces unacceptable overhead. Use practical trade-offs:

- **Randomized Checks:** Perform integrity checks on a randomized schedule.
- **Critical Events:** Prioritize checks during highly critical moments (e.g., buying items, completing a mission, saving state).
- **Layered Security:** Use fast, lightweight algorithms (like xxHash) for routine checks, but reserve a few, rare, full cryptographic checks (like **HMAC** or **digital signatures**) for ultimate verification.
- **False Positives:** Implement an appropriate recovery mechanism (e.g., resetting to a verified state, forcing an application restart, or falling back to offline mode) to avoid spoiling the user experience (UX) with unfair bans or crashes.

---

# 4) Ethics and Limitations (Crucial)

- **Our Goal:** We are teaching defensive and educational security principles, not how to cheat or bypass the protections of others' software.
- **Responsibility:** Always discuss the ethical and legal ramifications of modifying proprietary software, using public tooling (e.g., Cheat Engine), and respecting user privacy. Our focus is on **defense**, not offense.

---

<!-- _class: fit-90 -->

# Summary of Data Masking Techniques in Memory

|**Technique**|**Purpose in Memory**|**Application**|
|---|---|---|
|**XOR + Key**|Value Masking (Obfuscation)|Hiding hit points, currency, coordinates.|
|**Canary/Sentry**|Integrity Protection|Detecting corruption of an encrypted value.|
|**CRC32/xxHash**|Integrity Auditing|Periodically checking if a critical data structure has been tampered with.|

---

<!-- _class: fit-70 -->

# My summary

- When using memory scanners like Cheat Engine, we must be aware that the program we analyze is an executable copy residing in RAM. Within any code block (e.g., inside a function), instructions execute sequentially.
- With a basic understanding of Assembly language, an attacker can disassemble the code and change the program's flow of control by introducing a jump instruction (e.g., JMP), thereby bypassing critical code segments. This control-flow modification technique (often referred to as code patching or hooking or code injection) allows the attacker to circumvent even the most sophisticated memory integrity verification mechanisms.
- Many value masking operations rely on the $\text{XOR}$ gate. The $\text{XOR}$ Assembly mnemonic in x86-64 architectures (Intel and AMD) is two-operand, which clearly reveals which memory locations are being processed. This means that if the $\text{XOR}$ key is stored in memory near the masked value (even if it's randomly generated), an experienced programmer equipped with powerful tools like Cheat Engine can easily locate the key and decode the variables.

---

<!-- _class: fit-90 -->

# My summary

- In conclusion, for a purely offline application, we are ultimately destined to fail against a sufficiently skilled and persistent specialist. Our goal can only be to raise the barrier and significantly slow down the process of memory modification. By combining all discussed defensive methods (e.g., scattering state parameters and keys across various data structures), we can effectively increase the time required to reverse-engineer the program's logic.
- However, it is worth noting that knowledge of computer architecture, compilers, and low-level Assembly programming is becoming increasingly specialized. Mastering advanced techniques like code patching and injecting Assembly code remains a high barrier to entry for the average **computer science graduate** in the 21st century.

---

<!-- _class: caption-slide -->

# Thank You!
