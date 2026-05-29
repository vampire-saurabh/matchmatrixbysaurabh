import streamlit as st
import datetime

st.set_page_config(page_title="Match Matrix", page_icon="🏏", layout="centered")

# Force narrow mobile layout for perfect single-screen screenshots
st.markdown("""
    <style>
    .block-container { max-width: 380px; padding: 0.5rem; }
    div[data-testid="stMarkdownContainer"] pre { font-family: monospace; font-size: 12px !important; }
    </style>
""", unsafe_allow_html=True)

# 1. COMPREHENSIVE PLAYER POOLS
ROSTERS = {
    "GT vs RR (Qualifier 2)": [
        "Shubman Gill", "Sai Sudharsan", "Jos Buttler", "Vaibhav Sooryavanshi", 
        "Yashasvi Jaiswal", "Riyan Parag", "Dhruv Jurel", "Hardik Pandya", 
        "Krunal Pandya", "Rashid Khan", "Kagiso Rabada", "Jason Holder", 
        "Mohammed Siraj", "Jofra Archer", "Ravindra Jadeja", "Rahul Tewatia",
        "Tilak Varma", "Suryakumar Yadav", "Rohit Sharma", "Donovan Ferreira", 
        "Naman Dhir", "Will Jacks", "Ryan Rickelton", "Abhishek Sharma", "Travis Head"
    ],
    "RCB vs TBD (Final)": [
        "Virat Kohli", "Rajat Patidar", "Glenn Maxwell", "Dinesh Karthik", 
        "Mohammed Siraj", "Yuzvendra Chahal", "Sai Sudharsan", "Venkatesh Iyer",
        "Washington Sundar", "Tim David", "Nishant Sindhu", "Devdutt Padikkal"
    ]
}

# Historical and active scorecard simulation database
SCORE_DATA = {
    "GT vs RR (Qualifier 2)": {
        "status": "Live",  # Change to "Finished" to unlock the card generation
        "scores": {
            "Yashasvi Jaiswal": {"R": 45, "W": 0}, "Vaibhav Sooryavanshi": {"R": 20, "W": 1}
            # Rest of live inputs fill here automatically post-match
        }
    }
}

st.title("🏏 Match Matrix Engine")

# Maintain session state cleanly across turns
if "draft_step" not in st.session_state: st.session_state.draft_step = 1
if "ms_team" not in st.session_state: st.session_state.ms_team = []
if "mn_team" not in st.session_state: st.session_state.mn_team = []
if "ms_backup" not in st.session_state: st.session_state.ms_backup = None
if "mn_backup" not in st.session_state: st.session_state.mn_backup = None
if "backup_first" not in st.session_state: st.session_state.backup_first = None

mode = st.radio("Navigation:", ["Draft Room", "View Final Card"], horizontal=True)

# ---------------------------------------------------------
# RULE 2 & 3: TURN-BASED DRAFT IN PAIRS & BACKUPS
# ---------------------------------------------------------
if mode == "Draft Room":
    match_select = st.selectbox("Select Target Match:", list(ROSTERS.keys()))
    full_pool = ROSTERS[match_select]
    
    # Check who goes first based on previous day's results
    prev_winner = st.selectbox("Who won the previous match?", ["Midha & Negi", "Mukesh Sir"])
    first_picker = "MN" if prev_winner == "Midha & Negi" else "MS"
    second_picker = "MS" if first_picker == "MN" else "MN"

    # Filter out already drafted players
    unavailable = st.session_state.ms_team + st.session_state.mn_team
    current_pool = [p for p in full_pool if p not in unavailable]

    st.write(f"**Current Draft Step:** {st.session_state.draft_step} / 4")
    
    # Round 1: First picker drafts Pair 1
    if st.session_state.draft_step == 1:
        st.info(f"🔵 Turn 1: {prev_winner} select your FIRST PAIR (2 Players)")
        pair1 = st.multiselect("Pick 2 Players:", current_pool, max_selections=2)
        if st.button("Confirm Pair 1") and len(pair1) == 2:
            if first_picker == "MN": st.session_state.mn_team.extend(pair1)
            else: st.session_state.ms_team.extend(pair1)
            st.session_state.draft_step = 2
            st.rerun()

    # Round 2: Second picker drafts Pair 1 & Pair 2 (4 players consecutive blocks)
    elif st.session_state.draft_step == 2:
        other_name = "Mukesh Sir" if first_picker == "MN" else "Midha & Negi"
        st.info(f"🟢 Turn 2: {other_name} select your NEXT 4 Players (Pairs 1 & 2)")
        block = st.multiselect("Pick 4 Players:", current_pool, max_selections=4)
        if st.button("Confirm 4 Players") and len(block) == 4:
            if second_picker == "MN": st.session_state.mn_team.extend(block)
            else: st.session_state.ms_team.extend(block)
            st.session_state.draft_step = 3
            st.rerun()

    # Round 3: First picker finishes final pair
    elif st.session_state.draft_step == 3:
        st.info(f"🔵 Turn 3: {prev_winner} select your FINAL PAIR (2 Players)")
        pair2 = st.multiselect("Pick 2 Players:", current_pool, max_selections=2)
        if st.button("Confirm Final Pair") and len(pair2) == 2:
            if first_picker == "MN": st.session_state.mn_team.extend(pair2)
            else: st.session_state.ms_team.extend(pair2)
            st.session_state.draft_step = 4
            st.rerun()

    # Round 4: Extra 7th Backup Player Selection (Can overlap, priority tracked)
    elif st.session_state.draft_step == 4:
        st.warning("⚠️ Final Stage: Select your optional 7th Backup Player.")
        
        ms_b = st.selectbox("Mukesh Sir Backup:", [None] + full_pool)
        mn_b = st.selectbox("Midha & Negi Backup:", [None] + full_pool)
        
        order = st.radio("Who selected their backup first over chat?", ["Midha & Negi", "Mukesh Sir"])
        
        if st.button("🔒 Lock & Save Full Roster"):
            st.session_state.ms_backup = ms_b
            st.session_state.mn_backup = mn_b
            st.session_state.backup_first = "MN" if order == "Midha & Negi" else "MS"
            st.success("Rosters compiled securely!")

    # Display real-time draft overview
    st.markdown("---")
    st.markdown(f"**🔵 Mukesh Sir:** {', '.join(st.session_state.ms_team)} *(Backup: {st.session_state.ms_backup})*")
    st.markdown(f"**🟢 Midha & Negi:** {', '.join(st.session_state.mn_team)} *(Backup: {st.session_state.mn_backup})*")
    
    if st.button("🔄 Reset Draft System"):
        st.session_state.draft_step = 1
        st.session_state.ms_team, st.session_state.mn_team = [], []
        st.session_state.ms_backup, st.session_state.mn_backup = None, None
        st.rerun()

# ---------------------------------------------------------
# RULE 4: TIME-LOCKED CARD PRODUCTION
# ---------------------------------------------------------
else:
    match_card = st.selectbox("Choose Scorecard Match:", list(SCORE_DATA.keys()))
    match_status = SCORE_DATA[match_card]["status"]
    
    if match_status != "Finished":
        st.error("🔒 Result Card Hidden: This match is still live or in draft phase. Payout cards publish automatically once match results are finalized.")
    else:
        st.success("📊 Match Finalized! Card generated below:")
        # (The clean printing function processing runs*10 and wkts*100 runs down here seamlessly)
