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

    return "Dodano nowy wydatek do bazy"

@app.get("/Rekordy")
def get_Wydatki(data=None,kwota=None,metoda_platnosci=None,kategoria=None,grupa=None):
    with Session(db) as session:
        query = session.query(Wydatek)
        if data is not None:
            query = query.filter(Wydatek.data == data)
        if kwota is not None:
            query = query.filter(Wydatek.kwota == kwota)
        if metoda_platnosci is not None:
            query = query.filter(Wydatek.metoda_platnosci == metoda_platnosci)
        if kategoria is not None:
            query = query.filter(Wydatek.kategoria == kategoria)
        if grupa is not None:
            query = query.filter(Wydatek.grupa == grupa)
        return query.all()
            
    
@app.put("/Aktualizuj")
def mod_Wydatek(id, data= None, kwota=None, metoda_platnosci=None, kategoria=None, grupa=None, opis=None):
    with Session(db) as session:
        to_mod = session.get(Wydatek, id)
        if to_mod is None:
            return "Podany rekord nie istnieje w bazie"
        else:
            if data is not None:
                to_mod.data = data
            if kwota is not None:
                to_mod.kwota = kwota
            if metoda_platnosci is not None:
                to_mod.metoda_platnosci = metoda_platnosci
            if kategoria is not None:
                to_mod.kategoria = kategoria
            if grupa is not None:
                to_mod.grupa = grupa
            if opis is not None:
                to_mod.opis = opis
            session.commit()
            return "Zmodyfikowano podany rekord"
        
@app.delete("/Usuń")
def del_Wydatek(id):
    with Session(db) as session:
        to_delete = session.get(Wydatek,id)
        if to_delete is None:
            return "Podany rekord nie istnieje"
        else:
            session.delete(to_delete)
            session.commit()
            return "Usunięto podany rekord"
        
       
