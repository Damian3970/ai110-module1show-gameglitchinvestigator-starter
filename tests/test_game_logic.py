"""Regression tests for the bugs fixed in the Game Glitch Investigator.

Each section maps to a specific bug that was found and fixed, so a failure
here means a glitch has come back.
"""

import os
import sys

# Make the project root importable so `logic_utils` is found regardless of
# whether this file is run directly or via pytest.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logic_utils import (
    get_range_for_difficulty,
    is_in_range,
    check_guess,
)

# implement tests for each bug that was addressed

# ---------------------------------------------------------------------------
# Bug: reversed hints
# "Too High" used to tell you to "Go HIGHER" (and vice versa). The hint must
# point toward the secret.
# ---------------------------------------------------------------------------

def test_too_high_guess_says_go_lower():
    outcome, message = check_guess(50, 30)  # guess above secret
    assert outcome == "Too High"
    assert "LOWER" in message


def test_too_low_guess_says_go_higher():
    outcome, message = check_guess(5, 30)  # guess below secret
    assert outcome == "Too Low"
    assert "HIGHER" in message


def test_correct_guess_wins():
    outcome, message = check_guess(30, 30)
    assert outcome == "Win"
    assert "Correct" in message


# ---------------------------------------------------------------------------
# Bug: secret compared as a string
# The app used to pass the secret as a str on even attempts, so comparisons
# fell back to lexicographic ordering ("9" > "50"). With a numeric secret the
# comparison must be numeric.
# ---------------------------------------------------------------------------

def test_single_digit_guess_below_secret_is_too_low():
    # Lexicographically "9" > "50" would wrongly report "Too High".
    outcome, _message = check_guess(9, 50)
    assert outcome == "Too Low"


def test_double_digit_guess_above_secret_is_too_high():
    outcome, _message = check_guess(40, 9)
    assert outcome == "Too High"


# ---------------------------------------------------------------------------
# Bug: out-of-range guesses accepted
# Guesses outside the difficulty's [low, high] range must be rejected.
# ---------------------------------------------------------------------------

def test_guess_inside_range_is_valid():
    assert is_in_range(50, 1, 100) is True


def test_guess_at_boundaries_is_valid():
    assert is_in_range(1, 1, 100) is True
    assert is_in_range(100, 1, 100) is True


def test_guess_below_range_is_rejected():
    assert is_in_range(0, 1, 100) is False


def test_guess_above_range_is_rejected():
    assert is_in_range(101, 1, 100) is False
    assert is_in_range(50, 1, 20) is False  # out of range for Easy


# ---------------------------------------------------------------------------
# Bug: difficulty range / hardcoded prompt
# Ranges drive the prompt text, the secret, and validation, so they must be
# correct per difficulty.
# ---------------------------------------------------------------------------

def test_difficulty_ranges():
    assert get_range_for_difficulty("Easy") == (1, 20)
    assert get_range_for_difficulty("Normal") == (1, 100)
    assert get_range_for_difficulty("Hard") == (1, 50)


def test_unknown_difficulty_defaults_to_normal_range():
    assert get_range_for_difficulty("???") == (1, 100)
