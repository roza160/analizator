# Analiza zmian A → B

1. Lista ośmiu słowników została zastąpiona jednowymiarową tablicą nazw i macierzą NumPy float (8,4). Kolejność i wartości danych pozostały takie same.
2. Kolejność kolumn to HP, Atak, Obrona, Szybkość; etykiety służą także do raportowania.
3. Surowy wynik A: 0.1·HP + 2·Atak + 1.5·Obrona + Szybkość zastąpiono normalizacją min–max osobno dla każdej kolumny.
4. Stała kolumna daje zera. Maskowane dzielenie zapobiega dzieleniu przez zero, NaN i ostrzeżeniom.
5. Nowy wynik to iloczyn znormalizowanej macierzy i wag [0.20,0.40,0.25,0.15]. Wagi sumują się do 1.
6. Obliczenia wyniku, ról, filtrowania i pojedynków są wektorowe. Pętle pozostały przy formatowaniu raportów, co jest właściwe.
7. Pełny ranking malejący według siły zastępuje sam wybór najlepszej postaci. Sortowanie stabilne zachowuje kolejność wejściową przy remisach.
8. Role: atak ≥35 i szybkość ≥12 → Szturmowiec; HP ≥120 i obrona ≥18 → Obrońca; inaczej Wszechstronny. Ofensywa ma pierwszeństwo.
9. Filtr stosuje jednocześnie HP ≥100, szybkość ≥10, siłę ≥0.45. Zachowuje kolejność wejściową, a pusty wynik wypisuje jako Brak.
10. Statystyki grupy to minimum, średnia i maksimum każdej surowej cechy, zamiast samej średniej siły z A.
11. Wszystkie pary sił tworzą macierz n×n przez broadcasting; szansa wygranej to funkcja logistyczna ze współczynnikiem 8.
12. Przekątna macierzy ma 0.5, a szanse wzajemnych pojedynków sumują się do 1. Nie ma losowej symulacji ani generatora losowego.
13. Średnie szanse wykluczają walkę ze sobą: od sumy wiersza odejmuje się 0.5 i dzieli przez n−1.
14. Walidacja: macierz 2D dokładnie (liczba nazw,4), przynajmniej dwie postacie, nazwy unikatowe, dane nieujemne i skończone; naruszenia zgłaszają ValueError.
15. B nie zabrania pustego napisu jako nazwy ani wartości zerowych i nie normalizuje wag na nowo. Nie należy dopisywać takich wymagań.
16. Funkcje rozdzielają walidację, normalizację, siłę, role, pojedynki, CSV i testy. main() działa tylko po bezpośrednim uruchomieniu pliku.
17. Wbudowane testy sprawdzają stałe kolumny oraz przekątną i symetrię dopełniającą macierzy szans. main() uruchamia je po walidacji.
18. Raport konsolowy ma sekcje rankingu, filtrowania i statystyk; siła ma 3 miejsca, szansa 1 miejsce procentowe, statystyki 1 miejsce.
19. CSV: raport_postaci.csv, UTF-8 z BOM, średnik, newline='', pięć polskich nagłówków, ranking od 1, siła z 4 miejscami, szanse procentowe z 2 miejscami. Eksport obejmuje cały ranking, nie tylko wynik filtra.
20. Wydajność: siła i redukcje mają koszt O(n·4), sortowanie O(n log n), pełna macierz pojedynków O(n²) czasu i pamięci. NumPy usuwa pętle Pythona z obliczeń, ale nie zmienia kwadratowego kosztu wszystkich par. Dla 8 rekordów nie deklarujemy przyspieszenia na podstawie samego importu.

Wzorzec B zachowano w 02_kod_docelowy.py z równoważnym układem wierszy. Nie jest częścią materiału przekazanego modelowi w osobnej rozmowie.
