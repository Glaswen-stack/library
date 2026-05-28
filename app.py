
from fastapi import FastAPI, HTTPException
from pydantic import ValidationError

from schemas import Book, BookSell
from service import (buy_book, sell_book, get_all_books,
                     get_all_transactions, get_book_by_id,
                     get_book_list, get_profit)

app = FastAPI(title="Book Store API")


@app.post("/books/purchase")
async def purchase_book(book_data: Book):
    try:
        buy_book(book_data)
        return {"success": "purchased"}
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/books/sell")
async def sell_books(book_data: BookSell):
    try:
        sell_book(book_data)
        if book_data is None:
            raise HTTPException(status_code=404, detail="Book not found")
        else:
            return {"success": "sold"}
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/books")
async def get_books():
    try:
        list_books = get_book_list()
        return list_books
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/inventory")
async def get_inventory():
    inventory = get_all_books()
    return inventory


@app.get("/books/{book_id}")
async def get_book(book_id: int):
    try:
        book = get_book_by_id(book_id)
        if book is None:
            raise HTTPException(status_code=404, detail="Book not found")
        else:
            return book
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/transactions")
async def transactions_list():
    try:
        transactions = get_all_transactions()
        if transactions is None:
            raise HTTPException(status_code=404, detail="Transactions not found")
        else:
            return transactions
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/profit")
async def profit_for_books():
    try:
        profit = get_profit()
        if profit is None:
            raise HTTPException(status_code=404, detail="Transactions not found")
        else:
            return profit
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "ok"}