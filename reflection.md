# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- The number of attempts displayed on the left sidebar under the difficulty setting should match the number of attempts the user is allowed to submit. They do not match, it seems to allow 1 try less than the number stated
- Pressed the new game button should reset the game and allow the user to try again, but the game state remains unchanged



**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Guessed 1 with a secret of 87 |Hint should say "Go HIGHER!" |The hint says "Go LOWER!" |None |
|Guessed 5 several times consecutively with a secret of 12| Hint should say "Go HIGHER!" each time|Hint alternates each ime between "Go HIGHER!" and "Go LOWER!"| None|
| Compared the attempts allowed across difficulties | Higher difficulty should allow fewer attempts | Normal allowed 8 but Easy allowed 6 (Hard 5), so the limit rose then fell instead of decreasing | None |
---

## 2. How did you use AI as a teammate?

I used Claude (through the Claude Code agent) as a pair-debugging partner. It scanned `app.py`, `logic_utils.py`, and `tests/test_game_logic.py`, then proposed a fix plan that I reviewed and approved before any code changed.

One suggestion that was correct: for the bug where the hint alternated between "Go HIGHER!" and "Go LOWER!" on repeated identical guesses (secret 12, guessing 5), Claude traced it to a line that cast the secret to a string on even-numbered attempts (`secret = str(...)`), which forced a lexicographic comparison instead of a numeric one. It suggested deleting that cast so the code always compares integers, and also making `check_guess` return a single outcome string to satisfy the existing tests. I verified this by running `pytest tests/` (3 passed) and by guessing the same number several times in the running app and watching the hint stay consistent.

One suggestion that was misleading: echoing the README, Claude first listed "the secret number changes every time you click Submit" as a likely bug to fix. When I had it check the code, the secret was already stored safely in `st.session_state` behind an `if "secret" not in st.session_state` guard, so it never regenerated — the real cause was the string-cast above. Reading that one line of code disproved the suggestion and kept me from chasing a bug that didn't exist.

---

## 3. Debugging and testing your fixes

I decided a bug was fixed only after reproducing it, applying the change, and then seeing the wrong behavior gone — for the hint bugs that meant replaying the exact inputs from my bug log (guessing 1 against a secret of 87 and confirming it now says "Go HIGHER!"). The main automated test was `pytest tests/`, which reported `3 passed in 0.01s`; its three cases (`check_guess(50, 50)` → "Win", `(60, 50)` → "Too High", `(40, 50)` → "Too Low") proved the comparison logic and the outcome strings were right. I also called the logic by hand — `update_score(0, "Win", 1)` returned 100 and a deeper win clamped at the 10-point floor — and used the "Developer Debug Info" panel to watch `attempts`, `status`, and `secret` while testing the off-by-one and New Game fixes. AI mainly helped me *understand* the provided tests: it pointed out that the suite expected `check_guess` to return a single string, which told me the function had to be refactored rather than left returning a tuple.

---

## 4. What did you learn about Streamlit and state?

A Streamlit "rerun" means that every time you interact with the page — click a button, type a guess — Streamlit runs the entire script again from top to bottom. Because of that, ordinary variables are rebuilt from scratch on each run and forget everything, so anything that needs to persist (the secret, attempt count, score, win/lose status) has to be stored in `st.session_state`, which is the one thing that survives between reruns. The "New Game" bug was a perfect example: we reset some session-state values but forgot `status`, so the previous "won"/"lost" result carried over and blocked the next game. The "Attempts left" fix was about rerun *ordering* — the info box was drawn near the top using the count from before the guess, so we rendered it through an `st.empty()` placeholder and refreshed it after the guess was counted.

---

## 5. Looking ahead: your developer habits

The habit I want to keep is "reproduce, fix, re-test": writing the bug down with concrete inputs first, then running `pytest` after every change so a regression shows up immediately instead of later. Next time I would verify the AI's (and the README's) claims against the actual code before acting on them, the way the "secret regenerates on submit" lead fell apart once I read the session-state guard. This project changed how I see AI-generated code — it can look polished and "production-ready" while hiding real logic and state bugs, so I now treat it as a first draft to test and review rather than trust.
