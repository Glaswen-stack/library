from fastapi import FastAPI, HTTPException, Depends


from sqlalchemy.orm import Session
from database import get_db

from schemas import Book, BookSell, Author
from service import (
    buy_book,
    sell_book,
    get_all_books,
    get_book_by_id,
    get_book_list,
    get_profit,
    get_transaction_list,
    get_authors_list,
)

app = FastAPI(title="Book Store API")


@app.post("/books/purchase")
async def purchase_book(book_data: Book, db: Session = Depends(get_db)):
    try:
        purchased_book = buy_book(db, book_data)
        return {
            "id": purchased_book.id,
            "title": purchased_book.title,
            "count": purchased_book.count,
            "buy_price": purchased_book.buy_price,
            "sell_price": purchased_book.sell_price,
            "author": purchased_book.author,
            "genre": purchased_book.genre,
            "language": purchased_book.language,
            "year": purchased_book.year,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/books/sell")
async def sell_books(book_data: BookSell, db: Session = Depends(get_db)):
    try:
        sold_book = sell_book(db, book_data)
        return {
            "title": sold_book.title,
            "count": book_data.count,
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/books")
async def get_books(db: Session = Depends(get_db)):
    try:
        list_books = get_book_list(db)
        return list_books
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/inventory")
async def get_inventory(db: Session = Depends(get_db)):
    try:
        inventory = get_all_books(db)
        return inventory
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/books/{book_id}")
async def get_book(book_id: int, db: Session = Depends(get_db)):
    try:
        book = get_book_by_id(db, book_id)
        if book is None:
            raise HTTPException(status_code=404, detail="Book not found")
        return book
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/transactions")
async def transactions_list(db: Session = Depends(get_db)):
    try:
        transactions = get_transaction_list(db)
        return transactions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/authors", response_model=list[Author])
async def get_authors(db: Session = Depends(get_db)):
    try:
        authors = get_authors_list(db)
        return authors
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/profit")
async def profit_for_books(db: Session = Depends(get_db)):
    try:
        profit = get_profit(db)
        return profit
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health():
    return {"status": "ok"}
