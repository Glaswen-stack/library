import json
import os

def load_data(filename):
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, list):
        return data
    else:
        return [data]

def save_data(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def buy_book(book_name, count, buy_price, sell_price, author_name, genre, language, year):
    transactions_data = {
        "book_name": book_name,
        "count": count,
        "transaction_type": "buy",
        "price": buy_price,
    }

    if os.path.isfile("transactions.json"):
        transactions = load_data("transactions.json")
        transactions.append(transactions_data)
        save_data(transactions, "transactions.json")
    else:
        save_data([transactions_data], "transactions.json")

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
    if os.path.isfile("book.json"):
        books = load_data("book.json")
        found = False
        for book in books:
            if book["book_name"] == book_name and book["author_name"] == author_name:
                book["count"] += count
                found = True
                save_data(books, "book.json")
                break
        if not found:
            load_data("book.json")
            books.append(book_data)
            save_data(books, "book.json")
    else:
        save_data([book_data], "book.json")
    #РАБОТА С АВТОРАМИ
    author_data = {
        "author_name": author_name,
    }
    if os.path.isfile("authors.json"):
        authors = load_data("authors.json")
        found = False
        for author in authors:
            if author["author_name"] == author_name:
                found = True
                save_data(authors, "authors.json")
                break
        if not found:
            authors = load_data("authors.json")
            authors.append(author_data)
            save_data(authors, "authors.json")
    else:
        save_data([author_data], "authors.json")


def sell_book(book_name, count):
    books = load_data("book.json")
    found = False
    for book in books:
        if book["book_name"] == book_name and book["count"] >= count:
            book["count"] -= count
            found = True
            price = book["sell_price"]
            print(f"{book_name} продано {count} шт.")
            save_data(books, "book.json")
            transactions_data = {
                "book_name": book_name,
                "count": count,
                "transaction_type": "sell",
                "price": price,
            }
            if os.path.isfile("transactions.json"):
                transactions = load_data("transactions.json")
                transactions.append(transactions_data)
                save_data(transactions, "transactions.json")
            break

        elif book["book_name"] == book_name and book["count"] < count:
            raise ValueError (f"Книг {book_name} недостаточно для продажи")


    if not found:
        print(f"Книга {book_name} не найдена!")


# ------------------------------------------

# --- ЭТОТ КОД НЕ МЕНЯЙ. ОН ДОЛЖЕН ЗАРАБОТАТЬ ---
if __name__ == "__main__":
    print("Начинаем симуляцию магазина...")

    # 1. Закупаем книги на склад
    buy_book(
        book_name="Python Crash Course7",
        count=10,
        buy_price=1000,
        sell_price=1111,
        author_name="author3",
        genre="python",
        language="en",
        year=2001,
    )
     # 2. Продаем пару книг
    sell_book(book_name="Python Crash Course2", count=3)
    sell_book(book_name="Python Crash Course2", count=2)

    # 3. Пытаемся продать больше, чем есть на складе
    try:
        sell_book(book_name="Python Crash Course2", count=100)
        print("ОШИБКА: Твой код позволил продать 100 книг, хотя на складе их всего 5!")
    except ValueError:
        print("ОТЛИЧНО: Твой код правильно заблокировал продажу (выдал ValueError).")

    print("Симуляция завершена. Проверь файлы book.json и transaction.json!")
