# SmartHire AI — Intelligent Resume Screening & Recruitment Platform

An AI-powered recruitment platform built with Python and Streamlit to simplify resume screening, evaluate candidate skills, compare applicants, and support data-driven recruitment workflows.

## Overview

SmartHire AI helps recruiters and hiring teams analyze resumes against job requirements. It extracts resume text from PDF documents, identifies relevant skills, and calculates text similarity to help evaluate candidate-job alignment.

The platform provides an interactive interface for resume analysis and candidate comparison, helping make the initial screening process more organized and efficient.

## Key Features

- **PDF Resume Parsing:** Extracts text from uploaded PDF resumes.
- **Skill Matching:** Identifies relevant skills in resumes and job descriptions.
- **Resume Similarity Analysis:** Uses TF-IDF and cosine similarity to compare resume content with job requirements.
- **Candidate Ranking:** Helps prioritize candidates using calculated similarity and skill-match scores.
- **Candidate Comparison:** Supports comparison of multiple candidates.
- **Skill Gap Insights:** Highlights missing skills that may be relevant to a job description.
- **Hiring Pipeline Tracking:** Helps organize candidates across recruitment stages.
- **Reports and Visualizations:** Presents analysis results in an accessible format.
- **Interactive Dashboard:** Built with Streamlit for a user-friendly experience.

## Technology Stack

- **Programming Language:** Python
- **Web Framework:** Streamlit
- **Text Analysis:** TF-IDF and cosine similarity
- **PDF Processing:** pypdf
- **Data Processing:** Python libraries
- **Testing:** pytest
- **Version Control:** Git and GitHub

## Project Structure

```text
SmartHire-AI/
├── app.py
├── backend/
│   ├── pdf_reader.py
│   ├── resume_ranker.py
│   ├── similarity.py
│   └── skill_extractor.py
├── data/
├── models/
├── test_ranking.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/KARAN-2317/AI-Recruitment-System.git
cd AI-Recruitment-System
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Run the application

```bash
python -m streamlit run app.py
```

Streamlit will provide a local URL in the terminal. Open that URL in your browser to use the application.

## Running Tests

Run the automated tests with:

```bash
python -m pytest -q
```

## How It Works

1. Upload a resume in PDF format.
2. Provide the relevant job description.
3. Extract text and identify skills from the resume and job requirements.
4. Calculate text similarity and skill-match scores.
5. Review candidate analysis, comparisons, and skill gaps.
6. Use the results to support the initial screening process.

## Important Note

Similarity and skill-match scores are indicators of alignment with the supplied job description. They are not hiring probabilities and should not be treated as definitive measures of a candidate's ability. Final recruitment decisions should include human review and other relevant evaluation criteria.

## Future Improvements

- Expand skill extraction and language support.
- Add persistent storage for candidate records.
- Introduce configurable recruitment workflows.
- Improve evaluation using larger and more diverse test datasets.
- Add further reporting and analytics capabilities.

## Team Members

- Karan Dev Singh
- Abhay Kumar Gupta
- Ankur Singh

---

Developed as a college project to explore AI-assisted resume analysis and recruitment workflows.
