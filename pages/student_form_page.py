import streamlit as st
import pdfplumber, io
from db import add_student, get_all_subjects
from ui.styles import apply_pro_style

# Configuration de la page
st.set_page_config(page_title="Inscription Étudiant", layout="centered")
apply_pro_style()

st.title("📝 Formulaire d'Inscription")

# Récupération des sujets disponibles depuis la base de données
subjects = get_all_subjects()
sub_map = {s['title']: s['id'] for s in subjects}
default_idx = 0

# Pré-sélection du sujet si l'utilisateur vient de la page d'accueil
if 'selected_subject_from_app' in st.session_state:
    titles = list(sub_map.keys())
    if st.session_state.selected_subject_from_app in titles:
        default_idx = titles.index(st.session_state.selected_subject_from_app)

# Formulaire d'inscription
with st.form("student_form"):
    c1, c2 = st.columns(2)
    fn, ln = c1.text_input("Prénom"), c2.text_input("Nom")
    em, ph = st.text_input("Email"), st.text_input("Téléphone")
    
    target = st.selectbox("Sujet de PFE souhaité", list(sub_map.keys()), index=default_idx)
    
    cv = st.file_uploader("Télécharger votre CV (Format PDF uniquement)", type="pdf")
    lm = st.file_uploader("Télécharger votre Lettre de Motivation (Format PDF)", type="pdf")
    
    st.markdown("<br>", unsafe_allow_html=True) # Espacement léger
    
    # --- CENTRAGE DU BOUTON ---
    # On utilise des colonnes avec un ratio [1, 1, 1] pour isoler le milieu
    col_l, col_btn, col_r = st.columns([1, 1, 1])
    
    with col_btn:
        # use_container_width permet au bouton de remplir la colonne centrale
        submit_btn = st.form_submit_button("🚀 Postuler", use_container_width=True)
    
    # Logique de traitement après clic
    if submit_btn:
        if cv and lm and fn and ln:
            try:
                # 1. Lire le contenu binaire pour le stockage en base de données
                cv_bytes = cv.getvalue()
                
                # 2. Extraire le texte du CV pour l'analyse IA
                cv.seek(0) 
                with pdfplumber.open(io.BytesIO(cv.read())) as p:
                    cv_txt = "\n".join([page.extract_text() for page in p.pages if page.extract_text()])
                
                # 3. Extraire le texte de la lettre de motivation
                lm.seek(0)
                with pdfplumber.open(io.BytesIO(lm.read())) as p:
                    lm_txt = "\n".join([page.extract_text() for page in p.pages if page.extract_text()])
                
                # 4. Enregistrement 
                add_student(
                    fn, ln, em, ph, 
                    sub_map[target], 
                    cv.name, lm.name, 
                    cv_txt, lm_txt, 
                    cv_bytes
                )
                
                st.success("Candidature transmise avec succès ! Votre dossier est en cours d'examen.")
                st.balloons()
                
            except Exception as e:
                st.error(f"Une erreur est survenue lors du traitement des fichiers : {e}")
        else:
            st.warning("Veuillez remplir tous les champs et télécharger les documents requis.")