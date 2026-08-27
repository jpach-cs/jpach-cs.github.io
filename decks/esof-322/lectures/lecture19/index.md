---
marp: true
theme: pach
paginate: true
title: "Software Engineering"
---

# Software Engineering

*Lecture 19*

---

## Today’s Agenda

Software Security

---

## Gitlens?

- extension

---

- Create and log in in GitHub account
- Please turn of AI

![w:606px Content Placeholder 10](assets/image2.png)

---

# Software Security

---

## 1) Design Principle: "Never Trust the Client"

The most crucial rule: **never assume the client is honest.** Where possible, all critical logic and core data must reside on an **authoritative server (etc. Diablo IV)**. If your application or game operates offline, you must implement local detection, auditing, and anti-tamper mechanisms.

---

## 2) Methods for Detecting and Preventing Memory Manipulation (Client-Side)

- Redundant Value Copies (Mirroring)
- Store critical values in multiple memory locations (e.g., v, v\_copy1, v\_copy2) and compare them cyclically.

**Pro:** Simple, low overhead.

**Con:** Sophisticated attackers can identify and modify all redundant copies simultaneously.

---

## Etymology: The Canary in the Coal Mine

The name ***canary*** refers to a historical method of warning used in coal mines:

- **The Practice**: Miners would take small birds, such as canaries, with them underground.
- **Danger Detection**: Canaries are much more sensitive than humans to toxic gases (like carbon monoxide and methane), which are odorless and lethal.
- **The Warning**: If the level of dangerous gases rose, the canary would perish first. This immediately signaled to the miners that they had to evacuate the mine before the gas reached life-threatening concentrations for humans.

---

## Canary - Transfer to Computer Science

In computer science, especially in the field of memory security, the **"Canary Value"** serves an identical role:

- **The Purpose:** The value is placed in a strategic, yet **vulnerable location** (e.g., on the stack, or adjacent to critical data).
- **The Mechanism:** If an attacker attempts to overwrite a buffer or violate data integrity using exploits (like buffer overflow or memory manipulation via Cheat Engine), the attack **corrupts the canary first** or leads to its incorrect verification.
- **The Alert:** Before using the sensitive data, the application **checks the state of the canary**. If the canary is damaged, it signals that the environment has been compromised (attacked), and the application can safely **react** (e.g., terminate, reset the data) before malicious code is executed or fraudulent data is used.

---

## 2) Methods for Detecting and Preventing Memory Manipulation (Client-Side)

B. Sentry/Canary Values

Place a "sentry" (e.g., a 32-bit random token) adjacent to or associated with every critical data structure. If the sentry value is corrupted or does not match a verified state -&gt; a memory modification is detected.

*Note: This is often used to protect against* ***stack buffer overflows*** *(Stack Canaries).* In the data integrity context, it protects variable integrity.

---

## 2) Methods for Detecting and Preventing Memory Manipulation (Client-Side)

C. Checksums / CRC / Fast Hash

Calculate a quick checksum (like **CRC32** or **xxHash**) for a block of data, store the checksum separately, and periodically verify the block's integrity.

*Note:* **Fast**, but relatively **easy to bypass** if the attacker understands the algorithm and has access to the updated checksum value.

---

## 2) Methods for Detecting and Preventing Memory Manipulation (Client-Side)

D. Monotonic Counters / Versioning (Missing in original, but critical)

Maintain a **counter** that is incremented with every legitimate data update (e.g., item count, score). If the system detects a "rollback" or an impossible change (e.g., item count suddenly decreasing or skipping an incremental state), unauthorized modification is suspected.

---

## 2) Methods for Detecting and Preventing Memory Manipulation (Client-Side)

E. Obfuscation &amp; Anti-Debug Techniques

Making code analysis difficult for reverse engineers through **obfuscation** (e.g., control-flow flattening, symbol stripping) and implementing simple **debugger detection** checks (e.g., checking for the presence of specific debugger APIs or suspicious module names).

---

## 3) Performance and Practical Trade-offs

Continuous, full verification is often too computationally expensive and introduces unacceptable overhead. Use practical trade-offs:

- **Randomized Checks:** Perform integrity checks on a randomized schedule.
- **Critical Events:** Prioritize checks during highly critical moments (e.g., buying items, completing a mission, saving state).
- **Layered Security:** Use fast, lightweight algorithms (like xxHash) for routine checks, but reserve a few, rare, full cryptographic checks (like **HMAC** or **digital signatures**) for ultimate verification.
- **False Positives:** Implement an appropriate recovery mechanism (e.g., resetting to a verified state, forcing an application restart, or falling back to offline mode) to avoid spoiling the user experience (UX) with unfair bans or crashes.

---

## 4) Ethics and Limitations (Crucial)

- **Our Goal:** We are teaching defensive and educational security principles, not how to cheat or bypass the protections of others' software.
- **Responsibility:** Always discuss the ethical and legal ramifications of modifying proprietary software, using public tooling (e.g., Cheat Engine), and respecting user privacy. Our focus is on **defense**, not offense.

---

## Summary of Data Masking Techniques in Memory

|**Technique**|**Purpose in Memory**|**Application**|
|---|---|---|
|**XOR + Key**|Value Masking (Obfuscation)|Hiding hit points, currency, coordinates.|
|**Canary/Sentry**|Integrity Protection|Detecting corruption of an encrypted value.|
|**CRC32/xxHash**|Integrity Auditing|Periodically checking if a critical data structure has been tampered with.|

---

## My summary

- When using memory scanners like Cheat Engine, we must be aware that the program we analyze is an executable copy residing in RAM. Within any code block (e.g., inside a function), instructions execute sequentially.
- With a basic understanding of Assembly language, an attacker can disassemble the code and change the program's flow of control by introducing a jump instruction (e.g., JMP), thereby bypassing critical code segments. This control-flow modification technique (often referred to as code patching or hooking or code injection) allows the attacker to circumvent even the most sophisticated memory integrity verification mechanisms.
- Many value masking operations rely on the $\text{XOR}$ gate. The $\text{XOR}$ Assembly mnemonic in x86-64 architectures (Intel and AMD) is two-operand, which clearly reveals which memory locations are being processed. This means that if the $\text{XOR}$ key is stored in memory near the masked value (even if it's randomly generated), an experienced programmer equipped with powerful tools like Cheat Engine can easily locate the key and decode the variables.

---

## My summary

- In conclusion, for a purely offline application, we are ultimately destined to fail against a sufficiently skilled and persistent specialist. Our goal can only be to raise the barrier and significantly slow down the process of memory modification. By combining all discussed defensive methods (e.g., scattering state parameters and keys across various data structures), we can effectively increase the time required to reverse-engineer the program's logic.
- However, it is worth noting that knowledge of computer architecture, compilers, and low-level Assembly programming is becoming increasingly specialized. Mastering advanced techniques like code patching and injecting Assembly code remains a high barrier to entry for the average **computer science graduate** in the 21st century.

---

- Krótkie wyjaśnienie, plus zalety / ograniczenia1) Bitowe operacje / permutacje (shift, rotate)Co robi: przesunięcia bitów, zamiany bajtów, proste permutacje bitów wartości.Zaleta: bardzo szybkie, niskie koszty CPU.Wada: nie jest kryptografią — łatwe do odwrócenia jeśli atakujący zna schemat. Dobre jako obfuskacja, nie jako zabezpieczenie.2) XOR z maską (stałą)Co robi: masked = value ^ MASKZaleta: szybkie, proste.Wada: jeśli MASK jest stała i znana / znaleźć można miejsce gdzie maskowanie jest wykonywane → łatwe złamanie. Proste XOR to tylko obfuskacja.3) XOR z jednorazowym/ephemeral key (OTP-like)Co robi: generujesz losowy klucz dla każdej operacji/instancji i używasz go do XOR; klucz jest przechowywany lub natychmiast niszczony.Zaleta: jeśli klucz absolutnie nigdy nie jest ponownie użyty i jest tajny → teoretycznie bezpieczny (one-time pad).Wada: praktycznie nieosiągalne bez bezpiecznego zarządzania kluczami; jeśli atakujący może odczytać klucz w pamięci → złamane. Bardzo trudne w implementacji w kliencie.4) Pointer encoding / value scramblingCo robi: zamiast trzymać int health, trzymasz encoded = (health ^ key) + offset i dekodujesz tuż przed użyciem.Zaleta: utrudnia bezpośrednie wyszukiwanie wartości w pamięci.Wada: przy braku bezpiecznego key management — atakujący może znaleźć kod dekodujący i odtworzyć algorytm.5) CRC32 / checksumsCo robi: wykrywa, że dane zostały zmienione.Zaleta: szybkie, niskie koszty, dobre do wykrywania przypadkowych zmian.Wada: nie zabezpiecza — atakujący może zaktualizować checksumę po zmianie danych (jeśli ma dostęp do mechanizmu obliczania CRC). Nie daje poufności.6) Hash (SHA-256)Co robi: skrót dla wykrywania zmian / porównań.Zaleta: trudniej sfałszować kolizję (ale nie niemożliwe przy ataku celowym).Wada: sam hash nie chroni — atakujący może zmodyfikować i zaktualizować hash, o ile zna secret / mechanizm.7) Symetryczne szyfrowanie (AES, ChaCha20)Co robi: szyfruje wartości w pamięci; odczyt wymaga deszyfracji z kluczem.Zaleta: prawdziwa poufność jeśli klucz jest bezpieczny.Wada: klucz musi być przechowywany i używany w kliencie — jeśli atakujący ma pełny dostęp do pamięci procesu, może znaleźć klucz. Szyfrowanie kosztuje CPU, ale ChaCha20 jest szybkie.8) AEAD (AES-GCM, ChaCha20-Poly1305)Co robi: szyfruje i dodatkowo zapewnia integralność (autentykację).Zaleta: zabezpiecza przeciwnika który modyfikuje bajty — weryfikacja nie przejdzie bez prawidłowego tagu; to najlepsza praktyka dla danych poufnych w pamięci/na dysku.Wada: nadal wymaga bezpiecznego zarządzania kluczami.9) Asymetryczne podpisy (ED25519, RSA)Co robi: serwer podpisuje stan/plik prywatnym kluczem; klient weryfikuje podpis publicznym kluczem.Zaleta: klient nie może sam wykonać prawidłowego podpisu (jeśli prywatny klucz jest tylko na serwerze) — świetne dla signed saves.Wada: wymaga serwera, lub przynajmniej zaufanego źródła podpisu.10) Secure enclaves / OS key storesCo robi: klucze trzymane w systemowym, chronionym obszarze (TPM, Keychain, DPAPI, Secure Enclave).Zaleta: bardzo trudne do wykradzenia lokalnie.Wada: dostępność zależy od platformy; nie zawsze możliwe w prostych projektach.11) Anti-debug / obfuskacjaCo robi: wykrywa debugger, maskuje/kryptuje sekcje kodu; zmienia flow żeby utrudnić RE.Zaleta: opóźnia atakującego.Wada: często łamane przez zdeterminowanych analityków; może generować fałszywe alarmy.12) ASLR / DEP / systemowe technikiCo robi: bezpieczeństwo na poziomie systemu operacyjnego (losowanie adresów, ochrona pamięci).Zaleta: utrudnia pewne ataki.Wada: nie blokuje prostego skanowania wartości w pamięci, jeśli atakujący zna typ/rozmiar.Kluczowy problem: zarządzanie kluczami (key management)To jest najtrudniejszy aspekt. Bezpieczne szyfrowanie wymaga, żeby klucz NIE był dostępny atakującemu. Jeśli klucz jest w pamięci tego samego procesu, atakujący z dostępem do pamięci go znajdzie.Rozwiązania:Serwerowy klucz prywatny — najlepsze (klient tylko weryfikuje podpisy).Per-install secret przechowywany w OS keystore (lepsze niż nic).Hardware-backed keys (TPM, Secure Enclave).Ephemeral session keys: negocjowane z serwerem przy starcie sesji, trzymane krótko.Praktyczne rekomendacje (co stosować w projektach / labach)Dla prostych demonstracji (labów): pokaż najpierw prosty XOR / pointer-encoding żeby studenci zrozumieli ograniczenia.Następnie pokaż AES/ChaCha20-Poly1305 (AEAD): zademonstruj normalny atak (ustawienie klucza w procesie → szyfrowanie złamane) aby omówić key-management.W projektach produkcyjnych gier:Krytyczne kontrole / walidacje na serwerze (autoritative server) — to fundament.Signed saves / server-signed tokens jeśli chcesz chronić offline saves.Lokalnie: lekkie maskowanie (scrambling) + CRC/ HMAC (jeżeli secret pochodzi z bezpiecznego źródła) + losowe kontrole.Preferuj AEAD (np. ChaCha20-Poly1305) dla szybkości i bezpieczeństwa, jeśli musisz szyfrować dane w pamięci/dysk.Nie polegaj na samym CRC/obfuskacji jako na zabezpieczeniu przed świadomym atakiem.Przykładowe wzorcowe połączenia (security patterns)Pattern A (offline game, bez serwera): per-install secret (OS keystore) + ChaCha20-Poly1305 do szyfrowania save + HMAC dla integralności + monotonic counter.Pattern B (gra z serwerem): client sends state → server verifies and signs → client stores signed save; on load client verifies signature.Pattern C (lightweight protection): obfuscation (pointer encoding) + mirrored values + periodic CRC + logging + optional sandbox detection.

<!-- **Krótkie wyjaśnienie, plus zalety / ograniczenia**
**1) Bitowe operacje / permutacje (shift, rotate)**
Co robi: przesunięcia bitów, zamiany bajtów, proste permutacje bitów wartości.
Zaleta: bardzo szybkie, niskie koszty CPU.
Wada: **nie jest kryptografią** — łatwe do odwrócenia jeśli atakujący zna schemat. Dobre jako *obfuskacja*, nie jako zabezpieczenie.
**2) XOR z maską (stałą)**
Co robi: masked = value ^ MASK
Zaleta: szybkie, proste.
Wada: jeśli MASK jest stała i znana / znaleźć można miejsce gdzie maskowanie jest wykonywane → łatwe złamanie. Proste XOR to tylko obfuskacja.
**3) XOR z jednorazowym/ephemeral key (OTP-like)**
Co robi: generujesz losowy klucz dla każdej operacji/instancji i używasz go do XOR; klucz jest przechowywany lub natychmiast niszczony.
Zaleta: jeśli klucz absolutnie nigdy nie jest ponownie użyty i jest tajny → teoretycznie bezpieczny (one-time pad).
Wada: **praktycznie nieosiągalne** bez bezpiecznego zarządzania kluczami; jeśli atakujący może odczytać klucz w pamięci → złamane. Bardzo trudne w implementacji w kliencie.
**4) Pointer encoding / value scrambling**
Co robi: zamiast trzymać int health, trzymasz encoded = (health ^ key) + offset i dekodujesz tuż przed użyciem.
Zaleta: utrudnia bezpośrednie wyszukiwanie wartości w pamięci.
Wada: przy braku bezpiecznego key management — atakujący może znaleźć kod dekodujący i odtworzyć algorytm.
**5) CRC32 / checksums**
Co robi: wykrywa, że dane zostały zmienione.
Zaleta: szybkie, niskie koszty, dobre do wykrywania przypadkowych zmian.
Wada: **nie zabezpiecza** — atakujący może zaktualizować checksumę po zmianie danych (jeśli ma dostęp do mechanizmu obliczania CRC). Nie daje poufności.
**6) Hash (SHA-256)**
Co robi: skrót dla wykrywania zmian / porównań.
Zaleta: trudniej sfałszować kolizję (ale nie niemożliwe przy ataku celowym).
Wada: sam hash nie chroni — atakujący może zmodyfikować i zaktualizować hash, o ile zna secret / mechanizm.
**7) Symetryczne szyfrowanie (AES, ChaCha20)**
Co robi: szyfruje wartości w pamięci; odczyt wymaga deszyfracji z kluczem.
Zaleta: **prawdziwa poufność** jeśli klucz jest bezpieczny.
Wada: klucz musi być przechowywany i używany w kliencie — jeśli atakujący ma pełny dostęp do pamięci procesu, może znaleźć klucz. Szyfrowanie kosztuje CPU, ale ChaCha20 jest szybkie.
**8) AEAD (AES-GCM, ChaCha20-Poly1305)**
Co robi: szyfruje i dodatkowo zapewnia integralność (autentykację).
Zaleta: zabezpiecza przeciwnika który modyfikuje bajty — weryfikacja nie przejdzie bez prawidłowego tagu; to najlepsza praktyka dla danych poufnych w pamięci/na dysku.
Wada: nadal wymaga bezpiecznego zarządzania kluczami.
**9) Asymetryczne podpisy (ED25519, RSA)**
Co robi: serwer podpisuje stan/plik prywatnym kluczem; klient weryfikuje podpis publicznym kluczem.
Zaleta: klient nie może sam wykonać prawidłowego podpisu (jeśli prywatny klucz jest tylko na serwerze) — świetne dla signed saves.
Wada: wymaga serwera, lub przynajmniej zaufanego źródła podpisu.
**10) Secure enclaves / OS key stores**
Co robi: klucze trzymane w systemowym, chronionym obszarze (TPM, Keychain, DPAPI, Secure Enclave).
Zaleta: bardzo trudne do wykradzenia lokalnie.
Wada: dostępność zależy od platformy; nie zawsze możliwe w prostych projektach.
**11) Anti-debug / obfuskacja**
Co robi: wykrywa debugger, maskuje/kryptuje sekcje kodu; zmienia flow żeby utrudnić RE.
Zaleta: opóźnia atakującego.
Wada: często łamane przez zdeterminowanych analityków; może generować fałszywe alarmy.
**12) ASLR / DEP / systemowe techniki**
Co robi: bezpieczeństwo na poziomie systemu operacyjnego (losowanie adresów, ochrona pamięci).
Zaleta: utrudnia pewne ataki.
Wada: nie blokuje prostego skanowania wartości w pamięci, jeśli atakujący zna typ/rozmiar.
<br>
**Kluczowy problem: zarządzanie kluczami (key management)**
**To jest najtrudniejszy aspekt.** Bezpieczne szyfrowanie wymaga, żeby klucz NIE był dostępny atakującemu. Jeśli klucz jest w pamięci tego samego procesu, atakujący z dostępem do pamięci go znajdzie.
Rozwiązania:
**Serwerowy klucz prywatny** — najlepsze (klient tylko weryfikuje podpisy).
**Per-install secret** przechowywany w OS keystore (lepsze niż nic).
**Hardware-backed keys** (TPM, Secure Enclave).
**Ephemeral session keys**: negocjowane z serwerem przy starcie sesji, trzymane krótko.
<br>
**Praktyczne rekomendacje (co stosować w projektach / labach)**
**Dla prostych demonstracji (labów):** pokaż najpierw prosty XOR / pointer-encoding żeby studenci zrozumieli ograniczenia.
**Następnie pokaż AES/ChaCha20-Poly1305 (AEAD)**: zademonstruj normalny atak (ustawienie klucza w procesie → szyfrowanie złamane) aby omówić key-management.
**W projektach produkcyjnych gier:**
Krytyczne kontrole / walidacje na serwerze (autoritative server) — to fundament.
Signed saves / server-signed tokens jeśli chcesz chronić offline saves.
Lokalnie: lekkie maskowanie (scrambling) + CRC/ HMAC (jeżeli secret pochodzi z bezpiecznego źródła) + losowe kontrole.
**Preferuj AEAD** (np. ChaCha20-Poly1305) dla szybkości i bezpieczeństwa, jeśli musisz szyfrować dane w pamięci/dysk.
**Nie polegaj na samym CRC/obfuskacji** jako na zabezpieczeniu przed świadomym atakiem.
<br>
**Przykładowe wzorcowe połączenia (security patterns)**
**Pattern A (offline game, bez serwera):** per-install secret (OS keystore) + ChaCha20-Poly1305 do szyfrowania save + HMAC dla integralności + monotonic counter.
**Pattern B (gra z serwerem):** client sends state → server verifies and signs → client stores signed save; on load client verifies signature.
**Pattern C (lightweight protection):** obfuscation (pointer encoding) + mirrored values + periodic CRC + logging + optional sandbox detection. -->

---

## Practical Scenario – Restoring a Broken File Locally

**Situation:**

- You have a local branch of the project.
- You notice that **some functionality is broken**, but the problem appeared several commits ago.
- You do **not want to revert the entire history** or delete commits, because other changes were made along the way.

---

## Practical Scenario – Restoring a Broken File Locally

**Solution – restoring a file from a previous commit:**

- This command retrieves the version of the file from the specified commit and places it in your working directory.
- Other files in the project remain unchanged.

```
git checkout <commit-id> -- path/to/file

```

---

## Practical Scenario – Restoring a Broken File Locally

**Optional: check differences:**

- Compare the current state of the file (after checkout) with the latest version in the branch to see what has changed.

```
git diff

```

---

## Practical Scenario – Restoring a Broken File Locally

**Modify and test:**

- You can edit the file in your working directory.
- Test the changes locally.

---

## Practical Scenario – Restoring a Broken File Locally

**Commit the changes:**

- Creates a new commit that restores and/or fixes the file.
- The history remains intact, all previous commits are preserved.

**Effect:**

- Works similarly to git revert, but only affects specific files, not the entire commit.
- Does not require force push or rewriting history.

```
git add path/to/file
git commit -m "Fix broken functionality in <file>"
```

---

## Introduction to Git Revert

- git revert is used to **undo changes from a previous commit** by creating a **new commit**.
- Important: it does **not delete the original commit** – history remains intact.
- Safe for **shared branches** because it does not require --force.

---

## When to Use git revert - Use Cases for git revert

- Undo a commit that **introduced a bug** without affecting later commits.
- Correct mistakes on a **shared branch** without rewriting history.
- Can revert **single commits** or a **range of commits**.

---

## How git revert Works - Mechanics of git revert

- Git calculates the changes made in the target commit.
- Creates **inverse changes** in the working directory (staging area).
- Creates a **new commit** that applies these inverse changes.
- Later commits remain unchanged.

---

## git revert - Reverting a Commit Example

- C' is a new commit that undoes changes from C.
- Commits D and earlier remain untouched.

```
A --- B --- C --- D  (branch)
```

- git revert C

```
A --- B --- C --- D --- C'
```

---

## git revert - Key Points About git revert

- Creates a new commit, does not remove old commits.
- Does not require force push, safe for shared branches.
- Conflicts occur only if revert touches the same lines as later commits.
- Can be applied to single files (optional advanced usage).

---

## git revert - Comparison to Other Methods

|Method|Effect on History|Force Push Required?|Safe for Shared Branch?|
|---|---|---|---|
|git reset --hard|Rewrites history, discards commits|Yes|No|
|git commit --amend|Changes last commit locally|Yes if pushed|No|
|git revert|Adds new commit that undoes changes|No|Yes|

---

# Git Best Practices

---

## Best Practices for Commits and Branching

- Small, thematic commits:
  - One commit = one logical change / one functionality / one file (or tightly related files).
- Feature or fix branches:
  - Create a new branch for each independent change or bug fix.
  - Base it on main or develop.
  - Merge or rebase back after testing.
- One file per developer (or minimal overlap):
  - Reduces the chance of merge conflicts.
  - Encourages clear ownership and accountability.
- Use revert, not reset/amend, on shared branches:
  - Revert creates a safe new commit.
  - Avoids rewriting history in a collaborative environment.

---

## Consequences / Why It Matters

- Small commits make reverts safe:
  - If a commit breaks something, it can be reverted without affecting unrelated changes.
- Dedicated branches reduce conflicts:
  - Developers can work independently on different files without interfering with each other.
- One file per change / class (Python principle):
  - Mirrors good coding practices (e.g., one class per file).
  - Minimizes the probability of multiple developers editing the same file.
- Clear, readable history:
  - Easier code review and debugging.
  - Helps maintain project quality in Agile / fast-moving environments.

---

# Thank

*You!*
