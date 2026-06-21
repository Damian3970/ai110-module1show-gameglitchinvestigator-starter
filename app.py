import random
import streamlit as st

from logic_utils import (
    get_range_for_difficulty,
    is_in_range,
    parse_guess,
    check_guess,
    update_score,
    make_game_record,
    outcome_label,
)

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

if "attempts" not in st.session_state:
    st.session_state.attempts = 0 #FIX: consistent attempt counter for first game and new games

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

if "past_games" not in st.session_state:
    st.session_state.past_games = []

st.subheader("Make a guess")

st.info(
    f"Guess a number between {low} and {high}. " #FIX: range is no longer hardcoded
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

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
    # Archive the game being left behind (only if it actually had guesses)
    # so its guesses and secret are preserved in the history log.
    if st.session_state.history:
        st.session_state.past_games.append(
            make_game_record(
                st.session_state.secret,
                st.session_state.history,
                st.session_state.status,
            )
        )
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(low, high) #FIX: "New Game" considers difficulty range
    st.session_state.score = 0 #FIX: "New Game" resets game
    st.session_state.status = "playing"
    st.session_state.history = []
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
elif submit:
    st.session_state.attempts += 1

    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.session_state.history.append(raw_guess)
        st.error(err)
    elif not is_in_range(guess_int, low, high): #FIX: out-of-range guesses no longer accepted
        st.session_state.history.append(guess_int)
        st.error(f"Guess must be between {low} and {high}.")
    else:
        st.session_state.history.append(guess_int)

        outcome, message = check_guess(guess_int, st.session_state.secret) #FIX: now passes the int secret directly

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

with st.expander("Developer Debug Info"): #FIX: debug panel shows correct score
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

if st.session_state.past_games:
    total_games = len(st.session_state.past_games)
    with st.expander(f"📜 Previous Games ({total_games})"):
        # Most recent game first.
        for offset, game in enumerate(reversed(st.session_state.past_games)):
            game_number = total_games - offset
            guesses = ", ".join(str(g) for g in game["guesses"])
            st.markdown(
                f"**Game {game_number}** — "
                f"Secret: `{game['secret']}` — "
                f"{outcome_label(game['status'])}"
            )
            st.write("Guesses:", guesses)

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
