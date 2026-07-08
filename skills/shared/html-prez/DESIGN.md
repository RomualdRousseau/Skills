# DATA - AI Innovation Lab Presentation Design System (DESIGN.md)

This document specifies the unified visual identity and Tailwind CSS layout guidelines for the `html-prez` skill. It integrates the official corporate logos and symbols of **Servier** (located in the skill's `assets/` directory) with the technical "engineered blueprint" aesthetic of the **DATA - AI Innovation Lab**.

---

## 1. Official Servier Brand Assets

The following official Servier images are located directly within the `assets/` directory of the `html-prez` skill and must be used for slide branding:

| Asset Name | Filename | Purpose | Image Type |
| :--- | :--- | :--- | :--- |
| **Official Full Logo** | `Servier_Logo_RVB.png` | Standard brand signature for white backgrounds. | PNG (Color) |
| **Official Logo Signature** | `Servier_Logo_Sign_RVB.png` | Branding with the "moved by you" slogan below the text. | PNG (Color) |
| **Official Symbole** | `Servier_Symbole_RVB.png` | The Servier icon (smile curve and 10-point starburst) without text. | PNG (Color) |

### Dark Background Optimization (CSS Filters)
Since the official assets are provided in their colored/dark brand formats (intended for white backgrounds), you must use CSS hardware-accelerated filters to render them cleanly on dark blue backgrounds:

- **Render as Solid White**: Use the class `brightness-0 invert` (Tailwind classes for `filter: brightness(0) invert(1)`).
- **Render with High Contrast**: Use `brightness-200 contrast-150` for crisp visibility.

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

### Typography
- **Primary Body/Headers**: `Inter` (Sans-serif)
  - Titles: Extrabold (800) or Bold (700) with letter-spacing tracking-tight.
  - Body/Lists: Normal (400) or Medium (500) for high legibility.
- **Technical/Metadata**: `JetBrains Mono` (Monospace)
  - Badges, slide indices, version numbers, and technical references.

---

## 3. Four Canonical Slide Templates

The visual system supports 4 specific slide types to structure any presentation.

### Template 1: Title Slide (Dark Blue Theme)
*   **Theme**: Deep corporate immersion.
*   **Background**: Solid `#1d2366`.
*   **Visual Accents**: A massive, thick curved quarter-arc of `#2c3385` (35% opacity) swept from the bottom-left toward the top-center.
*   **Typography**: Huge white heading on the left, left-aligned, with critical terms highlighted in **Coral Orange** (`#ff5a24`).
*   **Branding**: White-filtered official logo signature (`Servier_Logo_Sign_RVB.png` with class `brightness-0 invert h-12`) positioned in the bottom-right.
*   **Metadata**: White date/reference in the bottom-left (`15/06/2026`).

### Template 2: Chapter Slide (White Theme)
*   **Theme**: Clean, high-impact section divider.
*   **Background**: Solid `#ffffff`.
*   **Visual Accents**: The same massive curved quarter-arc swept from bottom-left to top-center, but styled in light blue `#e8edf9`.
*   **Typography**: Large headings in Servier Dark Blue, with keywords highlighted in **Coral Orange**.
*   **Branding**: Official colored logo signature (`Servier_Logo_Sign_RVB.png` with class `h-12`) positioned in the bottom-right.
*   **Metadata**: Dark blue date in bottom-left.

### Template 3: Content Slide (White with Footer Band)
*   **Theme**: Structured data, technical cards, and grids.
*   **Background**: Solid `#ffffff`.
*   **Typography**: Clear Dark Blue headings on top-left; body text is clean slate.
*   **Content Modules (Data Factory Core)**:
  - **Technical Cards**: Standard rounded-xl boxes with subtle borders and transition hover glows (`.card-hover:hover`).
  - **Dashed Blueprint Overlay**: Subtle border-dashed borders (`border-slate-100`) can be absolute-positioned around the card grids to emphasize the Innovation Lab's engineering theme.
*   **Footer Strip**: A full-width band of `#f8fafc` at the absolute bottom.
  - Left: Slide number and presentation context.
  - Right: Official colored logo (`Servier_Logo_RVB.png` with class `h-8`) positioned in the bottom-right.

### Template 4: Closing Slide (Dark Blue / Minimalist)
*   **Theme**: Bold, clean brand exit.
*   **Background**: Solid `#1d2366`.
*   **Visual Accents**: Minimalist and highly striking. The official white-filtered Servier symbole (`Servier_Symbole_RVB.png` with class `brightness-0 invert h-28 w-28`) is positioned in the absolute center of the slide. No text, maximizing brand impact.

---

## 4. HTML & CSS Implementation Reference

### 1. The Quarter-Circle Accent Ring
To render the massive background swept ring without images, use absolute rounding:
```html
<!-- Background swept ring for Title Slide (Dark) -->
<div class="absolute -bottom-36 -left-36 w-[700px] h-[600px] border-[120px] border-[#2c3385]/35 rounded-full pointer-events-none"></div>

<!-- Background swept ring for Chapter Slide (Light) -->
<div class="absolute -bottom-36 -left-36 w-[700px] h-[600px] border-[120px] border-[#e8edf9] rounded-full pointer-events-none"></div>
```

### 2. Loading Official Image Assets

#### In Title / Dark Blue Slides (Solid White Filter)
```html
<img src="Servier_Logo_Sign_RVB.png" class="brightness-0 invert h-12 object-contain" alt="Servier Logo Signature">
```

#### In Chapter / Content Slides (Standard Color)
```html
<img src="Servier_Logo_Sign_RVB.png" class="h-12 object-contain" alt="Servier Logo Signature">
```

#### Centered Symbol on Closing Slide (Solid White Filter)
```html
<img src="Servier_Symbole_RVB.png" class="brightness-0 invert h-28 w-28 object-contain" alt="Servier Symbole">
```

---

## 5. PowerPoint (.pptx) Output Characteristics

When compiling HTML slides to PowerPoint (`.pptx`) format via PNG screenshots:
- **Pixel-Perfect Layout Fidelity**: Preserves 100% of the HTML5/CSS design, including complex layouts, gradients, shadows, and custom font rendering exactly as seen in the browser.
- **Non-Editable Elements**: Slides are exported as static, full-bleed images embedded in the PowerPoint pages. Individual text blocks, icons, and shapes **cannot be modified** inside PowerPoint. Use this skill when exact visual reproduction is more important than editability.
