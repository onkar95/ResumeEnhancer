from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from playwright.async_api import Browser, async_playwright

from app.schemas.resume import ResumeDocument

_playwright = None
_browser: Browser | None = None

TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "templates"
_env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)))

async def close_browser():
    global _browser, _playwright
    if _browser:
        await _browser.close()
        _browser = None
    if _playwright:
        await _playwright.stop()
        _playwright = None
        
async def get_browser() -> Browser:
    global _playwright, _browser
    if _browser is None:
        _playwright = await async_playwright().start()
        _browser = await _playwright.chromium.launch(headless=True)
    return _browser


def render_resume_html(resume: ResumeDocument) -> str:
    template = _env.get_template("resume_pdf.html")
    return template.render(resume=resume)


# async def generate_resume_pdf(resume: ResumeDocument) -> bytes:
#     """
#     Renders the resume to real, selectable-text PDF using headless
#     Chromium via Playwright -- avoids WeasyPrint's native Pango/GLib
#     dependency, which has no clean install path on Windows.
#     """

#     html_content = render_resume_html(resume)

#     async with async_playwright() as p:

#         browser = await p.chromium.launch(headless=True)

#         page = await browser.new_page()

#         await page.set_content(html_content, wait_until="networkidle")

#         pdf_bytes = await page.pdf(
#             format="A4",
#             print_background=True,
#             margin={
#                 "top": "12mm",
#                 "right": "12mm",
#                 "bottom": "12mm",
#                 "left": "12mm",
#             },
#         )

#         await browser.close()

#     return pdf_bytes


async def generate_resume_pdf(resume: ResumeDocument) -> bytes:
    html_content = render_resume_html(resume)
    browser = await get_browser()
    page = await browser.new_page()
    try:
        await page.set_content(html_content, wait_until="networkidle")
        pdf_bytes = await page.pdf(
            format="A4", print_background=True,
            margin={"top": "12mm", "right": "12mm",
                    "bottom": "12mm", "left": "12mm"},
        )
    finally:
        await page.close()   # close the page, not the browser
    return pdf_bytes
