"""Regression tests for the bugs fixed in the Game Glitch Investigator.

Each section maps to a specific bug that was found and fixed, so a failure
here means a glitch has come back.
"""

import os
import sys

# Make the project root importable so `logic_utils` is found regardless of
# whether this file is run directly or via pytest.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logic_utils import (  # noqa: E402  (import follows sys.path setup above)
    get_range_for_difficulty,
    is_in_range,
    check_guess,
    parse_guess,
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


# ===========================================================================
# Edge cases
# These probe unusual inputs (negatives, decimals, extreme values, junk) to
# pin down exactly how the game handles them. Several assert *documented*
# quirks (e.g. decimals truncate), so a change in behavior is caught here.
# ===========================================================================

# --- Negative numbers -------------------------------------------------------

def test_negative_number_parses_but_is_out_of_range():
    # "-5" is a valid integer, so parsing succeeds...
    ok, value, err = parse_guess("-5")
    assert (ok, value, err) == (True, -5, None)
    # ...but it must be rejected by the range check for any normal range.
    assert is_in_range(value, 1, 100) is False


def test_negative_secret_comparison_is_numeric():
    # check_guess should still order numbers correctly with negatives.
    assert check_guess(-10, -5)[0] == "Too Low"
    assert check_guess(-1, -5)[0] == "Too High"


# --- Decimals (rejected; the secret is always a whole number) --------------

def test_positive_decimal_is_rejected():
    assert parse_guess("3.9") == (False, None, "Please enter a whole number.")


def test_negative_decimal_is_rejected():
    assert parse_guess("-2.7") == (False, None, "Please enter a whole number.")


def test_whole_valued_decimal_is_rejected():
    # Even "5.0" (equal to a whole number) is rejected for containing a ".".
    assert parse_guess("5.0") == (False, None, "Please enter a whole number.")


# --- Extreme values ---------------------------------------------------------

def test_extremely_large_value_parses_but_is_out_of_range():
    ok, value, err = parse_guess("999999999999")
    assert ok is True
    assert err is None
    assert is_in_range(value, 1, 100) is False


def test_scientific_overflow_is_rejected_gracefully():
    # "1.0e999" contains a ".", so it's rejected as a non-whole number
    # rather than ever reaching int(float(...)) and overflowing.
    assert parse_guess("1.0e999") == (
        False, None, "Please enter a whole number."
    )


def test_is_in_range_handles_extremes():
    assert is_in_range(-(10 ** 9), 1, 100) is False
    assert is_in_range(10 ** 9, 1, 100) is False


# --- Accepted-but-unusual formatting ---------------------------------------

def test_whitespace_padded_number_is_accepted():
    assert parse_guess("  42  ") == (True, 42, None)


def test_plus_sign_and_leading_zeros_accepted():
    assert parse_guess("+5") == (True, 5, None)
    assert parse_guess("007") == (True, 7, None)


# --- Junk that must be rejected --------------------------------------------

def test_scientific_notation_with_dot_is_rejected():
    # Contains a ".", so it's rejected as a non-whole number (was 150 before).
    assert parse_guess("1.5e2") == (
        False, None, "Please enter a whole number."
    )


def test_scientific_notation_without_dot_is_rejected():
    # No ".", so int("1e3") is attempted directly and fails.
    assert parse_guess("1e3") == (False, None, "That is not a number.")


def test_whitespace_only_is_rejected():
    assert parse_guess("   ") == (False, None, "That is not a number.")


def test_thousands_separator_is_rejected():
    assert parse_guess("1,000") == (False, None, "That is not a number.")


def test_nan_text_is_rejected():
    assert parse_guess("nan") == (False, None, "That is not a number.")
