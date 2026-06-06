from pydantic import ValidationError
from schemas import Book, BookSell
from service import buy_book, sell_book

# ------------------------------------------

# --- ЭТОТ КОД НЕ МЕНЯЙ. ОН ДОЛЖЕН ЗАРАБОТАТЬ ---
if __name__ == "__main__":
    print("Начинаем симуляцию магазина...")

    buy_info = {
        "book_name": "Python Crash Course2",
        "count": 10,
        "buy_price": 1000,
        "sell_price": 1111,
        "author_name": "21",
        "genre": "python",
        "language": "en",
        "year": 2001,
    }
    book_class = Book(**buy_info)

    try:
        buy_book_class = Book(**buy_info)
        buy_book(buy_book_class)
    except ValidationError:
        print("Ошибка валидации")

    sell_info_1 = {
        "book_name": "Python Crash Course2",
        "count": 2,
    }
    sell_info_2 = {
        "book_name": "Python Crash Course2",
        "count": 3,
    }
    sell_info_3 = {
        "book_name": "Python Crash Course2",
        "count": 10,
    }

    try:
        sell_book_class_1 = BookSell(**sell_info_1)
        sell_book_class_2 = BookSell(**sell_info_2)
        sell_book_class_3 = BookSell(**sell_info_3)

        sell_book(sell_book_class_1)
        sell_book(sell_book_class_2)

        # 3. Пытаемся продать больше, чем есть на складе

        sell_book(sell_book_class_3)
        print("ОШИБКА: Твой код позволил продать 100 книг, хотя на складе их всего 5!")
    except ValidationError:
        print("Ошибка валидации")
    except ValueError:
        print("ОТЛИЧНО: Твой код правильно заблокировал продажу (выдал ValueError).")

    print("Симуляция завершена. Проверь файлы book.json и transaction.json!")
