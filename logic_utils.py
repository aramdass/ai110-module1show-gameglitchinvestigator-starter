def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    # FIX: Hard used to be 1-50, narrower (easier) than Normal's 1-100.
    # Ranges now widen as difficulty increases.
    ranges = {
        "Easy": (1, 20),
        "Normal": (1, 50),
        "Hard": (1, 100),
    }
    return ranges.get(difficulty, (1, 100))


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None or raw.strip() == "":
        return False, None, "Enter a guess."

    text = raw.strip()
    try:
        if "." in text:
            value = int(float(text))
        else:
            value = int(text)
    except (ValueError, TypeError):
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return the outcome string.

    outcome is one of: "Win", "Too High", "Too Low"
    """
    # FIX: returns a single outcome string (the pytest suite expects "Win" /
    # "Too High" / "Too Low", not a tuple) and compares ints directly. The old
    # lexicographic string-comparison fallback (e.g. "8" > "50") was removed.
    if guess == secret:
        return "Win"
    if guess > secret:
        return "Too High"
    return "Too Low"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number.

    A win is worth more the fewer attempts it took (min 10). Any wrong
    guess costs a flat 5 points.
    """
    # FIX: removed the even/odd quirk that rewarded some "Too High" guesses with
    # +5. Wins now scale cleanly with attempt count; any wrong guess is a flat -5.
    if outcome == "Win":
        points = 100 - 10 * (attempt_number - 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome in ("Too High", "Too Low"):
        return current_score - 5

    return current_score
