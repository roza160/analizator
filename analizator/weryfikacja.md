# Weryfikacja końcowa

**Wynik: 12/12 grup testów zakończonych powodzeniem.** Testy uruchomiono rzeczywiście, po kolejnych odpowiedziach modelu. Nie edytowano ręcznie jego kodu końcowego.

| Wymaganie | Działa / nie działa | Dowód lub wynik testu |
| --- | --- | --- |
| Dane NumPy i wagi | działa | 8 rekordów, float (8,4); zgodność z B |
| Normalizacja i wynik ważony | działa | Zgodność z B przy tolerancji 1e-12 |
| Stałe kolumny | działa | Zera zamiast NaN; brak ostrzeżeń |
| Walidacja | działa | 10 błędnych wejść → ValueError; zera dozwolone |
| Role | działa | 8 rekordów + 5 przypadków progowych; ofensywa ma pierwszeństwo |
| Pojedynki | działa | 4 scenariusze; przekątna 0,5; P + P.T = 1 |
| Dodatkowe dane | działa | Zbiory n=2,3,8,17,100; zgodność z B |
| Wbudowane testy | działa | testy() przechodzą bez błędu |
| Kolejność main() | działa | Walidacja → testy → obliczenia |
| CSV | działa | Identyczny bajtowo z B; BOM, średnik, 9 wierszy |
| Raport, ranking, filtr, statystyki | działa | stdout identyczny z B; filtr: Berserker |
| Przypadki brzegowe end-to-end | działa | 4 zbiory: remisy, Brak, 2 postacie, filtr na progu; stdout i CSV zgodne |

Lider: **Berserker**, siła 0.5348557692307693, średnia szansa 0.6397780578293101 (w CSV: 0.5349 i 63.98%). Kolejność: Berserker, Łotrzyk, Paladyn, Mag, Łucznik, Wojownik, Strażnik, Druid.

Zestawy brzegowe obejmują identyczne postacie, zachowanie kolejności nazw Z/A/M przy remisie, obie role jednocześnie, pusty filtr oraz postać dokładnie na progach HP=100, szybkość=10, siła=0.45. Średnie szanse bez walki ze sobą sprawdzono poprzez zgodność całego raportu i CSV.

## Odtwarzalność i dowody

- Python 3.12.14, NumPy 2.3.5.
- Polecenie: `python testy/porownaj.py kod_koncowy.py wyniki/finalne.json` — kod wyjścia 0.
- Bezpośrednie uruchomienie: `python kod_koncowy.py` — kod wyjścia 0; plik `raport_postaci.csv`.
- Pełne wyniki: `wyniki/finalne.json`; stdout obu programów: `wyniki/stdout_ai.txt`, `wyniki/stdout_B.txt`.
- CSV obu programów: `wyniki/raport_postaci.csv`, `wyniki/raport_B.csv`. Pliki są identyczne bajtowo.
- SHA-256 obu CSV: `1daf6136d3bf48f00a6f3728c9789d24cb0ea7252e7da6324125a9f03f1f5c55`.
- `kod_koncowy.py` jest identyczny z migawką odpowiedzi modelu `etapy/07.py`.
- Dwie korekty: brak walidacji po etapie 01 i niezgodny format CSV po etapie 05. Szczegóły oraz dowody przed/po w `korekty.md`.

Testy potwierdzają zgodność na opisanych zbiorach, a nie matematyczny dowód dla każdego możliwego wejścia. Nazwy zmiennych, organizacja funkcji i komunikaty ValueError mogą różnić się od B. Dodatkowa akceptacja konwertowalnych list przez część funkcji nie zmienia wyniku dla wymaganego formatu tablic NumPy. Nie wykonywano benchmarku szybkości; analizę kosztów obliczeń zawarto w `analiza_zmian.md`.
