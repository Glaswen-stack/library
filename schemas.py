
from pydantic import BaseModel, Field, model_validator, ValidationError


class Book(BaseModel):
    book_name: str = Field(min_length=1, max_length=200)
    count: int = Field(ge=0)
    buy_price: int = Field(gt=0)
    sell_price: int = Field(gt=0)
    author_name: str = Field(min_length=2, max_length=200)
    genre: str = Field(min_length=2, max_length=100)
    language: str = Field(min_length=2, max_length=50)
    year: int = Field(ge=1000, le=2026)

    @model_validator(mode="after")
    def check_profit(self):
        if self.sell_price <= self.buy_price:
            raise ValidationError("Цена продажи должна быть больше цены покупки")
        return self

class BookSell(BaseModel):
    book_name: str = Field(min_length=1, max_length=200)
    count: int = Field(gt=0)

class Transaction(BaseModel):
    book_name: str = Field(min_length=1, max_length=200)
    count: int = Field(ge=0)
    transaction_type: str = Field(min_length=1, max_length=200)
    price: int = Field(gt=0)

class Author(BaseModel):
    author_name: str = Field(min_length=1, max_length=200)

