# FIX: refactored game logic_utils.py
"""Core game logic for the Game Glitch Investigator guessing game.

This module holds the pure, UI-independent logic so it can be unit tested in
isolation from the Streamlit front end in ``app.py``. Every function here is
free of side effects and Streamlit state.
"""


def get_range_for_difficulty(difficulty: str):
    """Return the inclusive guessing range for a difficulty level.

    Args:
        difficulty: The difficulty name. Matching is case-sensitive and must
            be one of ``"Easy"``, ``"Normal"``, or ``"Hard"``.

    Returns:
        tuple[int, int]: The ``(low, high)`` bounds, both inclusive. Any
        unrecognized value falls back to the Normal range, ``(1, 100)``.

    Examples:
        >>> get_range_for_difficulty("Easy")
        (1, 20)
        >>> get_range_for_difficulty("unknown")
        (1, 100)
    """
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


def is_in_range(guess: int, low: int, high: int) -> bool:
    """Check whether a guess lies within an inclusive range.

    Args:
        guess: The number to test.
        low: Lower bound, inclusive.
        high: Upper bound, inclusive.

    Returns:
        bool: ``True`` if ``low <= guess <= high``, otherwise ``False``.

    Examples:
        >>> is_in_range(5, 1, 10)
        True
        >>> is_in_range(0, 1, 10)
        False
    """
    return low <= guess <= high


def parse_guess(raw: str):
    """Parse raw user input into a validated whole-number guess.

    Only whole numbers are accepted; decimals are rejected because the secret
    is always an integer, so a fractional guess can never be correct. Inputs
    are delegated to :func:`int`, so surrounding whitespace, a leading sign
    (``"+5"``), and leading zeros (``"007"``) are tolerated.

    Args:
        raw: The unprocessed input string from the guess field. ``None`` and
            the empty string are treated as "no input".

    Returns:
        tuple[bool, int | None, str | None]: A ``(ok, value, error)`` triple.
        On success, ``(True, parsed_int, None)``. On failure,
        ``(False, None, error_message)`` where ``error_message`` is one of:

        * ``"Enter a guess."`` - input was ``None`` or empty.
        * ``"Please enter a whole number."`` - input contained a decimal point.
        * ``"That is not a number."`` - input was non-numeric.

    Examples:
        >>> parse_guess("42")
        (True, 42, None)
        >>> parse_guess("3.5")
        (False, None, 'Please enter a whole number.')
        >>> parse_guess("abc")
        (False, None, 'That is not a number.')
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
    """Compare a guess against the secret and produce a result and hint.

    Args:
        guess: The player's numeric guess.
        secret: The secret number to match. Should be the same numeric type
            as ``guess`` so the comparison is numeric rather than lexical.

    Returns:
        tuple[str, str]: An ``(outcome, message)`` pair where ``outcome`` is
        one of ``"Win"``, ``"Too High"``, or ``"Too Low"``, and ``message`` is
        a player-facing hint that points toward the secret.

    Examples:
        >>> check_guess(50, 50)
        ('Win', '🎉 Correct!')
        >>> check_guess(80, 50)
        ('Too High', '📉 Go LOWER!')
        >>> check_guess(20, 50)
        ('Too Low', '📈 Go HIGHER!')
    """
    if guess == secret:
        return "Win", "🎉 Correct!"

    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Compute the new score after a guess.

    Scoring rules:
        * ``"Win"`` awards ``100 - 10 * (attempt_number + 1)`` points, floored
          at a minimum of 10, so winning sooner is worth more.
        * ``"Too High"`` and ``"Too Low"`` each cost 5 points.
        * Any other outcome leaves the score unchanged.

    Args:
        current_score: The score before this guess.
        outcome: The result from :func:`check_guess` (``"Win"``,
            ``"Too High"``, ``"Too Low"``, or any other string).
        attempt_number: The 1-based number of the attempt just made; used to
            scale the win bonus.

    Returns:
        int: The updated score. May be negative, since penalties have no floor.

    Examples:
        >>> update_score(0, "Win", 1)
        80
        >>> update_score(50, "Too High", 3)
        45
    """
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
    """Build an immutable-friendly summary of a finished game.

    A defensive copy of ``guesses`` is stored so that later mutations to the
    live game's history list cannot retroactively alter a saved record.

    Args:
        secret: The secret number for the game being archived.
        guesses: An iterable of the guesses made during the game. Copied into
            a new list in the returned record.
        status: The game's final status, typically ``"won"``, ``"lost"``, or
            ``"playing"`` (for a game abandoned mid-play).

    Returns:
        dict: A record of the form
        ``{"secret": secret, "guesses": [...], "status": status}``.

    Examples:
        >>> make_game_record(13, [10, 20, 13], "won")
        {'secret': 13, 'guesses': [10, 20, 13], 'status': 'won'}
    """
    return {
        "secret": secret,
        "guesses": list(guesses),
        "status": status,
    }


def outcome_label(status: str) -> str:
    """Map a game's status to a human-friendly, emoji-prefixed label.

    Args:
        status: A game status string. ``"won"`` and ``"lost"`` map to their
            respective labels; any other value (e.g. an abandoned game still
            marked ``"playing"``) is treated as abandoned.

    Returns:
        str: ``"🎉 Won"``, ``"💀 Lost"``, or ``"⏳ Abandoned"``.

    Examples:
        >>> outcome_label("won")
        '🎉 Won'
        >>> outcome_label("playing")
        '⏳ Abandoned'
    """
    if status == "won":
        return "🎉 Won"
    if status == "lost":
        return "💀 Lost"
    return "⏳ Abandoned"


def proximity_hint(guess, secret, low, high):
    """Return a Hot/Cold closeness label and a Streamlit color for a guess.

    Closeness is measured relative to the size of the playing range, so the
    same gap feels "hotter" on a wide range than on a narrow one.

    Args:
        guess: The player's numeric guess.
        secret: The secret number.
        low: Lower bound of the range, inclusive.
        high: Upper bound of the range, inclusive.

    Returns:
        tuple[str, str]: An ``(label, color)`` pair. ``label`` is an
        emoji-prefixed closeness description; ``color`` is a Streamlit color
        name such as ``green``, ``red``, ``orange``, ``blue``, or ``violet``.

    Examples:
        >>> proximity_hint(50, 50, 1, 100)
        ('🎯 Exact!', 'green')
        >>> proximity_hint(52, 50, 1, 100)
        ('🔥 Hot', 'red')
        >>> proximity_hint(1, 100, 1, 100)
        ('🧊 Cold', 'violet')
    """
    distance = abs(guess - secret)
    span = max(high - low, 1)
    ratio = distance / span
    if distance == 0:
        return "🎯 Exact!", "green"
    if ratio <= 0.10:
        return "🔥 Hot", "red"
    if ratio <= 0.25:
        return "🌤️ Warm", "orange"
    if ratio <= 0.50:
        return "❄️ Cool", "blue"
    return "🧊 Cold", "violet"


def build_session_summary(past_games):
    """Build a compact table of finished games for the session summary.

    Args:
        past_games: A list of game records as produced by
            :func:`make_game_record`.

    Returns:
        list[dict]: One row per game with the keys ``"Game"``, ``"Secret"``,
        ``"Guesses"`` (the number of guesses made), and ``"Result"`` (a label
        from :func:`outcome_label`).

    Examples:
        >>> games = [{"secret": 7, "guesses": [3, 7], "status": "won"}]
        >>> build_session_summary(games)
        [{'Game': 1, 'Secret': 7, 'Guesses': 2, 'Result': '🎉 Won'}]
    """
    rows = []
    for index, game in enumerate(past_games, start=1):
        rows.append({
            "Game": index,
            "Secret": game["secret"],
            "Guesses": len(game["guesses"]),
            "Result": outcome_label(game["status"]),
        })
    return rows
