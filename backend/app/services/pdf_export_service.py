from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from playwright.async_api import async_playwright

from app.schemas.resume import ResumeDocument

TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "templates"
_env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)))


def render_resume_html(resume: ResumeDocument) -> str:
    template = _env.get_template("resume_pdf.html")
    return template.render(resume=resume)


async def generate_resume_pdf(resume: ResumeDocument) -> bytes:
    """
    Renders the resume to real, selectable-text PDF using headless
    Chromium via Playwright -- avoids WeasyPrint's native Pango/GLib
    dependency, which has no clean install path on Windows.
    """

    html_content = render_resume_html(resume)

    async with async_playwright() as p:

        browser = await p.chromium.launch(headless=True)

        page = await browser.new_page()

        await page.set_content(html_content, wait_until="networkidle")

        pdf_bytes = await page.pdf(
            format="A4",
            print_background=True,
            margin={
                "top": "12mm",
                "right": "12mm",
                "bottom": "12mm",
                "left": "12mm",
            },
        )

        await browser.close()

    return pdf_bytes