import re
import unicodedata
from llama_cpp import Llama
from config import MODEL_PATH, LLM_CONFIG

# Variable globale pour stocker l'unique instance du modèle IA
_llm_instance = None

# ==========================================
# 1. Gestion du Modèle de Langage (LLM)
# ==========================================

# Initialisation et récupération de l'instance unique du modèle (Pattern Singleton)
def get_llm():
    global _llm_instance
    if _llm_instance is None:
        _llm_instance = Llama(model_path=MODEL_PATH, n_ctx=2048, verbose=False)
    return _llm_instance

# ==========================================
# 2. Algorithmes de Nettoyage Textuel
# ==========================================

# Normalisation du texte pour retirer les accents et passer en minuscules
def clean_for_match(text):
    if not text: return ""
    text = "".join(c for c in unicodedata.normalize("NFKD", str(text)) if not unicodedata.combining(c))
    text = text.lower()
    return re.sub(r"[^a-z0-9+#\s]", "", text)

# ==========================================
# 3. Moteur de Vérification Lexicale
# ==========================================

# Contrôle strict de la présence réelle d'une compétence dans le texte du CV
def phrase_supported_by_source(skill, source):
    s_clean = clean_for_match(skill)
    src_clean = clean_for_match(source)
    if not s_clean: return False
    
    # Étape 1 : Vérification d'une correspondance brute et directe
    if s_clean in src_clean: return True
    
    # Étape 2 : Vérification mot par mot pour les expressions composées
    words = [w for w in s_clean.split() if len(w) > 2]
    return all(w in src_clean for w in words) if words else False

# ==========================================
# 4. Fonction Principale d'Évaluation
# ==========================================

# Analyse complète du profil candidat face aux exigences d'un sujet PFE
def evaluate_candidate(cv_text, motivation_text, subject_title, subject_description):
    full_candidate = f"{cv_text} {motivation_text}"
    
    # Construction du prompt d'extraction structuré pour l'IA
    prompt = f"""[INST] 
    Tu es un expert en recrutement technique.
    MISSION : Extraire les compétences du candidat uniquement en fonction des exigences STRICTES du sujet.
    
    EXIGENCES DU SUJET (NE RIEN AJOUTER D'AUTRE) : {subject_description}
    CONTENU DU CV : {cv_text[:2000]}
    
    Réponds EXCLUSIVEMENT sous ce format :
    subject_requirements: skill1, skill2, ... (uniquement ceux listés dans les exigences)
    candidate_profile: skill1, skill2, ... (uniquement ceux trouvés dans le CV qui matchent les exigences)
    [/INST]"""

    try:
        # Appel du modèle LLM local pour générer les listes brutes
        llm = get_llm()
        raw = llm(prompt, max_tokens=1000, temperature=0.1)["choices"][0]["text"].strip()
        
        # Découpage et extraction des lignes de résultats retournées par l'IA
        parsed = {"reqs": [], "profile": []}
        for line in raw.splitlines():
            if "subject_requirements" in line.lower() and ":" in line:
                parsed["reqs"] = [i.strip() for i in line.split(":", 1)[1].split(",") if i.strip()]
            elif "candidate_profile" in line.lower() and ":" in line:
                parsed["profile"] = [i.strip() for i in line.split(":", 1)[1].split(",") if i.strip()]

        # Validation mathématique des compétences à l'aide des filtres de sécurité
        matching = [r for r in parsed["reqs"] if phrase_supported_by_source(r, full_candidate)]
        missing = [r for r in parsed["reqs"] if r not in matching]

        # Calcul du score d'adéquation finale en pourcentage
        score = round((len(matching) / max(len(parsed["reqs"]), 1)) * 100)

        # Envoi de la structure finale prête à être enregistrée dans PostgreSQL
        return {
            "decision": "accepted" if score >= 50 else "rejected",
            "reason": f"Score: {score}%. Basé sur l'analyse sémantique du CV.",
            "matching_skills": matching,
            "missing_skills": missing,
            "raw_output": raw
        }
    except Exception as e:
        # Gestion des erreurs de calcul avec renvoi d'un statut en attente
        return {"decision": "pending", "reason": str(e), "matching_skills": [], "missing_skills": []}