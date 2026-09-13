---
name: python-hexagonal
description: Hexagonal Architecture (Ports and Adapters) for high-integrity Python applications, decoupling business logic from external frameworks, databases, and APIs.
tags:
  - python
  - architecture
  - hexagonal
  - ddd
  - ports-and-adapters
depends_on:
  - python-developer
---

# Python Hexagonal Architecture

This skill provides architectural guidance for structuring high-integrity Python applications using **Hexagonal Architecture** (Ports and Adapters). It builds on the safety rules and testing standards of `python-developer` to isolate core business rules from external frameworks, delivery mechanisms, and I/O.

## 1. Architectural Structure

All code must be organized into three distinct layers to ensure clear separation of concerns, testability, and framework independence:

- **`presentation/`**: Delivery entry points (REST API, CLI, messaging consumers). Responsible for runtime validation at the boundary via `TypeGuards`.
- **`application/`**: Pure business logic and workflow orchestration.
  - **`model/`**: Domain entities and value objects (using `__slots__` for deterministic memory).
  - **`port/`**: Protocols defining abstract interfaces for data access and external services.
  - **`service/`**: Application services orchestrating business workflows.
- **`infrastructure/`**: Concrete adapters and implementations.
  - **`adapter/`**: Database repositories, cloud clients, and external API integrations that implement application ports.
  - **`config/`**: Environment variable loading and deployment configurations.
- **`shared/`**:
  - **`constant/`**: Immutable truths shared across layers.
  - **`exception/`**: Domain-specific fail-closed exceptions.

Consult [structure.md](references/structure.md) for full directory layouts and file conventions.

## 2. Core Architectural Principles

- **Dependency Inversion**: Dependencies point strictly inwards toward `application/`. The `application/` layer never imports from `infrastructure/` or `presentation/`.
- **Fail-Closed**: Logic must default to "Access Denied" or "Operation Aborted" upon encountering unknown states or exceptions.
- **Light CQRS**: Explicitly separate state-mutating operations from query operations:
  - **Commands**: Methods that change state should be named with imperative verbs (e.g., `create_user`, `submit_order`). Return `None` or a simple status.
  - **Queries**: Methods that read state start with `get_`, `list_`, or `find_`. They are side-effect free and return domain models or DTOs.
- **Late Abstraction**: Define `typing.Protocol` interfaces only when needed or when multiple concrete implementations are required.
- **Singular Naming**: Use singular package and directory names (`model`, `port`, `service`, `adapter`).

Detailed guidelines and patterns are documented in [guideline.md](references/guideline.md).

## 3. Dependency Injection Pattern

Collaborators and external services must be injected into application services at the composition root (in `presentation/` or `main.py`). Services never instantiate their own adapters or database connections:

```python
# Composition Root
repo = PostgresUserRepository(db_session)
mailer = SendgridEmailAdapter(api_key=cfg.SENDGRID_API_KEY)
service = UserRegistrationService(user_repo=repo, mailer=mailer)
```

## Project Interaction

- **Trigger**: "Refactor [module] to follow Hexagonal Architecture"
- **Trigger**: "Define the Protocols and Ports for [feature]"
- **Trigger**: "Implement the domain model for [entity]"
- **Trigger**: "Implement the application service for [workflow]"
- **Trigger**: "Create an infrastructure adapter for [external service/database]"
