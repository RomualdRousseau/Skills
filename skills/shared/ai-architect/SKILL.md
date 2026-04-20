---
name: ai-architect
description: Guides the design, evaluation, and implementation of AI/LLM features, focusing on RAG patterns, prompt engineering, and safety.
---

# AI/LLM Architect

This skill provides a structured approach to building reliable, scalable, and safe AI/LLM applications.

## 1. Prompt Engineering & Management
- **Separation of Concerns:** Separate instructions (the prompt) from data (user inputs). Treat prompts as code.
- **Versioning:** All prompts must be version-controlled. Do not hardcode complex prompts inline; use template files.
- **Context Management:** Implement token counting and context window chunking to prevent max-token errors.

## 2. Retrieval-Augmented Generation (RAG)
- **Data Ingestion:** Document parsing must be resilient. Implement chunking strategies (e.g., semantic or overlapping) based on the domain.
- **Retrieval Quality:** Use hybrid search (Keyword + Vector) for high-accuracy retrieval. Implement re-ranking (e.g., Cohere, Cross-Encoders) when precision is critical.
- **Citation:** Responses must explicitly cite the source chunks used to generate the answer.

## 3. Evaluation & Guardrails
- **Evaluation Driven Development (EDD):** Use frameworks like Ragas or LangSmith to quantitatively measure Helpfulness, Faithfulness, and Relevance before deploying prompt changes.
- **Guardrails:** Implement input validation (to detect prompt injection) and output validation (to enforce formatting and avoid hallucinations).
- **Fallbacks:** Always provide a graceful degradation path if the LLM provider is down or times out.

## Project Interaction

- **Trigger**: "Design a RAG pipeline for [document type]"
- **Trigger**: "Optimize the prompt for [specific task]"
- **Trigger**: "Implement an evaluation suite for the LLM using Ragas"
- **Trigger**: "Setup guardrails to prevent prompt injection"
- **Trigger**: "Define a chunking strategy for [dataset]"

