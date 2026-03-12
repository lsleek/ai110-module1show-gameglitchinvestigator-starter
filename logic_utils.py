import random

#FIX: Refactored logic into logic_utils.py using Copilot Agent mode
def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100

#FIX: Refactored logic into logic_utils.py using Copilot Agent mode
def parse_guess(raw: str):
    """Parse raw user input into an int guess.

    Returns:
        (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None

#FIX: Refactored logic into logic_utils.py using Copilot Agent mode
def check_guess(guess, secret):
    """Compare a guess to the secret value and return (outcome, message)."""
    if guess == secret:
        return "Win", "🎉 Correct!"

    try:
        # FIX: if guess is lower than secret, prompt to go higer
        if guess < secret:
            return "Too Low", "📈 Go HIGHER!"
        else:
            return "Too High", "📉 Go LOWER!"
    except TypeError:
        g = str(guess)
        if g == secret:
            return "Win", "🎉 Correct!"
        if g > secret:
            return "Too High", "📈 Go LOWER!"
        return "Too Low", "📉 Go HIGHER!"

#FIX: Refactored logic into logic_utils.py using Copilot Agent mode
def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        if attempt_number % 2 == 0:
            return current_score + 5
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score

#FIX: Refactored logic into logic_utils.py using Copilot Agent mode
def get_attempt_limit(difficulty: str):
    """Return the number of attempts allowed for a given difficulty."""
    return {"Easy": 6, "Normal": 8, "Hard": 5}.get(difficulty, 8)

#FIX: Refactored logic into logic_utils.py using Copilot Agent mode
def init_game_state(session_state, low: int, high: int):
    """Ensure session_state has required game fields initialized."""
    session_state.setdefault("secret", random.randint(low, high))
    # FIX: Start at 0 so that the first guess counts as attempt #1.
    session_state.setdefault("attempts", 0)
    session_state.setdefault("score", 0)
    session_state.setdefault("status", "playing")
    session_state.setdefault("history", [])


def start_new_game(session_state, low: int, high: int, reset_score: bool = False):
    """Reset the session state for a new game."""
    session_state["attempts"] = 0
    session_state["secret"] = random.randint(low, high)
    session_state["status"] = "playing"
    session_state["history"] = []
    if reset_score:
        session_state["score"] = 0


def get_comparison_secret(secret, attempt_number: int):
    """Return the secret value used for comparison based on the attempt number."""
    if attempt_number % 2 == 0:
        return str(secret)
    return secret
