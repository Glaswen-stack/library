import json
import urllib.request

BASE_URL = "http://127.0.0.1:8000"


id_purchased_book = None


def api_get_books():
    req = urllib.request.Request(f"{BASE_URL}/inventory", method="GET")
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode("utf-8"))


def api_get_transactions():
    req = urllib.request.Request(f"{BASE_URL}/transactions", method="GET")
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode("utf-8"))


def api_get_authors():
    req = urllib.request.Request(f"{BASE_URL}/authors", method="GET")
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode("utf-8"))


def api_get_book_count(book_name):
    books = api_get_books()
    for b in books:
        if b.get("book_name") == book_name:
            return b.get("count", 0)
    return 0


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

    count_before = api_get_book_count(book_data["book_name"])

    json_data = json.dumps(book_data).encode("utf-8")
    req = urllib.request.Request(
        f"{BASE_URL}/books/purchase", data=json_data, method="POST"
    )
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req) as response:
            assert response.status == 200
            books = api_get_books()
            saved_book = None
            for b in books:
                if b["book_name"] == book_data["book_name"]:
                    saved_book = b
                    global id_purchased_book
                    id_purchased_book = b["id"]
                    break
            count_after = count_before + book_data["count"]
            assert saved_book is not None
            assert saved_book["book_name"] == book_data["book_name"]
            assert saved_book["count"] == count_after
            print("✅ POST /books/purchase книга создана/найдена, count изменен")
    except Exception as e:
        print(f"❌ Ошибка в books/purchase: {e}")

    authors = api_get_authors()
    saved_author = None
    for a in authors:
        if a["author_name"] == book_data["author_name"]:
            saved_author = a
            break
    if saved_author["author_name"] == book_data["author_name"]:
        print("✅ POST /books/purchase автор найден")
    else:
        print(f"❌ Ошибка в books/purchase: автор не найден {book_data['author_name']}")

    transactions = api_get_transactions()
    saved_transaction = None
    for t in transactions:
        if t["book_name"] == book_data["book_name"]:
            saved_transaction = t
            break
    if (
        saved_transaction["count"] == book_data["count"]
        and saved_transaction["transaction_type"] == "buy"
    ):
        print("✅ POST /books/purchase транзакция найдена")
    else:
        print(f"❌ Ошибка в books/purchase: транзакция не найдена")


def test_sell_book():
    data = {
        "book_name": "Test",
        "count": 5,
    }

    count_before = api_get_book_count(data["book_name"])
    if count_before == 0:
        print("❌ Тест продажи пропущен: книга отсутствует или нет на складе")
        return

    json_data = json.dumps(data).encode("utf-8")
    req = urllib.request.Request(
        f"{BASE_URL}/books/sell", data=json_data, method="POST"
    )
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req) as response:
            assert response.status == 200
            count_after = api_get_book_count(data["book_name"])
            assert count_after == count_before - data["count"]

        transactions = api_get_transactions()
        saved_transaction = None
        for t in transactions:
            if t["book_name"] == data["book_name"] and t["transaction_type"] == "sell":
                saved_transaction = t
                break
        if (
            saved_transaction["count"] == data["count"]
            and saved_transaction["transaction_type"] == "sell"
        ):
            print("✅ POST /books/sell транзакция найдена")
        else:
            print(f"❌ Ошибка в books/sell: транзакция не найдена")

        print(f"✅ POST /books/sell ручка исполнена")
    except Exception as e:
        print(f"❌ Ошибка в books/sell: {e}")


def test_get_book_by_id():
    global id_purchased_book
    book_id = id_purchased_book
    url = f"{BASE_URL}/books/{book_id}"
    req = urllib.request.Request(url, method="GET")
    try:
        with urllib.request.urlopen(req) as response:
            assert response.status == 200
            data = response.read().decode("utf-8")
            book = json.loads(data)
            assert book.get("book_name") == "Test"
            assert "book_name" in book
            print(f" id книги {book_id} книга называется {book['book_name']}")
            print(
                f"✅ GET /books_by_id Книга с id={book_id} найдена: {book['book_name']}"
            )
    except Exception as e:
        print(f"❌ Ошибка /books/book_id: {e}")


def test_books_list():
    req = urllib.request.Request(f"{BASE_URL}/books")
    try:
        with urllib.request.urlopen(req) as response:
            assert response.status == 200
            data = response.read().decode("utf-8")
            books = json.loads(data)
            assert isinstance(books, list)
            assert len(books) >= 0
            print(f"✅ GET /books возвращает список")
    except Exception as e:
        print(f"❌ Ошибка в /books: {e}")


def test_inventory():
    try:
        inventory = api_get_books()
        assert isinstance(inventory, list)
        assert len(inventory) >= 0
        print("✅ GET /inventory возвращает список")
    except Exception as e:
        print(f"❌ Ошибка в /inventory: {e}")


def test_transaction_list():
    try:
        transactions = api_get_transactions()
        assert isinstance(transactions, list)
        assert len(transactions) >= 0
        print("✅ GET /transactions возвращает список")
    except Exception as e:
        print(f"❌ Ошибка в /transactions: {e}")


def test_authors_list():
    try:
        authors = api_get_authors()
        assert isinstance(authors, list)
        print("✅ GET /authors возвращает список авторов")
    except Exception as e:
        print(f"❌ Ошибка в GET /authors: {e}")


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
    test_authors_list()
    test_inventory()
    test_profit()
