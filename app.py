import streamlit as st
import json
import random

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
    .squad-card-ms { background-color: #e8f0fe; padding: 12px; border-radius: 8px; border-left: 5px solid #1a73e8; margin-bottom: 10px; }
    .squad-card-mn { background-color: #e6f4ea; padding: 12px; border-radius: 8px; border-left: 5px solid #137333; margin-bottom: 10px; }
    .team-blue { color: #1a73e8; font-weight: bold; font-size: 14px; }
    .team-green { color: #137333; font-weight: bold; font-size: 14px; }
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
        "player_stats": {}  # Stores performance stats
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

full_pool = ROSTERS[selected_match]
unavailable = ms_team + mn_team + ms_backup + mn_backup
current_pool = [p for p in full_pool if p not in unavailable]

# -------------------------------------------------------------
# AUTOMATED CALCULATION ENGINE
# -------------------------------------------------------------
def calculate_player_score(player_name):
    """Standard Fantasy Matrix Points Rule Matrix"""
    if not player_name or player_name == "---":
        return 0
    p_data = stats_store.get(player_name, {"runs": 0, "wickets": 0, "catches": 0})
    return (p_data["runs"] * 1) + (p_data["wickets"] * 20) + (p_data["catches"] * 8)

# -------------------------------------------------------------
# FINAL VIEW: POINTS MATRIX CARD + HEAD-TO-HEAD MATRIX GRID (STEP 8)
# -------------------------------------------------------------
if current_step >= 8:
    st.balloons()
    
    # 1. LIVE SCORES SUMMARY MATRIX
    ms_total = sum(calculate_player_score(p) for p in ms_team) + sum(calculate_player_score(p) for p in ms_backup)
    mn_total = sum(calculate_player_score(p) for p in mn_team) + sum(calculate_player_score(p) for p in mn_backup)
    
    st.markdown(f"""
    <div class="matrix-card">
        <h3 style="margin:0; font-size:18px;">📊 LIVE MATCH MATRIX CARD</h3>
        <p style="margin:4px 0 10px 0; font-size:11px; opacity:0.8;">{selected_match}</p>
        <div style="display:flex; justify-content:space-around; align-items:center; margin-top:5px;">
            <div>
                <div style="font-size:12px; color:#6ba4ff;">MUKESH SIR</div>
                <div style="font-size:22px; font-weight:bold;">{ms_total} pts</div>
            </div>
            <div style="font-size:20px; font-weight:bold; color:#e74c3c;">VS</div>
            <div>
                <div style="font-size:12px; color:#5eff8b;">MIDHA & NEGI</div>
                <div style="font-size:22px; font-weight:bold;">{mn_total} pts</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if ms_total > mn_total:
        st.info("🏆 Leaderboard Standing: Mukesh Sir is Winning!")
    elif mn_total > ms_total:
        st.success("🏆 Leaderboard Standing: Midha & Negi are Winning!")
    else:
        st.warning("⚖️ Leaderboard Standing: Scores are dead tied!")

    # 2. PERFORMANCE INPUT CONSOLE (DURING LIVE MATCH)
    st.markdown("---")
    st.markdown("### 🛠️ Score Calculator Entry")
    all_drafted_players = sorted(list(set(ms_team + mn_team + ms_backup + mn_backup)))
    target_player = st.selectbox("Select Player to Input Stats:", all_drafted_players)
    
    if target_player not in stats_store:
        stats_store[target_player] = {"runs": 0, "wickets": 0, "catches": 0}
        
    col_in1, col_in2, col_in3 = st.columns(3)
    with col_in1:
        new_runs = st.number_input("Runs:", min_value=0, value=stats_store[target_player]["runs"], step=1)
    with col_in2:
        new_wicks = st.number_input("Wickets:", min_value=0, value=stats_store[target_player]["wickets"], step=1)
    with col_in3:
        new_catches = st.number_input("Catches:", min_value=0, value=stats_store[target_player]["catches"], step=1)
        
    if st.button("💾 Update Scores & Recalculate Card", use_container_width=True):
        stats_store[target_player] = {"runs": new_runs, "wickets": new_wicks, "catches": new_catches}
        st.success(f"Scores synchronized for {target_player}!")
        st.rerun()

    # 3. THE 3x3 VISUAL HEAD-TO-HEAD COMPONENT ROWS
    st.markdown("---")
    st.markdown("### 📋 Head-to-Head Player Score Matrix")
    
    loops = max(len(ms_team), len(mn_team))
    for i in range(loops):
        p_ms = ms_team[i] if i < len(ms_team) else "---"
        p_mn = mn_team[i] if i < len(mn_team) else "---"
        
        score_ms = calculate_player_score(p_ms)
        score_mn = calculate_player_score(p_mn)
        
        slot_num = (i // 2) + 1
        sub_slot = (i % 2) + 1
        
        st.markdown(f"""
        <div class="grid-container">
            <div class="team-blue-card" style="text-align: left;">{p_ms}<br><span style='font-size:11px; opacity:0.7;'>({score_ms} pts)</span></div>
            <div class="vs-badge">PAIR {slot_num}.{sub_slot}</div>
            <div class="team-green-card" style="text-align: right;">{p_mn}<br><span style='font-size:11px; opacity:0.7;'>({score_mn} pts)</span></div>
        </div>
        """, unsafe_allow_html=True)
        
    # Extra Backups row display
    if ms_backup or mn_backup:
        b_ms = ms_backup[0] if ms_backup else "---"
        b_mn = mn_backup[0] if mn_backup else "---"
        st.markdown(f"""
        <div class="grid-container" style="background: rgba(231, 76, 60, 0.15); border: 1px dashed #e74c3c;">
            <div class="team-blue-card" style="text-align: left; font-style: italic;">{b_ms}<br><span style='font-size:11px;'>({calculate_player_score(b_ms)} pts)</span></div>
            <div class="vs-badge" style="background:#7f8c8d;">EXTRA</div>
            <div class="team-green-card" style="text-align: right; font-style: italic;">{b_mn}<br><span style='font-size:11px;'>({calculate_player_score(b_mn)} pts)</span></div>
        </div>
        """, unsafe_allow_html=True)

# -------------------------------------------------------------
# ACTIVE DRAFT PHASE (STEPS 1-7)
# -------------------------------------------------------------
else:
    st.subheader(f"Draft Progress: Step {current_step} / 7")

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
            st.markdown(f"**{t1_name} Backup**")
            if not mn_backup:
                b1 = st.selectbox("Select 1 Backup:", ["None"] + current_pool, key="b1_sel")
                if st.button("Confirm Team 1 Backup", key="b1_btn") and b1 != "None":
                    mn_backup.append(b1)
                    st.rerun()
            else: st.write(f"Locked: {mn_backup[0]}")

        with col2:
            st.markdown(f"**{t2_name} Backup**")
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
ms_core = ", ".join(ms_team) if ms_team else "None"
mn_core = ", ".join(mn_team) if mn_team else "None"
st.markdown(f"**🔵 Mukesh Sir Live List:** {ms_core}")
st.markdown(f"**🟢 Midha & Negi Live List:** {mn_core}")

if st.button("🚨 Wipe Board & Start New Draft", key="reset_board_final", use_container_width=True):
    shared_state["draft_step"] = 1
    shared_state["ms_team"].clear()
    shared_state["mn_team"].clear()
    shared_state["ms_backup"].clear()
    shared_state["mn_backup"].clear()
    shared_state["player_stats"].clear()
    st.rerun()
