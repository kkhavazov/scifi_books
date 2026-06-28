import requests
import pandas as pd

def get_isbn_by_title(title):
    url = "https://openlibrary.org/search.json"


    
    try:
        response = requests.get(url + f"?title={title.replace(' ', '+').lower()}")
        data = response.json()
        if data.get("numFound", 0) > 0:
            first_match = data["docs"][0]
            book_title = first_match.get("title", "Unknown Title")
            isbn_list = first_match.get("ia212", [])
            
            if isbn_list:
                return isbn_list
            else:
                print(f"Found '{book_title}', but no ISBN is listed.")
                return data
        else:
            print("No books found matching that title.")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

book_to_search = "The Great Gatsby"
data = get_isbn_by_title(book_to_search)
print(data["docs"][0].keys())