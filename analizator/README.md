# Odtworzenie analizatora RPG przez serię promptów

Wymagane: Python 3 i NumPy (w środowisku wykonania: NumPy 2.3.5).

Uruchomienie programu:

```bash
python kod_koncowy.py
```

Raport CSV powstaje w bieżącym katalogu.

Powtórzenie niezależnej weryfikacji:

```bash
python testy/porownaj.py kod_koncowy.py wyniki/finalne.json
```

Dokumentacja: `analiza_zmian.md`, `prompty.md`, `weryfikacja.md`.
Pełne prompty i odpowiedzi: `rozmowa/`. Niezmieniane migawki kodu: `etapy/`.

## Pochodzenie kodu i izolacja

Wykorzystano osobny kontekst modelu Codex: narzędzie `collaboration.spawn_agent`, nazwa `rozmowa_ai`, parametr `fork_turns=none`. Jest to niezależna sesja modelu uruchomiona narzędziowo, a nie nowy wątek otwarty ręcznie w interfejsie ChatGPT. Nie przekazano historii tej rozmowy ani wersji B. Rodzic analizował B i przeprowadzał testy; model implementujący dostawał A, kolejne wymagania w języku naturalnym i wyniki wymagające korekty. Model zapisywał pełne odpowiedzi i kod każdego etapu.

Sesje współdzielą system plików, więc izolacja polegała na pustym kontekście i jawnym zakazie czytania wzorca, testów oraz dokumentacji rodzica; nie stanowiła osobnego sandboxa systemowego. Model pracował wyłącznie na własnych migawkach i wiadomościach. Wzorzec B służył tylko niezależnemu porównaniu. Kod końcowy powstał przez kolejne odpowiedzi modelu, bez ręcznego przepisywania B.

Pierwsza korekta rozszerza niepełną specyfikację o walidację, której brak ujawnił test po pierwszym etapie. Nie przedstawiamy tego jako złamania wcześniejszego polecenia przez model. Błędy testów funkcji zaplanowanych na późniejsze etapy nie są liczone jako korekty.
