====OPIS PROJEKTU====
Personal Finance API jest to aplikacja która pozwala na zarządzanie wydatkami osobistymi. Wydatki są zapisywane w bazie danych. Informację, które składają się na wydatek to: id, data, kwota, metoda płatności, kategoria, grupa, opis.

Kategoria przyjmuje następujące wartości:
- jedzenie
- czynsz i opłaty
- transport
- zdrowie
- ubrania
- używki
- rozrywka
- sport
- środki czystości i kosmetyki
- różne

Grupa przyjmuje następujące wartości:
- podstawowe
- dodatkowe
- nieprzewidziane

Metoda płatności przyjmuje następujące wartości:
- gotówka
- karta
- przelew

====WYKORZYSTANE NARZĘDZIA====
- FastAPI - framework do tworzenia API w Pythonie
- PyDantic - biblioteka służąca do walidacji i parsowania danych
- Uvicorn - serwer na którym działa FastAPI i obsługuje zapytania HTTP
- SQLalchemy - biblioteka służąca do pracy z bazami danych, która umożliwia operowanie na danych za pomocą obiektów zamiast czystych zapytań SQL
- Typing - moduł pozwalający na dodawanie adnotacji typów
- Enum - klasa służąca do definiowania stałych zestawów wartości

====PLIKI====
- main.py - zawiera połączenie z FastAPI oraz implementację wszystkich endpointów a także funkcję parse_date do parsowania daty wprowadzonej przez użytkownika na format występujący w bazie danych
- dataBase.py - zawiera implementację i połączenie z bazą danych
- daneSchemat.py - zawiera schemat walidacji danych z PyDantic oraz typy wyliczeniowe

====URUCHOMIENIE PROJEKTU====
1. Należy pobrać wszystkie pliki z repo
2. Zainstalować wszystkie potrzebne biblioteki
3. W terminalu wpisać polecenie: 
py -3.12 -m uvicorn main:app --reload
4. Zostanie wyświetlony komunikat:
Uvicorn running on http://127.0.0.1:8000 (podany port może się różnić)
5. Wejść w podany link z dopiskiem na końcu /docs
