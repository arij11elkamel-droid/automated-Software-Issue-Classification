# Automated Software Issue Classification

A machine learning system that automatically classifies software issue reports into **bug**, **enhancement**, or **question** categories, developed as part of the *Principles of AI Engineering* course at the University of Passau (WS2024).

## What it does

Software teams using issue trackers (like JIRA) need to triage incoming reports quickly. This project provides a REST API that predicts an issue's category from its title and description, learns from corrections, and exposes monitoring metrics for the model's performance over time.

## Features

- **Text classification pipeline**: TF-IDF vectorization + a Random Forest classifier, trained on labeled issue data.
- **REST API (Flask)**:
  - `POST /api/predict` — classifies a new issue and returns a predicted label with a confidence score.
  - `POST /api/correct` — records a manual correction to a previous prediction.
  - `GET /api/predict/<id>` — retrieves a stored prediction.
  - `GET /metrics` — exposes Prometheus metrics.
- **Input safety check**: incoming text is language-detected (via `langdetect`); non-English input is rejected with a clear error message.
- **Persistence**: predictions and corrections are stored in a SQLite database (via SQLAlchemy).
- **Testing & CI**: automated tests with `pytest`, run on every push via GitLab CI, with coverage reporting (`pytest-cov`).
- **Monitoring**: a Prometheus metrics endpoint tracks accuracy, average prediction confidence, and per-category prediction counts, visualized with Grafana. The full stack (API + Prometheus + Grafana) is orchestrated with Docker Compose.

## Tech stack

Python, Flask, scikit-learn, SQLAlchemy, pytest, GitLab CI, Docker Compose, Prometheus, Grafana

## Note on data and models

The training datasets used for this project are not included in this repository due to licensing restrictions (they were provided as part of the university course). The trained model files (`.pkl`) are also excluded due to file size. As a result, the repository showcases the implementation rather than being directly runnable end-to-end without the original data.
