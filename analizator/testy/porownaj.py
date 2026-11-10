"""Niezależne testy funkcjonalne; wzorzec B nie jest przekazywany modelowi."""
import contextlib
import csv
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import numpy as np

ROOT = Path(__file__).resolve().parents[1]

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()) as captured:
        spec.loader.exec_module(module)
    assert not captured.getvalue(), 'Import uruchamia raport'
    return module

def run(target):
    b = load(ROOT / '02_kod_docelowy.py', 'wzorzec')
    a = load(target, 'wynik_ai')
    results = []
    def check(name, fn):
        try:
            detail = fn()
            results.append({'wymaganie': name, 'status': 'działa', 'dowod': str(detail or 'OK')})
        except Exception as exc:
            results.append({'wymaganie': name, 'status': 'nie działa', 'dowod': f'{type(exc).__name__}: {exc}'})
    def arrays():
        assert isinstance(a.NAZWY, np.ndarray)
        assert isinstance(a.STATYSTYKI, np.ndarray)
        assert a.STATYSTYKI.dtype.kind == 'f'
        np.testing.assert_array_equal(a.NAZWY, b.NAZWY)
        np.testing.assert_array_equal(a.STATYSTYKI, b.STATYSTYKI)
        np.testing.assert_allclose(a.WAGI, b.WAGI)
        return '8 nazw, macierz (8,4), float, zgodne dane i wagi'
    check('Dane NumPy i wagi', arrays)
    def numeric():
        np.testing.assert_allclose(a.normalizuj(b.STATYSTYKI), b.normalizuj(b.STATYSTYKI), rtol=1e-12, atol=1e-12)
        np.testing.assert_allclose(a.oblicz_sile(b.STATYSTYKI), b.oblicz_sile(b.STATYSTYKI), rtol=1e-12, atol=1e-12)
        return a.oblicz_sile(b.STATYSTYKI).tolist()
    check('Normalizacja i ważona siła', numeric)
    def constant():
        for data in [np.array([[10,20,30,40],[10,50,60,40.]]), np.ones((3,4)), np.array([[0,0,0,0],[0,0,0,0]])]:
            with np.errstate(all='raise'):
                np.testing.assert_allclose(a.normalizuj(data), b.normalizuj(data))
        return 'Stałe kolumny, wszystkie kolumny stałe i zera: bez NaN i ostrzeżeń'
    check('Stałe kolumny', constant)
    def validation():
        bad = [
            (np.array(['A','B']), np.ones((2,3))),
            (np.array(['A','B']), np.ones(8)),
            (np.array(['A','B']), np.ones((3,4))),
            (np.array(['A']), np.ones((1,4))),
            (np.array([],dtype=str), np.empty((0,4))),
            (np.array(['A','A']), np.ones((2,4))),
        ]
        for val in [-1., np.nan, np.inf, -np.inf]:
            data = np.ones((2,4)); data[0,0] = val
            bad.append((np.array(['A','B']), data))
        for names, data in bad:
            try: a.waliduj(names, data)
            except ValueError: pass
            else: raise AssertionError(f'Nie odrzucono {names!r}, {data!r}')
        a.waliduj(b.NAZWY, b.STATYSTYKI)
        a.waliduj(np.array(['A','B']), np.zeros((2,4)))
        return '10 niepoprawnych wejść → ValueError; poprawne dane i zera przyjęte'
    check('Walidacja', validation)
    def roles():
        edge = np.array([[120,35,18,12],[119,35,18,12],[120,34,18,12],[120,35,18,11],[119,34,17,11]])
        np.testing.assert_array_equal(a.okresl_role(b.STATYSTYKI), b.okresl_role(b.STATYSTYKI))
        np.testing.assert_array_equal(a.okresl_role(edge), b.okresl_role(edge))
        return '8 postaci oraz 5 granic progów i przypadek obu ról'
    check('Role i pierwszeństwo ofensywy', roles)
    def duels():
        for strength in [b.oblicz_sile(b.STATYSTYKI), np.array([.1,.6,.9]), np.array([.5,.5]), np.zeros(4)]:
            p = a.macierz_pojedynkow(strength)
            np.testing.assert_allclose(p,b.macierz_pojedynkow(strength),rtol=1e-12,atol=1e-12)
            np.testing.assert_allclose(np.diag(p),.5)
            np.testing.assert_allclose(p+p.T,1)
        return '4 scenariusze; logistyka k=8, przekątna 0.5, P+P.T=1'
    check('Macierz pojedynków',duels)
    def random_cases():
        rng=np.random.default_rng(20261104)
        for n in [2,3,8,17,100]:
            data=rng.integers(0,200,size=(n,4)).astype(float)
            data[:,0]=100
            np.testing.assert_allclose(a.normalizuj(data),b.normalizuj(data),rtol=1e-12,atol=1e-12)
            strength=a.oblicz_sile(data)
            np.testing.assert_allclose(strength,b.oblicz_sile(data),rtol=1e-12,atol=1e-12)
            np.testing.assert_array_equal(a.okresl_role(data),b.okresl_role(data))
            np.testing.assert_allclose(a.macierz_pojedynkow(strength),b.macierz_pojedynkow(strength),rtol=1e-12,atol=1e-12)
        return '5 zbiorów (n=2,3,8,17,100), seed=20261104, stałe HP, tolerancja 1e-12'
    check('Zgodność obliczeń dla dodatkowych danych',random_cases)
    def internal():
        a.testy()
        return 'testy() zakończone bez błędu'
    check('Wbudowane testy', internal)
    def main_order():
        calls=[]
        original_validate=a.waliduj
        original_tests=a.testy
        class Stop(Exception): pass
        def validation_probe(*args):
            calls.append('waliduj')
            return original_validate(*args)
        def tests_probe():
            calls.append('testy')
            raise Stop()
        a.waliduj=validation_probe
        a.testy=tests_probe
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                try: a.main()
                except Stop: pass
            assert calls==['waliduj','testy'],calls
        finally:
            a.waliduj=original_validate
            a.testy=original_tests
        return 'main(): najpierw waliduj(), potem testy(), przed raportem'
    check('Uruchamianie walidacji i testów w main',main_order)
    def execute(module, names=None, data=None):
        runner = ('import importlib.util; '
                  f's=importlib.util.spec_from_file_location("app", {str(module)!r}); '
                  'm=importlib.util.module_from_spec(s); s.loader.exec_module(m); ')
        if data is not None:
            runner += f'import numpy as np; m.NAZWY=np.array({names!r}); m.STATYSTYKI=np.array({data!r},dtype=float); '
        runner += 'm.main()'
        with tempfile.TemporaryDirectory() as td:
            result = subprocess.run([sys.executable,'-c',runner],cwd=td,capture_output=True,text=True,timeout=20)
            assert result.returncode == 0, result.stderr
            assert not result.stderr, result.stderr
            path = Path(td)/'raport_postaci.csv'
            return result.stdout, path.read_bytes()
    def exports():
        actual, raw = execute(target)
        expected, reference = execute(ROOT/'02_kod_docelowy.py')
        (ROOT/'wyniki'/'stdout_ai.txt').write_text(actual,encoding='utf-8')
        (ROOT/'wyniki'/'stdout_B.txt').write_text(expected,encoding='utf-8')
        (ROOT/'wyniki'/'raport_postaci.csv').write_bytes(raw)
        (ROOT/'wyniki'/'raport_B.csv').write_bytes(reference)
        assert raw[:3] == b'\xef\xbb\xbf', 'CSV nie zawiera BOM UTF-8'
        rows=list(csv.reader(io.StringIO(raw.decode('utf-8-sig')),delimiter=';'))
        expected_rows=list(csv.reader(io.StringIO(reference.decode('utf-8-sig')),delimiter=';'))
        assert rows == expected_rows, f'CSV różni się: {rows!r}'
        return 'Nagłówek + 8 wierszy identyczne z B; BOM, średnik, 4 miejsca, procenty 2 miejsca'
    check('CSV: zawartość, format i kodowanie',exports)
    def report():
        actual,_=execute(target)
        expected,_=execute(ROOT/'02_kod_docelowy.py')
        assert actual == expected, 'Raport tekstowy różni się od wzorca (porównanie ścisłe)'
        return 'stdout identyczny z B: ranking, filtr Berserker, statystyki i zapis'
    check('Raport, ranking, filtr i statystyki',report)
    def scenarios():
        cases=[(['A','B'],[[1,1,1,1],[1,1,1,1]]),
               (['Z','A','M'],[[120,35,18,12]]*3),
               (['A','B','C'],[[100,20,10,10],[130,50,20,20],[90,40,5,15]]),
               (['Granica','Inna'],[[100,0,18,10],[90,35,0,20]])]
        for names,data in cases:
            actual,raw=execute(target,names,data)
            expected,reference=execute(ROOT/'02_kod_docelowy.py',names,data)
            assert actual==expected, f'Raport różni się dla {names}'
            assert raw==reference, f'CSV różni się dla {names}'
        return '4 alternatywne zbiory: remisy, 2 postacie, stałe kolumny, Brak, obie role, średnie bez siebie, filtr dokładnie HP=100/szybkość=10/siła=0.45; stdout i CSV zgodne'
    check('Scenariusze brzegowe end-to-end',scenarios)
    return results

if __name__ == '__main__':
    target=Path(sys.argv[1]).resolve()
    results=run(target)
    text=json.dumps(results,ensure_ascii=False,indent=2)
    print(text)
    if len(sys.argv)>2: Path(sys.argv[2]).write_text(text+'\n',encoding='utf-8')
    sys.exit(any(r['status']!='działa' for r in results))
