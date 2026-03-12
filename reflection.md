# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?
1. The guess feedback output was inverted: when my guess was higher than the secret it told me to go higher, and when my guess was lower it told me to go lower.
2. The attempt counter was off by one because it started at 1; the UI showed fewer attempts left than actually available.
3. Changing difficulty updated the displayed range, but the secret number was still generated from the full 1–100 range.

---

## 2. How did you use AI as a teammate?

- **Which AI tools did you use on this project?**
  I used GitHub Copilot to suggest code fixes and refactorings while I worked through the bugs.

- **One example of a correct AI suggestion:**
  Copilot suggested fixing the inverted hint logic so that a too-high guess tells the player to go lower and a too-low guess tells them to go higher. I verified this by reviewing every message string in the code and then playing the game to confirm the hints matched the expected behavior.

- **One example of an incorrect/misleading AI suggestion:**
  Copilot updated the displayed range message when difficulty changed, but it did not update the logic that generated the secret number range. I discovered this by playing the game on Easy and seeing secrets above 20, then tracing the secret-generation code to find it still used 1–100.

---

## 3. Debugging and testing your fixes

- **How did you decide whether a bug was really fixed?**
  I verified the fix by observing the behavior in the running Streamlit app and by adding automated tests that asserted the correct behavior. When both manual play and the tests agreed, I treated the bug as fixed.

- **Describe at least one test you ran and what it showed you:**
  I added `pytest` tests for `check_guess()` to confirm it returns the correct hint text for too-high and too-low guesses. The failing tests showed the hints were reversed, and once I fixed the logic the tests passed.

- **Did AI help you design or understand any tests? How?**
  Yes. Copilot suggested edge cases like handling non-numeric input and verifying behavior when the secret is stored as a string (which happens when the app intentionally corrupts the secret on even attempts).

---

## 4. What did you learn about Streamlit and state?

- **How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?**
  Streamlit reruns the entire script on every interaction (button click, input change), so you can’t rely on normal in-memory variables staying around. Session state is how you persist values between reruns (like score, attempts, and the secret number), and it acts like a dictionary that survives the automatic script re-execution.

---

## 5. Looking ahead: your developer habits

- **What is one habit or strategy you want to reuse?**
  I want to keep writing small, focused tests for each function as I fix bugs; it gives me fast feedback and confidence that the fix really works.

- **What is one thing you would do differently next time with AI?**
  Next time, I’ll explicitly validate each AI suggestion with a small test or manual check before committing it.

- **How did this project change how you think about AI-generated code?**
  It made me realize AI can generate useful starting points quickly, but I still need to be the one who verifies behavior and writes tests to ensure it’s correct.
