# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] **Game's purpose:** A Streamlit number-guessing game. The player guesses a secret number within a difficulty-based range and a limited number of attempts, guided by "higher/lower" hints; the score rewards winning in fewer attempts.
- [x] **Bugs found:** hints pointed the wrong direction; the secret was cast to a string on even attempts, so the hint flipped on repeated identical guesses; "New Game" didn't reset `status`/`score`/`history`, leaving a finished game stuck; the "Attempts left" count was off by one; the range text was hardcoded to "1 and 100"; "Hard" had a narrower range than "Normal"; the attempts allowed didn't decrease with difficulty (Normal granted more than Easy), so the limit felt random; the scoring rewarded some wrong guesses; and `logic_utils.py` was unimplemented, so `pytest` couldn't run.
- [x] **Fixes applied:** mapped each outcome to a corrected hint message; removed the even-attempt string cast so guesses are always compared as integers; made "New Game" reset all session state; initialized `attempts` to 0 and rendered "Attempts left" through an `st.empty()` placeholder that refreshes after each guess is counted, so the count no longer trails by one; displayed the real difficulty range; widened "Hard" to 1–100; set the attempts allowed to decrease with difficulty (Easy 10, Normal 7, Hard 5); made scoring consistent (wins scale with attempts, every wrong guess is a flat −5); and refactored all four logic functions into `logic_utils.py`, with `check_guess` returning a single outcome string so the tests pass.

## 📸 Demo Walkthrough

A sample game on **Normal** difficulty (range 1–50, 7 attempts, secret = 32):

1. **Start.** The info bar reads "Guess a number between 1 and 50. Attempts left: 7" and the score is 0.
2. **Guess `25`** → the secret is higher, so the hint reads "📈 Go HIGHER!" (Too Low). Attempts left: 6, score: −5.
3. **Guess `40`** → the secret is lower, so the hint reads "📉 Go LOWER!" (Too High). Attempts left: 5, score: −10.
4. **Guess `32`** → "🎉 Correct!" with balloons and "You won! The secret was 32." The win adds 100 − 10 × (3 − 1) = 80 points, for a final score of 70, and the status becomes "won".
5. **Click "New Game"** → attempts, score, history, and status all reset, a fresh secret is drawn from the selected difficulty's range, and play starts over.

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
$ python -m pytest tests/ -v
============================= test session starts ==============================
collected 3 items

tests/test_game_logic.py::test_winning_guess PASSED                      [ 33%]
tests/test_game_logic.py::test_guess_too_high PASSED                     [ 66%]
tests/test_game_logic.py::test_guess_too_low PASSED                      [100%]

============================== 3 passed in 0.03s ===============================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
