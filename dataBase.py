from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import String
from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy.orm import Session
from sqlalchemy import func

connection = "sqlite:///data_base.db"
db = create_engine(connection)
class Base(DeclarativeBase):
    pass

class Wydatek(Base):
    __tablename__ = "Wydatek"
    id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(Date)
    kwota = Column(Float)
    metoda_platnosci = Column(String)
    kategoria = Column(String)
    grupa = Column(String)
    opis = Column(String)

Base.metadata.create_all(db)

