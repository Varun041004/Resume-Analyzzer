import pdfplumber
from docx import Document
import re

# ---------------- SKILL DATABASE ----------------
skill_map = {
    "python": ["python"],
    "sql": ["sql"],
    "r": [" r ", " r,", " r."],
    "machine learning": ["machine learning", "ml"],
    "deep learning": ["deep learning", "dl"],
    "nlp": ["nlp", "natural language processing"],
    "data visualization": ["data visualization", "visualization"],
    "matplotlib": ["matplotlib"],
    "seaborn": ["seaborn"],
    "power bi": ["power bi", "powerbi"],
    "aws": ["aws", "amazon web services"],
    "docker": ["docker"],
    "excel": ["excel"],
    "react": ["react"],
    "angular": ["angular"]
}

# ---------- Extract Text ----------
def extract_text(file):

    if hasattr(file, "name"):
        filename = file.name.lower()

        if filename.endswith('.pdf'):
            text = ''
            with pdfplumber.open(file) as pdf:
                for page in pdf.pages:
                    t = page.extract_text()
                    if t:
                        text += t + ' '
            return text

        elif filename.endswith('.docx'):
            doc = Document(file)
            return ' '.join([para.text for para in doc.paragraphs])

        elif filename.endswith('.txt'):
            file.seek(0)
            return file.read().decode("utf-8")

    return ""


# ---------- Preprocess ----------
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)
    return text


# ---------- Extract Skills ----------
def extract_skills(text):

    text = " " + text.lower() + " "
    found_skills = set()

    for canonical, variations in skill_map.items():
        for v in variations:
            if v in text:
                found_skills.add(canonical)
                break

    return list(found_skills)
