import streamlit as st
import json
import requests

st.set_page_config(page_title="Match Matrix", page_icon="🏏", layout="centered")

st.markdown("""
    <style>
    .block-container { max-width: 380px; padding: 0.5rem; }
    div[data-testid="stMarkdownContainer"] pre { font-family: monospace; font-size: 12px !important; }
    </style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# INDEPENDENT MULTI-MATCH LIVE SYNC
# -------------------------------------------------------------
# Base cloud URL. We append the match name to isolate the drafts!
SYNC_BASE_URL = "https://kv.rest/v1/matrix-2026-"

def get_match_slug(match_name):
    return match_name.lower().replace(" ", "").replace("(", "").replace(")", "").replace("-", "")

def load_live_state(match_name):
    slug = get_match_slug(match_name)
    try:
        r = requests.get(SYNC_BASE_URL + slug, timeout=5)
        if r.status_code == 200 and r.text:
            return json.loads(r.text)
    except:
        pass
    return {"draft_step": 1, "ms_team": [], "mn_team": [], "ms_backup": None, "mn_backup": None}

def save_live_state(match_name, state_dict):
    slug = get_match_slug(match_name)
    try:
        requests.post(SYNC_BASE_URL + slug, data=json.dumps(state_dict), timeout=5)
    except:
        pass

# -------------------------------------------------------------
# ACTUAL SCHEDULED MATCHES SQUAD DATABASE (IPL 2026 PLAYOFFS)
# -------------------------------------------------------------
ROSTERS = {
    "KKR vs SRH (Qualifier 2)": [
        "Sunil Narine", "Rahmanullah Gurbaz", "Venkatesh Iyer", "Shreyas Iyer", 
        "Nitish Rana", "Andre Russell", "Rinku Singh", "Ramandeep Singh", 
        "Mitchell Starc", "Vaibhav Arora", "Harshit Rana", "Varun Chakravarthy",
        "Travis Head", "Abhishek Sharma", "Rahul Tripathi", "Aiden Markram", 
        "Heinrich Klaasen", "Nitish Kumar Reddy", "Abdul Samad", "Shahbaz Ahmed", 
        "Pat Cummins", "Jaydev Unadkat", "Bhuvneshwar Kumar", "T Natarajan"
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

# 1. Select from actual upcoming schedule
selected_match = st.selectbox("🎯 Choose Active Schedule:", list(ROSTERS.keys()))

# Load the separate cloud slot assigned purely for this specific match
shared_state = load_live_state(selected_match)

prev_winner = st.selectbox("Who won the previous match?", ["Midha & Negi", "Mukesh Sir"])
t1_name = "Midha & Negi" if prev_winner == "Midha & Negi" else "Mukesh Sir"
t2_name = "Mukesh Sir" if t1_name == "Midha & Negi" else "Midha & Negi"

if st.button("🔄 Tap to Refresh Board Choices"):
    st.rerun()

current_step = shared_state["draft_step"]

# Drop picked selections cleanly from the current active pool
full_pool = ROSTERS[selected_match]
unavailable = shared_state["ms_team"] + shared_state["mn_team"]
current_pool = [p for p in full_pool if p not in unavailable]

st.subheader(f"Current Draft Step: {current_step} / 4")

if current_step == 1:
    st.info(f"🟢 Turn 1: {t1_name} select your FIRST 2 Players (Pair 1)")
    selected = st.multiselect("Pick 2 Players:", current_pool, max_selections=2)
    if st.button("Confirm 2 Players") and len(selected) == 2:
        if t1_name == "Midha & Negi":
            shared_state["mn_team"].extend(selected)
        else:
            shared_state["ms_team"].extend(selected)
        shared_state["draft_step"] = 2
        save_live_state(selected_match, shared_state)
        st.success("Sent! Tell your partner to refresh.")
        st.rerun()

elif current_step == 2:
    st.info(f"🔵 Turn 2: {t2_name} select your NEXT 4 Players (Pairs 1 & 2)")
    selected = st.multiselect("Pick 4 Players:", current_pool, max_selections=4)
    if st.button("Confirm 4 Players") and len(selected) == 4:
        if t2_name == "Midha & Negi":
            shared_state["mn_team"].extend(selected)
        else:
            shared_state["ms_team"].extend(selected)
        shared_state["draft_step"] = 3
        save_live_state(selected_match, shared_state)
        st.success("Sent! Tell your partner to refresh.")
        st.rerun()

elif current_step == 3:
    st.info(f"🟢 Turn 3: {t1_name} select your NEXT 4 Players (Pairs 2 & 3)")
    selected = st.multiselect("Pick 4 Players:", current_pool, max_selections=4)
    if st.button("Confirm 4 Players") and len(selected) == 4:
        if t1_name == "Midha & Negi":
            shared_state["mn_team"].extend(selected)
        else:
            shared_state["ms_team"].extend(selected)
        shared_state["draft_step"] = 4
        save_live_state(selected_match, shared_state)
        st.success("Sent! Tell your partner to refresh.")
        st.rerun()

elif current_step == 4:
    st.info(f"🔵 Turn 4: {t2_name} select your FINAL 2 Players (Pair 3)")
    selected = st.multiselect("Pick 2 Players:", current_pool, max_selections=2)
    if st.button("Confirm Final Players") and len(selected) == 2:
        if t2_name == "Midha & Negi":
            shared_state["mn_team"].extend(selected)
        else:
            shared_state["ms_team"].extend(selected)
        shared_state["draft_step"] = 5
        save_live_state(selected_match, shared_state)
        st.success("Draft finished successfully!")
        st.rerun()

else:
    st.balloons()
    st.success("✅ Draft Completed! Roster is locked.")

st.markdown("---")
ms_display = ", ".join(shared_state["ms_team"]) if shared_state["ms_team"] else "None"
mn_display = ", ".join(shared_state["mn_team"]) if shared_state["mn_team"] else "None"

st.markdown(f"**Selected Room:** {selected_match}")
st.markdown(f"**🔵 Mukesh Sir:** {ms_display}")
st.markdown(f"**🟢 Midha & Negi:** {mn_display}")

if st.button("🚨 Reset This Draft Room"):
    reset_dict = {"draft_step": 1, "ms_team": [], "mn_team": [], "ms_backup": None, "mn_backup": None}
    save_live_state(selected_match, reset_dict)
    st.rerun()
