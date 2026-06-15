import json
import urllib.request
import urllib.error

from service import load_data

BASE_URL = "http://127.0.0.1:8000"


def test_health():
    req = urllib.request.Request(f"{BASE_URL}/health")
    try:
        with urllib.request.urlopen(req) as response:
            assert response.status == 200
            print("✅ GET /health работает")
    except Exception as e:
        print(f"❌ Ошибка в GET /health: {e}")


def test_purchase():
    book_data = {
        "book_name": "Test",
        "count": 10,
        "buy_price": 100,
        "sell_price": 1000,
        "author_name": "Author",
        "genre": "Fiction",
        "language": "en",
        "year": 2023,
    }

    books_before = load_data("book.json")
    count_before = 0
    for book in books_before:
        if book["book_name"] == book_data["book_name"]:
            count_before = book["count"]
            break

    json_data = json.dumps(book_data).encode("utf-8")
    req = urllib.request.Request(
        f"{BASE_URL}/books/purchase", data=json_data, method="POST"
    )
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req) as response:
            assert response.status == 200
            books = load_data("book.json")
            saved_book = next(
                (b for b in books if b["book_name"] == book_data["book_name"]), None
            )
            assert saved_book["book_name"] == book_data["book_name"]
            print("✅ POST /books/purchase книга создана и найдена")
            count_after = count_before + book_data["count"]
            assert saved_book["count"] == count_after
            print("✅ POST /books/purchase count изменен")
    except Exception as e:
        print(f"❌ Ошибка в books/purchase: {e}")

    authors = load_data("authors.json")
    saved_author = next(
        (a for a in authors if a["author_name"] == book_data["author_name"]), None
    )
    if saved_author["author_name"] == book_data["author_name"]:
        print("✅ POST /books/purchase автор найден")
    else:
        print(f"❌ Ошибка в books/purchase: автор не найден {book_data['author_name']}")

    transactions = load_data("transactions.json")
    saved_transaction = next(
        (
            t
            for t in transactions
            if t["book_name"] == book_data["book_name"]
            and t["transaction_type"] == "buy"
        ),
        None,
    )
    if (
        saved_transaction["count"] == book_data["count"]
        and saved_transaction["price"] == book_data["buy_price"]
    ):
        print("✅ POST /books/purchase транзакция найдена")
    else:
        print(f"❌ Ошибка в books/purchase: транзакция не найдена")


def test_sell_book():
    url = f"{BASE_URL}/books/sell"
    data = {
        "book_name": "Test",
        "count": 1,
    }
    json_data = json.dumps(data).encode("utf-8")
    req = urllib.request.Request(url, data=json_data, method="POST")
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req) as response:
            assert response.status == 200
            print(f"✅ POST /books/sell ручка исполнена")
    except Exception as e:
        print(f"❌ Ошибка в books/sell: {e}")


def test_get_book_by_id():
    book_id = 1
    url = f"{BASE_URL}/books/{book_id}"
    req = urllib.request.Request(url, method="GET")
    try:
        with urllib.request.urlopen(req) as response:
            assert response.status == 200
            data = response.read().decode("utf-8")
            book = json.loads(data)
            assert book.get("book_name") == "Test"
            assert "book_name" in book
            print(f"✅ Книга с id={book_id} найдена: {book['book_name']}")
    except urllib.error.HTTPError as e:
        print(f"❌ Ошибка /books/book_id {e.code}: {e.reason}")


def test_books_list():
    req = urllib.request.Request(f"{BASE_URL}/books")
    try:
        with urllib.request.urlopen(req) as response:
            assert response.status == 200
            data = response.read().decode("utf-8")
            books = json.loads(data)
            assert isinstance(books, list)
            assert len(books) >= 0
            print("✅ GET /books возвращает список")
    except Exception as e:
        print(f"❌ Ошибка в /books: {e}")


def test_inventory():
    req = urllib.request.Request(f"{BASE_URL}/inventory")
    try:
        with urllib.request.urlopen(req) as response:
            assert response.status == 200
            data = response.read().decode("utf-8")
            inventory = json.loads(data)
            assert isinstance(inventory, list)
            assert len(inventory) >= 0
            print("✅ GET /inventory возвращает список")
    except Exception as e:
        print(f"❌ Ошибка в /inventory: {e}")


def test_transaction_list():
    req = urllib.request.Request(f"{BASE_URL}/transactions")
    try:
        with urllib.request.urlopen(req) as response:
            assert response.status == 200
            data = response.read().decode("utf-8")
            transactions = json.loads(data)
            assert isinstance(transactions, list)
            assert len(transactions) >= 0
            print("✅ GET /transactions возвращает список")
    except Exception as e:
        print(f"❌ Ошибка в /transactions: {e}")


def test_profit():
    req = urllib.request.Request(f"{BASE_URL}/profit", method="GET")
    try:
        with urllib.request.urlopen(req) as response:
            assert response.status == 200
            data = response.read().decode("utf-8")
            profit_data = json.loads(data)
            assert "revenue" in profit_data
            assert "expenses" in profit_data
            assert "profit" in profit_data
            print(
                f"✅ GET /profit работает: revenue={profit_data['revenue']}, expenses={profit_data['expenses']}, profit={profit_data['profit']}"
            )
    except Exception as e:
        print(f"❌ Ошибка в GET /profit: {e}")


if __name__ == "__main__":
    print("Запуск проверок API...")
    test_health()
    test_purchase()
    test_sell_book()
    test_books_list()
    test_get_book_by_id()
    test_transaction_list()
    test_inventory()
    test_profit()
