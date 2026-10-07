import base64
import warnings
from pathlib import Path
import re

import docx
import pdfplumber
import streamlit as st
import torch  
from llama_cpp import Llama
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

warnings.filterwarnings("ignore", category=FutureWarning)

# ==========================================
# 1. Sécurité et Contrôle d'Accès
# ==========================================
if "admin_logged_in" not in st.session_state or not st.session_state["admin_logged_in"]:
    st.error("🚫 Accès refusé. Veuillez vous connecter en tant qu'administrateur.")
    if st.button("Aller à la page de connexion"):
        st.switch_page("app.py")
    st.stop()

# Initialisation de l'état de session pour stocker les résultats d'analyse
if "ats_results" not in st.session_state:
    st.session_state["ats_results"] = None

# ==========================================
# 2. Configuration des Chemins
# ==========================================
BASE_DIR = Path(__file__).resolve().parent.parent
IMAGES_DIR = BASE_DIR / "images"
MODELS_DIR = BASE_DIR / "models"
BACKGROUND_PATH = IMAGES_DIR / "background.png"
MODEL_PATH = MODELS_DIR / "Phi-3.5-mini-instruct-Q4_K_M.gguf"

# ==========================================
# 3. Optimisation et Chargement des Modèles
# ==========================================
@st.cache_resource
def load_llm():
    return Llama(
        model_path=str(MODEL_PATH),
        n_ctx=2048,
        n_threads=6,
        n_batch=512,
        use_mmap=True,
        verbose=False
    )

@st.cache_resource
def load_embedding_model():
    # Force l'utilisation du CPU de manière optimisée pour l'inférence
    model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")
    model.eval() 
    return model

GLOBAL_LLM = load_llm()
GLOBAL_EMBEDDING = load_embedding_model()

# ==========================================
# 4. Utilitaires de Style
# ==========================================
@st.cache_data
def get_bg_base64(path: Path) -> str:
    if not path.exists(): return ""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def load_ats_style():
    bg64 = get_bg_base64(BACKGROUND_PATH)
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(10,15,35,0.85), rgba(10,15,35,0.85)),
                        url("data:image/png;base64,{bg64}") no-repeat center center fixed;
            background-size: cover;
        }}
        .skill-tag {{
            display: inline-block;
            padding: 6px 14px;
            border-radius: 4px;
            margin: 5px;
            font-family: 'Courier New', monospace;
            font-size: 13px;
            font-weight: bold;
            color: white;
            text-transform: uppercase;
        }}
        .matched-tag {{ background-color: #0d9488; border-bottom: 2px solid #065f46; }}
        .missing-tag {{ background-color: #be123c; border-bottom: 2px solid #881337; }}
        .ai-box {{
            background-color: rgba(255,255,255,0.05);
            padding: 20px;
            border-left: 4px solid #3b82f6;
            white-space: pre-wrap;
            color: #ffffff;
            line-height: 1.7;
        }}
        .section-header {{
            font-size: 16px;
            font-weight: bold;
            margin-top: 20px;
            color: #60a5fa;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# ==========================================
# 5. Algorithmes de Traitement
# ==========================================
def extract_text(file):
    text = ""
    if file.name.lower().endswith(".pdf"):
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
    elif file.name.lower().endswith(".docx"):
        doc = docx.Document(file)
        for para in doc.paragraphs:
            text += para.text + "\n"
    return text.lower().strip()

def extract_job_phrases(job_text):
    raw_lines = re.split(r'[\n,•·\-\*]', job_text)
    phrases = set()
    for line in raw_lines:
        clean = line.strip().lower()
        if len(clean) > 2 and not clean.startswith(('requis', 'profil', 'poste')):
            phrases.add(clean)
    return list(phrases)

def get_fit_info(score):
    if score >= 75: return "🔥 HIGH FIT", "#22c55e"
    elif score >= 50: return "⚡ MEDIUM FIT", "#eab308"
    return "❌ LOW FIT", "#ef4444"

# ==========================================
# 6. Moteur Principal et Interface
# ==========================================
def render_admin_ats_page():
    load_ats_style()

    st.markdown('<div style="text-align:center;font-size: 32px; font-weight: 900; color: white;">AI RECRUITMENT ATS</div>', unsafe_allow_html=True)
    st.markdown('<div style="text-align:center; color: #60a5fa; margin-bottom: 30px;">Analyseur Hybride Lexical & Sémantique (Phi-3.5)</div>', unsafe_allow_html=True)

    job_description = st.text_area("Saisir la description du poste", height=150)
    uploaded_files = st.file_uploader("Télécharger les CVs", type=["pdf", "docx"], accept_multiple_files=True)
    min_score = st.slider("Filtrer par score minimum", 0, 100, 0)

    # Lancement de l'analyse
    if st.button("LANCER L'ANALYSE COMPLETE", use_container_width=True):
        if not job_description or not uploaded_files:
            st.error("⚠️ Veuillez fournir une description de poste et au moins un CV.")
        else:
            results_storage = []
            progress_bar = st.progress(0)
            
            with torch.no_grad():
                job_embedding = GLOBAL_EMBEDDING.encode(job_description, convert_to_numpy=True)
                job_phrases = extract_job_phrases(job_description)
                
                for idx, file in enumerate(uploaded_files):
                    cv_text = extract_text(file)
                    
                    # Matching lexical
                    matched = list(set([p for p in job_phrases if p in cv_text]))
                    missing = list(set(job_phrases) - set(matched))
                    lexical = (len(matched) / len(job_phrases) * 100) if job_phrases else 50.0
                    
                    # Matching Sémantique
                    cv_emb = GLOBAL_EMBEDDING.encode(cv_text, convert_to_numpy=True)
                    semantic = float(cosine_similarity([job_embedding], [cv_emb])[0][0]) * 100
                    semantic = max(0.0, min(100.0, semantic)) # Sécurité bornes
                    
                    # Calcul Score Hybride
                    hybrid_score = round((0.4 * lexical) + (0.6 * semantic), 2)

                    if hybrid_score >= min_score:
                        # Génération du Rapport LLM
                        prompt = (
                            "<s><|system|>\n"
                            "Tu es un Expert en Recrutement Technique. Rédige un rapport d'évaluation clair en français brut.\n"
                            "CONSIGNE : PAS de Markdown (pas d'étoiles, pas de dièses).\n"
                            "<|end|>\n"
                            f"<|user|>\nPoste :\n{job_description[:400]}\n\nCV :\n{cv_text[:1200]}\n<|end|>\n"
                            "<|assistant|>\nRAPPORT D'EVALUATION TECHNIQUE\n\n"
                        )
                        response = GLOBAL_LLM(prompt, max_tokens=1000, temperature=0.1, stop=["<|end|>"])
                        report = response["choices"][0]["text"].strip()
                        
                        for char in ["*", "#", "_", "`", ">"]:
                            report = report.replace(char, "")

                        results_storage.append({
                            "name": file.name,
                            "score": hybrid_score,
                            "lexical": round(lexical, 2),
                            "semantic": round(semantic, 2),
                            "matched": matched,
                            "missing": missing,
                            "report": report
                        })
                    
                    progress_bar.progress((idx + 1) / len(uploaded_files))
            
            #Sauvegarde dans le session_state
            st.session_state["ats_results"] = results_storage
            st.rerun()

    #Rendu basé sur le session_state 
    if st.session_state["ats_results"] is not None:
        results = st.session_state["ats_results"]
        if results:
            st.write(f"📊 Candidats analysés : {len(results)}")
            
            for res in sorted(results, key=lambda x: x['score'], reverse=True):
                label, color = get_fit_info(res['score'])
                
                with st.expander(f"📁 {res['name']} — Score : {res['score']}%"):
                    st.markdown(f'<div style="font-size:18px; font-weight:800; color:{color};">{label}</div>', unsafe_allow_html=True)
                    
                    c1, c2 = st.columns(2)
                    c1.markdown(f"<small>MATCH LEXICAL</small><br><b>{res['lexical']}%</b>", unsafe_allow_html=True)
                    c2.markdown(f"<small>MATCH SÉMANTIQUE</small><br><b>{res['semantic']}%</b>", unsafe_allow_html=True)

                    st.markdown('<div class="section-header">COMPÉTENCES VALIDÉES</div>', unsafe_allow_html=True)
                    if res['matched']:
                        tags = "".join([f'<span class="skill-tag matched-tag">{m}</span>' for m in res['matched']])
                        st.markdown(tags, unsafe_allow_html=True)
                    else:
                        st.caption("Aucune correspondance lexicale directe.")

                    st.markdown('<div class="section-header">POINTS MANQUANTS À VÉRIFIER</div>', unsafe_allow_html=True)
                    if res['missing']:
                        tags = "".join([f'<span class="skill-tag missing-tag">{m}</span>' for m in res['missing']])
                        st.markdown(tags, unsafe_allow_html=True)
                    else:
                        st.caption("Le profil couvre tous les mots-clés.")

                    st.markdown('<div class="section-header">RAPPORT DE SYNTHÈSE IA</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="ai-box">{res["report"]}</div>', unsafe_allow_html=True)
        else:
            st.warning("Aucun candidat ne correspond aux critères de score actuels.")

if __name__ == "__main__":
    render_admin_ats_page()