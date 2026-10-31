
import re

SKILL_KEYWORDS = [
    "python", "java", "c++", "c#", "sql", "html", "css",
    "javascript", "typescript", "machine learning", "deep learning",
    "data analysis", "data science", "pandas", "numpy",
    "scikit-learn", "tensorflow", "pytorch", "nlp",
    "natural language processing", "computer vision",
    "excel", "power bi", "tableau", "statistics",
    "communication", "leadership", "project management",
    "problem solving", "git", "github", "aws", "azure",
    "docker", "flask", "django", "streamlit", "react",
    "node.js", "mongodb", "mysql", "postgresql", "api",
    "rest api", "data visualization", "data cleaning",
    "data structures", "algorithms", "linux", "sales",
    "marketing", "customer service", "microsoft office",
    "google workspace", "hubspot", "mailchimp", "slack",
    "accounting", "bookkeeping", "typing", "research",
    "project coordination", "time management"
]


def extract_skills(text):
    """Return recognized skills found in text."""
    if not text:
        return []

    text = text.lower()
    found = []

    for skill in SKILL_KEYWORDS:
        pattern = r"(?<!\w)" + re.escape(skill.lower()) + r"(?!\w)"
        if re.search(pattern, text):
            found.append(skill)

    return sorted(set(found))
