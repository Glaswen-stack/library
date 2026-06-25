from database import engine, Base, SessionLocal
from sqlalchemy import text

from models import Base

# db = SessionLocal()
# try:
#     result = db.execute(text("SELECT name FROM sqlite_master WHERE type='table';"))
#     tables = result.fetchall()
#     print("Список таблиц:", tables)
# finally:
#     db.close()

Base.metadata.create_all(engine)
print("Tables created")
