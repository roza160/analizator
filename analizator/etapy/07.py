"""Porównywanie postaci RPG z normalizacją statystyk w NumPy."""

import csv

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


def macierz_pojedynkow(sila):
    """Zwróć deterministyczne szanse zwycięstwa dla wszystkich par."""
    sila = np.asarray(sila, dtype=float)
    roznice = sila[:, np.newaxis] - sila[np.newaxis, :]
    return 1.0 / (1.0 + np.exp(-8.0 * roznice))


def zapisz_csv(sciezka, nazwy, role, sila, srednie_szanse, ranking):
    """Zapisz wszystkie postacie w kolejności rankingu do pliku UTF-8 z BOM i separatorem średnikowym."""
    with open(sciezka, "w", newline="", encoding="utf-8-sig") as plik:
        writer = csv.writer(plik, delimiter=";")
        writer.writerow([
            "Miejsce", "Postać", "Rola", "Siła", "Średnia szansa wygranej"
        ])
        for miejsce, indeks in enumerate(ranking, start=1):
            writer.writerow([
                miejsce, nazwy[indeks], role[indeks],
                f"{sila[indeks]:.4f}", f"{srednie_szanse[indeks]:.2%}",
            ])


def testy():
    """Ciche testy regresji normalizacji i macierzy pojedynków."""
    dane = np.array([[10, 20, 30, 40], [10, 50, 60, 40]], dtype=float)
    znormalizowane = normalizuj(dane)
    np.testing.assert_array_equal(znormalizowane[:, 0], [0.0, 0.0])
    np.testing.assert_array_equal(znormalizowane[:, 3], [0.0, 0.0])
    np.testing.assert_array_equal(znormalizowane[:, 1], [0.0, 1.0])
    np.testing.assert_array_equal(znormalizowane[:, 2], [0.0, 1.0])
    pojedynki = macierz_pojedynkow(np.array([0.1, 0.6, 0.9]))
    np.testing.assert_allclose(np.diag(pojedynki), 0.5)
    np.testing.assert_allclose(pojedynki + pojedynki.T, np.ones((3, 3)))


def main():
    waliduj(NAZWY, STATYSTYKI)
    testy()
    sila = oblicz_sile(STATYSTYKI)
    ranking = np.argsort(-sila, kind="stable")
    role = okresl_role(STATYSTYKI)
    pojedynki = macierz_pojedynkow(sila)
    srednie_szanse = (
        pojedynki.sum(axis=1) - np.diag(pojedynki)
    ) / (len(sila) - 1)

    print("=== RANKING POSTACI RPG ===")
    for miejsce, indeks in enumerate(ranking, start=1):
        print(
            f"{miejsce}. {NAZWY[indeks]:<12} | {role[indeks]:<13}"
            f" | siła: {sila[indeks]:.3f}"
            f" | średnia szansa: {srednie_szanse[indeks]:.1%}"
        )

    print("\n=== POSTACIE SPEŁNIAJĄCE WYMAGANIA ===")
    wybrane = NAZWY[maska_wyboru(STATYSTYKI)]
    print(", ".join(wybrane) if wybrane.size else "Brak")

    minima = np.min(STATYSTYKI, axis=0)
    srednie = np.mean(STATYSTYKI, axis=0)
    maksima = np.max(STATYSTYKI, axis=0)
    print("\n=== STATYSTYKI GRUPY ===")
    for kolumna, minimum, srednia, maksimum in zip(KOLUMNY, minima, srednie, maksima):
        print(
            f"{kolumna:<10}: min={minimum:.1f}, "
            f"średnia={srednia:.1f}, max={maksimum:.1f}"
        )

    sciezka = "raport_postaci.csv"
    zapisz_csv(sciezka, NAZWY, role, sila, srednie_szanse, ranking)
    print(f"\nZapisano: {sciezka}")


if __name__ == "__main__":
    main()
