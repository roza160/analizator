Przyjmuję wersję A i zapisuję ją bez zmian jako etap 00. Czekam na prompt 1.

```python
"""Pierwsza wersja systemu porównywania postaci RPG (bez NumPy)."""
postacie = [
    {"nazwa": "Wojownik", "hp": 120, "atak": 28, "obrona": 18, "szybkosc": 9},
    {"nazwa": "Mag", "hp": 75, "atak": 44, "obrona": 6, "szybkosc": 13},
    {"nazwa": "Łucznik", "hp": 95, "atak": 34, "obrona": 10, "szybkosc": 17},
    {"nazwa": "Paladyn", "hp": 140, "atak": 25, "obrona": 22, "szybkosc": 7},
    {"nazwa": "Łotrzyk", "hp": 80, "atak": 39, "obrona": 8, "szybkosc": 21},
    {"nazwa": "Berserker", "hp": 110, "atak": 42, "obrona": 7, "szybkosc": 12},
    {"nazwa": "Druid", "hp": 105, "atak": 26, "obrona": 15, "szybkosc": 14},
    {"nazwa": "Strażnik", "hp": 155, "atak": 18, "obrona": 26, "szybkosc": 5},
]
print("=== SIŁA POSTACI ===")
najlepsza_nazwa = ""
najlepsza_sila = -1
suma = 0
for postac in postacie:
    sila = postac["hp"] * 0.1 + postac["atak"] * 2 + postac["obrona"] * 1.5 + postac["szybkosc"]
    print(f'{postac["nazwa"]}: {sila:.2f}')
    suma += sila
    if sila > najlepsza_sila:
        najlepsza_sila = sila
        najlepsza_nazwa = postac["nazwa"]
print(f"\nNajsilniejsza postać: {najlepsza_nazwa}")
print(f"Średnia siła: {suma / len(postacie):.2f}")
```
