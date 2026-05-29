import streamlit as st

st.set_page_config(page_title="Match Matrix Engine", page_icon="🏏", layout="centered")

st.markdown("""
    <style>
    .block-container { max-width: 380px; padding: 0.5rem; }
    .matrix-card {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.15);
        margin-bottom: 15px;
        text-align: center;
    }
    .score-breakdown-card {
        background-color: #f8f9fa;
        border: 1px solid #e2e8f0;
        padding: 12px;
        border-radius: 8px;
        margin-bottom: 10px;
    }
    .grid-container {
        display: grid;
        grid-template-columns: 1fr auto 1fr;
        gap: 10px;
        align-items: center;
        margin-top: 8px;
        background: rgba(255, 255, 255, 0.1);
        padding: 10px;
        border-radius: 8px;
    }
    .team-blue-card { color: #6ba4ff; font-weight: bold; font-size: 14px; }
    .team-green-card { color: #5eff8b; font-weight: bold; font-size: 14px; }
    .vs-badge { background: #e74c3c; padding: 2px 6px; border-radius: 4px; font-size: 11px; font-weight: bold; color: white; }
    </style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# HIGH-SPEED SERVER CORESYNC
# -------------------------------------------------------------
@st.cache_resource
def get_shared_server_state():
    return {
        "draft_step": 1, 
        "ms_team": [], 
        "mn_team": [], 
        "ms_backup": [], 
        "mn_backup": [],
        "player_stats": {},
        "custom_players": []  # Tracks extra players added on the fly
    }

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

selected_match = st.selectbox("🎯 Active Schedule Room:", list(ROSTERS.keys()), key="match_selector")
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
stats_store = shared_state["player_stats"]

# Combine the fixed fixture lists with any custom added players
full_pool = ROSTERS[selected_match] + shared_state["custom_players"]
unavailable = ms_team + mn_team + ms_backup + mn_backup
current_pool = [p for p in full_pool if p not in unavailable]

# -------------------------------------------------------------
# AUTOMATED CALCULATION ENGINE
# -------------------------------------------------------------
def get_breakdown(player_name):
    if not player_name or player_name == "---":
        return {"runs": 0, "wickets": 0, "catches": 0, "total": 0}
    d = stats_store.get(player_name, {"runs": 0, "wickets": 0, "catches": 0})
    total = (d["runs"] * 1) + (d["wickets"] * 20) + (d["catches"] * 8)
    return {"runs": d["runs"], "wickets": d["wickets"], "catches": d["catches"], "total": total}

# -------------------------------------------------------------
# POST-MATCH RESULTS & SCORECARDS (STEP 8)
# -------------------------------------------------------------
if current_step >= 8:
    st.balloons()
    
    ms_total = sum(get_breakdown(p)["total"] for p in ms_team) + sum(get_breakdown(p)["total"] for p in ms_backup)
    mn_total = sum(get_breakdown(p)["total"] for p in mn_team) + sum(get_breakdown(p)["total"] for p in mn_backup)
    
    # Live Total Score Match Card
    st.markdown(f"""
    <div class="matrix-card">
        <h3 style="margin:0; font-size:16px;">🏆 LIVE FANTASY SCORECARD</h3>
        <div style="display:flex; justify-content:space-around; align-items:center; margin-top:10px;">
            <div>
                <div style="font-size:11px; color:#6ba4ff;">MUKESH SIR</div>
                <div style="font-size:22px; font-weight:bold;">{ms_total} pts</div>
            </div>
            <div style="font-size:18px; font-weight:bold; color:#e74c3c;">VS</div>
            <div>
                <div style="font-size:11px; color:#5eff8b;">MIDHA & NEGI</div>
                <div style="font-size:22px; font-weight:bold;">{mn_total} pts</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Performance Editor Console
    st.markdown("### 🛠️ Live Performance Entry")
    all_drafted = sorted(list(set(ms_team + mn_team + ms_backup + mn_backup)))
    target_p = st.selectbox("Select Player to Update Live Stats:", all_drafted)
    
    if target_p not in stats_store:
        stats_store[target_p] = {"runs": 0, "wickets": 0, "catches": 0}
        
    c1, c2, c3 = st.columns(3)
    with c1: r_in = st.number_input("Runs:", min_value=0, value=stats_store[target_p]["runs"], step=1, key="r_i")
    with c2: w_in = st.number_input("Wickets:", min_value=0, value=stats_store[target_p]["wickets"], step=1, key="w_i")
    with c3: cat_in = st.number_input("Catches:", min_value=0, value=stats_store[target_p]["catches"], step=1, key="c_i")
    
    if st.button("💾 Save & Calculate Live Card", use_container_width=True):
        stats_store[target_p] = {"runs": r_in, "wickets": w_in, "catches": cat_in}
        st.rerun()

    # The Fantasy Calculations Card Option Breakdown
    st.markdown("---")
    st.markdown("### 📋 Detailed Fantasy Points Cards")
    
    tab1, tab2 = st.tabs(["🔵 Mukesh Sir Points", "🟢 Midha & Negi Points"])
    
    with tab1:
        for p in ms_team + ms_backup:
            b = get_breakdown(p)
            st.markdown(f"""
            <div class="score-breakdown-card">
                <b style="color:#1a73e8;">{p}</b> — <b>{b['total']} Pts Total</b><br>
                <span style="font-size:12px; color:#555;">🏏 {b['runs']} Runs | 🎯 {b['wickets']} Wickets | 🤲 {b['catches']} Catches</span>
            </div>
            """, unsafe_allow_html=True)
            
    with tab2:
        for p in mn_team + mn_backup:
            b = get_breakdown(p)
            st.markdown(f"""
            <div class="score-breakdown-card">
                <b style="color:#137333;">{p}</b> — <b>{b['total']} Pts Total</b><br>
                <span style="font-size:12px; color:#555;">🏏 {b['runs']} Runs | 🎯 {b['wickets']} Wickets | 🤲 {b['catches']} Catches</span>
            </div>
            """, unsafe_allow_html=True)

    # 3x3 Grid Visual Card Layout
    st.markdown("---")
    st.markdown("### 📊 Head-to-Head Visual Card")
    loops = max(len(ms_team), len(mn_team))
    for i in range(loops):
        p_ms = ms_team[i] if i < len(ms_team) else "---"
        p_mn = mn_team[i] if i < len(mn_team) else "---"
        st.markdown(f"""
        <div class="grid-container" style="background:#222;">
            <div class="team-blue-card" style="text-align: left;">{p_ms}<br><span style='font-size:11px; opacity:0.7;'>({get_breakdown(p_ms)['total']} pts)</span></div>
            <div class="vs-badge">PAIR {(i//2)+1}.{(i%2)+1}</div>
            <div class="team-green-card" style="text-align: right;">{p_mn}<br><span style='font-size:11px; opacity:0.7;'>({get_breakdown(p_mn)['total']} pts)</span></div>
        </div>
        """, unsafe_allow_html=True)

# -------------------------------------------------------------
# ACTIVE DRAFT PHASE WITH CUSTOM PLAYER BYPASS
# -------------------------------------------------------------
else:
    st.subheader(f"Draft Progress: Step {current_step} / 7")
    
    # 🚨 NEW EMERGENCY OVERRIDE OPTION FOR MISSING PLAYERS
    with st.expander("➕ Can't find a player? Add them manually here"):
        new_player_name = st.text_input("Type Missing Player Name:")
        if st.button("Inject Player into Live Roster Pool"):
            if new_player_name.strip() and new_player_name not in shared_state["custom_players"]:
                shared_state["custom_players"].append(new_player_name.strip())
                st.success(f"Added {new_player_name}! You can now search them in the select box above.")
                st.rerun()

    if current_step == 1:
        st.info(f"🟢 Turn 1: {t1_name} select 2 Players")
        selected = st.multiselect("Pick 2 Players:", current_pool, max_selections=2, key="step_1_select")
        if st.button("Confirm 2 Players", key="btn_1"):
            if len(selected) == 2:
                if t1_name == "Midha & Negi": mn_team.extend(selected)
                else: ms_team.extend(selected)
                shared_state["draft_step"] = 2
                st.rerun()
            else: st.warning("Please pick exactly 2 players.")

    elif current_step == 2:
        st.info(f"🔵 Turn 2: {t2_name} select 2 Players")
        selected = st.multiselect("Pick 2 Players:", current_pool, max_selections=2, key="step_2_select")
        if st.button("Confirm 2 Players", key="btn_2"):
            if len(selected) == 2:
                if t2_name == "Midha & Negi": mn_team.extend(selected)
                else: ms_team.extend(selected)
                shared_state["draft_step"] = 3
                st.rerun()
            else: st.warning("Please pick exactly 2 players.")

    elif current_step == 3:
        st.info(f"🟢 Turn 3: {t1_name} select 2 Players")
        selected = st.multiselect("Pick 2 Players:", current_pool, max_selections=2, key="step_3_select")
        if st.button("Confirm 2 Players", key="btn_3"):
            if len(selected) == 2:
                if t1_name == "Midha & Negi": mn_team.extend(selected)
                else: ms_team.extend(selected)
                shared_state["draft_step"] = 4
                st.rerun()
            else: st.warning("Please pick exactly 2 players.")

    elif current_step == 4:
        st.info(f"🔵 Turn 4: {t2_name} select 2 Players")
        selected = st.multiselect("Pick 2 Players:", current_pool, max_selections=2, key="step_4_select")
        if st.button("Confirm 2 Players", key="btn_4"):
            if len(selected) == 2:
                if t2_name == "Midha & Negi": mn_team.extend(selected)
                else: ms_team.extend(selected)
                shared_state["draft_step"] = 5
                st.rerun()
            else: st.warning("Please pick exactly 2 players.")

    elif current_step == 5:
        st.info(f"🟢 Turn 5: {t1_name} select your FINAL 2 Core Players")
        selected = st.multiselect("Pick 2 Players:", current_pool, max_selections=2, key="step_5_select")
        if st.button("Confirm 2 Players", key="btn_5"):
            if len(selected) == 2:
                if t1_name == "Midha & Negi": mn_team.extend(selected)
                else: ms_team.extend(selected)
                shared_state["draft_step"] = 6
                st.rerun()
            else: st.warning("Please pick exactly 2 players.")

    elif current_step == 6:
        st.info(f"🔵 Turn 6: {t2_name} select your FINAL 2 Core Players")
        selected = st.multiselect("Pick 2 Players:", current_pool, max_selections=2, key="step_6_select")
        if st.button("Confirm 2 Players", key="btn_6"):
            if len(selected) == 2:
                if t2_name == "Midha & Negi": mn_team.extend(selected)
                else: ms_team.extend(selected)
                shared_state["draft_step"] = 7
                st.rerun()
            else: st.warning("Please pick exactly 2 players.")

    elif current_step == 7:
        st.info("📦 Step 7: Optional Extra Backup Selection")
        col1, col2 = st.columns(2)
        with col1:
            if not mn_backup:
                b1 = st.selectbox("Select 1 Backup:", ["None"] + current_pool, key="b1_sel")
                if st.button("Confirm Team 1 Backup", key="b1_btn") and b1 != "None":
                    mn_backup.append(b1)
                    st.rerun()
            else: st.write(f"Locked: {mn_backup[0]}")
        with col2:
            if not ms_backup:
                b2 = st.selectbox("Select 1 Backup:", ["None"] + current_pool, key="b2_sel")
                if st.button("Confirm Team 2 Backup", key="b2_btn") and b2 != "None":
                    ms_backup.append(b2)
                    st.rerun()
            else: st.write(f"Locked: {ms_backup[0]}")

        st.markdown("---")
        if st.button("🏁 Finish and Lock Draft Entirely", key="final_lock_btn", use_container_width=True):
            shared_state["draft_step"] = 8
            st.rerun()

st.markdown("---")
if st.button("🚨 Wipe Board & Start New Draft", key="reset_board_final", use_container_width=True):
    shared_state["draft_step"] = 1
    shared_state["ms_team"].clear()
    shared_state["mn_team"].clear()
    shared_state["ms_backup"].clear()
    shared_state["mn_backup"].clear()
    shared_state["player_stats"].clear()
    shared_state["custom_players"].clear()
    st.rerun()
