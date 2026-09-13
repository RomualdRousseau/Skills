---
name: gymnasium-env
description: Reinforcement learning environment development using Gymnasium. Covers gym.Env interfaces, state/action spaces, reward verification, and Fire CLI integration.
tags:
  - rl
  - gymnasium
  - simulation
  - python
  - environment
depends_on:
  - python-developer
---

# Gymnasium Environment Developer

This skill provides specialized standards for building Reinforcement Learning (RL) environments adhering to the Farama Foundation **Gymnasium** API. Extending `python-developer`, it emphasizes mathematical rigor, deterministic step transitions, bounded reward functions, and decoupled visualization.

## 1. The `gym.Env` Contract

All environments must strictly implement the standard Gymnasium lifecycle methods:

- **`reset(self, seed=None, options=None) -> tuple[ObsType, dict]`**: Re-initializes state deterministically. Always pass `seed` to the internal RNG.
- **`step(self, action: ActType) -> tuple[ObsType, float, bool, bool, dict]`**: Executes one transition step. Returns `(observation, reward, terminated, truncated, info)`.
- **`render(self) -> RenderFrame | list[RenderFrame] | None`**: Renders current state. Supports modes such as `human` (direct interactive window) and `rgb_array` (off-screen array).
- **`close(self)`**: Releases external hardware, window, or display resources cleanly.

Review [patterns.md](references/patterns.md) for scene-based environment design and lifecycle implementation details.

## 2. Observation & Action Space Standards

- **Space Types**: Use standard Gymnasium spaces (`gym.spaces.Box`, `gym.spaces.Discrete`, `gym.spaces.MultiDiscrete`).
- **Data Types**: Always use `np.float32` for continuous observations and actions to match PyTorch/JAX default tensor precisions.
- **Normalization**: Continuous observations must be normalized to `[-1.0, 1.0]` or `[0.0, 1.0]`. Unbounded observations degrade policy network training stability.
- **Validations**: Use `self.action_space.contains(action)` and assert bounds in debug/development builds.

## 3. Reward Engineering & Invariants

- **Bounds**: Rewards must be provably bounded to prevent gradient explosion.
- **Property Testing**: Test reward bounds and step state transitions using `Hypothesis` to prove no action can generate infinite, NaN, or out-of-bound values.
- **Sparse vs. Dense**: Start with sparse terminal rewards when feasible, or apply potential-based reward shaping to preserve optimal policy guarantees.

## 4. Package Structure & CLI

Organize environments into clean, modular packages. Consult [structure.md](references/structure.md) for recommended package layouts.

Expose the environment workflows using `python-fire` in `__main__.py` to allow immediate testing and inspection:

```python
import fire


class CLI:
    def play(self):
        """Run the environment with human controls (e.g. Raylib)."""
        ...

    def test_env(self, episodes=5):
        """Run random agents to verify step/reset interface contracts."""
        ...

    def train(self, agent_type="ppo", total_timesteps=100_000):
        """Train an RL agent on the environment."""
        ...


if __name__ == "__main__":
    fire.Fire(CLI)
```

## Project Interaction

- **Trigger**: "Build a new Gymnasium environment for [task]"
- **Trigger**: "Define the observation and action spaces for [scenario]"
- **Trigger**: "Implement and test the reward function for [goal]"
- **Trigger**: "Verify the Gymnasium interface contracts with random steps"
- **Trigger**: "Expose play and training CLI entry points using Fire"
