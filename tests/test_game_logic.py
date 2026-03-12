import os
import sys

# Ensure the project root is on sys.path so imports work regardless of current working directory.
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from logic_utils import (
    check_guess,
    get_attempt_limit,
    get_comparison_secret,
    get_range_for_difficulty,
    init_game_state,
    parse_guess,
    start_new_game,
    update_score,
)


def test_get_range_for_difficulty():
    assert get_range_for_difficulty("Easy") == (1, 20)
    assert get_range_for_difficulty("Normal") == (1, 100)
    assert get_range_for_difficulty("Hard") == (1, 50)
    # Default to normal range on unknown difficulty
    assert get_range_for_difficulty("Impossible") == (1, 100)


def test_get_attempt_limit():
    assert get_attempt_limit("Easy") == 6
    assert get_attempt_limit("Normal") == 8
    assert get_attempt_limit("Hard") == 5
    assert get_attempt_limit("Impossible") == 8


def test_parse_guess_valid_and_invalid():
    assert parse_guess("42") == (True, 42, None)
    assert parse_guess("  42  ")[0] is True
    assert parse_guess("4.0") == (True, 4, None)
    assert parse_guess(None) == (False, None, "Enter a guess.")
    assert parse_guess("") == (False, None, "Enter a guess.")
    assert parse_guess("abc") == (False, None, "That is not a number.")


def test_check_guess_normal_behavior():
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"
    assert "Correct" in message

    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message

    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message


def test_check_guess_type_mismatch_falls_back_to_string():
    # secret is stored as a string (as the app sometimes does on even attempts)
    outcome, message = check_guess(60, "50")
    assert outcome == "Too High"
    assert "LOWER" in message

    outcome, message = check_guess(40, "50")
    assert outcome == "Too Low"
    assert "HIGHER" in message


def test_update_score_on_win_and_minimum():
    # First attempt should yield 80 points (100 - 10*(1+1))
    assert update_score(0, "Win", attempt_number=1) == 80
    # Late win should floor at 10
    assert update_score(0, "Win", attempt_number=20) == 10


def test_update_score_on_feedback():
    assert update_score(0, "Too High", attempt_number=1) == -5
    assert update_score(0, "Too High", attempt_number=2) == 5
    assert update_score(0, "Too Low", attempt_number=1) == -5
    assert update_score(0, "Unknown", attempt_number=1) == 0


def test_init_and_restart_game_state():
    state = {}
    init_game_state(state, 1, 5)

    assert 1 <= state["secret"] <= 5
    assert state["attempts"] == 0
    assert state["score"] == 0
    assert state["status"] == "playing"
    assert state["history"] == []

    # State reset should preserve score unless asked to reset
    state["score"] = 123
    state["history"] = [1, 2]
    start_new_game(state, 1, 5, reset_score=False)
    assert 1 <= state["secret"] <= 5
    assert state["attempts"] == 0
    assert state["history"] == []
    assert state["score"] == 123

    start_new_game(state, 1, 5, reset_score=True)
    assert state["score"] == 0


def test_get_comparison_secret_behavior():
    assert get_comparison_secret(50, 1) == 50
    assert get_comparison_secret(50, 2) == "50"
