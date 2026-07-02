---
name: html-prez
description: Generates high-fidelity technical presentation slides using HTML5/Tailwind CSS and converts them to PDF. Use when the user needs to visualize technical concepts or export presentations for sharing.
---

# Presentation Generator

This skill enables the generation of high-fidelity, technical presentation slides that adhere to the DATA - AI Innovation Lab's visual identity, with the ability to export them as PDF.

## Workflow

1.  **Analyze Request:** Understand the technical content the user wants to visualize.
2.  **Reference Design System:** Review `DESIGN.md` for color palettes, typography, and component rules.
3.  **Co-location Mandate:** **ALL** generated/compiled slide formats (including `.html` interactive presentations, `.pdf` widescreen slide sheets, `.pptx` PowerPoint slide decks, and the subfolder of `.png` slide screenshots) **MUST ALWAYS** reside in the exact same directory as the `.md` slide outline page (typically `wiki/analyses/`). Never leave them in temporary folders or separate build directories.
4.  **Generate HTML:** Use the structure provided in `assets/slide-template.html` to create a single-file HTML document inside the same directory as the `.md` slide outline.
5.  **Incorporate Components:**
    *   Use `.card-hover` for interactive/grouped content.
    *   Use Lucide icons wrapped in styled containers.
    *   Apply `font-mono` to technical terms and badges.
6.  **PDF Export (Optional):** If the user requests a PDF, use the provided script to convert the generated HTML, outputting directly in the co-located directory:
    ```bash
    python3 scripts/generate_pdf.py <input.html> <output.pdf>
    ```
7.  **PNG Slide Export (Optional):** If the user requests individual PNG slides, use the provided Playwright screenshot capture script, outputting in a subfolder directly in the co-located directory:
    ```bash
    uv run python3 scripts/generate_png.py <input.html> <output_directory>
    ```
8.  **PDF/PPTX Compilation from Images (Optional):** If the user wants to compile individual PNG slides into standard widescreen PDF or Microsoft PowerPoint (`.pptx`) presentations, use the provided compilation script, outputting directly in the co-located directory:
    ```bash
    uv run python3 scripts/compile_presentation.py <slides_directory> <output_pdf> <output_pptx>
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

## PNG Tooling
The skill includes a `scripts/generate_png.py` tool powered by Playwright to navigate, render, and capture high-fidelity PNG screenshots of each individual slide page (`.slide-page`).

## Example Triggers

*   "Create a slide explaining our multi-agent orchestration and save it as PDF."
*   "Generate a presentation for the new LLMOps pipeline."
*   "Convert my presentation.html to a PDF slide."
*   "Render all slides from presentation.html as PNG screenshots."
*   "Combine all PNG screenshots in folder slides_dir/ into widescreen PDF and PowerPoint files."

## Reference Materials

*   **Design System:** [DESIGN.md](DESIGN.md)
*   **HTML Template:** [slide-template.html](assets/slide-template.html)
*   **PDF Tool:** [generate_pdf.py](scripts/generate_pdf.py)
*   **PNG Tool:** [generate_png.py](scripts/generate_png.py)
*   **Compilation Tool:** [compile_presentation.py](scripts/compile_presentation.py)
