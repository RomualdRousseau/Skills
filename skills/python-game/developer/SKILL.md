---
name: developer
description: Raylib game development using Python. Use when building minimal, modular, visually-debuggable games with a strict separation between simulation logic and rendering.
---

# Raylib Game Development

This skill provides a foundation for building games using Python and `raylib` for simulation and visualization.

## Core Philosophy

1.  **Module-Based First**: Start with module-level functions and minimal state. Only introduce classes when the game genuinely complexifies.
2.  **Layered Architecture**: Split the project into three layers:
    -   `core/` — data, physics, and input abstractions (no rendering)
    -   `game/` — gameplay logic; imports only from `core`
    -   `engine/` — Raylib adapter implementing the `core` input protocol and rendering primitives
3.  **Engine Injection**: `main.py` creates the engine and passes (injects) it into the game layer. This lets tests swap the real engine for a mock.
4.  **Simulation/Visualization Split**: Keep physics and state updates separate from Raylib drawing. The simulation must be testable without a graphics context.
5.  **Headless-Ready (Strict)**: Logic in `core/` and `game/` must never import from `engine/` or `pyray`.
6.  **Simple Before Object-Oriented**: Prefer plain functions and dataclasses. The Scene pattern is valid for complex state machines, but start with module-level functions and refactor only when needed.

## Project Structure

See [structure.md](references/structure.md) for the full package layout.

```text
spacerace/
├── pyproject.toml
├── justfile
├── README.md
├── TODO.md
├── src/spacerace/
│   ├── __init__.py
│   ├── main.py              # Entry point; wires engine into game
│   ├── core/
│   │   ├── __init__.py
│   │   ├── constant.py      # World constants (immutable laws)
│   │   ├── math.py          # Vector/wrap helpers
│   │   ├── physics.py       # Pure state transition functions
│   │   ├── input.py         # InputEngine protocol
│   │   └── state.py         # Dataclasses with __slots__
│   ├── game/
│   │   └── __init__.py      # Module-level gameplay functions
│   └── engine/
│       └── raylib_engine.py # Module-level Raylib implementation
└── tests/
```

## Testing & Verification

### Behavioral TDD (Core & Game Layers)

All simulation logic in `core/` and `game/` must be developed using a **Test-First** approach:

1.  **Red**: Write a failing test for a physics rule or state transition.
2.  **Green**: Implement the minimum logic to pass the test.
3.  **Refactor**: Optimize for efficiency while maintaining correctness.

### Vanilla BDD for Scenarios

Use `pytest` to describe gameplay behaviors using the **Given / When / Then** pattern:

- **Given**: A player at a specific position with a specific velocity.
- **When**: A specific input is applied.
- **Then**: The resulting position, velocity, and game status must match expectations.

### Headless Validation (Engine Injection)

Logic tests **must never require a hardware window**. The `game/` and `core/` layers receive an engine object via **Dependency Injection**.
- During testing, inject a `MockEngine` or a simple module with the `InputEngine` protocol functions.
- Verify that logic correctly reads input and calls rendering primitives without needing the actual hardware.

## Configuration & Constants

### Constants (`core/constant.py`)

Constants define the **"Laws of the World."**
- **Location**: Kept in `core/` to maintain locality with the physics engine.
- **Examples**: `GRAVITY`, `MAX_SPEED`, `SCREEN_SIZE`, `PLAYER_SPEED`.
- **Policy**: Immutable and importable by any layer.

### Configuration (`engine/config.py`)

Configuration represents **Deployment & Hardware Settings.**
- **Location**: Kept in `engine/` as it concerns rendering and environment setup.
- **Examples**: `SCREEN_WIDTH`, `FPS`, `ASSET_PATH`.
- **Injection Policy**: Business logic in `core/` and `game/` **must never** import this. Values are passed in via constructors or module setup during initialization.

## Key Workflows

### Gameplay Loop Design

Every game follows the same loop in `main.py`:

```python
engine.init()
player = game.init()

while not engine.should_quit():
    dt = engine.get_frame_time()
    engine.begin_frame()
    player = game.update(engine, player, dt)
    game.draw(engine, player)
    engine.end_frame()

engine.close()
```

### Visual Debugging with Raylib

- Use `render_mode="human"` equivalents (direct play mode) to visually inspect behavior.
- Use `engine.draw_*` primitives to implement debug overlays (vectors for velocities, collision boxes, etc.).

## Tooling & CLI

- **Dependencies**: `uv add raylib pytest`.
- **Raylib Note**: Although the package name is `raylib`, it must be imported as `pyray`. Always use the `pr` alias for consistency.

```python
import pyray as pr
```

- **Task Runner**: Use `just` for common commands (`just play`, `just test`, `just sync`).
- **Entry Point**: Define the play command in `pyproject.toml` under `[project.scripts]` rather than using a CLI framework for simple games.

```toml
[project.scripts]
spacerace-play = "spacerace.main:run"
```

## Project Interaction

- **Trigger**: "Build a Raylib game where [mechanic]"
- **Trigger**: "Implement the simulation logic for [mechanic]"
- **Trigger**: "Add a Raylib debug overlay for [state/variable]"
- **Trigger**: "Add [input/control] to move [entity]"
- **Trigger**: "Refactor the game into the core/game/engine layers"
