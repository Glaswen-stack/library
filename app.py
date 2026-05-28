from http.client import HTTPException

from fastapi import FastAPI

from schemas import Book, BookSell
from service import (buy_book, sell_book, get_all_books,
                     get_all_transactions, get_book_by_id,
                     get_book_list, get_profit)

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
async def get_books():
    list_books = get_book_list()
    return list_books

@app.get("/inventory")
async def get_inventory():
    inventory = get_all_books()
    return inventory


@app.get("/books/{book_id}")
async def get_book(book_id: int):
    book = get_book_by_id(book_id)
    if book is None:
        raise HTTPException
    return book

@app.get("/transactions")
async def transactions_list():
    transactions = get_all_transactions()
    return transactions

@app.get("/profit")
async def profit_for_books():
    profit = get_profit()
    return profit

@app.get("/health")
async def health():
    return {"status": "ok"}