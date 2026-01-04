import re
import unicodedata
import numpy as np
from sentence_transformers import SentenceTransformer
from config import JOB_ROLES

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

_ROLE_EMB = None
_ROLE_TEXT_CLEAN = None


# Cache the static roles for a better performance

def build_role_cache():
    global _ROLE_EMB, _ROLE_TEXT_CLEAN
    model = load_model()

    _ROLE_TEXT_CLEAN = {
        role: clean_text(meta["requirements"])
        for role, meta in JOB_ROLES.items()
    }

    role_texts = list(_ROLE_TEXT_CLEAN.values())
    role_embs = encode(model, role_texts)

    _ROLE_EMB = {
        role: role_embs[i]
        for i, role in enumerate(_ROLE_TEXT_CLEAN.keys())
    }


# -----------------------------
# Text Cleaning (Embedding-safe)
# -----------------------------
def clean_text(text: str) -> str:
    if not isinstance(text, str):
        return ""

    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


# -----------------------------
# Load Model
# -----------------------------
_MODEL = None


def load_model():
    global _MODEL
    if _MODEL is None:
        _MODEL = SentenceTransformer(MODEL_NAME, device="cpu")
        _MODEL.eval()
    return _MODEL


# -----------------------------
# Encode Helper
# -----------------------------
def encode(model, texts):
    return model.encode(
        texts,
        batch_size=32,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=False
    )


# -----------------------------
# SINGLE ROLE MATCHING
# -----------------------------
def compute_single_role_similarity(selected_role: str, student_job_responsibilities: str):
    if selected_role not in JOB_ROLES:
        raise ValueError(f"Unknown role: {selected_role}")

    if _ROLE_EMB is None:
        build_role_cache()

    model = load_model()
    student_text = clean_text(student_job_responsibilities)

    role_embedding = _ROLE_EMB[selected_role]
    student_embedding = encode(model, [student_text])[0]

    similarity = float(np.dot(role_embedding, student_embedding))

    return {
        "role": selected_role,
        "cosine_similarity": round(similarity, 4),
        "role_weight": JOB_ROLES[selected_role]["weight"]
    }
