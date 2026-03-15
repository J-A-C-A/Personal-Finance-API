from fastapi import FastAPI
from dataBase import db,Wydatek,Session
from datetime import datetime

app = FastAPI()

@app.get("/")
def health_check():
    return "API działa"

@app.post("/Nowy")
def add_Wydatek(data,kwota,metoda_platnosci,kategoria,grupa,opis):
    data_format = "%d.%m.%Y"
    wyd = Wydatek()
    wyd.data = datetime.strptime(data,data_format)
    wyd.kwota = kwota
    wyd.metoda_platnosci = metoda_platnosci
    wyd.kategoria = kategoria
    wyd.grupa = grupa
    wyd.opis = opis
    with Session(db) as session:
        session.add(wyd)
        session.commit()


