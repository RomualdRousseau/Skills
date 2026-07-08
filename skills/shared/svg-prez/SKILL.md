---
name: svg-prez
description: Direct vector slide generation and multi-format compilations (SVG, PPTX, PDF, PNG). Compiles PowerPoint (PPTX) with native, fully editable shapes and text, though the layout is non-pixel-perfect due to rendering differences. Use when PowerPoint editability is required.
---

# SVG Presentation Generator (svg-prez)

This skill enables the direct, high-fidelity compilation of widescreen presentations using clean, semantic SVG vector coordinates as the central source of truth. It bypasses heavy browser screenshotting and layout-lossy HTML parsing by rendering directly to PowerPoint (`.pptx`), vector PDFs (`.pdf`), and crisp PNG screenshots (`.png`).

## Workflow

```
[Slide Details / Config] ──(generate_svgs.py)──> [SlideX.svg (Vectors)]
                                                        │
                      ┌─────────────────────────────────┼────────────────────────────────┐
                      ▼ (compile_pptx.py)               ▼ (compile_pdf.py)               ▼ (compile_png.py)
            [Assembled Deck.pptx]              [Assembled Deck.pdf]             [SlideX.png (150 DPI)]
            (Native Editable Shapes)            (Widescreen Vectors)             (Crisp Slide Preview)
```

1.  **Direct SVG Generation**: Create clean, widescreen `1920x1080` pixel-perfect SVG files slide-by-slide using direct coordinates. Include custom inline paths for icons and cards to preserve infinite scaling and visual identity.
2.  **Native Widescreen PowerPoint**: Convert SVGs slide-by-slide into PowerPoint vector shapes using `svg2pptx`. Use `compile_pptx.py` to merge them into a single widescreen presentation, automatically injecting high-resolution corporate logos natively as brand pictures. Note that **PowerPoint (.pptx) outputs generated this way are native and fully editable, but not pixel-perfect** due to differences in font metrics, text wrap, and vector rendering engines between browsers/PDF tools and PowerPoint's OpenXML renderer.
3.  **High-Fidelity Vector PDF**: Merge all slide SVGs into a single, high-fidelity vector PDF using `compile_pdf.py` inside the PyMuPDF environment in milliseconds.
4.  **Crisp Raster Previews**: Render SVGs into crisp PNG screenshots at 150 DPI (high-resolution previews) using `compile_png.py` inside PyMuPDF with zero external binary dependencies.

---

## Bundled Compiler Tools

All scripts support automatic dependency resolution via `uv run` and reside in the `scripts/` directory:

### 1. Slide SVG Generator
Generates the 19 template-based, hand-crafted vector slides into the slides folder:
```bash
uv run python3 scripts/generate_svgs.py <output_dir>
```

### 2. PowerPoint (PPTX) Compiler & Merger
Translates SVGs into native PPTX shapes, merges them at the OpenXML layer, and injects brand logos:
```bash
uv run python3 scripts/compile_pptx.py <slides_dir> <output_pptx>
```

### 3. Vector PDF Compiler
Directly compiles and merges all SVG slides into a single vector-based widescreen PDF in milliseconds:
```bash
uv run python3 scripts/compile_pdf.py <slides_dir> <output_pdf>
```

### 4. Crisp PNG Slide Renderer
Renders all SVG slides into crisp, high-resolution PNG slides at 150 DPI for visual previews:
```bash
uv run python3 scripts/compile_png.py <slides_dir>
```

---

## Core Design Principles

*   **Slide Proportions**: Always widescreen `16:9` (coordinates `1920x1080` inside SVG, compiled to `13.333" x 7.5"` inside PPTX).
*   **Widescreen Grid Math**: Card structures and columns must use absolute coordinates (e.g. 3-card columns: width `568px`, spacing `36px` at x=72, 676, 1280).
*   **Typesetting Baseline**: Position text baselines at `top + height * 0.78` to prevent text cutoff. Set text-anchor based on alignment (`start` for left, `middle` for center, `end` for right).
*   **Zero Duplication**: Keep slides folders clean by co-locating standard formats (`SlideX.png`, `SlideX.svg`, `SlideX.pptx`) neatly together.

## Reference Materials

*   **Design Guidelines**: Sourced from the global presentation design standards.
*   **SVG Slide Template (Content)**: [slide-template.svg](assets/slide-template.svg)
*   **SVG Slide Template (Title)**: [slide-template-title.svg](assets/slide-template-title.svg)
*   **SVG Slide Template (Chapter)**: [slide-template-chapter.svg](assets/slide-template-chapter.svg)
*   **SVG Slide Template (Closing)**: [slide-template-closing.svg](assets/slide-template-closing.svg)
*   **SVG Slide Generator**: [generate_svgs.py](scripts/generate_svgs.py)
*   **PowerPoint Compiler**: [compile_pptx.py](scripts/compile_pptx.py)
*   **Vector PDF Compiler**: [compile_pdf.py](scripts/compile_pdf.py)
*   **PNG Slide Renderer**: [compile_png.py](scripts/compile_png.py)
