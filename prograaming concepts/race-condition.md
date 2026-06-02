# 🏁 Race Condition in Programming

> *Explained simply — as if you're in Standard 8!*

---

## 📚 Table of Contents

- [What is a Race Condition?](#-what-is-a-race-condition)
- [Real-Life Examples](#-real-life-examples)
- [Programming Example](#-programming-example)
- [Python Code — Broken Version](#-python-code--without-fix)
- [Python Code — Fixed Version](#-python-code--with-fix)
- [The Fix — Analogy](#-the-fix--analogy)
- [Summary Table](#-summary-table)
- [Key Takeaway](#-key-takeaway)

---

## 🧠 What is a Race Condition?

Think of it like a **race** — but a *bad* one where two runners crash into each other instead of finishing cleanly.

> A **race condition** happens when two or more things try to **read and change the same data at the same time**, and the final result depends on **who gets there first** — causing unexpected, buggy outcomes.

---

## 🌍 Real-Life Examples

### 🎟️ Example 1 — Last Movie Ticket

Imagine only **1 ticket** is left for a movie.

- **Riya** and **Raj** both open the booking app at the same time
- Both see `"1 ticket available"` ✅
- Both click **Buy** at the exact same moment
- The system sells the ticket to **both of them** 😱
- Now two people show up for one seat!

---

### 🏧 Example 2 — ATM Withdrawal

Your bank account has ₹500.

- **You** withdraw ₹500 from ATM in Rajkot
- **Someone else** (using your card) withdraws ₹500 from another ATM — same second
- Both ATMs check the balance, both see ₹500, both approve
- You end up with ₹0 but **₹1000 was given out** 😨

---

### 📝 Example 3 — Google Docs

Two friends editing the same line of a doc at the exact same time — one's change **erases** the other's!

---

## 💻 Programming Example

### The Problem — Two friends adding to a shared counter

#### 📋 Pseudo Code

```
counter = 0

Function add_one():
    read counter      → gets value (say 5)
    add 1 to it       → now it's 6
    write 6 back      → saves 6

Thread A runs add_one()
Thread B runs add_one()   ← at the EXACT same time!

Both read 5 → both write 6
Result: counter = 6   ← WRONG! Should be 7
```

> ⚠️ The problem is that `counter += 1` is **not one step** — it's secretly **three steps**:
> 1. **Read** the current value
> 2. **Add** 1 to it
> 3. **Write** it back
>
> If two threads do this simultaneously, they can **overwrite each other!**

---

## 🐍 Python Code — Without Fix

> ❌ Race Condition Happens Here

```python
import threading

counter = 0

def add_many_times():
    global counter
    for _ in range(100_000):
        counter += 1  # ⚠️ Not safe! 3 hidden steps

# Two threads running at the same time
thread_A = threading.Thread(target=add_many_times)
thread_B = threading.Thread(target=add_many_times)

thread_A.start()
thread_B.start()

thread_A.join()  # Wait for A to finish
thread_B.join()  # Wait for B to finish

print(f"Expected : 200000")
print(f"Got      : {counter}")  # Often something like 143829 😱
```

**Why is the result wrong?**
Because both threads are reading and writing `counter` at the same time, stepping on each other's work.

---

## 🐍 Python Code — With Fix

> ✅ Using a Lock (like a "Do Not Disturb" sign 🚪)

```python
import threading

counter = 0
lock = threading.Lock()  # 🔒 Only ONE thread can hold this at a time

def safe_add_many_times():
    global counter
    for _ in range(100_000):
        with lock:           # 🔒 Lock the door
            counter += 1    # ✅ Only I'm inside, no one else!
                             # 🔓 Door unlocks automatically after

thread_A = threading.Thread(target=safe_add_many_times)
thread_B = threading.Thread(target=safe_add_many_times)

thread_A.start()
thread_B.start()

thread_A.join()
thread_B.join()

print(f"Expected : 200000")
print(f"Got      : {counter}")  # Always 200000 ✅
```

---

## 🔐 The Fix — Analogy

Think of a **Lock** like a **bathroom door**:

| Step | What Happens |
|------|-------------|
| Thread A enters | 🔒 Locks the door |
| Thread B arrives | 🕐 Waits outside |
| Thread A finishes | 🔓 Unlocks the door |
| Thread B enters | 🔒 Locks the door |

> Now they **never** use the bathroom at the same time — and the counter is always correct!

---

## 📊 Summary Table

| | Without Lock ❌ | With Lock ✅ |
|---|---|---|
| Speed | Faster | Slightly slower |
| Result | Wrong / Unpredictable | Always correct |
| Safe? | No | Yes |
| Real-world use | Never for shared data | Always for shared data |

---

## 🎯 Key Takeaway

```
Race Condition  =  Two workers + One shared thing + No rules  =  💥 Chaos!

Lock            =  One worker at a time                       =  ✅ Safe & Correct!
```

> Run the broken Python example yourself — you'll see the counter produce a **different wrong number** almost every time you run it! 🎲

---

## 🧩 Quick Recap

| Concept | Meaning |
|---------|---------|
| **Thread** | A worker doing a task |
| **Shared Data** | Something both workers touch |
| **Race Condition** | Both workers clash on shared data |
| **Lock** | A rule: only one worker at a time |
| **`threading.Lock()`** | Python's built-in lock tool |

---

<div align="center">

Made with ❤️ for curious Standard 8 minds 🚀

</div>
