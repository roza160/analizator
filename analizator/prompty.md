# Seria promptów: od A do analizatora zgodnego funkcjonalnie z B

Prompty wysyłano kolejno w nowej sesji modelu Codex (`rozmowa_ai`, `fork_turns=none`). Model otrzymał tylko A oraz wymagania, bez B i bez jego fragmentów. Była to osobna sesja narzędziowa, nie ręcznie utworzony wątek w interfejsie ChatGPT. Pełne odpowiedzi są w `rozmowa/`, a niezmieniane migawki kodu w `etapy/`. Szczegóły izolacji: `README.md`. Lista 20 odtworzonych zmian: `analiza_zmian.md`.

Każdy następny prompt dotyczy kodu wypracowanego wcześniej. Braki funkcji przewidzianych na dalsze etapy nie są traktowane jako błędy modelu. Korekty rozszerzają specyfikację na podstawie rzeczywistych testów. Nie było ręcznej edycji wygenerowanego kodu.

## 1. Migracja i wynik

**Zmiana:** Przebudowa formatu danych i zastąpienie surowej sumy z A znormalizowanym wynikiem; stabilny ranking i bezpieczny import.

**Dokładny prompt:**

Zamień listę słowników z A na tablicę NumPy NAZWY oraz macierz STATYSTYKI typu float o kolumnach HP, Atak, Obrona, Szybkość, zachowując wszystkie osiem rekordów i ich kolejność. Dodaj WAGI [0.20, 0.40, 0.25, 0.15]. W funkcji normalizuj(dane) wykonaj normalizację min–max niezależnie dla kolumn. oblicz_sile(dane) ma zwracać wektor iloczynu macierzowego znormalizowanych danych i wag, bez pętli po postaciach. W main() pokaż wynik i ranking malejący, używając stabilnego sortowania, tak by remisy zachowały kolejność wejściową. Import modułu nie może uruchamiać raportu. Sprawdź kształty (8,), (8,4), zakres normalizacji i wagę sumującą się do 1. Zapisz pełny kod jako etapy/01.py oraz pełną odpowiedź jako rozmowa/01_odpowiedz.md. Kolejnych wymagań jeszcze nie otrzymałeś.

**Zachowana odpowiedź i kod:** `rozmowa/01_odpowiedz.md`, `etapy/01.py`.

## 2. Korekta 1: walidacja danych

**Zmiana:** Uszczelnienie kontraktu wejścia po wykryciu brakującej walidacji; dziesięć przypadków błędnych i akceptacja zer.

**Dokładny prompt:**

Korekta po teście etapu 01: podstawowe obliczenia i stałe kolumny działają, lecz test walidacji zakończył się AttributeError: brak waliduj. Rozszerz wymagania: dodaj waliduj(nazwy,dane) wywoływane na początku main(). Wymagaj macierzy 2D o kształcie (len(nazwy),4), co najmniej dwóch postaci, unikatowych nazw oraz wyłącznie nieujemnych, skończonych statystyk. Błędne wejścia mają zgłaszać ValueError przed obliczeniami. Sprawdź osobno: 1D, 3 kolumny, niezgodną liczbę nazw, 0 i 1 postać, duplikat, wartość ujemną, NaN, +Inf, -Inf. Dane zerowe są poprawne. Zachowaj działanie normalizacji stałych kolumn bez dzielenia przez zero i stabilne sortowanie. Zapisz pełny kod w etapy/02.py i pełną odpowiedź w rozmowa/02_odpowiedz.md. Nie czytaj plików testów rodzica.

**Zachowana odpowiedź i kod:** `rozmowa/02_odpowiedz.md`, `etapy/02.py`.

## 3. Role, filtrowanie i statystyki

**Zmiana:** Wprowadzenie trzech ról, pierwszeństwa ofensywy, koniunkcji warunków filtra i redukcji statystycznych po kolumnach.

**Dokładny prompt:**

Dodaj okresl_role(dane) z maskami NumPy: Szturmowiec gdy Atak>=35 i Szybkość>=12; Obrońca gdy HP>=120 i Obrona>=18; pozostałe Wszechstronny. Przy jednoczesnym spełnieniu obu ról pierwszeństwo ma Szturmowiec. Dodaj maskę wyboru spełniającą jednocześnie HP>=100, Szybkość>=10 i znormalizowaną ważoną siłę>=0.45; wypisz nazwy w kolejności wejściowej albo Brak. Dodaj KOLUMNY=(HP,Atak,Obrona,Szybkość) z polskimi napisami i statystyki min/średnia/max każdej kolumny przez redukcje NumPy. Zweryfikuj wartości dokładnie na granicach progów i przypadek obu ról. Zapisz pełny kod etapy/03.py i pełną odpowiedź rozmowa/03_odpowiedz.md.

**Zachowana odpowiedź i kod:** `rozmowa/03_odpowiedz.md`, `etapy/03.py`.

## 4. Prawdopodobieństwa pojedynków

**Zmiana:** Wektorowe wyznaczenie pełnej macierzy prawdopodobieństw oraz średnich z wyłączeniem walki ze sobą.

**Dokładny prompt:**

Dodaj macierz_pojedynkow(sila): różnice wszystkich par przez broadcasting, P(i,j)=1/(1+exp(-8*(siła_i-siła_j))). Przekątna ma wynosić 0.5, a P+P.T ma dawać jedynki. To deterministyczna ocena szans, bez losowania walk. W main oblicz dla każdej postaci średnią szansę przeciw wszystkim POZOSTAŁYM postaciom, wykluczając przekątną i dzieląc przez n-1. Ranking nadal zależy od siły, nie od losowań. Sprawdź dwa identyczne wyniki, nierówne wyniki i macierz 3 postaci. Zapisz pełny kod etapy/04.py i pełną odpowiedź rozmowa/04_odpowiedz.md.

**Zachowana odpowiedź i kod:** `rozmowa/04_odpowiedz.md`, `etapy/04.py`.

## 5. Raport i pierwsza wersja eksportu CSV

**Zmiana:** Złożenie czytelnego raportu konsolowego i pierwszego eksportu wszystkich postaci w kolejności rankingu.

**Dokładny prompt:**

Połącz dotychczasowe funkcje w raport i dodaj zapisz_csv(sciezka,nazwy,role,sila,srednie_szanse,ranking), eksportujący raport_postaci.csv z wierszami w kolejności rankingu i pozycjami od 1. Kolumny to Miejsce, Postać, Rola, Siła, Średnia szansa wygranej. Sprawdź, że plik zawiera wszystkie 8 postaci. Raport konsolowy ma mieć sekcje === RANKING POSTACI RPG ===, === POSTACIE SPEŁNIAJĄCE WYMAGANIA ===, === STATYSTYKI GRUPY ===. W rankingu drukuj numer z kropką i spacją, nazwę wyrównaną do lewej w polu 12, separator ' | ', rolę w polu 13, następnie ' | siła: ' z 3 miejscami po przecinku i ' | średnia szansa: ' jako procent z 1 miejscem. Przed kolejnymi sekcjami pusta linia. Statystyki: etykieta w polu 10, dwukropek, spacja, min=wartość, średnia=wartość, max=wartość (po przecinku i spacji), każda wartość z 1 miejscem. Na końcu pusta linia oraz Zapisano: raport_postaci.csv. Usuń dodatkowe wydruki z wersji A. Zapisz pełny kod etapy/05.py i pełną odpowiedź rozmowa/05_odpowiedz.md.

**Zachowana odpowiedź i kod:** `rozmowa/05_odpowiedz.md`, `etapy/05.py`.

## 6. Korekta 2: kontrakt eksportu CSV

**Zmiana:** Naprawa rzeczywistej niezgodności eksportu: BOM, separator i format liczb/procentów; zachowanie poprawnego stdout.

**Dokładny prompt:**

Korekta po testach etapu 05: raport konsolowy jest już zgodny, ale test CSV wykazał brak BOM UTF-8. Dodatkowa kontrola pliku ujawniła przecinek zamiast średnika i surowe liczby zamiast ustalonego formatu. Doprecyzowuję kontrakt zapisz_csv: użyj UTF-8 z BOM (utf-8-sig), newline='' oraz separatora ';'. Zachowaj dotychczasowe pięć nagłówków, kolejność rankingu i miejsca od 1. Siłę zapisuj jako tekst z dokładnie 4 miejscami po kropce, a średnią szansę jako procent z dokładnie 2 miejscami i znakiem %. Nie zmieniaj poprawnego raportu konsolowego ani obliczeń. Sprawdź bajty początkowe EF BB BF, 9 wierszy, 5 pól, kolejność nazw, przykład lidera: siła 0.5349 i szansa 63.98%. Sprawdź też CSV dla dwóch identycznych postaci: siła 0.0000, szansa 50.00%, stabilna kolejność. Pełny kod zapisz w etapy/06.py, pełną odpowiedź w rozmowa/06_odpowiedz.md.

**Zachowana odpowiedź i kod:** `rozmowa/06_odpowiedz.md`, `etapy/06.py`.

## 7. Testy regresji i kod końcowy

**Zmiana:** Dodanie cichych testów uruchamianych po walidacji i zachowanie końcowego kodu wygenerowanego przez model.

**Dokładny prompt:**

Zakończ program testami regresji. Dodaj testy() używające numpy.testing/assert: dla danych dwóch wierszy [10,20,30,40] oraz [10,50,60,40] kolumny HP i szybkości mają po normalizacji same zera, atak [0,1]. Dla sił [0.1,0.6,0.9] przekątna macierzy pojedynków wynosi 0.5, a macierz plus jej transpozycja jest równa 1 w tolerancji numerycznej. Testy muszą być ciche przy sukcesie. W main() kolejność: najpierw waliduj, następnie testy, dopiero potem właściwe obliczenia i raport. Zweryfikuj, że import niczego nie drukuje i nie tworzy CSV, a bezpośrednie uruchomienie drukuje raport i zapisuje plik. Zachowaj wszystkie dotychczasowe wymagania i sprawdź ponownie 2 postacie, remisy, stałe kolumny oraz pusty wynik filtra. Pełny finalny kod zapisz jako etapy/07.py ORAZ identyczny plik /workspace/rpg/kod_koncowy.py; pełną odpowiedź z kodem zachowaj w rozmowa/07_odpowiedz.md. Nie czytaj żadnego wzorca ani testów rodzica.

**Zachowana odpowiedź i kod:** `rozmowa/07_odpowiedz.md`, `etapy/07.py`.

## Rzeczywiste korekty po testach

1. Po prompcie 1: brak `waliduj` ujawniony przez `AttributeError` w niezależnym teście. Prompt 2 doprecyzował kontrakt i przypadki negatywne. Po zmianie wszystkie 10 błędnych wejść jest odrzucanych. Dowody: `wyniki/etap_01.json`, `wyniki/etap_02.json`.
2. Po prompcie 5: eksport istniał, ale miał UTF-8 bez BOM, przecinki oraz surowe liczby. Prompt 6 określił ścisły format eksportu. Po zmianie CSV i stdout są zgodne z B dla danych bazowych i czterech zbiorów brzegowych. Dowody: `wyniki/etap_05.json`, `wyniki/etap_05_raport.csv`, `wyniki/etap_06.json`.

Szczegółowy opis przed/po: `korekty.md`. Końcowa tabela i wyniki testów: `weryfikacja.md`, `wyniki/finalne.json`.
