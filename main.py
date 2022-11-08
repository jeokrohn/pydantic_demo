#!/usr/bin/env python
"""
Simple demo script to read informtion from a REST API and deserialize results into Python objecte
"""
from dataclasses import dataclass

class ListBooksResponse(BaseModel)

@dataclass
class Gutendex:
    """
    The simple API
    """
    endpoint = 'https://gutendex.com/books/'

    def list_of_books(self):

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
