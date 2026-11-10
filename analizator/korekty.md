# Dwie rzeczywiste korekty promptów

## 1. Walidacja po niepełnym etapie 01

- Stan przed: prompt 1 określał migrację do NumPy i obliczenia, ale nie określał kontraktu walidacji. Model poprawnie obsłużył nawet stałe kolumny; ten przypadek nie jest przedstawiany jako błąd.
- Rzeczywisty wynik testu: `AttributeError: module 'wynik_ai' has no attribute 'waliduj'` (`wyniki/etap_01.json`, sekcja Walidacja).
- Korekta specyfikacji w prompcie 2: jawne wymagania kształtu, co najmniej dwóch postaci, unikatowych nazw, nieujemnych skończonych liczb i ValueError przed obliczeniami. Wskazano konkretne przypadki testowe.
- Wynik po korekcie: `wyniki/etap_02.json` potwierdza odrzucenie wszystkich 10 niepoprawnych wejść, przyjęcie poprawnych danych i zer. Kod przed/po: `etapy/01.py`, `etapy/02.py`.

## 2. Format CSV po niepełnym etapie 05

- Stan przed: prompt 5 wymagał pliku, kolumn i kolejności, ale nie określał szczegółowego kodowania, separatora ani precyzji eksportu. Model wybrał UTF-8 bez BOM, domyślny przecinek i surowe wartości zmiennoprzecinkowe.
- Rzeczywisty wynik: `AssertionError: CSV nie zawiera BOM UTF-8` oraz niezgodność CSV dla dwóch identycznych postaci (`wyniki/etap_05.json`). W tym samym teście stdout jest identyczny z B. Oryginalny niezgodny plik zachowano jako `wyniki/etap_05_raport.csv`.
- Korekta w prompcie 6: UTF-8 z BOM, `newline=''`, średnik, siła z 4 miejscami, szansa jako procent z 2 miejscami; wskazano bajty BOM i wartości kontrolne lidera oraz remisujących postaci.
- Wynik po korekcie jest zapisany w `wyniki/etap_06.json`; końcowe potwierdzenie w `wyniki/finalne.json`.

Są to korekty niepełnej specyfikacji po realnych niezgodnościach. Nie twierdzimy, że model naruszył wcześniejsze wymagania, których jeszcze nie otrzymał. Pozostałe braki raportowane w logach etapów przyrostowych (np. brak pojedynków przed promptem 4) były zaplanowanymi zmianami i nie są liczone jako korekty.
