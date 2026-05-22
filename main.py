import json
import os
from gettext import translation

from schemas import Book, Transaction, Author


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

def save_data(data: list, filename: str) -> list | None:
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def find_book(book_name: str) -> int | None:
    books = load_data("book.json")
    for i, book in enumerate(books):
        if book["book_name"] == book_name:
            return i
    return None



def find_author(author_name: str) -> int | None:
    authors = load_data("authors.json")
    for i, author in enumerate(authors):
        if author["author_name"] == author_name:
            return i
    return None


def buy_book(book_name: str, count: int, buy_price: int, sell_price: int, author_name: str,
             genre: str, language: str, year: int) -> None:
    transactions_data = {
        "book_name": book_name,
        "count": count,
        "transaction_type": "buy",
        "price": buy_price,
    }

    transactions = load_data("transactions.json")
    transactions.append(transactions_data)
    save_data(transactions, "transactions.json")

    #РАБОТА С КНИГАМИ
    book_data = {
        "book_name": book_name,
        "count": count,
        "buy_price": buy_price,
        "sell_price": sell_price,
        "author_name": author_name,
        "genre": genre,
        "language": language,
        "year": year,
    }

    books = load_data("book.json")
    index = find_book(book_name)
    if index is not None:
        books[index]["count"] += count
    else:
        books.append(book_data)

    save_data(books, "book.json")

    #РАБОТА С АВТОРАМИ
    author_data = {
        "author_name": author_name,
    }

    authors = load_data("authors.json")
    author_index = find_author(author_name)
    if author_index is None:
        authors.append(author_data)
        save_data(authors, "authors.json")


def sell_book(book_name: str, count: int) -> None:
    books = load_data("book.json")
    index = find_book(book_name)
    if index is None:
        raise ValueError(f"Книга {book_name} не найдена!")

    elif books[index]["count"] < count:
        raise ValueError (f"Книг {book_name} недостаточно для продажи")
    else:
        books[index]["count"] -= count
        print(f"{book_name} было продано {count} шт!")
        price = books[index]["sell_price"]
        save_data(books, "book.json")
        transactions_data = {
            "book_name": book_name,
            "count": count,
            "transaction_type": "sell",
            "price": price,
        }

        transactions = load_data("transactions.json")
        transactions.append(transactions_data)
        save_data(transactions, "transactions.json")



# ------------------------------------------

# --- ЭТОТ КОД НЕ МЕНЯЙ. ОН ДОЛЖЕН ЗАРАБОТАТЬ ---
if __name__ == "__main__":
    print("Начинаем симуляцию магазина...")

    book_info = {
        "book_name": "Python Crash Course2",
        "count": 10,
        "buy_price": 1000,
        "sell_price": 1111,
        "author_name": "21",
        "genre": "python",
        "language": "en",
        "year": 2001,
    }
    book_class = Book(**book_info)
    author_class = Author(author_name=book_class.author_name)
    translation_class = Transaction(
        book_name=book_class.book_name,
        transaction_type="buy",
        price=book_class.buy_price,
        count=book_class.count,
    )
    try:
        buy_book(
            book_name=book_class.book_name,
            count=book_class.count,
            buy_price=book_class.buy_price,
            sell_price=book_class.sell_price,
            author_name=book_class.author_name,
            genre=book_class.genre,
            language=book_class.language,
            year=book_class.year
        )
    except ValueError:
        print("Ошибка валидации")



    # 1. Закупаем книги на склад
    # buy_book(
    #     book_name="Python Crash Course2",
    #     count=10,
    #     buy_price=-1000,
    #     sell_price=1111,
    #     author_name="author",
    #     genre="python",
    #     language="en",
    #     year=2001,
    # )
     # 2. Продаем пару книг
    sell_book(book_name=book_class.book_name, count=3)
    sell_book(book_name=book_class.book_name, count=2)

    # 3. Пытаемся продать больше, чем есть на складе
    try:
        sell_book(book_name=book_class.book_name, count=-100)
        print("ОШИБКА: Твой код позволил продать 100 книг, хотя на складе их всего 5!")
    except ValueError:
        print("ОТЛИЧНО: Твой код правильно заблокировал продажу (выдал ValueError).")

    print("Симуляция завершена. Проверь файлы book.json и transaction.json!")
