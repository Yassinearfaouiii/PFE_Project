import streamlit as st
import base64
import re
import plotly.express as px
import pandas as pd
from db import *
from llm_service import evaluate_candidate
from ui.styles import apply_pro_style

# ==========================================
# 1. Configuration et Sécurité de la Page
# ==========================================

# Définition du titre de la page et de l'affichage large
st.set_page_config(page_title="PFE Hub | Admin Dashboard", layout="wide")

# Application du style graphique global
apply_pro_style()

# Vérification des droits d'accès administrateur
if "admin_logged_in" not in st.session_state or not st.session_state["admin_logged_in"]:
    st.error("🚫 Accès refusé. Veuillez vous connecter.")
    if st.button("Aller à la page de connexion"): 
        st.switch_page("app.py")
    st.stop()

# ==========================================
# 2. Styles CSS Personnalisés (Glassmorphism)
# ==========================================

st.markdown("""
<style>
    .block-container { padding-top: 1.5rem; }
    
    /* Style des cartes de métriques (KPI) */
    [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(74, 144, 226, 0.2);
        border-radius: 15px;
        padding: 20px !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        text-align: center;
    }
    [data-testid="stMetricLabel"] p {
        color: #4A90E2 !important;
        font-size: 0.85rem !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 1.8px !important;
        text-shadow: 0 0 10px rgba(74, 144, 226, 0.4);
    }
    [data-testid="stMetricValue"] div {
        color: #ffffff !important;
        font-size: 2.2rem !important;
        font-weight: 800 !important;
    }

    /* Badges pour les statuts de décision */
    .fixed-status {
        font-weight: bold;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 0.75rem;
        border: 1px solid;
        text-transform: uppercase;
        letter-spacing: 1px;
        display: inline-block;
        width: 100px;
        text-align: center;
    }
    .stat-accepted { color: #00ff88; border-color: #00ff88; background: rgba(0, 255, 136, 0.1); }
    .stat-rejected { color: #ff4b4b; border-color: #ff4b4b; background: rgba(255, 75, 75, 0.1); }
    .stat-pending { color: #ffcc00; border-color: #ffcc00; background: rgba(255, 204, 0, 0.1); }

    /* Barres d'informations et expanders */
    .stExpander {
        background: rgba(15, 23, 42, 0.5) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 12px !important;
    }
    .glass-info-bar {
        background: linear-gradient(90deg, rgba(74, 144, 226, 0.12), transparent);
        padding: 12px 20px;
        border-radius: 10px;
        border-left: 4px solid #4A90E2;
        display: flex;
        gap: 40px;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. Fonctions Utilitaires
# ==========================================

# Bouton HTML pour télécharger le fichier CV en PDF
def create_dl_btn(pdf_data, name):
    if pdf_data:
        try:
            b64 = base64.b64encode(pdf_data).decode()
            return f'''<a href="data:application/pdf;base64,{b64}" download="{name}" style="text-decoration:none;">
                       <div style="background:#4A90E2; color:white; padding:10px; border-radius:8px; text-align:center; font-weight:bold; margin-bottom:10px;">📥 Télécharger CV</div></a>'''
        except: 
            return ""
    return ""

# Extraction du score numérique depuis le texte explicatif de l'IA
def extract_score_from_reason(reason_text):
    if not reason_text:
        return 0
    match = re.search(r"Score\s*:\s*(\d+)", str(reason_text), re.IGNORECASE)
    if match:
        return int(match.group(1))
    return 0

# ==========================================
# 4. En-tête et Statistiques Globales
# ==========================================

# Titre principal du Hub d'administration
st.markdown("<h1 style='text-align: center; color: #4A90E2; letter-spacing: 3px; font-weight: 900; margin-bottom: 30px;'>🛡️ ADMINISTRATION HUB</h1>", unsafe_allow_html=True)

# Récupération de la liste de tous les étudiants et des sujets
all_studs = get_students("")
all_subs = get_all_subjects()
total = len(all_studs)
acc = len([s for s in all_studs if s.get('decision', '').lower() == "accepted"])
pen = len([s for s in all_studs if s.get('decision', '').lower() == "pending"])

# Affichage des métriques générales sous forme de colonnes
m1, m2, m3, m4 = st.columns(4)
with m1: st.metric("👥 Candidats", total)
with m2: st.metric("📂 Projets PFE", len(all_subs))
with m3: st.metric(label="✅ ACCEPTÉS", value=acc)
with m4: st.metric("⏳ En attente", pen)

st.markdown("<br>", unsafe_allow_html=True)

# Création des trois onglets principaux du tableau de bord
tab_cand, tab_subj, tab_dash = st.tabs(["🚀 GESTION DES CANDIDATURES", "📑 CATALOGUE DES SUJETS", "📊 ADMIN DASHBOARD"])

# ==========================================
# 5. Onglet 1 : Gestion des Candidatures
# ==========================================
with tab_cand:
    # Barre de recherche et filtre par statut du dossier
    f1, f2 = st.columns([2, 1])
    query = f1.text_input("🔍 Rechercher un profil...", placeholder="Nom, spécialité, projet...")
    status_f = f2.selectbox("État du dossier", ["Tous", "Pending", "Accepted", "Rejected"])
    
    # Filtrage des candidats selon les critères sélectionnés
    candidates = [c for c in get_students(query) if status_f == "Tous" or c.get('decision', '').lower() == status_f.lower()]

    # Affichage des cartes expanders pour chaque candidat trouvé
    for c in candidates:
        with st.container():
            st.write("") 
            decision_status = c.get('decision', 'PENDING').lower()
            
            # Bloc déroulant contenant l'identité de l'étudiant et son sujet
            with st.expander(f"👤 {c['first_name'].upper()} {c['last_name'].upper()} | 🎯 {c['subject_title']}"):
                
                # Barre d'informations de contact (Email, Téléphone, Statut)
                st.markdown(f'''<div class="glass-info-bar">
                    <span>📧 <b>Email:</b> {c['email']}</span>
                    <span>📞 <b>Téléphone:</b> {c['phone']}</span>
                    <span>Statut: <div class="fixed-status stat-{decision_status}">{c.get('decision', 'PENDING')}</div></span>
                </div>''', unsafe_allow_html=True)
                
                col_left, col_right = st.columns([2.5, 1])
                
                # Zone d'affichage du texte du CV et des retours de l'IA
                with col_left:
                    st.markdown("#### 📄 Analyse IA & CV")
                    st.text_area("Données brutes du CV", c['cv_text'], height=130, key=f"cv_{c['id']}")
                    if c.get('decision', '').lower() != "pending":
                        st.divider()
                        res1, res2 = st.columns(2)
                        res1.success(f"**Points forts:**\n{c.get('matching_skills')}")
                        res2.warning(f"**Manquants:**\n{c.get('missing_skills')}")
                        st.info(f"💡 **Synthèse décisionnelle:** {c.get('reason')}")
                
                # Zone de boutons d'action (Téléchargement, Évaluation IA, Suppression)
                with col_right:
                    st.markdown("#### 🛠️ Décision")
                    st.markdown(create_dl_btn(c.get('cv_pdf'), f"CV_{c['last_name']}.pdf"), unsafe_allow_html=True)
                    if st.button("🧠 Lancer l'Analyse IA", key=f"ai_{c['id']}", use_container_width=True):
                        with st.spinner("L'IA analyse le profil..."):
                            res = evaluate_candidate(c['cv_text'], c['motivation_text'], c['subject_title'], c['subject_description'])
                            update_student_analysis(c['id'], res['decision'], res['reason'], res['matching_skills'], res['missing_skills'], res['raw_output'])
                        st.rerun()
                    if st.button("🗑️ Supprimer Dossier", key=f"del_{c['id']}", use_container_width=True):
                        delete_student(c['id'])
                        st.rerun()

# ==========================================
# 6. Onglet 2 : Catalogue des Sujets (CRUD)
# ==========================================
with tab_subj:
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Fenêtre popover contenant le formulaire d'ajout d'un sujet PFE
    with st.popover("➕ Publier un nouveau sujet PFE", use_container_width=True):
        with st.form("new_subject_form"):
            t = st.text_input("Titre du projet")
            d = st.text_area("Description détaillée (Technos, objectifs...)")
            if st.form_submit_button("Ajouter au catalogue", use_container_width=True):
                create_subject(t, d)
                st.rerun()

    # Liste d'affichage des sujets PFE existants avec options d'édition/suppression
    for s in get_all_subjects():
        with st.container():
            sc1, sc2, sc3 = st.columns([4, 0.6, 0.6])
            sc1.markdown(f"**{s['title']}**\n\n{s['description']}")
            
            # Formulaire popover d'édition des données du sujet
            with sc2:
                with st.popover("📝 Modifier"):
                    with st.form(f"edit_form_{s['id']}"):
                        new_t = st.text_input("Titre", value=s['title'])
                        new_d = st.text_area("Description", value=s['description'])
                        if st.form_submit_button("Sauvegarder"):
                            update_subject(s['id'], new_t, new_d)
                            st.rerun()
            
            # Bouton de suppression directe du sujet PFE
            with sc3:
                if st.button("🗑️", key=f"del_sub_{s['id']}"):
                    delete_subject(s['id'])
                    st.rerun()
            st.divider()

# ================================
# 7. Onglet 3 : Student Dashboard 
# ================================
with tab_dash:
    st.markdown("<br>", unsafe_allow_html=True)

    # Filtres du dashboard : Sélection du sujet PFE et saisie d'une compétence
    d_col1, d_col2 = st.columns([1.5, 2])

    with d_col1:
        subjects_list = ["Tous les sujets"] + [s['title'] for s in all_subs]
        selected_subject = st.selectbox("🎯 Filtrer par Sujet sélectionné", subjects_list, key="dash_sub_filter")

    with d_col2:
        search_skill = st.text_input("💡 Chercher une compétence (Skill)", placeholder="Ex: Python, React, SQL...", key="dash_skill_search")

    # Initialisation des listes pour la récolte des données analytiques
    students_data_for_table = []
    all_extracted_skills = []
    decisions_list = []

    # Parcours des étudiants pour extraire et nettoyer les compétences trouvées
    for s in all_studs:
        match_subject = (selected_subject == "Tous les sujets" or s.get('subject_title') == selected_subject)

        skills_raw = s.get('matching_skills')
        student_skills_list = []

        if skills_raw:
            lines = skills_raw if isinstance(skills_raw, list) else str(skills_raw).split('\n')
            for line in lines:
                cleaned = str(line).replace('-', '').replace('*', '').replace('•', '').strip()
                if cleaned and cleaned[0].isdigit() and "." in cleaned:
                    cleaned = cleaned.split(".", 1)[1].strip()
                if cleaned and len(cleaned) < 30:
                    student_skills_list.append(cleaned.upper())

        skills_txt = " ".join(student_skills_list)
        match_skill = True
        if search_skill.strip():
            match_skill = search_skill.lower() in skills_txt.lower()

        # Enregistrement des données filtrées pour l'affichage graphique et tableau
        if match_subject and match_skill:
            decisions_list.append(s.get('decision', 'PENDING').upper())
            all_extracted_skills.extend(student_skills_list)
            score = extract_score_from_reason(s.get('reason'))

            students_data_for_table.append({
                "Rang": 0,
                "Score IA (%)": score,
                "Étudiant": f"{s.get('first_name','').upper()} {s.get('last_name','').upper()}",
                "Email": s.get('email',''),
                "Téléphone": s.get('phone',''),
                "Sujet": s.get('subject_title',''),
                "Décision": s.get('decision','PENDING').upper()
            })

    # Tri des lignes du tableau de classement par ordre de score décroissant
    students_data_for_table = sorted(students_data_for_table, key=lambda x: x["Score IA (%)"], reverse=True)
    for i, row in enumerate(students_data_for_table):
        row["Rang"] = i + 1

    # Affichage des trois compteurs de métriques filtrés (KPIs)
    dash_m1, dash_m2, dash_m3 = st.columns(3)
    with dash_m1: st.metric("👥 Étudiants Filtrés", len(students_data_for_table))
    with dash_m2: st.metric("🧠 Total de Skills Détectés", len(all_extracted_skills))
    with dash_m3: st.metric("📊 Compétences Uniques", len(set(all_extracted_skills)))

    st.markdown("---")

    # Génération et construction des graphiques Plotly s'il y a des données disponibles
    if students_data_for_table:
        g_col1, g_col2 = st.columns(2)

        # Graphique à barres horizontales (Top 10 des compétences)
        with g_col1:
            st.markdown("#### 🛠️ Top des Compétences les plus trouvées")
            if all_extracted_skills:
                df_skills = pd.DataFrame(all_extracted_skills, columns=["Compétence"])
                skill_counts = df_skills["Compétence"].value_counts().reset_index()
                skill_counts.columns = ["Compétence", "Nombre"]

                fig_bar = px.bar(skill_counts.head(10), x="Nombre", y="Compétence", orientation="h", text_auto=True)
                fig_bar.update_layout(height=350)
                st.plotly_chart(fig_bar, use_container_width=True)

        # Graphique en anneau (Répartition des décisions des recruteurs)
        with g_col2:
            st.markdown("#### 📈 Répartition des Décisions")
            if decisions_list:
                df_dec = pd.DataFrame(decisions_list, columns=["Statut"])
                decision_counts = df_dec["Statut"].value_counts().reset_index()
                decision_counts.columns = ["Statut", "Nombre"]

                fig_pie = px.pie(decision_counts, values="Nombre", names="Statut", hole=0.4)
                fig_pie.update_layout(height=350)
                st.plotly_chart(fig_pie, use_container_width=True)

        st.markdown("---")

        # Affichage du tableau de données final (Classement général des profils)
        st.markdown("### 🏆 Classement Général des Étudiants")
        df_ranking = pd.DataFrame(students_data_for_table)
        st.dataframe(df_ranking, use_container_width=True, hide_index=True)

    else:
        st.info("ℹ️ Aucun étudiant ne correspond aux critères de recherche actuels.")