import streamlit as st
import json
import requests
import random

st.set_page_config(page_title="Match Matrix", page_icon="🏏", layout="centered")

# Mobile visual container adjustments
st.markdown("""
    <style>
    .block-container { max-width: 380px; padding: 0.5rem; }
    div[data-testid="stMarkdownContainer"] pre { font-family: monospace; font-size: 12px !important; }
    </style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# SECURE CENTRAL STORAGE SYNC 
# -------------------------------------------------------------
SYNC_BASE_URL = "https://kv.rest/v1/matrix-2026-"

def get_match_slug(match_name):
    return match_name.lower().replace(" ", "").replace("(", "").replace(")", "").replace("-", "")

def load_live_state(match_name):
    slug = get_match_slug(match_name)
    try:
        # Cache-busting parameter forces mobile browsers to download live entries
        cb_url = f"{SYNC_BASE_URL}{slug}?cb={random.randint(1, 999999)}"
        r = requests.get(cb_url, timeout=4)
        if r.status_code == 200 and r.text.strip():
            return json.loads(r.text)
    except:
        pass
    return {"draft_step": 1, "ms_team": [], "mn_team": []}

def save_live_state(match_name, state_dict):
    slug = get_match_slug(match_name)
    try:
        requests.post(SYNC_BASE_URL + slug, data=json.dumps(state_dict), timeout=4)
    except:
        pass

# -------------------------------------------------------------
# ACTIVE FIXTURE ROSTERS
# -------------------------------------------------------------
ROSTERS = {
    "GT vs RR (Qualifier 2)": [
        "Vaibhav Sooryavanshi", "Yashasvi Jaiswal", "Sanju Samson", "Riyan Parag", 
        "Dhruv Jurel", "Ravindra Jadeja", "Jofra Archer", "Shimron Hetmyer", 
        "Rovman Powell", "Ravichandran Ashwin", "Trent Boult", "Avesh Khan", 
        "Sandeep Sharma", "Yuzvendra Chahal", "Donovan Ferreira", "Shubman Gill", 
        "Sai Sudharsan", "Jos Buttler", "Rashid Khan", "Mohammed Siraj", 
        "Kagiso Rabada", "Rahul Tewatia", "Shahrukh Khan", "David Miller", 
        "Vijay Shankar", "Mohit Sharma", "Noor Ahmad", "Spencer Johnson"
    ],
    "RCB vs TBD (The Grand Final)": [
        "Virat Kohli", "Faf du Plessis", "Rajat Patidar", "Glenn Maxwell", 
        "Cameron Green", "Dinesh Karthik", "Mahipal Lomror", "Karn Sharma",
        "Mohammed Siraj", "Yuzvendra Chahal", "Lockie Ferguson", "Yash Dayal",
        "Sunil Narine", "Travis Head", "Heinrich Klaasen", "Andre Russell",
        "Venkatesh Iyer", "Shreyas Iyer", "Pat Cummins", "Abhishek Sharma"
    ]
}

st.title("🏏 Match Matrix Engine")

selected_match = st.selectbox(
    "🎯 Choose Active Schedule Room:", 
    list(ROSTERS.keys()), 
    key="match_selector"
)

# Load accurate board state from the live network pipeline
shared_state = load_live_state(selected_match)

prev_winner = st.selectbox("Who won the previous match?", ["Midha & Negi", "Mukesh Sir"], key="winner_selector")
t1_name = "Midha & Negi" if prev_winner == "Midha & Negi" else "Mukesh Sir"
t2_name = "Mukesh Sir" if t1_name == "Midha & Negi" else "Midha & Negi"

# Fixed Indentation Block for the Refresh Command Matrix
if st.button("🔄 Tap to Refresh Board Choices"):
    st.rerun()

current_step = shared_state.get("draft_step", 1)
ms_team = shared_state.get("ms_team", [])
mn_team = shared_state.get("mn_team", [])

full_pool = ROSTERS[selected_match]
unavailable = ms_team + mn_team
current_pool = [p for p in full_pool if p not in unavailable]

st.subheader(f"Current Draft Step: {current_step} / 4")

# -------------------------------------------------------------
# TRANSACTION STEPS PIPELINE
# -------------------------------------------------------------
if current_step == 1:
    st.info(f"🟢 Turn 1: {t1_name} select your FIRST 2 Players (Pair 1)")
    selected = st.multiselect("Pick 2 Players:", current_pool, max_selections=2, key="step_1_select")
    if st.button("Confirm 2 Players", key="btn_1"):
        if len(selected) == 2:
            if t1_name == "Midha & Negi":
                mn_team.extend(selected)
            else:
                ms_team.extend(selected)
            shared_state["mn_team"] = mn_team
            shared_state["ms_team"] = ms_team
            shared_state["draft_step"] = 2
            save_live_state(selected_match, shared_state)
            st.success("Sent successfully! Inform your partner to refresh.")
            st.rerun()
        else:
            st.warning("Please select exactly 2 players before confirming.")

elif current_step == 2:
    st.info(f"🔵 Turn 2: {t2_name} select your NEXT 4 Players (Pairs 1 & 2)")
    selected = st.multiselect("Pick 4 Players:", current_pool, max_selections=4, key="step_2_select")
    if st.button("Confirm 4 Players", key="btn_2"):
        if len(selected) == 4:
            if t2_name == "Midha & Negi":
                mn_team.extend(selected)
            else:
                ms_team.extend(selected)
            shared_state["mn_team"] = mn_team
            shared_state["ms_team"] = ms_team
            shared_state["draft_step"] = 3
            save_live_state(selected_match, shared_state)
            st.success("Sent successfully! Board updated.")
            st.rerun()
        else:
            st.warning("Please select exactly 4 players before confirming.")

elif current_step == 3:
    st.info(f"🟢 Turn 3: {t1_name} select your NEXT 4 Players (Pairs 2 & 3)")
    selected = st.multiselect("Pick 4 Players:", current_pool, max_selections=4, key="step_3_select")
    if st.button("Confirm 4 Players", key="btn_3"):
        if len(selected) == 4:
            if t1_name == "Midha & Negi":
                mn_team.extend(selected)
            else:
                ms_team.extend(selected)
            shared_state["mn_team"] = mn_team
            shared_state["ms_team"] = ms_team
            shared_state["draft_step"] = 4
            save_live_state(selected_match, shared_state)
            st.success("Sent successfully! Board updated.")
            st.rerun()
        else:
            st.warning("Please select exactly 4 players before confirming.")

elif current_step == 4:
    st.info(f"🔵 Turn 4: {t2_name} select your FINAL 2 Players (Pair 3)")
    selected = st.multiselect("Pick 2 Players:", current_pool, max_selections=2, key="step_4_select")
    if st.button("Confirm Final Players", key="btn_4"):
        if len(selected) == 2:
            if t2_name == "Midha & Negi":
                mn_team.extend(selected)
            else:
                ms_team.extend(selected)
            shared_state["mn_team"] = mn_team
            shared_state["ms_team"] = ms_team
            shared_state["draft_step"] = 5
            save_live_state(selected_match, shared_state)
            st.success("Draft completed!")
            st.rerun()
        else:
            st.warning("Please select exactly 2 players before confirming.")

else:
    st.balloons()
    st.success("✅ Draft Completed! Roster selections are locked down.")

st.markdown("---")
ms_display = ", ".join(ms_team) if ms_team else "None"
mn_display = ", ".join(mn_team) if mn_team else "None"

st.markdown(f"**Current Active Room:** {selected_match}")
st.markdown(f"**🔵 Mukesh Sir Picks:** {ms_display}")
st.markdown(f"**🟢 Midha & Negi Picks:** {mn_display}")

if st.button("🚨 Reset This Draft Room"):
    reset_dict = {"draft_step": 1, "ms_team": [], "mn_team": []}
    save_live_state(selected_match, reset_dict)
    st.rerun()
