from fastapi import FastAPI

from schemas import Book, BookSell
from service import buy_book, sell_book, get_all_books, get_all_transactions


app = FastAPI(title="Book Store API")


@app.post("/books/purchase")
async def purchase_book(book_data: Book):
    try:
        buy_book(book_data)
        return {"success"}
    except ValueError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}

@app.post("/books/sell")
async def sell_books(book_data: BookSell):
    try:
        sell_book(book_data)
        return {"success"}
    except ValueError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}

@app.get("/books")
async def books_list():
    books = get_all_books()
    return books

@app.get("/transactions")
async def transactions_list():
    transactions = get_all_transactions()
    return transactions
