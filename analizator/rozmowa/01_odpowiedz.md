Przekształcono dane do tablic NumPy i dodano normalizację min–max kolumn oraz obliczanie siły przez iloczyn macierzowy. Ranking używa stabilnego sortowania malejącego. Raport uruchamia się wyłącznie przy bezpośrednim wykonaniu skryptu.

Sprawdzono kształty `(8,)` i `(8, 4)`, typ `float`, zakres normalizacji `[0, 1]`, sumę wag równą 1, kształt wektora wyników oraz brak raportu przy imporcie. Sprawdzono też zachowanie kolejności remisów przez stabilne sortowanie.

```python
"""Porównywanie postaci RPG z normalizacją statystyk w NumPy."""

import numpy as np

NAZWY = np.array([
    "Wojownik", "Mag", "Łucznik", "Paladyn", "Łotrzyk", "Berserker", "Druid", "Strażnik"
])
# Kolumny: HP, Atak, Obrona, Szybkość.
STATYSTYKI = np.array([
    [120, 28, 18, 9],
    [75, 44, 6, 13],
    [95, 34, 10, 17],
    [140, 25, 22, 7],
    [80, 39, 8, 21],
    [110, 42, 7, 12],
    [105, 26, 15, 14],
    [155, 18, 26, 5],
], dtype=float)
WAGI = np.array([0.20, 0.40, 0.25, 0.15])


def normalizuj(dane):
    """Normalizuj każdą kolumnę do [0, 1]; stałe kolumny otrzymują 0."""
    dane = np.asarray(dane, dtype=float)
    minimum = np.min(dane, axis=0)
    rozstep = np.max(dane, axis=0) - minimum
    return np.divide(
        dane - minimum, rozstep,
        out=np.zeros_like(dane), where=rozstep != 0,
    )


def oblicz_sile(dane):
    """Zwróć wektor ważonych wyników znormalizowanych statystyk."""
    return normalizuj(dane) @ WAGI


def main():
    sila = oblicz_sile(STATYSTYKI)
    ranking = np.argsort(-sila, kind="stable")
    print("=== SIŁA POSTACI ===")
    for nazwa, wynik in zip(NAZWY, sila):
        print(f"{nazwa}: {wynik:.4f}")
    print("\n=== RANKING MALEJĄCY ===")
    for miejsce, indeks in enumerate(ranking, start=1):
        print(f"{miejsce}. {NAZWY[indeks]}: {sila[indeks]:.4f}")
    print(f"\nNajsilniejsza postać: {NAZWY[ranking[0]]}")
    print(f"Średnia siła: {np.mean(sila):.4f}")


if __name__ == "__main__":
    main()
```

Wynik uruchomienia:

```text
=== SIŁA POSTACI ===
Wojownik: 0.4538
Mag: 0.4750
Łucznik: 0.4587
Paladyn: 0.4889
Łotrzyk: 0.5106
Berserker: 0.5349
Druid: 0.3950
Strażnik: 0.4500

=== RANKING MALEJĄCY ===
1. Berserker: 0.5349
2. Łotrzyk: 0.5106
3. Paladyn: 0.4889
4. Mag: 0.4750
5. Łucznik: 0.4587
6. Wojownik: 0.4538
7. Strażnik: 0.4500
8. Druid: 0.3950

Najsilniejsza postać: Berserker
Średnia siła: 0.4709
```
