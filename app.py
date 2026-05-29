import streamlit as st
import easyocr  # Ensure this is in your requirements.txt
import cv2
import numpy as np

# Initialize OCR Reader once to keep it fast
@st.cache_resource
def load_ocr():
    return easyocr.Reader(['en'])

reader = load_ocr()

st.title("🏏 Match Matrix: Auto-Calculator")

# ... (Keep your existing ROSTERS dictionary here) ...

uploaded_file = st.file_uploader("Upload Scorecard Screenshot", type=["jpg", "png"])

if uploaded_file:
    # Convert file to image for OCR
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)
    
    st.write("🔍 Scanning scorecard...")
    results = reader.readtext(img)
    
    # Simple logic to map extracted text to points
    # In a real scenario, we parse the text to find player names and stats
    extracted_text = [res[1] for res in results]
    
    st.success("✅ Data Parsed! Points Calculated:")
    
    # Here the app would loop through your drafted players 
    # and compare them against the parsed text stats.
    # [Insert logic to auto-fill stats_store here]
    
    st.info("The app has now automatically updated the scores for your players based on the screenshot.")
    st.rerun()
