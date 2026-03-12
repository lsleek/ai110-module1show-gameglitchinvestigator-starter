import streamlit as st

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


def get_hot_cold_hint(guess, secret):
    """Return a hot/cold emoji string based on guess distance from secret."""
    try:
        distance = abs(int(guess) - int(secret))
    except Exception:
        return ""

    if distance == 0:
        return "🎉 Perfect!"
    if distance <= 3:
        return "🔥 Hot"
    if distance <= 10:
        return "🟠 Warm"
    return "❄️ Cold"

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit = get_attempt_limit(difficulty)

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

# FIX: If the user changes difficulty, restart the game so the secret range matches.
if st.session_state.get("difficulty") != difficulty:
    st.session_state.difficulty = difficulty
    start_new_game(st.session_state, low, high, reset_score=True)

init_game_state(st.session_state, low, high)

st.subheader("Make a guess")

st.info(
    # FIX: shows actual ranges based on difficulty level instead of hardcoded 1-100
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

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
    start_new_game(st.session_state, low, high)
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
        st.session_state.history.append(
            {
                "guess": raw_guess,
                "outcome": "Invalid",
                "hint": err,
            }
        )
        st.error(err)
    else:
        secret = get_comparison_secret(
            st.session_state.secret, st.session_state.attempts
        )

        outcome, message = check_guess(guess_int, secret)
        hot_cold = get_hot_cold_hint(guess_int, secret)

        st.session_state.history.append(
            {
                "guess": guess_int,
                "outcome": outcome,
                "hint": message,
                "hot_cold": hot_cold,
            }
        )

        if show_hint:
            hint_msg = f"{message} {hot_cold}"
            if outcome == "Win":
                st.success(hint_msg)
            elif outcome == "Too High":
                st.warning(hint_msg)
            else:
                st.info(hint_msg)

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

    # Show a simple session summary table (guess + outcome + hot/cold)
    if st.session_state.history:
        st.subheader("Session summary")
        st.table(st.session_state.history)

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
