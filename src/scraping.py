import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, text
engine = create_engine("sqlite+pysqlite:///data/scifi_books_hugo_awarded.db", echo=True)
with engine.connect() as conn:
    conn.execute(text("CREATE TABLE IF NOT EXISTS books_awarded (year int, category string, title string, author string, winner bool)"))

for year in range(1953, 2027):
    url = f"https://www.sfadb.com/Hugo_Awards_{year}"
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        for block in soup.find_all("div", class_="categoryblock"):
            category = block.find("div", class_="category").get_text(strip=True)

            for li in block.find_all("li"):
                author_tag = li.find("a")
                author = author_tag.get_text(strip=True) if author_tag else None

                # Try common title tags first
                title_tag = li.find("b") or li.find("i")

                if title_tag:
                    title = title_tag.get_text(strip=True)
                else:
                    text_author = author_tag.previous_sibling.strip(" ,") if author_tag else ""
                    title = text_author.strip("“”\" ")

                winner = li.find("span", class_="winner") is not None
                

                with engine.begin() as conn:
                    conn.execute(
                    text("""
                        INSERT INTO books_awarded
                        (year, category, title, author, winner)
                        VALUES (:year, :category, :title, :author, :winner)
                    """),
                    {
                        "year": year,
                        "category": category,
                        "title": title,
                        "author": author,
                        "winner": winner,
                    },
                )