DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "pfe_platform",
    "user": "postgres",
    "password": "12345",
}

MODEL_PATH = "models/Phi-3.5-mini-instruct-Q4_K_M.gguf"

LLM_CONFIG = {
    "n_ctx": 2048,
    "n_threads": 6,
    "max_tokens": 1000,
}
