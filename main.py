#!/usr/bin/env python
"""
Simple demo script to read informtion from a REST API and deserialize results into Python objecte
"""
import json
import logging
from collections.abc import Generator
from dataclasses import dataclass
from typing import Optional

from pydantic import BaseModel
from requests import Session

log = logging.getLogger(__name__)


class Person(BaseModel):
    """
    A person. Based on the documentation at https://gutendex.com/:
        {
          "birth_year": <number or null>,
          "death_year": <number or null>,
          "name": <string>
        }
    """
    birth_year: Optional[int]
    death_year: Optional[int]
    name: str


class Book(BaseModel):
    """
    A book. Based on the documentation at https://gutendex.com/:
        {
          "id": <number of Project Gutenberg ID>,
          "title": <string>,
          "subjects": <array of strings>,
          "authors": <array of Persons>,
          "translators": <array of Persons>,
          "bookshelves": <array of strings>,
          "languages": <array of strings>,
          "copyright": <boolean or null>,
          "media_type": <string>,
          "formats": <Format>,
          "download_count": <number>
        }
    """
    id: int
    title: str
    subjects: list[str]
    authors: list[Person]
    translators: list[Person]
    bookshelves: list[str]
    languages: list[str]
    copyright: Optional[bool]
    media_type: str
    formats: dict
    download_count: int


class ListBooksResponse(BaseModel):
    """
    Response object. Based on the documentation at https://gutendex.com/:
        Book data will be returned in the format

        {
          "count": <number>,
          "next": <string or null>,
          "previous": <string or null>,
          "results": <array of Books>
        }
        where results is an array of 0-32 book objects, next and previous are URLs to the next and previous pages of
        results, and count in the total number of books for the query on all pages combined.
    """
    count: int
    next: Optional[str]
    previous: Optional[str]
    results: list[Book]


@dataclass
class Gutendex:
    """
    The simple API
    """
    endpoint = 'https://gutendex.com/books/'

    def list_of_books(self, **params) -> Generator[Book, None, None]:
        with Session() as session:
            url = self.endpoint
            while True:
                with session.get(url=url, params=params) as r:
                    r.raise_for_status()
                    data = r.json()
                # deserialize JSON response into a ListBooksResponse object
                response = ListBooksResponse.parse_obj(data)
                log.debug(f'GET {url}: {len(response.results)} books')
                yield from response.results

                # API uses pagination; get the next URL and take it from there...
                url = response.next
                params = None
                if not url:
                    # no next page; we are done here
                    break


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    api = Gutendex()
    # get the 1st 50 books
    books = [book for book, _ in zip(api.list_of_books(), range(50))]
    print(f'Got {len(books)} books.')

    # get some French books
    books = [book for book, _ in zip(api.list_of_books(languages='fr'), range(50))]
    print(f'Got {len(books)} French books')

    # serialize one book into JSON
    book_json = books[0].json()
    print(F'book JSON: {book_json}')

    # serialize some books into JSON
    # ..directly
    books_json = json.dumps([book.dict() for book in books[:3]])
    print(books_json)

    # .. or with a helper class
    class SerializeHelper(BaseModel):
        books: list[Book]

    helper = SerializeHelper(books=books[:3])
    print(helper.json())

    # .. and avoiding the nested list in 'books'
    class SerializeHelperRoot(BaseModel):
        __root__: list[Book]

    helper = SerializeHelperRoot(__root__=books[:3])
    print(helper.json())
