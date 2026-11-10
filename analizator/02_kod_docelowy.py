"""Docelowy, wektorowy analizator balansu postaci RPG z NumPy."""
import csv
import numpy as np

NAZWY = np.array(["Wojownik", "Mag", "Łucznik", "Paladyn", "Łotrzyk", "Berserker", "Druid", "Strażnik"])
STATYSTYKI = np.array([
    [120, 28, 18, 9], [75, 44, 6, 13], [95, 34, 10, 17],
    [140, 25, 22, 7], [80, 39, 8, 21], [110, 42, 7, 12],
    [105, 26, 15, 14], [155, 18, 26, 5],
], dtype=float)
WAGI = np.array([0.20, 0.40, 0.25, 0.15])
KOLUMNY = ("HP", "Atak", "Obrona", "Szybkość")

def waliduj(nazwy, dane):
    if dane.ndim != 2 or dane.shape != (len(nazwy), 4):
        raise ValueError("Każda postać musi mieć dokładnie 4 statystyki.")
    if len(nazwy) < 2:
        raise ValueError("Potrzeba co najmniej dwóch postaci.")
    if len(set(nazwy.tolist())) != len(nazwy):
        raise ValueError("Nazwy postaci muszą być unikatowe.")
    if not np.all(np.isfinite(dane)) or np.any(dane < 0):
        raise ValueError("Statystyki muszą być nieujemnymi, skończonymi liczbami.")

def normalizuj(dane):
    minimum = np.min(dane, axis=0)
    rozpietosc = np.ptp(dane, axis=0)
    return np.divide(dane - minimum, rozpietosc, out=np.zeros_like(dane, dtype=float), where=rozpietosc != 0)

def oblicz_sile(dane):
    return normalizuj(dane) @ WAGI

def okresl_role(dane):
    ofensywa = (dane[:, 1] >= 35) & (dane[:, 3] >= 12)
    obrona = (dane[:, 0] >= 120) & (dane[:, 2] >= 18)
    return np.select([ofensywa, obrona], ["Szturmowiec", "Obrońca"], default="Wszechstronny")

def macierz_pojedynkow(sila):
    roznice = sila[:, None] - sila[None, :]
    wynik = 1 / (1 + np.exp(-8 * roznice))
    np.fill_diagonal(wynik, 0.5)
    return wynik

def zapisz_csv(sciezka, nazwy, role, sila, srednie_szanse, ranking):
    with open(sciezka, "w", encoding="utf-8-sig", newline="") as plik:
        pisarz = csv.writer(plik, delimiter=";")
        pisarz.writerow(["Miejsce", "Postać", "Rola", "Siła", "Średnia szansa wygranej"])
        for miejsce, indeks in enumerate(ranking, start=1):
            pisarz.writerow([miejsce, nazwy[indeks], role[indeks], f"{sila[indeks]:.4f}", f"{srednie_szanse[indeks]:.2%}"])

def testy():
    przyklad = np.array([[10, 20, 30, 40], [10, 50, 60, 40]], dtype=float)
    wynik = normalizuj(przyklad)
    np.testing.assert_allclose(wynik[:, 0], [0, 0])
    np.testing.assert_allclose(wynik[:, 1], [0, 1])
    np.testing.assert_allclose(wynik[:, 3], [0, 0])
    proby = macierz_pojedynkow(np.array([0.1, 0.6, 0.9]))
    assert np.allclose(np.diag(proby), 0.5)
    assert np.allclose(proby + proby.T, 1.0)

def main():
    waliduj(NAZWY, STATYSTYKI)
    testy()
    sila = oblicz_sile(STATYSTYKI)
    role = okresl_role(STATYSTYKI)
    ranking = np.argsort(-sila, kind="stable")
    pojedynki = macierz_pojedynkow(sila)
    srednie_szanse = (pojedynki.sum(axis=1) - 0.5) / (len(NAZWY) - 1)
    print("=== RANKING POSTACI RPG ===")
    for miejsce, indeks in enumerate(ranking, start=1):
        print(f"{miejsce}. {NAZWY[indeks]:12} | {role[indeks]:13} | siła: {sila[indeks]:.3f} | średnia szansa: {srednie_szanse[indeks]:.1%}")
    print("\n=== POSTACIE SPEŁNIAJĄCE WYMAGANIA ===")
    maska = (STATYSTYKI[:, 0] >= 100) & (STATYSTYKI[:, 3] >= 10) & (sila >= 0.45)
    wybrane = NAZWY[maska]
    print(", ".join(wybrane.tolist()) if len(wybrane) else "Brak")
    print("\n=== STATYSTYKI GRUPY ===")
    for indeks, etykieta in enumerate(KOLUMNY):
        print(f"{etykieta:10}: min={np.min(STATYSTYKI[:, indeks]):.1f}, średnia={np.mean(STATYSTYKI[:, indeks]):.1f}, max={np.max(STATYSTYKI[:, indeks]):.1f}")
    zapisz_csv("raport_postaci.csv", NAZWY, role, sila, srednie_szanse, ranking)
    print("\nZapisano: raport_postaci.csv")

if __name__ == "__main__":
    main()
