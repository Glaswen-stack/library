import json
import os

def buy_book(book_name, count, buy_price, sell_price, author_name, genre, language, year):
    transactions_data = {
        "book_name": book_name,
        "count": count,
        "transaction_type": "buy",
        "price": buy_price,
    }

    if os.path.isfile("transactions.json"):
        with open("transactions.json", "r", encoding="utf-8") as f:
            transactions = json.load(f)
            transactions.append(transactions_data)
            with open("transactions.json", "w", encoding="utf-8") as f:
                json.dump(transactions, f, ensure_ascii=False, indent=4)
    else:
        with open("transactions.json", "w", encoding="utf-8") as f:
            json.dump([transactions_data], f, ensure_ascii=False, indent=4)
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
        with open("book.json", "r", encoding="utf-8") as f:
            books = json.load(f)
        found = False
        for book in books:
            if book["book_name"] == book_name and book["author_name"] == author_name:
                book["count"] += count
                found = True
                with open("book.json", "w", encoding="utf-8") as f:
                    json.dump(books, f, ensure_ascii=False, indent=4)
                break
        if not found:
            with open("book.json", "r", encoding="utf-8") as f:
                books = json.load(f)
            books.append(book_data)
            with open("book.json", "w", encoding="utf-8") as f:
                json.dump(books, f, ensure_ascii=False, indent=4)
    else:
        with open("book.json", "w", encoding="utf-8") as f:
            json.dump([book_data], f, ensure_ascii=False, indent=4)
    #РАБОТА С АВТОРАМИ
    author_data = {
        "author_name": author_name,
    }
    if os.path.isfile("authors.json"):
        with open("authors.json", "r", encoding="utf-8") as f:
            authors = json.load(f)
        found = False
        for author in authors:
            if author["author_name"] == author_name:
                found = True
                with open("authors.json", "w", encoding="utf-8") as f:
                    json.dump(authors, f, ensure_ascii=False, indent=4)
                break
        if not found:
            with open("authors.json", "r", encoding="utf-8") as f:
                authors = json.load(f)
            authors.append(author_data)
            with open("authors.json", "w", encoding="utf-8") as f:
                json.dump(authors, f, ensure_ascii=False, indent=4)
    else:
        with open("authors.json", "w", encoding="utf-8") as f:
            json.dump([author_data], f, ensure_ascii=False, indent=4)


def sell_book(book_name, count):

    with open("book.json", "r", encoding="utf-8") as f:
        books = json.load(f)
    found = False
    for book in books:
        if book["book_name"] == book_name and book["count"] >= count:
            book["count"] -= count
            found = True
            price = book["sell_price"]
            print(f"{book_name} продано {count} шт.")
            with open("book.json", "w", encoding="utf-8") as f:
                json.dump(books, f, ensure_ascii=False, indent=4)
            transactions_data = {
                "book_name": book_name,
                "count": count,
                "transaction_type": "sell",
                "price": price,
            }
            if os.path.isfile("transactions.json"):
                with open("transactions.json", "r", encoding="utf-8") as f:
                    transactions = json.load(f)
                    transactions.append(transactions_data)
                    with open("transactions.json", "w", encoding="utf-8") as f:
                        json.dump(transactions, f, ensure_ascii=False, indent=4)
            break
        elif book["book_name"] == book_name and book["count"] < count:
            raise ValueError (f"Книг {book_name} недостаточно для продажи")


    if not found:
        print(f"Книга {book_name} не найдена")


# ------------------------------------------

# --- ЭТОТ КОД НЕ МЕНЯЙ. ОН ДОЛЖЕН ЗАРАБОТАТЬ ---
if __name__ == "__main__":
    print("Начинаем симуляцию магазина...")

    # 1. Закупаем книги на склад
    buy_book(
        book_name="Python Crash Course2",
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
