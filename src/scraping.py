import requests
from bs4 import BeautifulSoup

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
                    # Fallback: text before the author link
                    text = author_tag.previous_sibling.strip(" ,") if author_tag else ""
                    title = text.strip("“”\" ")

                winner = li.find("span", class_="winner") is not None

                print(category, title, author, winner, year)