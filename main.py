from fastapi import FastAPI
from dataBase import db,Wydatek,Session,func
from datetime import datetime
from daneSchemat import Schemat,Kategoria,Grupa,Metoda_platnosci,Sortowanie
from typing import Optional

app = FastAPI()

@app.get("/")
def health_check():
    return "API działa"

@app.get("/Rekordy")
def get_Wydatki(data=None,kwota=None,kategoria: Optional[Kategoria]= None, metoda_platnosci: Optional[Metoda_platnosci]= None, grupa: Optional[Grupa]= None, sortowanie: Optional[Sortowanie]= None):
    kolumny = {"data": Wydatek.data,
               "metoda płatności": Wydatek.metoda_platnosci,
               "kategoria": Wydatek.kategoria,
               "grupa": Wydatek.grupa}
    
    with Session(db) as session:
        query = session.query(Wydatek)
        if data is not None:
            query = query.filter(Wydatek.data == parse_date(data))
        if kwota is not None:
            query = query.filter(Wydatek.kwota == kwota)
        if metoda_platnosci is not None:
            query = query.filter(Wydatek.metoda_platnosci == metoda_platnosci.value)
        if kategoria is not None:
            query = query.filter(Wydatek.kategoria == kategoria.value)
        if grupa is not None:
            query = query.filter(Wydatek.grupa == grupa.value)
        if sortowanie is not None:
            query = query.order_by(kolumny[sortowanie.value])
        return query.all()
    
@app.get("/Rekord")
def get_Wydatek(id):
    with Session(db) as session:
        query = session.get(Wydatek,id)
        if query is None:
            return "Podany rekord nie istnieje"
        else:
            return query

@app.get("/Analiza1")
def analise_Wydatek(data_od=None, data_do=None, kategoria =  None):
    with Session(db) as session:
        query = session.query(func.sum(Wydatek.kwota))
        if data_od is not None:
            query = query.filter(Wydatek.data >= parse_date(data_od))
        if data_do is not None:
            query = query.filter(Wydatek.data <= parse_date(data_do))
        if kategoria is not None:
            query = query.filter(Wydatek.kategoria == kategoria)
        return query.scalar()
    
@app.get("/Analiza1 z walidacją")
def analise_Wydatek(data_od=None, data_do=None, kategoria: Optional[Kategoria]= None, metoda_platnosci: Optional[Metoda_platnosci]= None, grupa: Optional[Grupa]= None):
    with Session(db) as session:
        query = session.query(func.sum(Wydatek.kwota))
        if data_od is not None:
            query = query.filter(Wydatek.data >= parse_date(data_od))
        if data_do is not None:
            query = query.filter(Wydatek.data <= parse_date(data_do))
        if kategoria is not None:
            query = query.filter(Wydatek.kategoria == kategoria.value)
        if metoda_platnosci is not None:
            query = query.filter(Wydatek.metoda_platnosci == metoda_platnosci.value)
        if grupa is not None:
            query = query.filter(Wydatek.grupa == grupa.value)
        return query.scalar()

@app.get("/Analiza2")
def analise_Wydatek2(data_od=None, data_do=None, kategoria=None,grupa=None):
    with Session(db) as session:
        query = session.query(func.sum(Wydatek.kwota),Wydatek.kategoria)
        query = query.group_by(Wydatek.kategoria)
        if data_od is not None:
            query = query.filter(Wydatek.data >= parse_date(data_od))
        if data_do is not None:
            query = query.filter(Wydatek.data <= parse_date(data_do))
        if kategoria is not None:
            query = query.filter(Wydatek.kategoria == kategoria)
        if grupa is not None:
            query = query.filter(Wydatek.grupa == grupa)
        wyniki = [{"kategoria":item[1], "suma":item[0]} for item in query.all()]
        return wyniki

@app.get("/Analiza2 z walidacją")
def analise_Wydatek2(data_od=None, data_do=None, grupa: Optional[Grupa]=None):
    with Session(db) as session:
        query = session.query(func.sum(Wydatek.kwota),Wydatek.kategoria)
        query = query.group_by(Wydatek.kategoria)
        if data_od is not None:
            query = query.filter(Wydatek.data >= parse_date(data_od))
        if data_do is not None:
            query = query.filter(Wydatek.data <= parse_date(data_do))
        if grupa is not None:
            query = query.filter(Wydatek.grupa == grupa.value)
        wyniki = [{"Kategoria":item[1], "Suma":item[0]} for item in query.all()]
        return wyniki
    
@app.get("/Analiza3 z walidacja")
def analise_Wydatek3(data_od=None, data_do=None, kategoria: Optional[Kategoria]=None):
    with Session(db) as session:
        query = session.query(func.sum(Wydatek.kwota),Wydatek.grupa)
        query = query.group_by(Wydatek.grupa)
        if data_od is not None:
            query = query.filter(Wydatek.data >= parse_date(data_od))
        if data_do is not None:
            query = query.filter(Wydatek.data <= parse_date(data_do))
        if kategoria is not None:
            query = query.filter(Wydatek.kategoria == kategoria.value)
        wyniki = [{"Grupa":item[1], "Suma":item[0]} for item in query.all()]
        return wyniki

@app.get("/Analiza4 z walidacja")
def analise_Wydatek4(data_od=None, data_do=None, kategoria: Optional[Kategoria]=None, grupa: Optional[Grupa]=None):
    with Session(db) as session:
        query = session.query(func.sum(Wydatek.kwota),Wydatek.metoda_platnosci)
        query = query.group_by(Wydatek.metoda_platnosci)
        if data_od is not None:
            query = query.filter(Wydatek.data >= parse_date(data_od))
        if data_do is not None:
            query = query.filter(Wydatek.data <= parse_date(data_do))
        if kategoria is not None:
            query = query.filter(Wydatek.kategoria == kategoria.value)
        if grupa is not None:
            query = query.filter(Wydatek.grupa == grupa.value)
        wyniki = [{"Metoda płatności":item[1], "Suma":item[0]} for item in query.all()]
        return wyniki


@app.post("/Nowy")
def add_Wydatek(data,kwota,metoda_platnosci,kategoria,grupa,opis):
    wyd = Wydatek()
    wyd.data = parse_date(data)
    wyd.kwota = kwota
    wyd.metoda_platnosci = metoda_platnosci
    wyd.kategoria = kategoria
    wyd.grupa = grupa
    wyd.opis = opis
    with Session(db) as session:
        session.add(wyd)
        session.commit()
    return "Dodano nowy wydatek do bazy"

@app.post("/Nowy z walidacją")
def add_Wydatek(wydatek: Schemat):
    wyd = Wydatek()
    wyd.data = parse_date(wydatek.data)
    wyd.kwota = wydatek.kwota
    wyd.metoda_platnosci = wydatek.metoda_platnosci.value
    wyd.kategoria = wydatek.kategoria.value
    wyd.grupa = wydatek.grupa.value
    wyd.opis = wydatek.opis
    with Session(db) as session:
        session.add(wyd)
        session.commit()
    return "Dodano nowy wydatek do bazy"
    
@app.put("/Aktualizuj")
def mod_Wydatek(id, data= None, kwota=None, metoda_platnosci=None, kategoria=None, grupa=None, opis=None):
    with Session(db) as session:
        to_mod = session.get(Wydatek, id)
        if to_mod is None:
            return "Podany rekord nie istnieje w bazie"
        else:
            if data is not None:
                to_mod.data = parse_date(data)
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
        

@app.put("/Aktualizuj z walidacją")
def mod_Wydatek(id, data= None, kwota=None, metoda_platnosci: Optional[Metoda_platnosci]=None, kategoria: Optional[Kategoria]=None, grupa: Optional[Grupa]=None, opis=None):
    with Session(db) as session:
        to_mod = session.get(Wydatek, id)
        if to_mod is None:
            return "Podany rekord nie istnieje w bazie"
        else:
            if data is not None:
                to_mod.data = parse_date(data)
            if kwota is not None:
                to_mod.kwota = kwota
            if metoda_platnosci is not None:
                to_mod.metoda_platnosci = metoda_platnosci.value
            if kategoria is not None:
                to_mod.kategoria = kategoria.value
            if grupa is not None:
                to_mod.grupa = grupa.value
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
        
def parse_date(data):
    if data is not None:
        data_format = ["%d.%m.%Y","%d/%m/%Y","%d-%m-%Y","%Y.%m.%d","%Y/%m/%d","%Y-%m-%d"]
        for format in data_format:
            try:
                nowa_data = datetime.strptime(data,format).date()
                return nowa_data
            except:
                continue
        return None
    
