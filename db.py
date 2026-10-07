import psycopg2
from psycopg2.extras import RealDictCursor
from config import DB_CONFIG

def get_connection():
    return psycopg2.connect(
        host=DB_CONFIG["host"], port=DB_CONFIG["port"],
        dbname=DB_CONFIG["dbname"], user=DB_CONFIG["user"],
        password=DB_CONFIG["password"], cursor_factory=RealDictCursor
    )

# --- ADMIN ---
def get_admin_credentials(username):
    conn = get_connection(); cur = conn.cursor()
    cur.execute("SELECT username, password FROM admins WHERE username = %s", (username,))
    res = cur.fetchone(); cur.close(); conn.close()
    return res

# --- SUJETS (CRUD) ---
def get_all_subjects():
    conn = get_connection(); cur = conn.cursor()
    cur.execute("SELECT id, title, description FROM subjects ORDER BY id ASC")
    rows = cur.fetchall(); cur.close(); conn.close()
    return rows

def create_subject(title, description):
    conn = get_connection(); cur = conn.cursor()
    cur.execute("INSERT INTO subjects (title, description) VALUES (%s, %s)", (title, description))
    conn.commit(); cur.close(); conn.close()

def update_subject(subject_id, title, description):
    conn = get_connection(); cur = conn.cursor()
    cur.execute("UPDATE subjects SET title=%s, description=%s WHERE id=%s", (title, description, subject_id))
    conn.commit(); cur.close(); conn.close()

def delete_subject(subject_id):
    conn = get_connection(); cur = conn.cursor()
    cur.execute("DELETE FROM subjects WHERE id = %s", (subject_id,))
    conn.commit(); cur.close(); conn.close()

def get_subject_by_id(subject_id):
    conn = get_connection(); cur = conn.cursor()
    cur.execute("SELECT * FROM subjects WHERE id = %s", (subject_id,))
    res = cur.fetchone(); cur.close(); conn.close()
    return res

# --- ÉTUDIANTS ---

def add_student(fn, ln, email, phone, sub_id, cv_fn, lm_fn, cv_txt, lm_txt, cv_blob):
    """
    Ajoute un étudiant avec son CV au format texte et au format binaire (PDF).
    """
    conn = get_connection(); cur = conn.cursor()
    sub = get_subject_by_id(sub_id)
    cur.execute("""
        INSERT INTO students (
            first_name, last_name, email, phone, subject_id, subject_title, 
            subject_description, cv_filename, motivation_filename, cv_text, 
            motivation_text, decision, cv_pdf
        ) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'pending', %s)
    """, (fn, ln, email, phone, sub_id, sub['title'], sub['description'], cv_fn, lm_fn, cv_txt, lm_txt, psycopg2.Binary(cv_blob)))
    conn.commit(); cur.close(); conn.close()

def get_students(search=""):
    conn = get_connection(); cur = conn.cursor()
    # Utilisation de requêtes paramétrées pour la sécurité
    if search:
        search_term = f"%{search.lower()}%"
        query = """
            SELECT * FROM students 
            WHERE LOWER(first_name) LIKE %s 
            OR LOWER(last_name) LIKE %s 
            OR LOWER(subject_title) LIKE %s
            ORDER BY created_at DESC
        """
        cur.execute(query, (search_term, search_term, search_term))
    else:
        cur.execute("SELECT * FROM students ORDER BY created_at DESC")
    
    rows = cur.fetchall(); cur.close(); conn.close()
    return rows

def update_student_analysis(sid, dec, reas, match, miss, raw):
    conn = get_connection(); cur = conn.cursor()
    cur.execute("""
        UPDATE students SET decision=%s, reason=%s, matching_skills=%s, missing_skills=%s, 
        raw_llm_output=%s, analyzed_at=CURRENT_TIMESTAMP WHERE id=%s
    """, (dec, reas, match, miss, raw, sid))
    conn.commit(); cur.close(); conn.close()

def delete_student(sid):
    conn = get_connection(); cur = conn.cursor()
    cur.execute("DELETE FROM students WHERE id = %s", (sid,))
    conn.commit(); cur.close(); conn.close()