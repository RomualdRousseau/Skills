# Mermaid.js Documentation Standards

Use Mermaid.js for all architecture, sequence, and flowchart diagrams within Markdown files. This ensures diagrams are version-controlled and rendered natively in the browser.

## 1. General Styling

- **Theme**: Use `theme: neutral` or `theme: base` for professional clarity.
- **Direction**:
    - **Flowcharts**: Prefer `TD` (Top-Down) for processes and `LR` (Left-to-Right) for system architectures.
    - **Sequence Diagrams**: Use participant aliases for cleaner code.

## 2. Architecture Diagrams (C4 Light)

Use flowcharts to represent the Hexagonal Architecture layers.

```mermaid
graph LR
    subgraph Presentation
        CLI[__main__.py / Fire CLI]
        API[FastAPI / Controllers]
    end

    subgraph Application
        Service[Domain Services]
        Model[Data Models / __slots__]
    end

    subgraph Infrastructure
        Adapter[DB / API Adapters]
    end

    CLI --> Service
    API --> Service
    Service --> Model
    Service --> Adapter
```

## 3. Sequence Diagrams (Scene Pattern)

Use sequence diagrams to illustrate the coordination between Scenes, Logic, and Renderers.

```mermaid
sequenceDiagram
    participant E as gym.Env
    participant S as Scene
    participant L as game.logic
    participant R as ui.renderer

    E->>S: step(action)
    S->>L: update_physics(state, action)
    L-->>S: next_state
    S-->>E: observation, reward, done
    Note over E,R: If render_mode == "human"
    E->>S: render()
    S->>R: draw(state)
```

## 4. State Machines (Scene Transitions)

Use state diagrams for Scene status or RL phase transitions.

```mermaid
stateDiagram-v2
    [*] --> Initializing
    Initializing --> Running: reset()
    Running --> Running: step()
    Running --> Terminated: goal reached
    Running --> Truncated: time limit
    Terminated --> Running: reset()
    Truncated --> Running: reset()
```

## 5. Integration

Include Mermaid diagrams directly in `README.md`, `SKILL.md`, or ADRs. Always wrap them in a code block:

```text
 {backtick}{backtick}{backtick}mermaid
 graph TD;
     A-->B;
 {backtick}{backtick}{backtick}
```
