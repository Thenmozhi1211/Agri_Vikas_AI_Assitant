import sys
from pathlib import Path

# Add project root directory to Python search path
sys.path.append(str(Path(__file__).resolve().parent.parent))

# Rest of your imports follow...
from config.settings import AGRI_URL, RAW_DIR, CLEANED_DIR
from pathlib import Path
from datetime import datetime

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

from config.settings import AGRI_URL, RAW_DIR, CLEANED_DIR


def clean_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup([
        "script",
        "style",
        "noscript",
        "svg",
        "nav",
        "footer",
    ]):
        tag.decompose()

    text = soup.get_text(separator="\n")

    lines = []

    for line in text.splitlines():
        line = line.strip()

        if line:
            lines.append(line)

    return "\n".join(lines)


def scrape_agrisnet():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    raw_file = RAW_DIR / f"agrisnet_{timestamp}.html"
    text_file = CLEANED_DIR / f"agrisnet_{timestamp}.txt"

    print("Opening Agrisnet...")
    print(AGRI_URL)

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True)

        page = browser.new_page()

        page.goto(
            AGRI_URL,
            wait_until="domcontentloaded",
            timeout=60000
        )

        page.wait_for_timeout(3000)

        html = page.content()

        title = page.title()

        raw_file.write_text(
            html,
            encoding="utf-8"
        )

        cleaned_text = clean_html(html)

        text_file.write_text(
            cleaned_text,
            encoding="utf-8"
        )

        browser.close()

    print("\nScraping completed.")
    print(f"Title : {title}")
    print(f"HTML  : {raw_file}")
    print(f"Text  : {text_file}")

    return text_file


if __name__ == "__main__":
    scrape_agrisnet()