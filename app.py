import streamlit as st
from db import get_all_subjects, get_admin_credentials
from ui.styles import apply_pro_style


st.set_page_config(page_title="PFE Excellence", layout="wide")
apply_pro_style()

st.markdown("<h1 style='text-align:center;'>🚀 PFE EXCELLENCE HUB</h1>", unsafe_allow_html=True)

t1, t2 = st.tabs(["📚 Catalogue des Sujets", "🔐 Espace Admin"])

with t1:
    search = st.text_input("🔍 Rechercher un projet...", placeholder="Ex: Machine Learning, Web...")
    subs = get_all_subjects()
    for s in subs:
        if search.lower() in s['title'].lower():
            with st.container():
                c1, c2 = st.columns([4, 1])
                c1.subheader(s['title'])
                c1.write(s['description'])
                if c2.button("Postuler", key=f"app_{s['id']}", width="stretch"):
                    st.session_state.selected_subject_from_app = s['title']
                    st.switch_page("pages/student_form_page.py")
            st.divider()

with t2:
    # Si l'admin est déjà connecté, on lui propose d'aller directement au Dashboard
    if st.session_state.get("admin_logged_in"):
        st.success("✅ Vous êtes déjà connecté en tant qu'administrateur.")
        if st.button("Aller au Dashboard Admin", width="stretch"):
            st.switch_page("pages/admin_dashboard_page.py")
        
        if st.button("Se déconnecter", type="secondary"):
            st.session_state.admin_logged_in = False
            st.rerun()
    else:
        # Formulaire de connexion
        with st.form("login"):
            st.subheader("Connexion Administration")
            u = st.text_input("Identifiant")
            p = st.text_input("Mot de passe", type="password")
            
            if st.form_submit_button("Se connecter", width="stretch"):
                admin = get_admin_credentials(u)
                if admin and admin['password'] == p:
                    # INITIALISATION DE LA SESSION
                    st.session_state.admin_logged_in = True 
                    st.success("Accès autorisé ! Redirection...")
                    # Petite pause visuelle puis redirection
                    st.switch_page("pages/admin_dashboard_page.py")
                else:
                    st.error("❌ Identifiant ou mot de passe incorrect.")