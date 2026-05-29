import streamlit as st

st.set_page_config(page_title="IPL Fantasy", page_icon="🏏", layout="centered")

# Force narrow layout for perfect mobile screenshots
st.markdown("""
    <style>
    .block-container { max-width: 380px; padding: 0.5rem; }
    div[data-testid="stMarkdownContainer"] pre { font-family: monospace; font-size: 12px !important; }
    </style>
""", unsafe_allow_html=True)

UPCOMING_MATCHES = {
    "IPL 2026 - QUALIFIER 2: GT vs RR": ["Shubman Gill", "Sai Sudharsan", "Jos Buttler", "Vaibhav Sooryavanshi", "Yashasvi Jaiswal", "Riyan Parag", "Dhruv Jurel", "Hardik Pandya"],
    "IPL 2026 - FINAL: RCB vs TBD": ["Virat Kohli", "Rajat Patidar", "Glenn Maxwell", "Mohammed Siraj"]
}

SCORECARD_DB = {
    "IPL 2026 - ELIMINATOR: SRH vs RR": {
        "MS": ["Ishan Kishan", "Heinrich Klaasen", "Dhruv Jurel", "Riyan Parag", "Donovan Ferreira", "Dasun Shanaka"],
        "MN": ["Vaibhav Sooryavanshi", "Abhishek Sharma", "Travis Head", "Yashasvi Jaiswal", "Nitish Kumar Reddy", "Pat Cummins"],
        "scores": {
            "Ishan Kishan": {"R": 33, "W": 0}, "Heinrich Klaasen": {"R": 18, "W": 0}, "Dhruv Jurel": {"R": 50, "W": 0},
            "Riyan Parag": {"R": 26, "W": 0}, "Donovan Ferreira": {"R": 12, "W": 0}, "Dasun Shanaka": {"R": 5, "W": 0},
            "Vaibhav Sooryavanshi": {"R": 97, "W": 0}, "Abhishek Sharma": {"R": 0, "W": 0}, "Travis Head": {"R": 17, "W": 0},
            "Yashasvi Jaiswal": {"R": 29, "W": 0}, "Nitish Kumar Reddy": {"R": 38, "W": 1}, "Pat Cummins": {"R": 1, "W": 0}
        }
    }
}

st.title("🏏 MI & MN Draft")

mode = st.radio("Mode:", ["Draft Picks", "Get Card"], horizontal=True)

if mode == "Draft Picks":
    match = st.selectbox("Match:", list(UPCOMING_MATCHES.keys()))
    pool = UPCOMING_MATCHES[match]
    
    ms_selected = st.multiselect("🔵 Mukesh Sir (White)", pool, max_selections=6)
    mn_selected = st.multiselect("🟢 Midha & Negi (Green)", [p for p in pool if p not in ms_selected], max_selections=6)
    
    if st.button("🔒 Save Draft"):
        st.session_state.ms = ms_selected
        st.session_state.mn = mn_selected
        st.success("Draft Saved!")

else:
    match_card = st.selectbox("Match Card:", list(SCORECARD_DB.keys()))
    data = SCORECARD_DB[match_card]
    
    ms_team = st.session_state.get("ms", data["MS"])
    mn_team = st.session_state.get("mn", data["MN"])
    scores = data["scores"]
    
    def process(team):
        lines, total = [], 0
        for p in team:
            s = scores.get(p, {"R": 0, "W": 0})
            r, w = s["R"], s["W"]
            inr = (r * 10) + (w * 100)
            total += inr
            p_short = p if len(p) <= 14 else p[:12] + ".."
            lines.append(f"{p_short:<14} {r:>2} {w:>1}  ₹{inr:>4}")
        return lines, total

    ms_lines, ms_tot = process(ms_team)
    mn_lines, mn_tot = process(mn_team)
    win = f"🏆 WINNER: MIDHA & NEGI +₹{mn_tot-ms_tot:,}" if mn_tot > ms_tot else f"🏆 WINNER: MUKESH SIR +₹{ms_tot-mn_tot:,}"

    card = f"""=================================
🏏 {match_card.split(':')[0].strip()}
=================================
🔵 MUKESH SIR
---------------------------------
Player Name        R  W   INR
---------------------------------
"""
    for l in ms_lines: card += l + "\n"
    card += f"---------------------------------\n👉 TOTAL:              ₹{ms_tot:,}\n\n🟢 MIDHA & NEGI\n---------------------------------\nPlayer Name        R  W   INR\n---------------------------------\n"
    for l in mn_lines: card += l + "\n"
    card += f"---------------------------------\n👉 TOTAL:              ₹{mn_tot:,}\n=================================\n{win}\n================================="

    st.text_area("Screenshot Copy", value=card, height=450)
