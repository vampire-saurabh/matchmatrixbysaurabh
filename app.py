import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Match Matrix", page_icon="🏏", layout="centered")

st.markdown("""
    <style>
    .block-container { max-width: 380px; padding: 0.5rem; }
    div[data-testid="stMarkdownContainer"] pre { font-family: monospace; font-size: 12px !important; }
    </style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# FREE PUBLIC SYNC HUB (No Secrets Required)
# -------------------------------------------------------------
# We use an open cloud bin to relay the draft picks between your two phones
SYNC_API = "https://kv.rest/v1/matrix-draft-saurabh-mukesh-2026"

def load_live_state():
    try:
        r = requests.get(SYNC_API, timeout=5)
        if r.status_code == 200 and r.text:
            import json
            return json.loads(r.text)
    except:
        pass
    # Default layout matched exactly to your working 4-step structure
    return {"draft_step": 1, "ms_team": [], "mn_team": [], "ms_backup": None, "mn_backup": None}

def save_live_state(state_dict):
    try:
        import json
        requests.post(SYNC_API, data=json.dumps(state_dict), timeout=5)
    except:
        pass

# Instantly pull what's on the other person's phone
shared_state = load_live_state()

# Roster pool built directly from your WhatsApp history screenshot
ROSTERS = {
    "GT vs RR (Qualifier 2)": [
        "Vaibhav Abhishek", "Ishan kalaasen", "Head Jaiswal", "Dhruv Parag",
        "Reddy cummins", "Donovan Shanka", "Abhishek Sharma", "Travis Head",
        "Heinrich Klaasen", "Pat Cummins", "Nitish Reddy", "Sanju Samson",
        "Yashasvi Jaiswal", "Riyan Parag", "Dhruv Jurel", "Abdul Samad",
        "Shahbaz Ahmed", "Jaydev Unadkat", "Bhuvneshwar Kumar", "T Natarajan",
        "Cummins", "Klaasen", "Head", "Abhishek"
    ]
}

st.title("🏏 Match Matrix Engine")

match_select = st.selectbox("GT vs RR (Qualifier 2)", list(ROSTERS.keys()), label_visibility="collapsed")
full_pool = ROSTERS[match_select]

prev_winner = st.selectbox("Who won the previous match?", ["Midha & Negi", "Mukesh Sir"])
t1_name = "Midha & Negi" if prev_winner == "Midha & Negi" else "Mukesh Sir"
t2_name = "Mukesh Sir" if t1_name == "Midha & Negi" else "Midha & Negi"

# Main sync button to see the other person's pick instantly
if st.button("🔄 Tap to Refresh Board Choices"):
    st.rerun()

current_step = shared_state["draft_step"]

# Filter out already drafted players
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
        save_live_state(shared_state)
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
        save_live_state(shared_state)
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
        save_live_state(shared_state)
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
        shared_state["draft_step"] = 5  # Draft complete
        save_live_state(shared_state)
        st.success("Draft finished successfully!")
        st.rerun()

else:
    st.balloons()
    st.success("✅ Draft Completed! Roster is locked.")

st.markdown("---")
# Roster Output Displays
ms_display = ", ".join(shared_state["ms_team"]) if shared_state["ms_team"] else "None"
mn_display = ", ".join(shared_state["mn_team"]) if shared_state["mn_team"] else "None"

st.markdown(f"**🔵 Mukesh Sir:** {ms_display}")
st.markdown(f"**🟢 Midha & Negi:** {mn_display}")

if st.button("🔄 Reset Draft System"):
    reset_dict = {"draft_step": 1, "ms_team": [], "mn_team": [], "ms_backup": None, "mn_backup": None}
    save_live_state(reset_dict)
    st.rerun()
