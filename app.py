import streamlit as st
import json
import random

st.set_page_config(page_title="Match Matrix Engine", page_icon="🏏", layout="centered")

st.markdown("""
    <style>
    .block-container { max-width: 380px; padding: 0.5rem; }
    div[data-testid="stMarkdownContainer"] pre { font-family: monospace; font-size: 12px !important; }
    </style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# HIGH-SPEED SERVER CORESYNC (Bypasses Outdated Singletons)
# -------------------------------------------------------------
@st.cache_resource
def get_shared_server_state():
    # This creates a shared data cache directly inside the main live server process
    return {
        "draft_step": 1, 
        "ms_team": [], 
        "mn_team": [], 
        "ms_backup": [], 
        "mn_backup": []
    }

# Connect straight to the shared server state dictionary
shared_state = get_shared_server_state()

# -------------------------------------------------------------
# MATCH DAY FIXTURE SQUADS
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

prev_winner = st.selectbox("Who won the previous match?", ["Midha & Negi", "Mukesh Sir"], key="winner_selector")
t1_name = "Midha & Negi" if prev_winner == "Midha & Negi" else "Mukesh Sir"
t2_name = "Mukesh Sir" if t1_name == "Midha & Negi" else "Midha & Negi"

if st.button("🔄 Tap to Refresh Board Choices", key="global_refresh_btn"):
    st.rerun()

current_step = shared_state["draft_step"]
ms_team = shared_state["ms_team"]
mn_team = shared_state["mn_team"]
ms_backup = shared_state["ms_backup"]
mn_backup = shared_state["mn_backup"]

full_pool = ROSTERS[selected_match]
unavailable = ms_team + mn_team + ms_backup + mn_backup
current_pool = [p for p in full_pool if p not in unavailable]

st.subheader(f"Draft Progress: Step {current_step} / 7")

# -------------------------------------------------------------
# DRAFT SEQUENCER ENGINE (2 PLAYERS EACH DISCRETE ROUNDS)
# -------------------------------------------------------------
if current_step == 1:
    st.info(f"🟢 Turn 1: {t1_name} select 2 Players")
    selected = st.multiselect("Pick 2 Players:", current_pool, max_selections=2, key="step_1_select")
    if st.button("Confirm 2 Players", key="btn_1"):
        if len(selected) == 2:
            if t1_name == "Midha & Negi": mn_team.extend(selected)
            else: ms_team.extend(selected)
            shared_state["draft_step"] = 2
            st.success("Locked! Tell Mukesh Sir to hit refresh.")
            st.rerun()
        else:
            st.warning("Please pick exactly 2 players.")

elif current_step == 2:
    st.info(f"🔵 Turn 2: {t2_name} select 2 Players")
    selected = st.multiselect("Pick 2 Players:", current_pool, max_selections=2, key="step_2_select")
    if st.button("Confirm 2 Players", key="btn_2"):
        if len(selected) == 2:
            if t2_name == "Midha & Negi": mn_team.extend(selected)
            else: ms_team.extend(selected)
            shared_state["draft_step"] = 3
            st.success("Locked! Ready for Step 3.")
            st.rerun()
        else:
            st.warning("Please pick exactly 2 players.")

elif current_step == 3:
    st.info(f"🟢 Turn 3: {t1_name} select 2 Players")
    selected = st.multiselect("Pick 2 Players:", current_pool, max_selections=2, key="step_3_select")
    if st.button("Confirm 2 Players", key="btn_3"):
        if len(selected) == 2:
            if t1_name == "Midha & Negi": mn_team.extend(selected)
            else: ms_team.extend(selected)
            shared_state["draft_step"] = 4
            st.success("Locked! Ready for Step 4.")
            st.rerun()
        else:
            st.warning("Please pick exactly 2 players.")

elif current_step == 4:
    st.info(f"🔵 Turn 4: {t2_name} select 2 Players")
    selected = st.multiselect("Pick 2 Players:", current_pool, max_selections=2, key="step_4_select")
    if st.button("Confirm 2 Players", key="btn_4"):
        if len(selected) == 2:
            if t2_name == "Midha & Negi": mn_team.extend(selected)
            else: ms_team.extend(selected)
            shared_state["draft_step"] = 5
            st.success("Locked! Ready for Step 5.")
            st.rerun()
        else:
            st.warning("Please pick exactly 2 players.")

elif current_step == 5:
    st.info(f"🟢 Turn 5: {t1_name} select your FINAL 2 Core Players")
    selected = st.multiselect("Pick 2 Players:", current_pool, max_selections=2, key="step_5_select")
    if st.button("Confirm 2 Players", key="btn_5"):
        if len(selected) == 2:
            if t1_name == "Midha & Negi": mn_team.extend(selected)
            else: ms_team.extend(selected)
            shared_state["draft_step"] = 6
            st.success("Locked! Ready for Step 6.")
            st.rerun()
        else:
            st.warning("Please pick exactly 2 players.")

elif current_step == 6:
    st.info(f"🔵 Turn 6: {t2_name} select your FINAL 2 Core Players")
    selected = st.multiselect("Pick 2 Players:", current_pool, max_selections=2, key="step_6_select")
    if st.button("Confirm 2 Players", key="btn_6"):
        if len(selected) == 2:
            if t2_name == "Midha & Negi": mn_team.extend(selected)
            else: ms_team.extend(selected)
            shared_state["draft_step"] = 7
            st.success("Core picks finished! Moving to backups.")
            st.rerun()
        else:
            st.warning("Please pick exactly 2 players.")

elif current_step == 7:
    st.info("📦 Step 7: Optional Extra Backup Selection")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**{t1_name} Backup**")
        if not mn_backup:
            b1 = st.selectbox("Select 1 Backup:", ["None"] + current_pool, key="b1_sel")
            if st.button("Confirm Team 1 Backup", key="b1_btn") and b1 != "None":
                mn_backup.append(b1)
                st.rerun()
        else:
            st.write(f"Locked: {mn_backup[0]}")

    with col2:
        st.markdown(f"**{t2_name} Backup**")
        if not ms_backup:
            b2 = st.selectbox("Select 1 Backup:", ["None"] + current_pool, key="b2_sel")
            if st.button("Confirm Team 2 Backup", key="b2_btn") and b2 != "None":
                ms_backup.append(b2)
                st.rerun()
        else:
            st.write(f"Locked: {ms_backup[0]}")

    if st.button("🏁 Finish and Lock Draft Entirely", key="final_lock_btn"):
        shared_state["draft_step"] = 8
        st.rerun()

else:
    st.balloons()
    st.success("✅ Draft Completed! Roster boards are fully locked.")

st.markdown("---")
ms_core = ", ".join(ms_team) if ms_team else "None"
mn_core = ", ".join(mn_team) if mn_team else "None"
ms_b_str = f" (Backup: {ms_backup[0]})" if ms_backup else ""
mn_b_str = f" (Backup: {mn_backup[0]})" if mn_backup else ""

st.markdown(f"**🔵 Mukesh Sir Core Squad:** {ms_core}{ms_b_str}")
st.markdown(f"**🟢 Midha & Negi Core Squad:** {mn_core}{mn_b_str}")

if st.button("🚨 Wipe Board & Start New Draft", key="reset_board_final"):
    shared_state["draft_step"] = 1
    shared_state["ms_team"].clear()
    shared_state["mn_team"].clear()
    shared_state["ms_backup"].clear()
    shared_state["mn_backup"].clear()
    st.rerun()
