---
name: data-scientist
description: Provides workflows and instructions for data science tasks using Python, Jupyter Notebooks, and uv for ultra-fast dependency and virtual environment management. Use when starting new data analysis, machine learning, or Python notebook projects.
---

# Data Scientist

## Overview

This skill equips the agent to perform data science tasks efficiently by utilizing `uv` for Python environment and package management, alongside Jupyter Notebooks for interactive data exploration and reporting.

## Workflow: Environment Setup with `uv`

Whenever starting a new data science task or project, follow these steps to ensure a reproducible environment:

1. **Initialize Virtual Environment**:
   Always create a local virtual environment using `uv`.
   ```bash
   uv venv
   ```

2. **Install Dependencies**:
   Use `uv pip` to install required packages. It is significantly faster than standard `pip`.
   ```bash
   uv pip install pandas numpy matplotlib jupyter
   ```
   If there is a `requirements.txt`, install it via:
   ```bash
   uv pip install -r requirements.txt
   ```

3. **Running Commands**:
   Execute Jupyter tools within the environment using `uv run`.
   ```bash
   uv run jupyter notebook
   ```

## Working with Jupyter Notebooks

**MANDATE: Always use Jupyter Notebooks (`.ipynb`) instead of standalone Python scripts (`.py`) for all data science, analysis, and visualization tasks.**

When requested to create or work with notebooks:

1. **Creating Notebooks**:
   You can generate a `.ipynb` file programmatically by writing the JSON structure of a Jupyter Notebook.

2. **Executing Notebooks**:
   To run a notebook and execute all cells, use `jupyter nbconvert` via `uv run`:
   ```bash
   uv pip install nbconvert ipykernel
   uv run jupyter nbconvert --to notebook --execute my_notebook.ipynb --output my_notebook_executed.ipynb
   ```

3. **Dependencies**:
   Always ensure `ipykernel` and `jupyter` are installed in the `uv` environment if you need to interact with notebooks.

## Best Practices

- **Notebooks over Scripts**: Always prefer `.ipynb` for interactivity, documentation, and inline visualizations.
- **Reproducibility**: Always document the packages installed. If asked to finalize a project, generate a `requirements.txt` using `uv pip freeze > requirements.txt`.
- **Speed**: Never use standard `pip` or `python -m venv`. Always prefer `uv`.
- **Data Exploration**: Prefer `pandas` for tabular data, and `matplotlib` or `seaborn` for visualizations unless specified otherwise.
