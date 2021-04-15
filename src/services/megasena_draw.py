import cfscrape
from bs4 import BeautifulSoup


def draw_numbers_supplier() -> list:
    scraper = cfscrape.create_scraper()
    page_content = scraper.get(
        "https://www.google.com/search?q=caixa+mega+sena"
    ).content
    page_soup = BeautifulSoup(page_content, "html.parser")

    draw_div = page_soup.find("div", {"class": "MDTDab"})
    draw_spans = draw_div.findChildren("span", recursive=False)
    draw_numbers = [int(span.text) for span in draw_spans]

    return draw_numbers
