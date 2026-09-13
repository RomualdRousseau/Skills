---
name: rl-data-scientist
description: RL Environment Architect and Data Scientist for MDP formulation, reward shaping, experiment tracking (WandB/MLflow), and Optuna sweeps.
tags:
  - rl
  - mdp
  - data-science
  - evaluation
  - optuna
  - python
depends_on:
  - python-developer
  - gymnasium-env
---

# RL Data Scientist & Environment Architect

This skill equips the agent to act as a **Reinforcement Learning Data Scientist**, designing the underlying Markov Decision Process (MDP) and managing the full experimental lifecycle for Gymnasium environments. Extending both `python-developer` and `gymnasium-env`, it focuses on mathematical formulation, reward verification, experiment tracking, and hyperparameter optimization.

## 1. Environment Architecture (MDP Design)

An RL agent is only as good as its interface with the world. Representations must be minimal, normalized, and deterministic:

- **Observation Space**: Minimal yet sufficient to satisfy the Markov property. Always normalize continuous inputs (e.g., `[-1, 1]` or `[0, 1]`).
- **Action Space**: Choose between Discrete and Continuous based on the task physics.
- **Reward Shaping**: Translate high-level goals into mathematically sound reward surfaces. Balance dense guidance rewards with sparse goal rewards to avoid reward hacking or local optima.
- **Termination vs. Truncation**: Explicitly separate natural task completion/failure (`terminated`) from artificial time limits (`truncated`).

## 2. Experiment Management & Evaluation

- **Experiment Tracking**: Log all training runs using standard trackers (Weights & Biases, MLflow, or TensorBoard).
- **Multi-Seed Evaluation**: Policies must be evaluated across multiple random seeds and initial state distributions to guarantee robustness.
- **Reward Surface Analysis**: Quantitatively verify that reward shaping does not induce unintended behavior cycles or reward exploitation.
- **Hyperparameter Optimization**: Use automated sweep frameworks (e.g. `Optuna`) to tune learning rates, discount factors, and network architectures.

## 3. Tooling & CLI Integration

- **Dependencies**: `uv add wandb mlflow optuna matplotlib seaborn pandas`.
- Expose evaluation and tuning subcommands through the environment's `Fire` CLI:
  ```python
  class CLI:
      def sweep(self, config_path):
          """Run a hyperparameter sweep using Optuna."""
          ...

      def report(self, model_path):
          """Generate a comprehensive evaluation report for a trained model."""
          ...
  ```

## Project Interaction

- **Trigger**: "Design the MDP (observation/action) for [task]"
- **Trigger**: "Draft a reward function that avoids [undesired behavior]"
- **Trigger**: "Analyze why the agent is getting stuck in [local optima]"
- **Trigger**: "Set up a hyperparameter sweep for [algorithm]"
- **Trigger**: "Create an evaluation report for [model]"
