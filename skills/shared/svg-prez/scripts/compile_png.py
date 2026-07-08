#!/usr/bin/env python3
import os
import glob
import sys

# Inline Metadata for UV to automatically fetch dependencies
# /// script
# dependencies = [
#   "pymupdf",
# ]
# ///

def main():
    if len(sys.argv) < 2:
        print("Usage: compile_png.py <slides_dir>")
        sys.exit(1)

    slides_dir = sys.argv[1]

    print("=== HIGH-FIDELITY PNG SLIDE RENDERER ===")
    print(f"Slides Folder: {slides_dir}")

    try:
        import fitz
    except ImportError:
        print("Error: 'pymupdf' is required.")
        sys.exit(1)

    svgs = glob.glob(os.path.join(slides_dir, "*.svg"))
    if not svgs:
        print("Error: No SVG slides found inside the slides folder.")
        sys.exit(1)

    # Sort numerically (Slide1, Slide2, ... Slide19)
    svgs = sorted(svgs, key=lambda x: int(os.path.basename(x).replace("Slide", "").replace(".svg", "")))

    for svg_path in svgs:
        base_name = os.path.basename(svg_path).replace(".svg", "")
        png_path = os.path.join(slides_dir, f"{base_name}.png")
        print(f"Rendering {base_name}.svg -> {base_name}.png...")
        
        try:
            doc = fitz.open(svg_path)
            # Render at 150 DPI for crisp visual presentation previews
            pix = doc[0].get_pixmap(dpi=150)
            pix.save(png_path)
            doc.close()
        except Exception as e:
            print(f"✗ Failed rendering {base_name}.svg: {e}")
            sys.exit(1)

    print("\n✓ All vector SVG slides successfully rendered to high-fidelity PNGs.")
    print("=== PNG RENDERING COMPLETE ===")

if __name__ == "__main__":
    main()
