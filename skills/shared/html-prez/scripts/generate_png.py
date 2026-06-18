#!/usr/bin/env python3
import sys
import os
import asyncio

async def capture_slides_as_png(input_html, output_dir):
    input_html_abs = os.path.abspath(input_html)
    output_dir_abs = os.path.abspath(output_dir)
    os.makedirs(output_dir_abs, exist_ok=True)

    print(f"Loading slide deck: {input_html_abs}")
    print(f"Output directory: {output_dir_abs}")

    # Import playwright here to avoid crash if not installed
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        print("Error: The 'playwright' package is required for PNG slide generation.")
        print("Please install it using: uv pip install playwright && uv run playwright install chromium")
        sys.exit(1)

    async with async_playwright() as p:
        # Launch headless browser with certificate and web security disabled to load unpkg/cdn resources
        browser = await p.chromium.launch(args=["--disable-web-security", "--ignore-certificate-errors"])
        context = await browser.new_context(viewport={"width": 1280, "height": 720}, ignore_https_errors=True)
        page = await context.new_page()

        # Load the HTML file
        try:
            await page.goto(f"file://{input_html_abs}", wait_until="networkidle")
        except Exception as e:
            print(f"Error loading file in browser: {e}")
            await browser.close()
            sys.exit(1)
            
        await page.wait_for_timeout(1000)  # Allow fonts, CDNs, and Lucide icons to fully render

        # Find total slide count
        slides = await page.query_selector_all(".slide-page")
        total_slides = len(slides)
        
        if total_slides == 0:
            print("Error: No slides found matching the class '.slide-page' in the HTML.")
            await browser.close()
            sys.exit(1)
            
        print(f"Found {total_slides} slides to render.")

        for i in range(total_slides):
            print(f"Rendering Slide {i + 1}/{total_slides}...")
            
            # Select the currently visible slide element
            active_slide = await page.query_selector(".slide-page:not(.hidden)")
            if active_slide:
                output_path = os.path.join(output_dir_abs, f"Slide{i + 1}.png")
                # Take element screenshot
                await active_slide.screenshot(path=output_path)
                print(f"  ✓ Saved: Slide{i + 1}.png")
            else:
                print(f"  ✗ Error: Could not locate active slide element at index {i}")

            # Advance to the next slide if not the last one
            if i < total_slides - 1:
                # Try clicking the next button first
                next_btn = await page.query_selector("#next-btn")
                if next_btn:
                    await page.click("#next-btn")
                else:
                    # Fallback to pressing Spacebar
                    await page.keyboard.press("Space")
                await page.wait_for_timeout(400)  # Wait for display class transitions to settle

        await browser.close()
    print("PNG slide rendering completed successfully!")

def main():
    if len(sys.argv) < 3:
        print("Usage: generate_png.py <input_html> <output_directory>")
        print("Example: uv run python3 scripts/generate_png.py presentation.html slides_output/")
        sys.exit(1)

    input_html = sys.argv[1]
    output_dir = sys.argv[2]

    if not os.path.exists(input_html):
        print(f"Error: Input file {input_html} not found.")
        sys.exit(1)

    asyncio.run(capture_slides_as_png(input_html, output_dir))

if __name__ == "__main__":
    main()
