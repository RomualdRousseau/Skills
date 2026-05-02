# Monorepo Project Structure for AI Environments

This structure supports building complex simulations that function as both interactive games and Gymnasium-compliant RL environments.

## Root Level

```text
/
├── pyproject.toml       # Workspace-level config (e.g., [tool.uv.workspace])
├── justfile             # Root tasks (e.g., just run-all, just test-all)
├── TODO.md              # Monorepo-level backlog
├── assets/              # Centralized assets (fonts, images, etc.)
├── repo-env/            # 👈 Specialized simulation package
│   ├── pyproject.toml
│   ├── justfile
│   ├── TODO.md          # Project backlog
│   └── src/
├── repo-agents/         # 👈 Specialized agent training/inference package
│   ├── pyproject.toml
│   ├── justfile
│   ├── TODO.md          # Project backlog
│   └── src/
└── .venv/               # Single shared virtual environment
```

## Package Internal Structure

Each package (e.g., `Environment/`) follows this modular layout:

```text
mygame-repo/
├── src/mygame/              # 👈 Package lives here (src layout)
│   ├── __init__.py
│   ├── __main__.py          # 👈 Entry point (fire) with play, test-env, and agent commands
│   ├── env/
│   │   ├── __init__.py
│   │   ├── gym_env.py       # The Gymnasium class (Wrapper around Scenes)
│   │   └── reward.py        # Reward shaping logic (Pure functions)
│   ├── core/
│   │   ├── __init__.py
│   │   ├── base.py          # Base class/protocol
│   │   ├── config.py        # Environment-driven configuration
│   │   ├── physics.py       # Domain logic & high-integrity transition rules
│   │   └── loader.py        # Asset loading
│   ├── game/
│   │   ├── __init__.py
│   │   ├── scene/
│   │   │   ├── __init__.py
│   │   │   ├── menu.py      # UI/Menu Scene (Game mode)
│   │   │   └── main_env.py  # The main simulation Scene (RL mode)
│   │   ├── state.py         # Dataclasses (__slots__ mandatory)
│   │   └── gameplay.py      # Pure state transition logic (I/O-free)
│   ├── engine/
│   │   ├── __init__.py
│   │   ├── ui/
│   │   │   ├── __init__.py
│   │   │   └── renderer.py  # Raylib-based drawing logic
│   │   ├── audio/           # Raylib-based Audio stuffs
│   │   └── input/           # Raylib-based Input stuffs
│   └── shared/
│       ├── __init__.py
│       ├── constant.py      # Physics constants, colors, titles
│       └── math.py          # Vector and physics math helpers
└── tests/
    ├── unit/
    ├── integration/
    └── property/            # 👈 Property-based tests (Hypothesis)
```

## Modular Design Guidelines

1.  **Scene Isolation**: Each `Scene` in `scene/` coordinates its own `game/logic` and `ui/renderer`.
2.  **Gym Wrapper**: The `gym.Env` in `env/gym_env.py` manages one or more scenes (e.g., automatically switching from a Loading Scene to the Main Env Scene).
3.  **Headless-Ready**: Logic in `game/` and `core/` must never depend on `ui/renderer` or `pyray` calls, allowing the simulation to run at maximum speed without a window.
4.  **Absolute Imports**: Maintain absolute paths within each package's `src/` directory for tool compatibility (`uv`, `ruff`, `ty`).
