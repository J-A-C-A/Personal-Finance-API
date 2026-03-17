from pydantic import BaseModel
from enum import Enum

class Kategoria(Enum):
    val1 = "jedzenie"
    val2 = "czynsz i opłaty"
    val3 = "transport"
    val4 = "zdrowie"
    val5 = "ubrania"
    val6 = "używki"
    val7 = "rozrywka"
    val8 = "sport"
    val9 = "środki czystości i kosmetyki"
    val10 = "różne"

class Grupa(Enum):
    val1 = "podstawowe"
    val2 = "dodatkowe"
    val3 = "nieprzewidziane"

class Metoda_platnosci(Enum):
    val1 = "gotówka"
    val2 = "karta"
    val3 = "przelew"

class Schemat(BaseModel):
    data:str
    kwota:float
    metoda_platnosci:Metoda_platnosci
    kategoria:Kategoria
    grupa:Grupa
    opis:str

