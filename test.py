# from pydantic import BaseModel, Field
#
# class Product(BaseModel):
#     buy_price: int = Field(gt=0)
#     sell_price: int = Field(gt=0)
#
# try:
#     p = Product(buy_price=-1000, sell_price=500)
# except Exception as e:
#     print(f"Ошибка: {e}")