from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import func

from models import Book as BookModel
from models import Author as AuthorModel
from models import Transaction as TransactionModel

from schemas import Book, BookSell, ProfitInfo


def get_all_books(db: Session) -> list[BookModel]:
    return db.query(BookModel).all()


def get_book_by_id(db: Session, book_id: int) -> BookModel | None:
    return db.query(BookModel).filter(BookModel.id == book_id).first()


def get_book_list(db: Session) -> list[dict]:
    books = db.query(BookModel.id, BookModel.title).all()
    return [
        {
            "id": b.id,
            "title": b.title,
        }
        for b in books
    ]


def get_transaction_list(db: Session) -> list[TransactionModel]:
    return db.query(TransactionModel).all()


def get_authors_list(db: Session) -> list[AuthorModel]:
    return db.query(AuthorModel).all()


def get_profit(db: Session) -> ProfitInfo:
    total_buy = (
        db.query(func.sum(TransactionModel.price * TransactionModel.count))
        .filter(TransactionModel.transaction_type == "buy")
        .scalar()
        or 0
    )
    total_sell = (
        db.query(func.sum(TransactionModel.price * TransactionModel.count))
        .filter(TransactionModel.transaction_type == "sell")
        .scalar()
        or 0
    )
    profit = total_sell - total_buy
    return ProfitInfo(revenue=total_sell, expenses=total_buy, profit=profit)


def buy_book(db: Session, book_data: Book) -> BookModel:
    author = (
        db.query(AuthorModel)
        .filter(AuthorModel.author_name == book_data.author_name)
        .first()
    )
    if not author:
        author = AuthorModel(author_name=book_data.author_name)
        db.add(author)
        db.commit()
        db.refresh(author)

    book = db.query(BookModel).filter(BookModel.title == book_data.book_name).first()

    if book:
        book.count += book_data.count
    else:
        book = BookModel(
            title=book_data.book_name,
            count=book_data.count,
            buy_price=book_data.buy_price,
            sell_price=book_data.sell_price,
            genre=book_data.genre,
            language=book_data.language,
            year=book_data.year,
            author_id=author.id,
        )
        db.add(book)
    db.commit()
    db.refresh(book)

    transaction = TransactionModel(
        book_id=book.id,
        title=book.title,
        transaction_type="buy",
        count=book_data.count,
        price=book_data.buy_price,
    )
    db.add(transaction)
    db.commit()

    return book


def sell_book(db: Session, sell_data: BookSell) -> BookModel:
    book = db.query(BookModel).filter(BookModel.title == sell_data.book_name).first()
    if not book:
        raise ValueError(f"Книга '{sell_data.book_name}' не найдена")
    if book.count < sell_data.count:
        raise ValueError(f"Недостаточно книг '{sell_data.book_name}' на складе")

    book.count -= sell_data.count

    transaction = TransactionModel(
        book_id=book.id,
        title=book.title,
        transaction_type="sell",
        count=sell_data.count,
        price=book.sell_price,
    )
    db.add(transaction)
    db.commit()
    db.refresh(book)
    return book
