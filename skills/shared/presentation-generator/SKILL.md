---
name: presentation-generator
description: Generates high-fidelity technical presentation slides using HTML5/Tailwind CSS and converts them to PDF. Use when the user needs to visualize technical concepts or export presentations for sharing.
---

# Presentation Generator

This skill enables the generation of high-fidelity, technical presentation slides that adhere to the DATA - AI Innovation Lab's visual identity, with the ability to export them as PDF.

## Workflow

1.  **Analyze Request:** Understand the technical content the user wants to visualize.
2.  **Reference Design System:** Review `references/design-system.md` for color palettes, typography, and component rules.
3.  **Generate HTML:** Use the structure provided in `assets/slide-template.html` to create a single-file HTML document.
4.  **Incorporate Components:**
    *   Use `.card-hover` for interactive/grouped content.
    *   Use Lucide icons wrapped in styled containers.
    *   Apply `font-mono` to technical terms and badges.
5.  **PDF Export (Optional):** If the user requests a PDF, use the provided script to convert the generated HTML.
    ```bash
    python3 scripts/generate_pdf.py <input.html> <output.pdf>
    ```

## Core Design Principles

*   **Aspect Ratio:** Always 16:9 (`aspect-video`).
*   **Colors:** Primary accent is Indigo-600. Neutral base is Slate.
*   **Typography:** 'Inter' for headings/body, 'JetBrains Mono' for technical elements.
*   **Blueprint Feel:** Use dashed borders and mono-font badges to convey a technical, engineered aesthetic.

## PDF Tooling
The skill includes a `scripts/generate_pdf.py` tool. It attempts to use (in order):
1. System Chromium/Chrome (Headless)
2. wkhtmltopdf
3. Playwright (Python)

## Project Interaction

- **Trigger**: "Create a slide explaining our multi-agent orchestration and save it as PDF."
- **Trigger**: "Generate a presentation for the new LLMOps pipeline."
- **Trigger**: "Convert my presentation.html to a PDF slide."

## Reference Materials

*   **Design System:** [design-system.md](references/design-system.md)
*   **HTML Template:** [slide-template.html](assets/slide-template.html)
*   **PDF Tool:** [generate_pdf.py](scripts/generate_pdf.py)
