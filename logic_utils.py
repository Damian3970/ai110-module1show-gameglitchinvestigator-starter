#FIX: refactored game logic_utils.py

def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


def is_in_range(guess: int, low: int, high: int) -> bool:
    """Return True if guess falls within the inclusive [low, high] range."""
    return low <= guess <= high


def parse_guess(raw: str):
    """
    Parse user input into a whole-number guess.

    Only whole numbers are accepted; decimals are rejected (the secret is
    always an integer, so a fractional guess can never be correct).

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    if "." in raw:
        return False, None, "Please enter a whole number."

    try:
        value = int(raw)
    except ValueError:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    if guess == secret:
        return "Win", "🎉 Correct!"

    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score


def make_game_record(secret, guesses, status):
    """
    Build a summary of a finished game for the history log.

    Stores a copy of the guesses so later changes to the live game's
    history list cannot mutate the saved record.

    Returns: {"secret": ..., "guesses": [...], "status": ...}
    """
    return {
        "secret": secret,
        "guesses": list(guesses),
        "status": status,
    }


def outcome_label(status: str) -> str:
    """Human-friendly label for a game's final status."""
    if status == "won":
        return "🎉 Won"
    if status == "lost":
        return "💀 Lost"
    return "⏳ Abandoned"
