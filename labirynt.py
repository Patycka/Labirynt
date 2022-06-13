

def odczyt_plik():
    file = open('mapa.txt', 'r')
    mapa = file.read().split('\n')
    file.close()

    return mapa

def sprawdz_poprawnosc_danych():
    mapa = odczyt_plik()

    liczba_wierszy, liczba_kolumn = map(int, mapa[0].split())

    # Sprawdzenie, czy ilość wierszy zdefiniowana w pierwszej linii pokrywa z ilością
    # wierszy w pliku, z wyłączeniem pierwszej linii.
    assert len(mapa[1:]) == liczba_wierszy, "Niepoprawna ilość wierszy"

    # Sprawdzenie, czy zgadza się ilość znaków w każdym wierszu labiryntu
    for wiersz in mapa[1:]:
        assert len(wiersz) == liczba_kolumn, "Niepoprawna ilość kolumn"

    assert sum(x.count('#') for x in mapa[1:]) == 1, "Niepoprawna ilość wejść"
    assert sum(x.count('$') for x in mapa[1:]) >= 1, "Brak conajmniej jednego wyjścia"

    # Sprawdzenie czy w pliku znajdują się tylko dozwolone znaki: x, ., #, $
    for wiersz in mapa[1:]:
        assert any(c not in 'x.#$' for c in wiersz) == False, 'Znak inny niż x, ., #, $'


def main():
    sprawdz_poprawnosc_danych()


main()
