import streamlit as st

st.set_page_config(page_title="Match Matrix", page_icon="🏏", layout="centered")

# Tight column width to match mobile screenshot size perfectly
st.markdown("""
    <style>
    .block-container { max-width: 380px; padding: 0.5rem; }
    div[data-testid="stMarkdownContainer"] pre { font-family: monospace; font-size: 12px !important; }
    </style>
""", unsafe_allow_html=True)

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

# Track session step values
if "draft_step" not in st.session_state: st.session_state.draft_step = 1
if "ms_team" not in st.session_state: st.session_state.ms_team = []
if "mn_team" not in st.session_state: st.session_state.mn_team = []
if "ms_backup" not in st.session_state: st.session_state.ms_backup = None
if "mn_backup" not in st.session_state: st.session_state.mn_backup = None
if "backup_first" not in st.session_state: st.session_state.backup_first = None

mode = st.radio("Navigation:", ["Draft Room", "View Final Card"], horizontal=True)

if mode == "Draft Room":
    match_select = st.selectbox("Select Target Match:", list(ROSTERS.keys()))
    full_pool = ROSTERS[match_select]
    
    # Define who goes first based on last match winner
    prev_winner = st.selectbox("Who won the previous match?", ["Midha & Negi", "Mukesh Sir"])
    t1_name = "Midha & Negi" if prev_winner == "Midha & Negi" else "Mukesh Sir"
    t2_name = "Mukesh Sir" if t1_name == "Midha & Negi" else "Midha & Negi"
    
    # Map steps to active picking roles
    step_mapping = {
        1: {"team_key": "T1", "label": f"🟢 Round 1: {t1_name} (Pick 2)"},
        2: {"team_key": "T2", "label": f"🔵 Round 2: {t2_name} (Pick 2)"},
        3: {"team_key": "T1", "label": f"🟢 Round 3: {t1_name} (Pick 2)"},
        4: {"team_key": "T2", "label": f"🔵 Round 4: {t2_name} (Pick 2)"},
        5: {"team_key": "T1", "label": f"🟢 Round 5: {t1_name} (Pick 2)"},
        6: {"team_key": "T2", "label": f"🔵 Round 6: {t2_name} (Pick 2)"}
    }

    unavailable = st.session_state.ms_team + st.session_state.mn_team
    current_pool = [p for p in full_pool if p not in unavailable]

    if st.session_state.draft_step <= 6:
        current_step = step_mapping[st.session_state.draft_step]
        st.info(current_step["label"])
        
        selected_pair = st.multiselect("Select exactly 2 players:", current_pool, max_selections=2)
        
        if st.button(f"Confirm Selection") and len(selected_pair) == 2:
            # Route choices to the correct structural arrays
            active_team = t1_name if current_step["team_key"] == "T1" else t2_name
            if active_team == "Midha & Negi":
                st.session_state.mn_team.extend(selected_pair)
            else:
                st.session_state.ms_team.extend(selected_pair)
                
            st.session_state.draft_step += 1
            st.rerun()

    # Step 7: The Backup Stage
    elif st.session_state.draft_step == 7:
        st.warning("⚠️ Final Stage: Select your optional 7th Extra/Backup Player.")
        ms_b = st.selectbox("Mukesh Sir Backup:", [None] + full_pool)
        mn_b = st.selectbox("Midha & Negi Backup:", [None] + full_pool)
        order = st.radio("Who selected their backup first?", ["Midha & Negi", "Mukesh Sir"])
        
        if st.button("🔒 Lock & Save Full Roster"):
            st.session_state.ms_backup = ms_b
            st.session_state.mn_backup = mn_b
            st.session_state.backup_first = "MN" if order == "Midha & Negi" else "MS"
            st.success("Draft complete! Go to 'View Final Card' tab once match finishes.")

    # Live roster overview tracker beneath the picker fields
    st.markdown("---")
    st.write(f"**Draft Progress:** Step {st.session_state.draft_step if st.session_state.draft_step <= 7 else 7} / 7")
    st.markdown(f"**🔵 Mukesh Sir ({len(st.session_state.ms_team)}/6):** {', '.join(st.session_state.ms_team)}")
    if st.session_state.ms_backup: st.write(f"*(Backup: {st.session_state.ms_backup})*")
    
    st.markdown(f"**🟢 Midha & Negi ({len(st.session_state.mn_team)}/6):** {', '.join(st.session_state.mn_team)}")
    if st.session_state.mn_backup: st.write(f"*(Backup: {st.session_state.mn_backup})*")
    
    if st.button("🔄 Reset Draft System"):
        st.session_state.draft_step = 1
        st.session_state.ms_team, st.session_state.mn_team = [], []
        st.session_state.ms_backup, st.session_state.mn_backup = None, None
        st.rerun()

else:
    # Keeps scorecards hidden during active gameplay as requested
    st.error("🔒 Result Card Hidden: Payout cards can only be published once the match is finalized.")
