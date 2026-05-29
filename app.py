import streamlit as st
import json
import requests
import random

st.set_page_config(page_title="Match Matrix", page_icon="🏏", layout="centered")

# Set mobile-friendly constraint widths
st.markdown("""
    <style>
    .block-container { max-width: 380px; padding: 0.5rem; }
    div[data-testid="stMarkdownContainer"] pre { font-family: monospace; font-size: 12px !important; }
    </style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# HARDENED CLOUD SYNCHRONIZATION DATA LAYER
# -------------------------------------------------------------
# Shared endpoint matrix
SYNC_BASE_URL = "https://kv.rest/v1/matrix-2026-"

def get_match_slug(match_name):
    return match_name.lower().replace(" ", "").replace("(", "").replace(")", "").replace("-", "")

def load_live_state(match_name):
    slug = get_match_slug(match_name)
    # Aggressive multi-try loop to counter volatile mobile packet drops
    for _ in range(3):
        try:
            # Appending a randomized integer completely busts local ISP/browser caching layers
            cb_url = f"{SYNC_BASE_URL}{slug}?cb={random.randint(1, 100000)}"
            r = requests.get(cb_url, timeout=3)
            if r.status_code == 200 and r.text:
                return json.loads(r.text)
        except:
            continue
    # Secure structural fallback schema if network requests fail
    return {"draft_step": 1, "ms_team": [], "mn_team": [], "ms_backup": None, "mn_backup": None}

def save_live_state(match_name, state_dict):
    slug = get_match_slug(match_name)
    try:
        requests.post(SYNC_BASE_URL + slug, data=json.dumps(state_dict), timeout=4)
    except:
        pass

# -------------------------------------------------------------
# PLAYOFFS SCHEDULE & VERIFIED ROSTERS
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

# Explicit tracking keys bind UI components strictly to session lifecycles
selected_match = st.selectbox(
    "🎯 Choose Active Schedule Room:", 
    list(ROSTERS.keys()), 
    key="match_selector"
)  

# Pull state tied directly to this specific dropdown match room key
shared_state = load_live_state(selected_match)

prev_winner = st.selectbox("Who won the previous match?", ["Midha & Negi", "Mukesh Sir"], key="winner_selector")
t1_name = "Midha & Negi" if prev_winner == "Midha & Negi" else "Mukesh Sir"
t2_name = "Mukesh Sir" if t1_name == "Midha & Negi" else "Midha & Negi"

if st.button("🔄 Tap to Refresh Board Choices"):
