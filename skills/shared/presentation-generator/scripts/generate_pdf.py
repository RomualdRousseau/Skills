#!/usr/bin/env python3
import os
import subprocess
import sys


def main():
    if len(sys.argv) < 3:
        print("Usage: generate_pdf.py <input_html> <output_pdf>")
        sys.exit(1)

    input_html = sys.argv[1]
    output_pdf = sys.argv[2]

    if not os.path.exists(input_html):
        print(f"Error: Input file {input_html} not found.")
        sys.exit(1)

    # Strategy 1: Check for chromium/google-chrome
    browsers = ["chromium-browser", "chromium", "google-chrome", "google-chrome-stable"]
    for browser in browsers:
        try:
            subprocess.run(
                [browser, "--version"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            print(f"Using {browser} for PDF generation...")
            cmd = [
                browser,
                "--headless",
                "--disable-gpu",
                "--print-to-pdf=" + output_pdf,
                input_html,
            ]
            subprocess.run(cmd, check=True)
            print(f"Successfully generated {output_pdf}")
            return
        except (subprocess.CalledProcessError, FileNotFoundError):
            continue

    # Strategy 2: Check for wkhtmltopdf
    try:
        subprocess.run(
            ["wkhtmltopdf", "--version"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        print("Using wkhtmltopdf for PDF generation...")
        subprocess.run(
            ["wkhtmltopdf", "--enable-local-file-access", input_html, output_pdf],
            check=True,
        )
        print(f"Successfully generated {output_pdf}")
        return
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    # Strategy 3: Check for playwright
    try:
        import asyncio

        from playwright.async_api import async_playwright

        async def run():
            async with async_playwright() as p:
                browser = await p.chromium.launch()
                page = await browser.new_page()
                await page.goto(f"file://{os.path.abspath(input_html)}")
                await page.pdf(
                    path=output_pdf, format="A4", landscape=True, print_background=True
                )
                await browser.close()

        print("Using playwright for PDF generation...")
        asyncio.run(run())
        print(f"Successfully generated {output_pdf}")
        return
    except ImportError:
        pass

    print("Error: No PDF generation tool found.")
    print("Please install one of the following:")
    print("1. Chromium/Google Chrome: sudo apt install chromium-browser")
    print("2. wkhtmltopdf: sudo apt install wkhtmltopdf")
    print("3. Playwright: pip install playwright && playwright install chromium")
    sys.exit(1)


if __name__ == "__main__":
    main()
