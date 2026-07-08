# DATA - AI Innovation Lab Presentation Design System (DESIGN.md)

This document specifies the unified visual identity and SVG layout guidelines for the `svg-prez` skill. It integrates the official corporate logos and symbols of **Servier** (located in the skill's `assets/` directory) with the technical "engineered blueprint" aesthetic of the **DATA - AI Innovation Lab**.

---

## 1. Official Servier Brand Assets

The following official Servier images are located directly within the `assets/` directory of the `svg-prez` skill and must be used for slide branding:

| Asset Name | Filename | Purpose | Image Type |
| :--- | :--- | :--- | :--- |
| **Official Full Logo** | `Servier_Logo_RVB.png` | Standard brand signature for white backgrounds. | PNG (Color) |
| **Official Logo Signature** | `Servier_Logo_Sign_RVB.png` | Branding with the "moved by you" slogan below the text (light backgrounds). | PNG (Color) |
| **Official Symbole** | `Servier_Symbole_RVB.png` | The Servier icon (smile curve and 10-point starburst) on light backgrounds. | PNG (Color) |
| **Official White Logo Signature** | `Servier_Logo_Sign_Blanc.png` | White version of the logo signature, optimized natively for dark backgrounds (Slide 1). | PNG (White) |
| **Official White Symbole** | `Servier_Symbole_Blanc.png` | White version of the Servier symbol, optimized natively for dark backgrounds (Slide 19). | PNG (White) |

### Dark Background Image Support
Since PowerPoint (.pptx) does not support SVG inline CSS filters (like `brightness(0) invert(1)`) on `<image>` elements, **you must use the native white PNG assets** (`_Blanc.png`) directly in the SVG code and PowerPoint compilers for dark blue background templates. This guarantees that logos display perfectly in both browsers and PowerPoint without any visual loss or color ghosting.

---

## 2. Core Visual Elements & Palette

### Corporate Colors
| Element | Hex Code | Tailwind Custom Class | Description |
| :--- | :--- | :--- | :--- |
| **Servier Dark Blue** | `#1d2366` | `bg-[#1d2366]` / `text-[#1d2366]` | Main background for Title and Closing slides; primary text color for Chapter and Content slides. |
| **Coral Orange Accent** | `#ff5a24` | `bg-[#ff5a24]` / `text-[#ff5a24]` | Key highlights, active tags, and Servier logomark starburst. |
| **Light Blue Overlay (Dark)** | `#2c3385` | `border-[#2c3385]` | Background accent ring on dark slides. |
| **Light Blue Overlay (Light)**| `#e8edf9` | `border-[#e8edf9]` | Background accent ring on light slides. |
| **Muted Slate** | `#64748b` | `text-slate-500` | Sub-details and bullet descriptions on content slides. |
| **Light Footer Band** | `#f8fafc` | `bg-[#f8fafc]` / `bg-slate-50` | Dedicated footer strip for Content slides. |

### Outer Slide Borders
- **Base Rounding**: The outermost slide background frame rectangle must have a subtle, elegant rounded edge defined as **`rx="0"`** (e.g. `<rect x="0" y="0" width="1920" height="1080" rx="0" .../>`). This renders natively and beautifully in both browser SVGs and PowerPoint templates without creating oversized corner adjustments.
- **Card Rounding**: Inner content cards are styled with **`rx="20"`** for high-impact definition.

### Typography
- **Primary Body/Headers**: `'Segoe UI', 'Arial', sans-serif`
  - High PowerPoint compatibility, native on Windows and Mac.
  - Titles: Extrabold (800) or Bold (700) with letter-spacing tracking-tight.
  - Body/Lists: Normal (400) or Medium (500) for high legibility.
- **Technical/Metadata**: `'JetBrains Mono', monospace`
  - Badges, slide indices, version numbers, and technical references.

---

## 3. Four Canonical Slide Templates

The visual system supports 4 specific slide types to structure any presentation.

### Template 1: Title Slide (Dark Blue Theme)
*   **Theme**: Deep corporate immersion.
*   **Background**: Solid `#1d2366`.
*   **Slide Frame**: Rounded border frame with `rx="0"`.
*   **Visual Accents**: A massive, thick curved quarter-arc of `#2c3385` (35% opacity) swept from the bottom-left toward the top-center.
*   **Typography**: Huge white heading on the left, left-aligned in **Segoe UI**, with critical terms highlighted in **Coral Orange** (`#ff5a24`).
*   **Branding**: Native white logo signature (`Servier_Logo_Sign_Blanc.png`) positioned in the bottom-right.
*   **Metadata**: White date/reference in the bottom-left (`15/06/2026`).

### Template 2: Chapter Slide (White Theme)
*   **Theme**: Clean, high-impact section divider.
*   **Background**: Solid `#ffffff`.
*   **Slide Frame**: Rounded border frame with `rx="0"`.
*   **Visual Accents**: The same massive curved quarter-arc swept from bottom-left to top-center, but styled in light blue `#e8edf9`.
*   **Typography**: Large headings in Servier Dark Blue, with keywords highlighted in **Coral Orange**.
*   **Branding**: Official colored logo signature (`Servier_Logo_Sign_RVB.png`) positioned in the bottom-right.
*   **Metadata**: Dark blue date in bottom-left.

### Template 3: Content Slide (White with Footer Band)
*   **Theme**: Structured data, technical cards, and grids.
*   **Background**: Solid `#ffffff`.
*   **Slide Frame**: Rounded border frame with `rx="0"`.
*   **Typography**: Clear Dark Blue headings on top-left; body text is clean slate.
*   **Content Modules (Data Factory Core)**:
  - **Technical Cards**: Standard rounded-xl boxes (`rx="20"`) with subtle borders and transition hover glows (`filter="url(#card-shadow)"`).
  - **Dashed Blueprint Overlay**: Subtle border-dashed borders (`stroke-dasharray="8,6" stroke="#a5b4fc"`) can be applied around card grids to emphasize the Innovation Lab's engineering theme.
*   **Footer Strip**: A full-width band of `#f8fafc` at the absolute bottom.
  - Left: Slide number and presentation context.
  - Right: Official colored logo (`Servier_Logo_RVB.png`) positioned in the bottom-right.

### Template 4: Closing Slide (Dark Blue / Minimalist)
*   **Theme**: Bold, clean brand exit.
*   **Background**: Solid `#1d2366`.
*   **Slide Frame**: Rounded border frame with `rx="0"`.
*   **Visual Accents**: Minimalist and highly striking. The official native white Servier symbole (`Servier_Symbole_Blanc.png`) is positioned in the absolute center of the slide. No text, maximizing brand impact.

---

## 4. SVG Template Implementation Reference

### 1. The Quarter-Circle Accent Ring
To render the massive background swept ring, use absolute `<ellipse>` geometry:
```xml
<!-- Background swept ring for Title/Closing Slide (Dark) -->
<ellipse cx="309" cy="846" rx="525" ry="450" fill="none" stroke="#2c3385" stroke-width="180" opacity="0.35" pointer-events="none"/>

<!-- Background swept ring for Chapter/Content Slide (Light) -->
<ellipse cx="309" cy="846" rx="525" ry="450" fill="none" stroke="#e8edf9" stroke-width="180" opacity="0.4" pointer-events="none"/>
```

### 2. Loading Official Image Assets

#### In Title Slide (Natively White Signature)
```xml
<image x="1560" y="960" width="288" height="60" href="data:image/png;base64,...[Servier_Logo_Sign_Blanc.png]"/>
```

#### In Chapter Slide (Standard Color Signature)
```xml
<image x="1560" y="960" width="288" height="60" href="data:image/png;base64,...[Servier_Logo_Sign_RVB.png]"/>
```

#### Centered Symbol on Closing Slide (Natively White Symbol)
```xml
<image x="824" y="404" width="272" height="272" href="data:image/png;base64,...[Servier_Symbole_Blanc.png]"/>
```
