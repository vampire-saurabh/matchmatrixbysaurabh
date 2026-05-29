import streamlit as st
import json
import requests

st.set_page_config(page_title="Match Matrix", page_icon="🏏", layout="centered")

# Tight column width to match mobile screenshot size perfectly
st.markdown("""
    <style>
    .block-container { max-width: 380px; padding: 0.5rem; }
    div[data-testid="stMarkdownContainer"] pre { font-family: monospace; font-size: 12px !important; }
    </style>
""", unsafe_allow_html=True)

# Free open data hub to sync your two phones instantly
# This unique URL acts as the invisible live database connecting you both
SYNC_URL = "https://kv.rest/v1/matrix-draft-saurabh-mukesh-2026"

ROSTERS = {
    "GT vs RR (Qualifier 2)": [
        "Shubman Gill", "Sai Sudharsan", "Jos Buttler", "Vaibhav Sooryavanshi", 
        "Yashasvi Jaiswal", "Riyan Parag", "Dhruv Jurel", "Hardik Pandya", 
        "Krunal Pandya", "Rashid Khan", "Kagiso Rabada", "Jason Holder", 
        "Mohammed Siraj", "Jofra Archer", "Ravindra Jadeja", "Rahul Tewatia",
        "Tilak Varma", "Suryakumar Yadav", "Rohit Sharma", "Donovan Ferreira", 
        "Naman Dhir", "Will Jacks", "Ryan Rickelton"
    ],
    "RCB vs TBD (Final)": [
        "Virat Kohli", "Rajat Patidar", "Glenn Maxwell", "Dinesh Karthik", 
        "Mohammed Siraj", "Yuzvendra Chahal", "Sai Sudharsan", "Venkatesh Iyer",
        "Washington Sundar", "Tim David", "Nishant Sindhu", "Devdutt Padikkal"
    ]
}

# Functions to Pull and Push data between both devices
def load_cloud_data():
    try:
        r = requests.get(SYNC_URL)
        if r.status_code == 200 and r.text:
            return json.loads(r.text)
    except:
        pass
    return {"draft_step": 1, "ms_team": [], "mn_team": [], "ms_backup": None, "mn_backup": None, "backup_first": None}

def save_cloud_data(data):
    try: requests.post(SYNC_URL, data=json.dumps(data))
    except: pass

# Always load the latest live choices from the cloud
cloud_state = load_cloud_data()

st.title("🏏 Match Matrix Engine")

mode = st.radio("Navigation:", ["Draft Room", "View Final Card"], horizontal=True)

if mode == "Draft Room":
    match_select = st.selectbox("Select Target Match:", list(ROSTERS.keys()))
    full_pool = ROSTERS[match_select]
    
    prev_winner = st.selectbox("Who won the previous match?", ["Midha & Negi", "Mukesh Sir"])
    t1_name = "Midha & Negi" if prev_winner == "Midha & Negi" else "Mukesh Sir"
    t2_name = "Mukesh Sir" if t1_name == "Midha & Negi" else "Midha & Negi"
    
    step_mapping = {
        1: {"team_key": "T1", "label": f"🟢 Round 1: {t1_name} (Pick 2)"},
        2: {"team_key": "T2", "label": f"🔵 Round 2: {t2_name} (Pick 2)"},
        3: {"team_key": "T1", "label": f"🟢 Round 3: {t1_name} (Pick 2)"},
        4: {"team_key": "T2", "label": f"🔵 Round 4: {t2_name} (Pick 2)"},
        5: {"team_key": "T1", "label": f"🟢 Round 5: {t1_name} (Pick 2)"},
        6: {"team_key": "T2", "label": f"🔵 Round 6: {t2_name} (Pick 2)"}
    }

    unavailable = cloud_state["ms_team"] + cloud_state["mn_team"]
    current_pool = [p for p in full_pool if p not in unavailable]

    if st.button("🔄 Tap to Refresh Board Choices"):
        st.rerun()

    current_step_num = cloud_state["draft_step"]

    if current_step_num <= 6:
        current_step = step_mapping[current_step_num]
        st.info(current_step["label"])
        
        selected_pair = st.multiselect("Select exactly 2 players:", current_pool, max_selections=2)
        
        if st.button(f"Confirm & Send to Partner") and len(selected_pair) == 2:
            active_team = t1_name if current_step["team_key"] == "T1" else t2_name
            if active_team == "Midha & Negi":
                cloud_state["mn_team"].extend(selected_pair)
            else:
                cloud_state["ms_team"].extend(selected_pair)
                
            cloud_state["draft_step"] += 1
            save_cloud_data(cloud_state)
            st.success("Sent! Tell your partner to refresh their page.")
            st.rerun()

    elif current_step_num == 7:
        st.warning("⚠️ Final Stage: Select your optional 7th Extra/Backup Player.")
        ms_b = st.selectbox("Mukesh Sir Backup:", [None] + full_pool)
        mn_b = st.selectbox("Midha & Negi Backup:", [None] + full_pool)
        order = st.radio("Who selected their backup first?", ["Midha & Negi", "Mukesh Sir"])
        
        if st.button("🔒 Lock & Save Full Roster"):
            cloud_state["ms_backup"] = ms_b
            cloud_state["mn_backup"] = mn_b
            cloud_state["backup_first"] = "MN" if order == "Midha & Negi" else "MS"
            cloud_state["draft_step"] += 1
            save_cloud_data(cloud_state)
            st.success("Draft fully locked across all devices!")
            st.rerun()

    st.markdown("---")
    st.write(f"**Draft Progress:** Step {current_step_num if current_step_num <= 7 else 7} / 7")
    st.markdown(f"**🔵 Mukesh Sir ({len(cloud_state['ms_team'])}/6):** {', '.join(cloud_state['ms_team'])}")
    if cloud_state["ms_backup"]: st.write(f"*(Backup: {cloud_state['ms_backup']})*")
    
    st.markdown(f"**🟢 Midha & Negi ({len(cloud_state['mn_team'])}/6):** {', '.join(cloud_state['mn_team'])}")
    if cloud_state["mn_backup"]: st.write(f"*(Backup: {cloud_state['mn_backup']})*")
    
    if st.button("🚨 Wipe Board & Start New Draft"):
        reset_data = {"draft_step": 1, "ms_team": [], "mn_team": [], "ms_backup": None, "mn_backup": None, "backup_first": None}
        save_cloud_data(reset_data)
        st.rerun()

else:
    st.error("🔒 Result Card Hidden: Payout cards can only be published once the match is finalized.")
