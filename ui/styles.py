import streamlit as st

def apply_pro_style():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;500&display=swap');
    
    .stApp {
        background: linear-gradient(rgba(10, 10, 20, 0.85), rgba(10, 10, 20, 0.85)), 
                    url("https://images.unsplash.com/photo-1550751827-4bd374c3f58b?q=80&w=2070");
        background-size: cover; background-attachment: fixed;
        font-family: 'Inter', sans-serif;
    }
    
    /* Titres futuristes */
    h1, h2 { font-family: 'Orbitron', sans-serif; color: #00d4ff !important; text-transform: uppercase; letter-spacing: 2px; }
    
    /* Cartes Glassmorphism */
    div[data-testid="stExpander"], .stForm, div.stButton > button:first-child {
        background: rgba(255, 255, 255, 0.03) !important;
        backdrop-filter: blur(15px);
        border-radius: 12px !important;
        border: 1px solid rgba(0, 212, 255, 0.2) !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }
    
    /* Boutons bleus néon */
    .stButton>button {
        background: linear-gradient(45deg, #00d4ff, #0056b3) !important;
        color: white !important; font-weight: bold !important;
        border: none !important; transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 0 15px #00d4ff ; }
    
    /* Statuts */
    .status-accepted { color: #00ff88; font-weight: bold; background: rgba(0, 255, 136, 0.1); padding: 5px 10px; border-radius: 5px; }
    .status-pending { color: #ffcc00; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)