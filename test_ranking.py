import pytest
from backend.resume_ranker import rank_resume


JOB = (
    "Python developer required. "
    "Skills: Python, SQL, Machine Learning, Pandas."
)


@pytest.mark.parametrize(
    "resume",
    [
        (
            "Python developer with Python, SQL, "
            "Machine Learning and Pandas experience."
        ),
        "Python developer with Python and SQL knowledge.",
        (
            "Graphic designer experienced in Photoshop, "
            "Illustrator and logo design."
        ),
        "",
    ],
    ids=[
        "good-match",
        "partial-match",
        "no-match",
        "empty-resume",
    ],
)
def test_rank_resume_returns_expected_fields(resume):
    result = rank_resume(resume, JOB)

    assert isinstance(result, dict)

    expected_fields = [
        "similarity_score",
        "skill_match_score",
        "resume_skills",
        "job_skills",
        "matched_skills",
        "missing_skills",
    ]

    for field in expected_fields:
        assert field in result


@pytest.mark.parametrize(
    "resume",
    [
        (
            "Python developer with Python, SQL, "
            "Machine Learning and Pandas experience."
        ),
        "Python developer with Python and SQL knowledge.",
        (
            "Graphic designer experienced in Photoshop, "
            "Illustrator and logo design."
        ),
        "",
    ],
    ids=[
        "good-match",
        "partial-match",
        "no-match",
        "empty-resume",
    ],
)
def test_rank_scores_are_valid_percentages(resume):
    result = rank_resume(resume, JOB)

    assert 0 <= result["similarity_score"] <= 100
    assert 0 <= result["skill_match_score"] <= 100


def test_rank_resume_returns_skill_lists():
    result = rank_resume(
        "Python developer with Python and SQL knowledge.",
        JOB,
    )

    assert isinstance(result["matched_skills"], list)
    assert isinstance(result["missing_skills"], list)
