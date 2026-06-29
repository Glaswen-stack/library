from sqlalchemy import ForeignKey, Column, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    book_name = Column(String, nullable=False)
    count = Column(Integer, nullable=False)
    buy_price = Column(Integer, nullable=False)
    sell_price = Column(Integer, nullable=False)
    genre = Column(String, nullable=False)
    language = Column(String, nullable=False)
    year = Column(Integer, nullable=False)

    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False)

    author = relationship("Author", back_populates="books")
    transactions = relationship("Transaction", back_populates="book")


class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True, index=True)
    author_name = Column(String, nullable=False)

    books = relationship("Book", back_populates="author")


class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    book_name = Column(String, nullable=False)
    count = Column(Integer, nullable=False)
    transaction_type = Column(String, nullable=False)
    price = Column(Integer, nullable=False)

    book = relationship("Book", back_populates="transactions")
