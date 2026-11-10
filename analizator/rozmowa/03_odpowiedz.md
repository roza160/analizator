Dodano role wyznaczane maskami NumPy, z pierwszeństwem Szturmowca przy spełnieniu obu ról. Maska wyboru łączy warunki HP, szybkości i ważonej siły; nazwy zachowują kolejność wejściową, a pusty wybór daje `Brak`. Dodano `KOLUMNY` oraz minima, średnie i maksima obliczane redukcjami NumPy.

Sprawdzono wartości na progach ról i poniżej nich, jednoczesne spełnienie obu ról, granice HP=100, Szybkość=10 i siła=0.45 oraz odrzucanie wartości poniżej progów. Dla danych podstawowych wybrany zostaje Berserker.

```python
"""Porównywanie postaci RPG z normalizacją statystyk w NumPy."""

import numpy as np

NAZWY = np.array([
    "Wojownik", "Mag", "Łucznik", "Paladyn", "Łotrzyk", "Berserker", "Druid", "Strażnik"
])
KOLUMNY = ("HP", "Atak", "Obrona", "Szybkość")
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


def waliduj(nazwy, dane):
    """Odrzuć niepoprawne nazwy i statystyki przed obliczeniami."""
    try:
        nazwy = np.asarray(nazwy)
        dane = np.asarray(dane, dtype=float)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError("Nazwy i statystyki muszą tworzyć poprawne tablice.") from exc
    if nazwy.ndim != 1:
        raise ValueError("Nazwy muszą być tablicą jednowymiarową.")
    if dane.ndim != 2 or dane.shape != (len(nazwy), 4):
        raise ValueError("Statystyki muszą mieć kształt (liczba nazw, 4).")
    if len(nazwy) < 2:
        raise ValueError("Wymagane są co najmniej dwie postacie.")
    try:
        unikatowe = np.unique(nazwy).size == len(nazwy)
    except (TypeError, ValueError) as exc:
        raise ValueError("Nazwy muszą umożliwiać sprawdzenie unikatowości.") from exc
    if not unikatowe:
        raise ValueError("Nazwy postaci muszą być unikatowe.")
    if not np.all(np.isfinite(dane)) or np.any(dane < 0):
        raise ValueError("Statystyki muszą być nieujemne i skończone.")


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


def okresl_role(dane):
    """Wyznacz role maskami; Szturmowiec ma pierwszeństwo."""
    dane = np.asarray(dane, dtype=float)
    szturmowcy = (dane[:, 1] >= 35) & (dane[:, 3] >= 12)
    obroncy = (dane[:, 0] >= 120) & (dane[:, 2] >= 18)
    return np.select(
        [szturmowcy, obroncy],
        ["Szturmowiec", "Obrońca"],
        default="Wszechstronny",
    )


def maska_wyboru(dane):
    """Wybierz postacie spełniające łącznie trzy warunki."""
    dane = np.asarray(dane, dtype=float)
    return (
        (dane[:, 0] >= 100)
        & (dane[:, 3] >= 10)
        & (oblicz_sile(dane) >= 0.45)
    )


def main():
    waliduj(NAZWY, STATYSTYKI)
    sila = oblicz_sile(STATYSTYKI)
    ranking = np.argsort(-sila, kind="stable")
    role = okresl_role(STATYSTYKI)
    print("=== SIŁA POSTACI ===")
    for nazwa, wynik, rola in zip(NAZWY, sila, role):
        print(f"{nazwa}: {wynik:.4f} — {rola}")
    print("\n=== RANKING MALEJĄCY ===")
    for miejsce, indeks in enumerate(ranking, start=1):
        print(f"{miejsce}. {NAZWY[indeks]}: {sila[indeks]:.4f}")
    print(f"\nNajsilniejsza postać: {NAZWY[ranking[0]]}")
    print(f"Średnia siła: {np.mean(sila):.4f}")
    wybrane = NAZWY[maska_wyboru(STATYSTYKI)]
    print("\n=== WYBRANE POSTACIE ===")
    print(", ".join(wybrane) if wybrane.size else "Brak")
    minima = np.min(STATYSTYKI, axis=0)
    srednie = np.mean(STATYSTYKI, axis=0)
    maksima = np.max(STATYSTYKI, axis=0)
    print("\n=== STATYSTYKI KOLUMN ===")
    for kolumna, minimum, srednia, maksimum in zip(KOLUMNY, minima, srednie, maksima):
        print(f"{kolumna}: min={minimum:.2f}, średnia={srednia:.2f}, max={maksimum:.2f}")


if __name__ == "__main__":
    main()
```

Wynik uruchomienia:

```text
=== SIŁA POSTACI ===
Wojownik: 0.4538 — Obrońca
Mag: 0.4750 — Szturmowiec
Łucznik: 0.4587 — Wszechstronny
Paladyn: 0.4889 — Obrońca
Łotrzyk: 0.5106 — Szturmowiec
Berserker: 0.5349 — Szturmowiec
Druid: 0.3950 — Wszechstronny
Strażnik: 0.4500 — Obrońca

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

=== WYBRANE POSTACIE ===
Berserker

=== STATYSTYKI KOLUMN ===
HP: min=75.00, średnia=110.00, max=155.00
Atak: min=18.00, średnia=32.00, max=44.00
Obrona: min=6.00, średnia=14.00, max=26.00
Szybkość: min=5.00, średnia=12.25, max=21.00
```
