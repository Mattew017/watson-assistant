import requests
from bs4 import BeautifulSoup

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}
HOST = 'https://libgen.is/'
URL = 'https://libgen.is/search.php?req='


def search_books(string: str, count_of_books=5):
    """
    parse https://libgen.is for books
    :param string: search string
    :param count_of_books: count of searching books
    :return: list of books url's
    """
    req = requests.get(URL + string, headers=HEADERS)
    soup = BeautifulSoup(req.content, features="html.parser")
    books = soup.find_all('tr', valign='top')
    list_of_books = []
    count = 0
    for book in books:
        for ref in book.find_all('a', title=""):
            reference = (ref['href'])
            if reference.startswith('book'):
                if count >= count_of_books:
                    return list_of_books
                list_of_books.append(HOST + reference)
                count += 1
    return list_of_books


