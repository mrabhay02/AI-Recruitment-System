
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_similarity(resume_text, job_description):
    """
    Calculate TF-IDF cosine similarity as a percentage.
    This is text similarity, not a probability of being hired.
    """
    if not resume_text or not job_description:
        return 0.0

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        max_features=10000
    )

    try:
        vectors = vectorizer.fit_transform(
            [resume_text, job_description]
        )
        score = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
        return round(float(score) * 100, 2)

    except ValueError:
        return 0.0
