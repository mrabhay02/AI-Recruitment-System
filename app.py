import html
import re

import pandas as pd
import plotly.express as px
import streamlit as st

from backend.pdf_reader import extract_text_from_pdf
from backend.resume_ranker import rank_resume


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="SmartHire AI | Talent Intelligence",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

:root {
    --bg: #080d18;
    --panel: #101827;
    --border: #293951;
    --text: #f8fafc;
    --muted: #9aaac0;
    --blue: #60a5fa;
    --purple: #a78bfa;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background:
        radial-gradient(ellipse at 85% 0%, #1a2c50 0%, transparent 36%),
        radial-gradient(ellipse at 0% 45%, #101a31 0%, transparent 40%),
        var(--bg);
    color: var(--text);
}

.block-container {
    max-width: 1250px;
    padding-top: 2rem;
    padding-bottom: 2.5rem;
}

h1, h2, h3 {
    font-family: 'Space Grotesk', sans-serif;
    color: var(--text);
}

.hero {
    padding: 38px;
    margin-bottom: 30px;
    border: 1px solid #2b3d5b;
    border-radius: 24px;
    background: linear-gradient(125deg, #162540, #0c1424);
    position: relative;
    overflow: hidden;
}

.hero-label {
    color: var(--blue);
    font-size: 11px;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    font-weight: 700;
}

.hero h1 {
    font-size: clamp(30px, 4vw, 48px);
    line-height: 1.12;
    margin: 16px 0;
}

.hero p {
    color: #b3c0d3;
    font-size: 15px;
    line-height: 1.8;
    max-width: 720px;
}

.section-heading {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 24px;
    font-weight: 700;
    margin: 30px 0 6px;
}

.section-subtitle {
    color: var(--muted);
    font-size: 13px;
    margin-bottom: 20px;
}

.panel {
    background: linear-gradient(145deg, #121e31, #0d1524);
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 23px;
    margin-bottom: 16px;
}

.panel p {
    color: #a8b6ca;
    line-height: 1.7;
}

/* HOME WORKSPACE CARDS */

.workspace-card {
    min-height: 245px;
    background: linear-gradient(145deg, #172641, #0d1524);
    border: 1px solid #304766;
    border-radius: 22px;
    padding: 25px;
    margin-bottom: 12px;
    transition: transform .2s ease, border-color .2s ease;
}

.workspace-card:hover {
    transform: translateY(-4px);
    border-color: #60a5fa;
}

.workspace-icon {
    width: 58px;
    height: 58px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 16px;
    background: linear-gradient(135deg, #1d4ed8, #6d28d9);
    border: 1px solid #587ee8;
    font-size: 28px;
    margin-bottom: 20px;
}

.workspace-tag {
    display: inline-block;
    font-size: 10px;
    letter-spacing: 1px;
    font-weight: 700;
    color: #a5c9ff;
    background: #172b47;
    border: 1px solid #304565;
    border-radius: 30px;
    padding: 5px 10px;
    margin-bottom: 10px;
}

.workspace-card h3 {
    font-size: 22px;
    margin: 4px 0 10px;
}

.workspace-card p {
    color: #a8b6ca;
    font-size: 13px;
    line-height: 1.75;
}

/* METRICS */

.metric {
    background: linear-gradient(145deg, #142139, #0e1727);
    border: 1px solid #2b3e5b;
    border-radius: 17px;
    padding: 21px;
    margin: 10px 0;
}

.metric-label {
    color: var(--muted);
    font-size: 12px;
    letter-spacing: .5px;
}

.metric-value {
    color: var(--text);
    font-family: 'Space Grotesk', sans-serif;
    font-size: 29px;
    font-weight: 700;
    margin-top: 8px;
}

/* ANALYSIS SCORE CARDS */

.result-card {
    min-height: 155px;
    padding: 23px;
    margin: 10px 0 18px;
    border-radius: 20px;
    background: linear-gradient(135deg, #172945, #101827);
    border: 1px solid #365277;
}

.result-card.purple {
    background: linear-gradient(135deg, #282044, #101827);
    border-color: #554477;
}

.result-card-label {
    color: #a8bad2;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
}

.result-card-value {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 39px;
    font-weight: 700;
    color: #f8fafc;
    margin-top: 14px;
}

.result-card-note {
    font-size: 12px;
    color: #9fb3cf;
    margin-top: 9px;
}

/* SKILL PANELS */

.skill-panel {
    background: linear-gradient(145deg, #121e31, #0c1422);
    border: 1px solid #30435f;
    border-radius: 18px;
    padding: 20px;
    margin: 8px 0 16px;
}

.skill-panel.matched {
    border-color: #245c56;
    background: linear-gradient(145deg, #102b2c, #0c1724);
}

.skill-panel.missing {
    border-color: #69414b;
    background: linear-gradient(145deg, #2b1a27, #0c1422);
}

.skill-panel-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 17px;
    font-weight: 700;
    margin-bottom: 15px;
    color: #f8fafc;
}

.skill-pill {
    display: inline-block;
    padding: 7px 11px;
    margin: 4px 5px 4px 0;
    border-radius: 30px;
    font-size: 12px;
    font-weight: 600;
    overflow-wrap: anywhere;
}

.skill-pill.matched {
    color: #a7f3d0;
    background: #123b35;
    border: 1px solid #28675b;
}

.skill-pill.missing {
    color: #fecdd3;
    background: #42232d;
    border: 1px solid #79404d;
}

.skill-pill.neutral {
    color: #bfdbfe;
    background: #172b47;
    border: 1px solid #304565;
}

/* CANDIDATE CARDS */

.candidate-score-card {
    background: linear-gradient(145deg, #142239, #0c1423);
    border: 1px solid #304565;
    border-radius: 20px;
    padding: 22px;
    margin: 10px 0 18px;
}

.candidate-label {
    color: #91a6c2;
    font-size: 10px;
    letter-spacing: 1.4px;
    font-weight: 700;
    text-transform: uppercase;
    margin-bottom: 12px;
}

.candidate-name {
    color: #f8fafc;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 18px;
    font-weight: 700;
    overflow-wrap: anywhere;
    margin-bottom: 18px;
}

.candidate-stat {
    background: #111c2d;
    border: 1px solid #293951;
    border-radius: 12px;
    padding: 12px;
    text-align: center;
    margin-top: 12px;
}

.candidate-stat-value {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 25px;
    font-weight: 700;
    color: #f8fafc;
}

.candidate-stat-label {
    font-size: 10px;
    color: #9aaac0;
    margin-top: 4px;
}

/* COMPARISON SUMMARY */

.comparison-summary {
    background: linear-gradient(135deg, #142c3b, #101827);
    border: 1px solid #31616a;
    border-radius: 18px;
    padding: 21px;
    margin: 14px 0 20px;
}

.comparison-summary-title {
    color: #a7f3d0;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 17px;
    font-weight: 700;
    margin-bottom: 7px;
}

.comparison-summary-text {
    color: #c5d5e5;
    font-size: 13px;
    line-height: 1.7;
}

/* BUTTONS */

div.stButton > button,
div.stDownloadButton > button {
    border-radius: 11px;
    min-height: 44px;
    font-weight: 600;
    transition: all .2s ease;
}

div.stButton > button:hover,
div.stDownloadButton > button:hover {
    border-color: var(--blue);
    color: #ffffff;
}

/* SIDEBAR AND INPUTS */

[data-testid="stSidebar"] {
    background: #0a1120;
    border-right: 1px solid #25354e;
}

[data-testid="stSidebar"] p {
    color: #bac6d8;
}

[data-testid="stFileUploader"] {
    background: #101827;
    border: 1px dashed #3b506e;
    border-radius: 14px;
    padding: 12px;
}

div[data-testid="stTextArea"] textarea {
    background: #0d1727;
    color: var(--text);
    border: 1px solid #344763;
    border-radius: 12px;
}

/* TEAM */

.team-section {
    margin-top: 48px;
    padding-top: 34px;
    border-top: 1px solid #293951;
}

.team-title {
    text-align: center;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 30px;
    font-weight: 700;
    color: #f8fafc;
    margin-bottom: 8px;
}

.team-subtitle {
    text-align: center;
    color: #9aaac0;
    font-size: 14px;
    margin-bottom: 28px;
}

.team-card {
    background: linear-gradient(145deg, #142239, #0c1423);
    border: 1px solid #304565;
    border-radius: 20px;
    padding: 27px 12px;
    text-align: center;
    margin-bottom: 14px;
}

.team-avatar {
    width: 66px;
    height: 66px;
    margin: 0 auto 16px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #2563eb, #7c3aed);
    border: 2px solid #647ce8;
    color: white;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 25px;
    font-weight: 700;
}

.team-name {
    color: #f8fafc;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 16px;
    font-weight: 700;
    margin: 10px 0;
    overflow-wrap: anywhere;
}

.team-role {
    display: inline-block;
    color: #a5c9ff;
    background: #172b47;
    border: 1px solid #304565;
    border-radius: 30px;
    padding: 6px 11px;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: .7px;
}

.team-footer {
    text-align: center;
    color: #72839c;
    font-size: 12px;
    margin-top: 14px;
}

hr {
    border-color: #293951;
}
</style>
""", unsafe_allow_html=True)


# =========================================================
# CONSTANTS
# =========================================================

PAGES = [
    "Overview",
    "Resume Analyzer",
    "Candidate Comparison",
    "About Project",
    "How It Works",
]

TEAM_MEMBERS = [
    ("Karan Dev Singh", "MEMBER 01", "K"),
    ("Abhay Kumar Gupta", "MEMBER 02", "A"),
    ("Ankur Singh", "MEMBER 03", "A"),
]


# =========================================================
# SESSION STATE NAVIGATION
# =========================================================

if "workspace_page" not in st.session_state:
    st.session_state["workspace_page"] = "Overview"

if "next_page" in st.session_state:
    pending_page = st.session_state.pop("next_page")
    if pending_page in PAGES:
        st.session_state["workspace_page"] = pending_page

if "hiring_pipeline" not in st.session_state:
    st.session_state["hiring_pipeline"] = []


def go_to_page(page):
    st.session_state["next_page"] = page


# =========================================================
# COMMON FUNCTIONS
# =========================================================

def section_heading(title, subtitle=None):
    st.markdown(
        f'<div class="section-heading">{html.escape(title)}</div>',
        unsafe_allow_html=True,
    )

    if subtitle:
        st.markdown(
            f'<div class="section-subtitle">{html.escape(subtitle)}</div>',
            unsafe_allow_html=True,
        )


def metric_card(label, value):
    st.markdown(
        f"""
        <div class="metric">
            <div class="metric-label">{html.escape(str(label))}</div>
            <div class="metric-value">{html.escape(str(value))}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def safe_percentage(value):
    try:
        value = float(value)
    except (TypeError, ValueError):
        return 0.0

    if pd.isna(value):
        return 0.0

    return max(0.0, min(100.0, value))


def make_pie_chart(labels, values, title):
    chart_df = pd.DataFrame({
        "Category": labels,
        "Value": values,
    })

    chart_df = chart_df[chart_df["Value"] > 0]

    if chart_df.empty:
        st.info("There is no data available for this chart.")
        return

    fig = px.pie(
        chart_df,
        names="Category",
        values="Value",
        title=title,
        hole=0.58,
    )

    fig.update_layout(
        paper_bgcolor="#101827",
        plot_bgcolor="#101827",
        font_color="#f1f5f9",
        title_font_color="#f1f5f9",
        legend_title_text="",
        margin=dict(t=60, b=15, l=10, r=10),
    )

    fig.update_traces(
        textposition="inside",
        textinfo="label+percent",
    )

    st.plotly_chart(fig, use_container_width=True)


def get_pdf_text(uploaded_file):
    if uploaded_file is None:
        return ""

    try:
        uploaded_file.seek(0)
        extracted_text = extract_text_from_pdf(uploaded_file)
        return extracted_text.strip() if extracted_text else ""

    except Exception as error:
        st.error(f"Could not read PDF: {error}")
        return ""


def get_result(resume_text, job_description):
    try:
        result = rank_resume(resume_text, job_description)

        if not isinstance(result, dict):
            st.error(
                "Unexpected result from the resume-ranking function."
            )
            return None

        return result

    except Exception as error:
        st.error(f"Resume analysis failed: {error}")
        return None


def build_pdf_report(lines):
    """
    Create a small, dependency-free PDF report.
    Uses standard Helvetica and converts unsupported characters safely.
    """
    import textwrap

    prepared_lines = []
    for line in lines:
        line = str(line).encode("latin-1", "replace").decode("latin-1")
        if not line:
            prepared_lines.append("")
        else:
            prepared_lines.extend(textwrap.wrap(line, width=88) or [""])

    pages = [
        prepared_lines[i:i + 48]
        for i in range(0, len(prepared_lines), 48)
    ]

    if not pages:
        pages = [["SmartHire AI Report"]]

    objects = []
    page_ids = []
    content_ids = []
    font_id = 3
    next_id = 4

    objects.append("<< /Type /Catalog /Pages 2 0 R >>")
    objects.append(None)
    objects.append("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")

    for _ in pages:
        page_ids.append(next_id)
        content_ids.append(next_id + 1)
        next_id += 2

    kids = " ".join(f"{page_id} 0 R" for page_id in page_ids)
    objects[1] = f"<< /Type /Pages /Kids [{kids}] /Count {len(pages)} >>"

    for page_id, content_id, page_lines in zip(
        page_ids, content_ids, pages
    ):
        commands = ["BT", "/F1 10 Tf", "50 790 Td", "14 TL"]

        for index, line in enumerate(page_lines):
            if index:
                commands.append("T*")

            escaped = (
                line.replace("\\", "\\\\")
                .replace("(", "\\(")
                .replace(")", "\\)")
            )
            commands.append(f"({escaped}) Tj")

        commands.append("ET")
        stream = "\n".join(commands).encode("latin-1", "replace")

        page_object = (
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 842] "
            f"/Resources << /Font << /F1 {font_id} 0 R >> >> "
            f"/Contents {content_id} 0 R >>"
        )

        while len(objects) < page_id - 1:
            objects.append(None)

        objects.append(page_object)
        objects.append(
            f"<< /Length {len(stream)} >>\nstream\n".encode("latin-1")
            + stream
            + b"\nendstream"
        )

    pdf = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0]

    for object_number, obj in enumerate(objects, start=1):
        offsets.append(len(pdf))
        pdf.extend(f"{object_number} 0 obj\n".encode("latin-1"))

        if isinstance(obj, bytes):
            pdf.extend(obj)
        else:
            pdf.extend((obj or "<< >>").encode("latin-1"))

        pdf.extend(b"\nendobj\n")

    xref_offset = len(pdf)
    pdf.extend(f"xref\n0 {len(objects) + 1}\n".encode("latin-1"))
    pdf.extend(b"0000000000 65535 f \n")

    for offset in offsets[1:]:
        pdf.extend(f"{offset:010d} 00000 n \n".encode("latin-1"))

    pdf.extend(
        f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\n"
        f"startxref\n{xref_offset}\n%%EOF".encode("latin-1")
    )

    return bytes(pdf)


def create_candidate_pdf_report(result, candidate_name):
    matched = result.get("matched_skills", []) or []
    missing = result.get("missing_skills", []) or []
    resume_skills = result.get("resume_skills", []) or []
    job_skills = result.get("job_skills", []) or []

    lines = [
        "SMARTHIRE AI - CANDIDATE ANALYSIS REPORT",
        "=" * 44,
        f"Candidate / Resume: {candidate_name}",
        "",
        f"Text Similarity: {safe_percentage(result.get('similarity_score', 0)):.1f}%",
        f"Skill Match: {safe_percentage(result.get('skill_match_score', 0)):.1f}%",
        "",
        "MATCHED SKILLS",
        "-" * 20,
        ", ".join(str(skill) for skill in matched) or "None identified",
        "",
        "MISSING JOB SKILLS",
        "-" * 20,
        ", ".join(str(skill) for skill in missing) or "None identified",
        "",
        "SKILLS FOUND IN RESUME",
        "-" * 20,
        ", ".join(str(skill) for skill in resume_skills) or "None identified",
        "",
        "SKILLS IDENTIFIED IN JOB DESCRIPTION",
        "-" * 20,
        ", ".join(str(skill) for skill in job_skills) or "None identified",
        "",
        "IMPORTANT NOTE",
        "Text similarity and skill match are screening aids, not hiring probabilities.",
        "Review the original resume and use human judgment before making decisions.",
    ]

    return build_pdf_report(lines)


def get_skill_learning_suggestions(missing_skills):
    """
    Rule-based suggestions for commonly requested skills.
    """
    suggestions = {
        "python": "Practise Python fundamentals, functions, files, and small automation projects.",
        "sql": "Learn SELECT, JOIN, GROUP BY, subqueries, and practise on a sample database.",
        "machine learning": "Study model training, validation, feature engineering, and evaluation metrics.",
        "pandas": "Practise data cleaning, filtering, grouping, and merging DataFrames.",
        "numpy": "Practise arrays, vectorized operations, broadcasting, and numerical calculations.",
        "scikit-learn": "Build a complete pipeline with preprocessing, train/test split, and model evaluation.",
        "deep learning": "Start with neural-network basics, backpropagation, and a small image or text project.",
        "tensorflow": "Follow a beginner model-building tutorial and train/evaluate a small neural network.",
        "pytorch": "Practise tensors, datasets, training loops, and model evaluation.",
        "nlp": "Learn text preprocessing, TF-IDF, embeddings, and build a text-classification project.",
        "natural language processing": "Learn tokenization, TF-IDF, embeddings, and text-classification basics.",
        "computer vision": "Practise image preprocessing, OpenCV, and a simple object or image classifier.",
        "opencv": "Build small projects for image transformations, thresholding, and object/face detection.",
        "excel": "Practise lookup functions, pivot tables, charts, and data-cleaning workflows.",
        "power bi": "Create a dashboard using data modelling, measures, and interactive visuals.",
        "tableau": "Build an interactive dashboard with calculated fields and filters.",
        "aws": "Learn core cloud services, IAM, storage, deployment, and basic cost awareness.",
        "docker": "Containerize a small app and practise images, containers, volumes, and ports.",
        "git": "Practise commits, branches, merges, pull requests, and resolving conflicts.",
        "java": "Practise object-oriented programming, collections, exceptions, and a small application.",
        "javascript": "Practise modern JavaScript, async functions, DOM basics, and API calls.",
        "react": "Build a small component-based interface using state, props, and forms.",
        "html": "Practise semantic page structure, accessible forms, and responsive layouts.",
        "css": "Practise Flexbox, Grid, responsive design, and reusable styling.",
        "statistics": "Revise distributions, probability, hypothesis testing, and descriptive statistics.",
        "data analysis": "Complete an end-to-end project covering cleaning, exploration, visualization, and insights.",
        "communication": "Practise concise project explanations, structured writing, and mock presentations.",
        "leadership": "Practise planning a small team project, delegating tasks, and documenting decisions.",
    }

    output = []

    for skill in missing_skills or []:
        normalized = str(skill).strip().lower()

        suggestion = suggestions.get(
            normalized,
            f"Study the core concepts of {skill}, complete a guided exercise, "
            f"and build a small project demonstrating practical use."
        )

        output.append((str(skill), suggestion))

    return output


def result_download_button(result, filename):
    export_data = {
        "Similarity Score": [result.get("similarity_score", 0)],
        "Skill Match Score": [result.get("skill_match_score", 0)],
        "Resume Skills": [
            ", ".join(
                str(skill)
                for skill in (result.get("resume_skills", []) or [])
            )
        ],
        "Job Skills": [
            ", ".join(
                str(skill)
                for skill in (result.get("job_skills", []) or [])
            )
        ],
        "Matched Skills": [
            ", ".join(
                str(skill)
                for skill in (result.get("matched_skills", []) or [])
            )
        ],
        "Missing Skills": [
            ", ".join(
                str(skill)
                for skill in (result.get("missing_skills", []) or [])
            )
        ],
    }

    csv_data = pd.DataFrame(export_data).to_csv(index=False)

    st.download_button(
        "⬇ Download CSV Report",
        data=csv_data,
        file_name=filename,
        mime="text/csv",
        use_container_width=True,
    )


def show_skill_pills(skills, style="neutral"):
    if not skills:
        st.caption("No skills to display.")
        return

    pills = []

    for skill in skills:
        escaped_skill = html.escape(str(skill))
        pills.append(
            f'<span class="skill-pill {style}">{escaped_skill}</span>'
        )

    st.markdown("".join(pills), unsafe_allow_html=True)


def show_result_score_card(label, value, note, purple=False):
    card_class = "result-card purple" if purple else "result-card"

    st.markdown(
        f"""
        <div class="{card_class}">
            <div class="result-card-label">
                {html.escape(str(label))}
            </div>
            <div class="result-card-value">
                {safe_percentage(value):.1f}%
            </div>
            <div class="result-card-note">
                {html.escape(str(note))}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# CANDIDATE SCORECARD
# =========================================================

def show_candidate_score_card(name, result, label):
    similarity = safe_percentage(result.get("similarity_score", 0))
    skill_match = safe_percentage(result.get("skill_match_score", 0))

    matched_skills = result.get("matched_skills", []) or []
    missing_skills = result.get("missing_skills", []) or []

    with st.container(border=True):
        st.caption(label)
        st.markdown(f"### {html.escape(str(name))}")

        st.markdown("**Text Similarity**")
        st.progress(int(round(similarity)), text=f"{similarity:.1f}%")

        st.markdown("**Skill Match**")
        st.progress(int(round(skill_match)), text=f"{skill_match:.1f}%")

        stat1, stat2 = st.columns(2)

        with stat1:
            st.metric("Matched Skills", len(matched_skills))

        with stat2:
            st.metric("Missing Skills", len(missing_skills))


# =========================================================
# FEATURE: CANDIDATE PROFILE SUMMARY
# =========================================================

def build_candidate_profile_summary(resume_text, result):
    """Extract only details explicitly present in the resume text."""
    text = resume_text or ""

    email_match = re.search(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text,
    )

    phone_match = re.search(
        r"(?<!\w)(?:\+?\d[\d\s().-]{7,}\d)(?!\w)",
        text,
    )

    years_match = re.search(
        r"\b(\d{1,2})\+?\s+years?\s+(?:of\s+)?(?:experience|exp)\b",
        text,
        re.I,
    )

    education_terms = [
        "Ph.D.", "PhD", "Master of Technology", "M.Tech", "M.E.",
        "Master of Science", "M.Sc", "MBA", "Bachelor of Technology",
        "B.Tech", "B.E.", "Bachelor of Science", "B.Sc", "BCA", "MCA",
        "Bachelor of Computer Applications",
        "Master of Computer Applications",
    ]

    lower_text = text.lower()
    education_found = []

    for term in education_terms:
        if term.lower() in lower_text and term not in education_found:
            education_found.append(term)

    return {
        "Email": (
            email_match.group(0)
            if email_match
            else "Not found in resume text"
        ),
        "Phone": (
            phone_match.group(0).strip()
            if phone_match
            else "Not found in resume text"
        ),
        "Experience": (
            f"{years_match.group(1)} years (as stated)"
            if years_match
            else "Not explicitly found in resume text"
        ),
        "Education keywords": (
            ", ".join(education_found)
            if education_found
            else "Not found in resume text"
        ),
        "Skills detected": (
            ", ".join(
                str(x) for x in (result.get("resume_skills", []) or [])
            )
            or "No skills detected"
        ),
    }


def show_candidate_profile_summary(resume_text, result):
    section_heading(
        "Candidate Profile Summary",
        "A quick summary of details explicitly found in the uploaded resume.",
    )

    profile = build_candidate_profile_summary(resume_text, result)
    left, right = st.columns(2)
    items = list(profile.items())

    with left:
        for label, value in items[:3]:
            st.markdown(f"**{html.escape(label)}**")
            st.write(value)

    with right:
        for label, value in items[3:]:
            st.markdown(f"**{html.escape(label)}**")
            st.write(value)

    st.caption(
        "This summary uses simple text extraction and may miss details "
        "or misread formatting. Verify the original resume; no missing "
        "details are inferred."
    )


# =========================================================
# RESUME ANALYSIS RESULTS
# =========================================================

def show_resume_result(result, candidate_name):
    if not result:
        return

    similarity = safe_percentage(result.get("similarity_score", 0))
    skill_match = safe_percentage(result.get("skill_match_score", 0))

    resume_skills = result.get("resume_skills", []) or []
    job_skills = result.get("job_skills", []) or []
    matched_skills = result.get("matched_skills", []) or []
    missing_skills = result.get("missing_skills", []) or []

    section_heading("Analysis Results", f"Results for {candidate_name}")

    show_candidate_profile_summary(
        st.session_state.get("last_resume_text", ""),
        result,
    )

    score_left, score_right = st.columns(2)

    with score_left:
        show_result_score_card(
            "Text Similarity",
            similarity,
            "How closely the resume text matches the job description.",
        )

    with score_right:
        show_result_score_card(
            "Skill Match",
            skill_match,
            "How many required job skills were matched.",
            purple=True,
        )

    chart_left, chart_right = st.columns(2)

    with chart_left:
        make_pie_chart(
            ["Matched Skills", "Missing Skills"],
            [len(matched_skills), len(missing_skills)],
            "Job Skill Coverage",
        )

    with chart_right:
        make_pie_chart(
            ["Text Similarity", "Remaining Difference"],
            [similarity, 100 - similarity],
            "Text Similarity Overview",
        )

    section_heading(
        "Skill Breakdown",
        "Identify strengths and skills that may need improvement.",
    )

    skill_left, skill_right = st.columns(2)

    with skill_left:
        st.markdown(
            """
            <div class="skill-panel matched">
                <div class="skill-panel-title">✓ Matched Skills</div>
            """,
            unsafe_allow_html=True,
        )

        show_skill_pills(matched_skills, "matched")
        st.markdown("</div>", unsafe_allow_html=True)

    with skill_right:
        st.markdown(
            """
            <div class="skill-panel missing">
                <div class="skill-panel-title">! Missing Skills</div>
            """,
            unsafe_allow_html=True,
        )

        show_skill_pills(missing_skills, "missing")
        st.markdown("</div>", unsafe_allow_html=True)

    with st.expander("View all extracted skills"):
        st.markdown("**Resume Skills**")
        show_skill_pills(resume_skills, "neutral")

        st.markdown("**Job Description Skills**")
        show_skill_pills(job_skills, "neutral")

    safe_name = "".join(
        char if char.isalnum() or char in "-_" else "_"
        for char in str(candidate_name)
    )

    result_download_button(result, f"{safe_name}_analysis.csv")

    # FEATURE 1: SKILL GAP & LEARNING SUGGESTIONS
    section_heading(
        "Skill Gap & Learning Suggestions",
        "Practical next steps based on the job skills not yet matched.",
    )

    learning_suggestions = get_skill_learning_suggestions(missing_skills)

    if learning_suggestions:
        for skill, suggestion in learning_suggestions:
            st.markdown(
                f"- **{html.escape(skill)}:** {html.escape(suggestion)}"
            )
    else:
        st.success(
            "No missing job skills were identified by the current skill "
            "extractor. Review the resume manually to confirm proficiency."
        )

    # FEATURE 2: DOWNLOADABLE PDF REPORT
    pdf_data = create_candidate_pdf_report(result, candidate_name)

    st.download_button(
        "⬇ Download Candidate PDF Report",
        data=pdf_data,
        file_name=f"{safe_name}_analysis.pdf",
        mime="application/pdf",
        use_container_width=True,
        key=f"pdf_report_{safe_name}",
    )

    st.caption(
        "Similarity is not a probability of getting hired. "
        "Use the results as screening support."
    )


# =========================================================
# TEAM SECTION
# =========================================================

def show_team():
    st.markdown("""
    <div class="team-section">
        <div class="team-title">Meet Our Team ✦</div>
        <div class="team-subtitle">
            The minds behind SmartHire AI
        </div>
    </div>
    """, unsafe_allow_html=True)

    columns = st.columns(3)

    for column, (name, role, initial) in zip(columns, TEAM_MEMBERS):
        with column:
            st.markdown(
                f"""
                <div class="team-card">
                    <div class="team-avatar">{initial}</div>
                    <div class="team-name">{html.escape(name)}</div>
                    <div class="team-role">{role}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("""
    <div class="team-footer">
        SmartHire AI ✦ | Resume Analysis & Candidate Comparison
        <br><br>
        Built to support smarter resume screening.
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:
    st.markdown("""
    <div style="padding:12px 0 22px;">
        <div style="font-size:28px;font-weight:700;">
            SmartHire <span style="color:#60a5fa;">✦</span>
        </div>
        <div style="color:#93a4bd;font-size:13px;">
            Talent Intelligence Workspace
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.caption("NAVIGATION")

    selected_page = st.radio(
        "Workspace",
        PAGES,
        key="workspace_page",
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown("**SmartHire AI**")
    st.caption("Resume intelligence, skill matching and comparison.")


# =========================================================
# PAGE 1 — OVERVIEW
# =========================================================

if selected_page == "Overview":

    st.markdown("""
    <div class="hero">
        <div class="hero-label">
            AI-powered recruitment workspace
        </div>
        <h1>Discover talent.<br>Understand the match.</h1>
        <p>
            Analyze resumes, identify relevant skills and compare
            candidates against job descriptions in one intelligent
            workspace.
        </p>
    </div>
    """, unsafe_allow_html=True)

    section_heading(
        "Your Workspace",
        "Choose a tool to get started.",
    )

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown("""
        <div class="workspace-card">
            <div class="workspace-icon">📄</div>
            <div class="workspace-tag">01 · RESUME INTELLIGENCE</div>
            <h3>Resume Analyzer</h3>
            <p>
                Upload a resume PDF and compare it with a job
                description. Explore text similarity, skill-match
                scores and missing skills through visual reports.
            </p>
        </div>
        """, unsafe_allow_html=True)

        if st.button(
            "Open Resume Analyzer →",
            key="overview_analyzer",
            type="primary",
            use_container_width=True,
        ):
            go_to_page("Resume Analyzer")
            st.rerun()

    with col2:
        st.markdown("""
        <div class="workspace-card">
            <div class="workspace-icon">📊</div>
            <div class="workspace-tag">02 · TALENT COMPARISON</div>
            <h3>Candidate Comparison</h3>
            <p>
                Compare two candidates against the same job
                description. Review their scores, matched skills,
                missing skills and visual comparison charts.
            </p>
        </div>
        """, unsafe_allow_html=True)

        if st.button(
            "Compare Candidates →",
            key="overview_compare",
            type="primary",
            use_container_width=True,
        ):
            go_to_page("Candidate Comparison")
            st.rerun()

    section_heading(
        "The Process",
        "A simple resume-screening workflow.",
    )

    col_a, col_b, col_c = st.columns(3)

    with col_a:
        metric_card("01", "Extract Resume Text")

    with col_b:
        metric_card("02", "Match Required Skills")

    with col_c:
        metric_card("03", "Review & Compare")


# =========================================================
# PAGE 2 — RESUME ANALYZER
# =========================================================

elif selected_page == "Resume Analyzer":

    st.markdown("""
    <div class="hero">
        <div class="hero-label">Resume intelligence</div>
        <h1>Resume Analyzer</h1>
        <p>
            Upload a candidate's resume and enter the job description
            to evaluate text similarity and skill coverage.
        </p>
    </div>
    """, unsafe_allow_html=True)

    uploaded_resume = st.file_uploader(
        "Upload Resume (PDF)",
        type=["pdf"],
        key="single_resume",
    )

    job_description = st.text_area(
        "Job Description",
        placeholder="Paste the job description here...",
        height=200,
        key="single_job_description",
    )

    if st.button(
        "✦ Analyze Resume",
        type="primary",
        use_container_width=True,
    ):
        if uploaded_resume is None:
            st.warning("Please upload a resume PDF.")

        elif not job_description.strip():
            st.warning("Please enter the job description.")

        else:
            with st.spinner("Analyzing resume..."):
                resume_text = get_pdf_text(uploaded_resume)

                if not resume_text:
                    st.error(
                        "No text could be extracted from the PDF. "
                        "A scanned PDF may require OCR."
                    )
                else:
                    result = get_result(
                        resume_text,
                        job_description.strip(),
                    )

                    if result is not None:
                        st.session_state["last_resume_result"] = result
                        st.session_state["last_resume_name"] = uploaded_resume.name
                        st.session_state["last_resume_text"] = resume_text

    if st.session_state.get("last_resume_result") is not None:
        show_resume_result(
            st.session_state["last_resume_result"],
            st.session_state.get("last_resume_name", "Candidate"),
        )


# =========================================================
# PAGE 3 — CANDIDATE COMPARISON
# =========================================================

elif selected_page == "Candidate Comparison":

    st.markdown("""
    <div class="hero">
        <div class="hero-label">Comparative evaluation</div>
        <h1>Candidate Comparison</h1>
        <p>
            Compare two candidate resumes against the same job
            description and review their matching scores side by side.
        </p>
    </div>
    """, unsafe_allow_html=True)

    comparison_job = st.text_area(
        "Job Description",
        placeholder="Enter the common job description...",
        height=170,
        key="comparison_job",
    )

    col1, col2 = st.columns(2)

    with col1:
        resume1 = st.file_uploader(
            "Candidate 1 Resume (PDF)",
            type=["pdf"],
            key="candidate1_pdf",
        )

    with col2:
        resume2 = st.file_uploader(
            "Candidate 2 Resume (PDF)",
            type=["pdf"],
            key="candidate2_pdf",
        )

    if st.button(
        "⚖ Compare Candidates",
        type="primary",
        use_container_width=True,
    ):
        if not comparison_job.strip():
            st.warning("Please enter the job description.")

        elif resume1 is None or resume2 is None:
            st.warning("Please upload both candidate PDFs.")

        else:
            with st.spinner("Comparing candidates..."):
                text1 = get_pdf_text(resume1)
                text2 = get_pdf_text(resume2)

                if not text1 or not text2:
                    st.error(
                        "Could not extract text from one or both PDFs."
                    )
                else:
                    result1 = get_result(text1, comparison_job.strip())
                    result2 = get_result(text2, comparison_job.strip())

                    if result1 is not None and result2 is not None:
                        st.session_state["comparison_result1"] = result1
                        st.session_state["comparison_result2"] = result2
                        st.session_state["comparison_name1"] = resume1.name
                        st.session_state["comparison_name2"] = resume2.name

    result1 = st.session_state.get("comparison_result1")
    result2 = st.session_state.get("comparison_result2")

    if result1 is not None and result2 is not None:

        name1 = st.session_state.get("comparison_name1", "Candidate 1")
        name2 = st.session_state.get("comparison_name2", "Candidate 2")

        section_heading(
            "Comparison Results",
            "Compare candidate scores and skill coverage visually.",
        )

        candidate_col1, candidate_col2 = st.columns(2)

        with candidate_col1:
            show_candidate_score_card(name1, result1, "CANDIDATE 01")

        with candidate_col2:
            show_candidate_score_card(name2, result2, "CANDIDATE 02")

        comparison_df = pd.DataFrame([
            {
                "Candidate": name1,
                "Text Similarity (%)": safe_percentage(
                    result1.get("similarity_score", 0)
                ),
                "Skill Match (%)": safe_percentage(
                    result1.get("skill_match_score", 0)
                ),
                "Matched Skills": len(result1.get("matched_skills", []) or []),
                "Missing Skills": len(result1.get("missing_skills", []) or []),
            },
            {
                "Candidate": name2,
                "Text Similarity (%)": safe_percentage(
                    result2.get("similarity_score", 0)
                ),
                "Skill Match (%)": safe_percentage(
                    result2.get("skill_match_score", 0)
                ),
                "Matched Skills": len(result2.get("matched_skills", []) or []),
                "Missing Skills": len(result2.get("missing_skills", []) or []),
            },
        ])

        section_heading(
            "Detailed Score Table",
            "Numeric breakdown of both candidates.",
        )

        st.dataframe(
            comparison_df,
            use_container_width=True,
            hide_index=True,
        )

        chart_left, chart_right = st.columns(2)

        with chart_left:
            make_pie_chart(
                [name1, name2],
                [
                    safe_percentage(result1.get("skill_match_score", 0)),
                    safe_percentage(result2.get("skill_match_score", 0)),
                ],
                "Skill Match Comparison",
            )

        with chart_right:
            make_pie_chart(
                [name1, name2],
                [
                    safe_percentage(result1.get("similarity_score", 0)),
                    safe_percentage(result2.get("similarity_score", 0)),
                ],
                "Text Similarity Comparison",
            )

        score1 = safe_percentage(result1.get("skill_match_score", 0))
        score2 = safe_percentage(result2.get("skill_match_score", 0))
        similarity1 = safe_percentage(result1.get("similarity_score", 0))
        similarity2 = safe_percentage(result2.get("similarity_score", 0))

        if score1 > score2:
            summary_title = "✦ Higher Skill Match"
            summary_text = (
                f"{name1} has the higher skill-match score "
                f"({score1:.1f}% compared with {score2:.1f}%)."
            )

        elif score2 > score1:
            summary_title = "✦ Higher Skill Match"
            summary_text = (
                f"{name2} has the higher skill-match score "
                f"({score2:.1f}% compared with {score1:.1f}%)."
            )

        else:
            summary_title = "✦ Equal Skill Match"
            summary_text = (
                "Both candidates have the same skill-match score "
                f"({score1:.1f}%)."
            )

        st.markdown(
            f"""
            <div class="comparison-summary">
                <div class="comparison-summary-title">
                    {html.escape(summary_title)}
                </div>
                <div class="comparison-summary-text">
                    {html.escape(summary_text)}
                    <br><br>
                    Text similarity:
                    {html.escape(str(name1))} — {similarity1:.1f}%,
                    {html.escape(str(name2))} — {similarity2:.1f}%.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.download_button(
            "⬇ Download Comparison CSV",
            data=comparison_df.to_csv(index=False),
            file_name="candidate_comparison.csv",
            mime="text/csv",
            use_container_width=True,
        )

        # FEATURE 3: CANDIDATE SHORTLISTING

        section_heading(
            "Candidate Shortlisting",
            "Select candidates to keep on your shortlist and export the selection.",
        )

        shortlist_col1, shortlist_col2 = st.columns(2)

        with shortlist_col1:
            shortlist1 = st.checkbox(
                f"Shortlist {name1}",
                key="shortlist_candidate1",
            )

        with shortlist_col2:
            shortlist2 = st.checkbox(
                f"Shortlist {name2}",
                key="shortlist_candidate2",
            )

        shortlisted_rows = []

        if shortlist1:
            shortlisted_rows.append({
                "Candidate": name1,
                "Text Similarity (%)": similarity1,
                "Skill Match (%)": score1,
                "Matched Skills": ", ".join(
                    str(skill)
                    for skill in (result1.get("matched_skills", []) or [])
                ),
                "Missing Skills": ", ".join(
                    str(skill)
                    for skill in (result1.get("missing_skills", []) or [])
                ),
                "Shortlist Status": "Shortlisted",
            })

        if shortlist2:
            shortlisted_rows.append({
                "Candidate": name2,
                "Text Similarity (%)": similarity2,
                "Skill Match (%)": score2,
                "Matched Skills": ", ".join(
                    str(skill)
                    for skill in (result2.get("matched_skills", []) or [])
                ),
                "Missing Skills": ", ".join(
                    str(skill)
                    for skill in (result2.get("missing_skills", []) or [])
                ),
                "Shortlist Status": "Shortlisted",
            })

        if shortlisted_rows:
            shortlisted_df = pd.DataFrame(shortlisted_rows).sort_values(
                by=["Skill Match (%)", "Text Similarity (%)"],
                ascending=False,
            )

            st.dataframe(
                shortlisted_df,
                use_container_width=True,
                hide_index=True,
            )

            st.download_button(
                "⬇ Download Shortlist CSV",
                data=shortlisted_df.to_csv(index=False),
                file_name="smarthire_shortlist.csv",
                mime="text/csv",
                use_container_width=True,
            )

        else:
            st.info(
                "No candidates selected yet. Use the checkboxes above "
                "to shortlist candidates."
            )

        # FEATURE 4: CANDIDATE RANKING LEADERBOARD

        section_heading(
            "Candidate Ranking Leaderboard",
            "Upload multiple additional resumes to rank them against the same job description.",
        )

        leaderboard_files = st.file_uploader(
            "Upload multiple resumes (PDF)",
            type=["pdf"],
            accept_multiple_files=True,
            key="leaderboard_resumes",
        )

        if st.button(
            "🏆 Build Ranking Leaderboard",
            key="build_leaderboard",
            use_container_width=True,
        ):
            if not comparison_job.strip():
                st.warning(
                    "Enter the job description above before building the leaderboard."
                )

            elif not leaderboard_files:
                st.warning("Upload at least one PDF for the leaderboard.")

            else:
                ranked_rows = []

                with st.spinner("Ranking uploaded resumes..."):
                    for uploaded in leaderboard_files:
                        candidate_text = get_pdf_text(uploaded)

                        if not candidate_text:
                            continue

                        candidate_result = get_result(
                            candidate_text,
                            comparison_job.strip(),
                        )

                        if candidate_result is None:
                            continue

                        ranked_rows.append({
                            "Candidate": uploaded.name,
                            "Text Similarity (%)": safe_percentage(
                                candidate_result.get("similarity_score", 0)
                            ),
                            "Skill Match (%)": safe_percentage(
                                candidate_result.get("skill_match_score", 0)
                            ),
                            "Matched Skills": len(
                                candidate_result.get("matched_skills", []) or []
                            ),
                            "Missing Skills": len(
                                candidate_result.get("missing_skills", []) or []
                            ),
                        })

                if ranked_rows:
                    leaderboard_df = pd.DataFrame(ranked_rows).sort_values(
                        by=["Skill Match (%)", "Text Similarity (%)"],
                        ascending=False,
                    ).reset_index(drop=True)

                    leaderboard_df.insert(
                        0,
                        "Rank",
                        range(1, len(leaderboard_df) + 1),
                    )

                    st.session_state["leaderboard_results"] = leaderboard_df

                else:
                    st.warning(
                        "No readable resume text was found in the uploaded PDFs."
                    )

        leaderboard_df = st.session_state.get("leaderboard_results")

        if leaderboard_df is not None and not leaderboard_df.empty:
            st.dataframe(
                leaderboard_df,
                use_container_width=True,
                hide_index=True,
            )

            top_candidate = leaderboard_df.iloc[0]

            st.success(
                f"Highest skill-match score in this leaderboard: "
                f"{top_candidate['Candidate']} "
                f"({top_candidate['Skill Match (%)']:.1f}%)."
            )

            st.download_button(
                "⬇ Download Ranking Leaderboard CSV",
                data=leaderboard_df.to_csv(index=False),
                file_name="smarthire_candidate_leaderboard.csv",
                mime="text/csv",
                use_container_width=True,
                key="download_leaderboard_csv",
            )

            st.caption(
                "Ranking is based on skill-match score, with text similarity "
                "as a tie-breaker. It is not a hiring probability or a final "
                "hiring decision."
            )

        # FEATURE 5: HIRING PIPELINE TRACKER

        section_heading(
            "Hiring Pipeline Tracker",
            "Track candidate progress during this app session and export the pipeline as CSV.",
        )

        with st.form("pipeline_add_form", clear_on_submit=True):
            pipeline_col1, pipeline_col2 = st.columns([2, 1])

            with pipeline_col1:
                pipeline_name = st.text_input(
                    "Candidate name",
                    placeholder="e.g. Candidate resume filename",
                )

            with pipeline_col2:
                pipeline_status = st.selectbox(
                    "Current stage",
                    [
                        "Applied",
                        "Shortlisted",
                        "Interview",
                        "Selected",
                        "Rejected",
                    ],
                )

            pipeline_notes = st.text_input(
                "Notes (optional)",
                placeholder="e.g. Technical round pending",
            )

            add_pipeline_candidate = st.form_submit_button(
                "＋ Add to Hiring Pipeline",
                use_container_width=True,
            )

        if add_pipeline_candidate:
            if not pipeline_name.strip():
                st.warning("Enter a candidate name first.")

            else:
                st.session_state["hiring_pipeline"].append({
                    "Candidate": pipeline_name.strip(),
                    "Stage": pipeline_status,
                    "Notes": pipeline_notes.strip(),
                })

                st.success(
                    f"Added {pipeline_name.strip()} to the hiring pipeline."
                )

                st.rerun()

        pipeline_rows = st.session_state.get("hiring_pipeline", [])

        if pipeline_rows:
            pipeline_df = pd.DataFrame(pipeline_rows)

            st.dataframe(
                pipeline_df,
                use_container_width=True,
                hide_index=True,
            )

            pipeline_left, pipeline_right = st.columns(2)

            with pipeline_left:
                st.download_button(
                    "⬇ Download Hiring Pipeline CSV",
                    data=pipeline_df.to_csv(index=False),
                    file_name="smarthire_hiring_pipeline.csv",
                    mime="text/csv",
                    use_container_width=True,
                    key="download_pipeline_csv",
                )

            with pipeline_right:
                if st.button(
                    "Clear Hiring Pipeline",
                    key="clear_pipeline",
                    use_container_width=True,
                ):
                    st.session_state["hiring_pipeline"] = []
                    st.rerun()

            st.caption(
                "Pipeline data is stored in Streamlit session state and may "
                "reset when the session is restarted."
            )

        else:
            st.info(
                "No candidates in the pipeline yet. Add a candidate above "
                "to start tracking."
            )

        st.caption(
            "Scores are screening aids, not hiring probabilities. "
            "Review the actual resumes before making a hiring decision."
        )


# =========================================================
# PAGE 4 — ABOUT PROJECT
# =========================================================

elif selected_page == "About Project":

    st.markdown("""
    <div class="hero">
        <div class="hero-label">Project overview</div>
        <h1>About SmartHire AI</h1>
        <p>
            An AI-assisted resume screening application that helps
            compare resume content with job requirements.
        </p>
    </div>
    """, unsafe_allow_html=True)

    section_heading("What is SmartHire AI?")

    st.markdown("""
    <div class="panel">
        <h3>Smarter Resume Screening</h3>
        <p>
            SmartHire AI extracts text from PDF resumes, identifies
            relevant skills and compares candidates with a job description.
        </p>
        <p>
            It presents text similarity, skill-match scores, matched
            skills and missing skills to support the screening process.
        </p>
    </div>
    """, unsafe_allow_html=True)

    section_heading("Technology Stack")

    col1, col2, col3 = st.columns(3)

    with col1:
        metric_card("Interface", "Streamlit")

    with col2:
        metric_card("Data Processing", "Pandas")

    with col3:
        metric_card("Visualization", "Plotly")

    section_heading("Key Capabilities")

    st.markdown("""
    - PDF resume text extraction
    - Resume-to-job text similarity
    - Skill matching and missing-skill identification
    - Two-candidate comparison
    - Candidate ranking leaderboard
    - Candidate profile summary
    - Hiring pipeline tracking
    - Interactive charts and CSV reports
    """)


# =========================================================
# PAGE 5 — HOW IT WORKS
# =========================================================

elif selected_page == "How It Works":

    st.markdown("""
    <div class="hero">
        <div class="hero-label">Application workflow</div>
        <h1>How It Works</h1>
        <p>
            From PDF upload to candidate comparison, understand
            the steps behind the application.
        </p>
    </div>
    """, unsafe_allow_html=True)

    steps = [
        (
            "01 — Upload Resume",
            "The user uploads a candidate resume in PDF format.",
        ),
        (
            "02 — Extract Text",
            "The PDF reader extracts available text from the document.",
        ),
        (
            "03 — Identify Skills",
            "The backend processes resume text and job requirements.",
        ),
        (
            "04 — Calculate Scores",
            "The ranking module returns text-similarity and skill-match scores.",
        ),
        (
            "05 — Review Results",
            "The interface displays matched skills, missing skills and charts.",
        ),
        (
            "06 — Export Report",
            "The user can download supported results as CSV files.",
        ),
    ]

    for title, description in steps:
        st.markdown(
            f"""
            <div class="panel">
                <h3>{html.escape(title)}</h3>
                <p>{html.escape(description)}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    section_heading("Important Notes")

    st.markdown("""
    - Similarity is not the probability of getting hired.
    - Skill-match scores depend on the backend implementation.
    - Scanned PDFs may need OCR before text can be extracted.
    - Final hiring decisions should involve human review.
    """)


# =========================================================
# TEAM SECTION AT THE END
# =========================================================

show_team()