import random
import streamlit as st

# FIX (AI-assisted refactor): the game logic lived inline in app.py and couldn't
# be unit-tested. Moved it into logic_utils.py so pytest can import it directly.
from logic_utils import (
    get_range_for_difficulty,
    parse_guess,
    check_guess,
    update_score,
)

# FIX: the hint directions were swapped (e.g. "Too High" told the player to "Go
# HIGHER"). check_guess now returns only the outcome; map it to the corrected
# message here so the arrows and wording actually point the right way.
HINT_MESSAGES = {
    "Win": "🎉 Correct!",
    "Too High": "📉 Go LOWER!",
    "Too Low": "📈 Go HIGHER!",
}

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

# FIX: limits used to be Easy 6 / Normal 8 / Hard 5, so attempts rose then fell
# instead of decreasing — the count felt random. They now drop as difficulty rises.
attempt_limit_map = {
    "Easy": 10,
    "Normal": 7,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

if "attempts" not in st.session_state:
    # FIX: was 1, which made "Attempts left" off by one and clashed with
    # New Game resetting it to 0.
    st.session_state.attempts = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

st.subheader("Make a guess")

# Placeholder so we can refresh "Attempts left" AFTER a guess is counted.
# Otherwise the info renders at the top of the script using the attempt
# count from before this guess, so it always shows one more than is left.
attempts_info = st.empty()


def render_attempts_left():
    remaining = max(attempt_limit - st.session_state.attempts, 0)
    attempts_info.info(
        # FIX: was hardcoded "between 1 and 100"; now reflects the actual range.
        f"Guess a number between {low} and {high}. "
        f"Attempts left: {remaining}"
    )


render_attempts_left()

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

if new_game:
    # FIX: New Game only reset attempts + secret before, so score/history/status
    # leaked across games and a finished game stayed "won"/"lost" forever (the
    # status check below would st.stop() immediately, making it unplayable).
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(low, high)  # FIX: was hardcoded 1-100, ignoring difficulty.
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    st.session_state.attempts += 1

    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.session_state.history.append(raw_guess)
        st.error(err)
    else:
        st.session_state.history.append(guess_int)

        # FIX: removed the even-attempt `secret = str(...)` cast that broke int
        # comparisons (and produced lying hints). Always compare against the int secret.
        outcome = check_guess(guess_int, st.session_state.secret)
        message = HINT_MESSAGES[outcome]

        if show_hint:
            st.warning(message)

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

    # The guess above changed the attempt count, so re-render the info box
    # to show the correct number of attempts left.
    render_attempts_left()

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
