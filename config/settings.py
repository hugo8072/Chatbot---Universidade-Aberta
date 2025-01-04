import os

# Flask settings
FLASK_CONFIG = {
    'debug': True,
    'host': '0.0.0.0',
    'port': 5000
}

# Path to the static folder, where static files (CSS, JavaScript, images) are located
STATIC_FOLDER = os.path.join('views', 'static')

# Path to the templates folder, where HTML files are located
TEMPLATES_FOLDER = os.path.join('views', 'templates')

# Path to the LLaMA model used in the application
MODEL_PATH = "data/llms/Hermes-3-Llama-3.1-8B.Q4_K_M.gguf"

# Dictionary with paths to FAISS databases, used for fast vector search
FAISS_PATHS = {
    '1': 'data/faiss/db_faiss_uab',
    '2': 'data/faiss/db_faiss_mpv',
    '3': 'data/faiss/db_faiss_excel'
}

# Dictionary with paths to context files, which contain relevant information for the model
CONTEXT_FILES = {
    '1': 'data/context/UAB.txt',
    '2': 'data/context/MPV.txt',
    '3': 'data/context/Dados_UCS.xlsx'
}
