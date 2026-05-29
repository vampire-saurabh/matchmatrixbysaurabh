import streamlit as st

st.set_page_config(page_title="Match Matrix Engine", page_icon="🏏", layout="centered")

# --- DATA STATE ---
if 'stats' not in st.session_state:
    st.session_state.stats = {}
if 'teams' not in st.session_state:
    st.session_state.teams = {"Mukesh Sir": [], "Midha & Negi": []}

st.title("🏏 Match Matrix: Auto-Calculator")

# --- STEP 1: DEFINE TEAMS ---
st.subheader("1. Setup Teams")
col1, col2 = st.columns(2)
with col1:
    p1 = st.text_input("Add Player to Mukesh Sir:")
    if st.button("Add to Mukesh"):
        st.session_state.teams["Mukesh Sir"].append(p1)
with col2:
    p2 = st.text_input("Add Player to Midha & Negi:")
    if st.button("Add to Midha"):
        st.session_state.teams["Midha & Negi"].append(p2)

# --- STEP 2: AUTO-CALCULATOR ---
st.markdown("---")
st.subheader("2. Calculate Fantasy Points")
st.write("Select a player to quickly set their performance:")

all_players = st.session_state.teams["Mukesh Sir"] + st.session_state.teams["Midha & Negi"]
selected_p = st.selectbox("Select Player", all_players)

if selected_p:
    # Use sliders for instant point updates (No typing required)
    runs = st.slider("Runs Scored", 0, 150, 0)
    wicks = st.slider("Wickets Taken", 0, 10, 0)
    catch = st.slider("Catches Taken", 0, 5, 0)
    
    # CALCULATE AUTOMATICALLY
    pts = (runs * 1) + (wicks * 20) + (catch * 8)
    st.metric("Total Fantasy Points", pts)
    
    if st.button("Save Stats"):
        st.session_state.stats[selected_p] = pts

# --- STEP 3: SCOREBOARD ---
st.markdown("---")
st.subheader("🏆 Live Scoreboard")
for team, players in st.session_state.teams.items():
    st.write(f"**{team}**")
    total_score = sum([st.session_state.stats.get(p, 0) for p in players])
    st.write(f"Total: {total_score} pts")
    st.write(players)
