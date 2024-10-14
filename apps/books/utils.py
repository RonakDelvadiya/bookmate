from bookmate.load_env_vars import var_settings
from pydantic import BaseModel, Field
from django.utils import timezone
import requests, random


class FetchBookDetailsFromIsbndb(BaseModel):
    title: str = Field(default=f"Title_{timezone.now().strftime('%Y_%m_%d_%H_%M_%S')}")
    author: str = Field(default=f"Author_{timezone.now().strftime('%Y_%m_%d_%H_%M_%S')}")
    number_of_pages: int = Field(default_factory=lambda: random.randint(1, 500), alias="number of pages of given book")


def fetch_book_details_from_isbndb(title) -> FetchBookDetailsFromIsbndb :
    url = f"https://api2.isbndb.com/books/{title}?page=1&pageSize=1&column=title"
    headers = {
        "accept": "application/json",
        "Authorization": var_settings.ISBN_API_KEY
    }
    try:
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        data = response.json()
        if data.get('books'):
            book_data = data['books'][0]
            return FetchBookDetailsFromIsbndb(
                    author=book_data.get('authors', ['Unknown'])[0],
                    number_of_pages=book_data.get('pages', 0),
                    title=book_data.get('title', title)
                )
    except (requests.RequestException, ValueError, KeyError) as e:
        print(f"Error fetching book details from ISBNDB: {e}")
    return FetchBookDetailsFromIsbndb.model_dump()