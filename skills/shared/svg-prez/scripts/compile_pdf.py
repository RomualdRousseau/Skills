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
    if len(sys.argv) < 3:
        print("Usage: compile_pdf.py <slides_dir> <output_pdf>")
        sys.exit(1)

    slides_dir = sys.argv[1]
    output_pdf = sys.argv[2]

    print("=== HIGH-FIDELITY VECTOR PDF COMPILER ===")
    print(f"Slides Folder: {slides_dir}")
    print(f"Destination: {output_pdf}")

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

    doc = fitz.open()
    for svg_path in svgs:
        print(f"Adding vector slide: {os.path.basename(svg_path)}...")
        svg_doc = fitz.open(svg_path)
        pdf_bytes = svg_doc.convert_to_pdf()
        svg_doc.close()
        
        temp_pdf = fitz.open("pdf", pdf_bytes)
        doc.insert_pdf(temp_pdf)
        temp_pdf.close()

    doc.save(output_pdf)
    doc.close()
    print(f"\n✓ Unified vector PDF successfully saved to {output_pdf}")
    print("=== PDF COMPILATION COMPLETE ===")

if __name__ == "__main__":
    main()
