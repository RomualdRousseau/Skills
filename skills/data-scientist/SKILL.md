---
name: data-scientist
description: Interactive data science and machine learning exploration using Jupyter Notebooks, pandas, numpy, and uv for reproducible environments.
tags:
  - data-science
  - jupyter
  - exploration
  - analysis
  - machine-learning
  - python
depends_on:
  - python-developer
---

# Data Scientist

This skill equips the agent to perform exploratory data science, data analysis, and machine learning experimentation. Extending `python-developer`, it emphasizes reproducible virtual environments with `uv` and interactive Jupyter Notebooks for reporting and visual exploration.

## 1. Environment Setup with `uv`

Whenever starting a new data science task or notebook project, follow these steps to guarantee speed and reproducibility:

1. **Initialize Virtual Environment**:
   Always create a local virtual environment using `uv`:
   ```bash
   uv venv
   ```

2. **Install Dependencies**:
   Install required packages via `uv pip`:
   ```bash
   uv pip install pandas numpy matplotlib seaborn jupyter ipykernel
   ```
   If a `requirements.txt` or `pyproject.toml` is provided:
   ```bash
   uv pip install -r requirements.txt
   ```

3. **Running Jupyter**:
   Launch or run Jupyter tools within the environment using `uv run`:
   ```bash
   uv run jupyter notebook
   ```

## 2. Working with Jupyter Notebooks

Prefer Jupyter Notebooks (`.ipynb`) over transient scripts for exploratory analysis, metric visualization, and reporting:

1. **Creating Notebooks**: Generate valid JSON `.ipynb` files programmatically.
2. **Automated Headless Execution**: Run and evaluate notebook cells via `jupyter nbconvert`:
   ```bash
   uv run jupyter nbconvert --to notebook --execute analysis.ipynb --output analysis_executed.ipynb
   ```
3. **Reproducibility**: Freeze dependencies into `requirements.txt` using `uv pip freeze > requirements.txt` or configure `pyproject.toml`.

## 3. Best Practices

- **Clarity & Structure**: Organize notebooks into logical sections (Data Ingestion, Cleaning, Exploratory Analysis, Modeling, Conclusions).
- **Visualization**: Use clear labels, legends, and readable color palettes in `matplotlib` / `seaborn`.
- **Safety**: Avoid mutating raw input datasets directly; maintain pure transformation steps.

## Project Interaction

- **Trigger**: "Start a data analysis notebook on [dataset]"
- **Trigger**: "Train a baseline machine learning model on [data]"
- **Trigger**: "Create inline visualizations for [metrics]"
- **Trigger**: "Initialize a Jupyter workspace with uv"
- **Trigger**: "Execute and validate notebook [filename.ipynb]"
