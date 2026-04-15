# Monorepo Project Structure for AI Environments

This structure supports building complex simulations that function as both interactive games and Gymnasium-compliant RL environments.

## Root Level

```text
/
├── pyproject.toml       # Workspace-level config (e.g., [tool.uv.workspace])
├── justfile             # Root tasks (e.g., just run-all, just test-all)
├── TODO.md              # Monorepo-level backlog
├── assets/              # Centralized assets (fonts, images, etc.)
├── Environment/         # Specialized simulation package
└── Agents/              # Specialized agent training/inference package
```

## Package Internal Structure

Each package (e.g., `Environment/`) follows this modular layout:

```text
src/your_package_name/
├── __init__.py
├── __main__.py          # Entry point (fire) with play, test-env, and agent commands
├── env/
│   ├── gym_env.py       # The Gymnasium class (Wrapper around Scenes)
│   └── reward.py        # Reward shaping logic (Pure functions)
├── core/
│   ├── base.py          # Scene base class/protocol
│   ├── physics.py       # Domain logic & high-integrity transition rules
│   ├── config.py        # Environment-driven configuration
│   └── loader.py        # Asset loading
├── game/
    ├── scene/
│   │   ├── menu.py      # UI/Menu Scene (Game mode)
│   │   └── main_env.py  # The main simulation Scene (RL mode)
│   ├── state.py         # Dataclasses (__slots__ mandatory)
│   └── gameplay.py      # Pure state transition logic (I/O-free)
├── ui/
│   └── renderer.py      # Raylib-based drawing logic
├── audio/               # Audio stuffs
└── util/
    ├── constant.py      # Physics constants, colors, titles
    └── math.py          # Vector and physics math helpers
```

## Modular Design Guidelines

1.  **Scene Isolation**: Each `Scene` in `scene/` coordinates its own `game/logic` and `ui/renderer`.
2.  **Gym Wrapper**: The `gym.Env` in `env/gym_env.py` manages one or more scenes (e.g., automatically switching from a Loading Scene to the Main Env Scene).
3.  **Headless-Ready**: Logic in `game/` and `core/` must never depend on `ui/renderer` or `pyray` calls, allowing the simulation to run at maximum speed without a window.
4.  **Absolute Imports**: Maintain absolute paths within each package's `src/` directory for tool compatibility (`uv`, `ruff`, `ty`).
