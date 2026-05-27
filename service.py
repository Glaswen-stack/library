import json
import os

from typing import Optional
from schemas import Book, BookSell, Transaction, Author

def get_all_books() -> list:
    books = load_data("book.json")
    return books

def get_all_transactions() -> list:
    transactions = load_data("transactions.json")
    return transactions


def load_data(filename: str) -> list:
    if os.path.isfile(filename):
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            return data
        else:
            return [data]
    else:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=4)
        return []


def save_data(data: list, filename: str) -> Optional[list]:
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def find_book(book_name: str) -> Optional[int]:
    books = load_data("book.json")
    for i, book in enumerate(books):
        if book["book_name"] == book_name:
            return i
    return None


def find_author(author_name: str) -> Optional[int]:
    authors = load_data("authors.json")
    for i, author in enumerate(authors):
        if author["author_name"] == author_name:
            return i
    return None


def buy_book(book: Book) -> None:
    transactions_data = Transaction(
        book_name=book.book_name,
        count=book.count,
        transaction_type="buy",
        price=book.buy_price,
    )

    transactions = load_data("transactions.json")
    transactions.append(transactions_data.model_dump())
    save_data(transactions, "transactions.json")

    # РАБОТА С КНИГАМИ

    books = load_data("book.json")
    index = find_book(book.book_name)
    if index is not None:
        books[index]["count"] += book.count
    else:
        books.append(book.model_dump())

    save_data(books, "book.json")

    # РАБОТА С АВТОРАМИ
    author_data = Author(
        author_name=book.author_name,
    )

    authors = load_data("authors.json")
    author_index = find_author(book.author_name)
    if author_index is None:
        authors.append(author_data.model_dump())
        save_data(authors, "authors.json")


def sell_book(book: BookSell) -> None:
    books = load_data("book.json")
    index = find_book(book.book_name)
    if index is None:
        raise ValueError(f"Книга {book.book_name} не найдена!")

    elif books[index]["count"] < book.count:
        raise ValueError(f"Книг {book.book_name} недостаточно для продажи")
    else:
        books[index]["count"] -= book.count
        print(f"{book.book_name} было продано {book.count} шт!")
        price = books[index]["sell_price"]
        save_data(books, "book.json")
        transactions_data = Transaction(
            book_name=book.book_name,
            count=book.count,
            transaction_type="sell",
            price=price,
        )

        transactions = load_data("transactions.json")
        transactions.append(transactions_data.model_dump())
        save_data(transactions, "transactions.json")