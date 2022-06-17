from turtle import*
import time
from math import sqrt

# ---- Stałe ---------
margx = 20
margy = 60
szerokosc_okna = 800
wysokosc_okna = 700
nazwa_pliku = 'mapa.txt'


# ------------ Obsługa klawiatury - początek ----------

pressed_key = ""


def set_direction(key):
    def result():
        global pressed_key
        pressed_key = key
        print(f'The key was pressed')
    return result


def ini_keyboard():
    '''
    Funkcja pozwala na wyjście z programu, jeżeli użytkownik wybierze przycisk 'q'
    '''
    for direction in ["", "q"]:
        onkey(set_direction(direction.lower()), direction)
    hideturtle()
    listen()

# ----------- Obsługa klawiatury - koniec ----------



def odczytaj_plik():
    '''
    Funkcja odczytuje plik z mapą labiryntu i zwraca tą mapę jako lista stringów.
    '''
    file = open(nazwa_pliku, 'r')
    mapa = file.read().split('\n')
    file.close()

    return mapa

def sprawdz_poprawnosc_danych(mapa):
    '''
    Funkcja sprawdza poprawność danych wpisanych w pliku tekstowym. Sprawdzane są:
    - pierwsza linia pliku, czy zawiera 2 liczby typu int
    - ilość wierszy, czy jest zgodna z ilością zdefiniowaną w pierwszej linii
    - ilość kolumn, czy jest zgodna z ilością zdefiniowaną w pierwszej linii
    - czy dane zawierają jedno wejście i przynajmniej jedno wyjście
    - czy dane zawierają inne znaki niż te dozwolone
    '''
    liczba_wierszy, liczba_kolumn = odczytaj_ilosc_wierszy_kolumn(mapa)

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

def odczytaj_ilosc_wierszy_kolumn(mapa):
    # Zamień elementy z pierwszej linii na typ int
    pierwsza_linia = mapa[0].split()
    assert len(pierwsza_linia) == 2, 'Niepoprawna ilość argumentów w pierwszej linii'
    assert pierwsza_linia[0].isdigit(), "Rozmiar wiersza nie jest typu int"
    assert pierwsza_linia[1].isdigit(), "Rozmiar kolumny nie jest typu int"
    assert map(int, mapa[0].split()), "Niepoprawna pierwsza linia w pliku"
    liczba_wierszy, liczba_kolumn = map(int, mapa[0].split())
    return (liczba_wierszy, liczba_kolumn)

def pokaz_plansze(path_lenth=0):
    '''
    Funkcja tworzy ekran labiryntu i nagłówki informacyjne
    '''
    screen = Screen()
    screen.setup(szerokosc_okna+margx, wysokosc_okna+margy)
    screen.title("Labirynt")

def zaktualizuj_naglowek(path_lenth):
    '''
    Funkcja tworzy nagłówki informacyjne
    '''
    path_length_obj = Turtle()

    current_path_length(path_length_obj, path_lenth)
    path_length_obj.hideturtle()

def current_path_length(obj, current_path):
    '''
    Funkcja wypisuje nagłówek zawierający długość przebytej ścieżki.
    '''
    obj.penup()
    obj.goto(0, wysokosc_okna/2+15)
    obj.clear()
    obj.color('navajo white')
    obj.shape('square')
    obj.shapesize(stretch_wid=1, stretch_len=szerokosc_okna/20)
    obj.stamp()
    obj.color('blue')
    obj.goto(0, wysokosc_okna/2+5)
    obj.write(f'Current path length: {current_path}', font=(
        "Arial", 12), align='center')
    obj.penup()
    obj.goto(0, -wysokosc_okna/2-10)
    obj.color('grey')
    obj.shape('square')
    obj.shapesize(stretch_wid=0.8, stretch_len=szerokosc_okna/20)
    obj.stamp()
    obj.color('blue')
    obj.goto(0, -wysokosc_okna/2-20)
    obj.write(f'Searching for an exit from the labyrinth', font=("Arial", 10, "bold"), align='center')
    obj.fillcolor("blue")
    obj.hideturtle()

def stworz_strukture_planszy(pen, kolo, mapa):

    '''
    Funkcja tworzy planszę z kwadratami na podstawie listy dwuwymiarowej mapa.
    Korzysta ze słownika, który na podstawie znaku w liście wybiera kolor kwadratu.
    Kolejne indeksy listy mapa wskazują lokalizację każdego kwadratu.
    '''

    plansza_slownik = {'x': 'maroon', '.': 'gainsboro',
                       '#': 'orange', '$': 'red', 'o': 'blue'}
    for index_wiersze in range(len(mapa)):
        for index_kolumny in range(len(mapa[index_wiersze])):
            color = plansza_slownik.get(mapa[index_wiersze][index_kolumny])
            dodaj_kwadrat(pen, kolo, color, 10, 10, index_wiersze, index_kolumny)

def zaktualizuj_strukture_planszy(pen, kolo, mapa):
    # o - odwiedzone, k - pozycja kropki, b - bieżąca ścieżka
    plansza_slownik = {'x': 'maroon', '.': 'gainsboro',
                       '#': 'orange', '$': 'red', 'o': 'gray', 'k': 'kropka', 'b': 'blue'}
    for index_wiersze in range(len(mapa)):
        for index_kolumny in range(len(mapa[index_wiersze])):
            color = plansza_slownik.get(mapa[index_wiersze][index_kolumny])
            if color == 'kropka' or color == 'gray':
                dodaj_kwadrat(pen, kolo, color, 10, 10, index_wiersze, index_kolumny)

def dodaj_kwadrat(obj, kolo, color, ilosc_wierszy, ilosc_kolumn, index_wiersze, index_kolumny):
    '''
    Funkcja zamienia indeksy wierszy i kolumn z listy na współprzędne kwadratów. Wywołuje funkcję
    rysująca kwadraty podając odpowiednie współrzędne i kolory.
    '''
    global wysokosc_okna
    global szerokosc_okna

    odstep_wysokosc = wysokosc_okna / ilosc_wierszy
    odstep_szerokosc = szerokosc_okna / ilosc_kolumn

    # Zamiana indeksów listy na współrzędne (wiersze -> y, kolumny -> x)
    x = index_kolumny
    y = index_wiersze

    x = x * odstep_szerokosc - szerokosc_okna/2
    y = -1 * (y * odstep_wysokosc - wysokosc_okna/2 )

    if (color == "orange") or (color == 'red'):
        kolor_wypelnienia = 'gainsboro'
        kolor_obramowki = color
        if color == "orange":
            kolor_wypelnienia = "blue"
    elif color == 'kropka':
        kolor_wypelnienia = 'blue'
        kolor_obramowki = 'black'
    else:
        kolor_wypelnienia = color
        kolor_obramowki = 'black'

    szerokosc_obramowki = 4
    narysuj_wypelniony_prostokat(
        obj, x, y, odstep_szerokosc*0.95, odstep_wysokosc*0.95, szerokosc_obramowki, kolor_obramowki, kolor_wypelnienia)
    
    if color == 'orange' or color == 'kropka':
        r_kola = odstep_szerokosc/4
        x_kola = x + odstep_szerokosc/2
        y_kola = y - odstep_wysokosc/2 - r_kola
        narysuj_kolo(kolo, x_kola, y_kola, r_kola)

def narysuj_wypelniony_prostokat(board, x, y, width, height, size, color, fill):
    board.fillcolor(fill)
    board.pencolor(color)
    board.pensize(size)
    board.setheading(0)
    
    board.begin_fill()
    board.up()
    board.goto(x, y)
    board.down()
    # draw top
    board.forward(width)
    # draw right
    board.right(90)
    board.forward(height)
    # draw bottom
    board.right(90)
    board.forward(width)
    # draw left
    board.right(90)
    board.forward(height)
    board.end_fill()

def narysuj_kolo(obj, x, y, promien):
    obj.clear()
    obj.up()
    obj.goto(x, y)
    obj.down()
    obj.pencolor("red")
    obj.fillcolor("red")
    obj.begin_fill()
    obj.circle(promien)
    obj.end_fill()
    obj.hideturtle()

def zmien_strukture_mapy(mapa):
    '''
    Funkcja tworzy dwyuwymiarową listę, zawierającą znaki zawarte w pliku.
    '''
    for indeks_wiersz in range(len(mapa)):
        lista_znakow = [znak for znak in mapa[indeks_wiersz]]
        mapa[indeks_wiersz] = lista_znakow

def zwroc_indeks_znaku(mapa, znak):
    for wiersz in mapa:
        if znak in wiersz:
            pozycja = [mapa.index(wiersz), wiersz.index(znak)]
            return pozycja

def zwroc_indeks_nastepnej_pozycji(mapa, znak_poprz):
    current_path = 0
    for index_wiersz in range(len(mapa)):
        for index_kolumna in range(len(mapa[0])):
            if znak_poprz == mapa[index_wiersz][index_kolumna]:
                if znak_poprz != '#':
                    mapa[index_wiersz][index_kolumna] = 'b'

                if (index_wiersz == len(mapa) - 1) or (index_kolumna == len(mapa) - 1):
                    if (index_wiersz == len(mapa) - 1) and (index_kolumna == len(mapa) - 1):
                        if mapa[index_wiersz - 1][index_kolumna] == '.' or mapa[index_wiersz - 1][index_kolumna] == '$':
                            if mapa[index_wiersz - 1][index_kolumna] == '$':
                                return '$'
                            mapa[index_wiersz - 1][index_kolumna] = 'k'
                            current_path += 1
                        elif mapa[index_wiersz][index_kolumna - 1] == '.' or mapa[index_wiersz][index_kolumna - 1] == '$':
                            if mapa[index_wiersz][index_kolumna - 1] == '$':
                                return '$'
                            mapa[index_wiersz][index_kolumna - 1] = 'k'
                            current_path += 1
                        else:
                            mapa[index_wiersz][index_kolumna] = 'o'
                            if mapa[index_wiersz - 1][index_kolumna] == 'b':
                                mapa[index_wiersz - 1][index_kolumna] = 'k'
                            elif mapa[index_wiersz][index_kolumna - 11] == 'b':
                                mapa[index_wiersz][index_kolumna - 1] = 'k'
                    elif index_wiersz == len(mapa) - 1:
                        if mapa[index_wiersz - 1][index_kolumna] == '.' or mapa[index_wiersz - 1][index_kolumna] == '$':
                            if mapa[index_wiersz - 1][index_kolumna] == '$':
                                return '$'
                            mapa[index_wiersz - 1][index_kolumna] = 'k'
                            current_path += 1
                        elif mapa[index_wiersz][index_kolumna + 1] == '.' or mapa[index_wiersz][index_kolumna + 1] == '$':
                            if mapa[index_wiersz][index_kolumna + 1] == '$':
                                return '$'
                            mapa[index_wiersz][index_kolumna + 1] = 'k'
                            current_path += 1
                        elif mapa[index_wiersz][index_kolumna - 1] == '.' or mapa[index_wiersz][index_kolumna - 1] == '$':
                            if mapa[index_wiersz][index_kolumna - 1] == '$':
                                return '$'
                            mapa[index_wiersz][index_kolumna - 1] = 'k'
                            current_path += 1
                        else:
                            mapa[index_wiersz][index_kolumna] = 'o'
                            if mapa[index_wiersz - 1][index_kolumna] == 'b':
                                mapa[index_wiersz - 1][index_kolumna] = 'k'
                            elif mapa[index_wiersz][index_kolumna + 1] == 'b':
                                mapa[index_wiersz][index_kolumna + 1] = 'k'
                            elif mapa[index_wiersz][index_kolumna - 11] == 'b':
                                mapa[index_wiersz][index_kolumna - 1] = 'k'
                    else:
                        if mapa[index_wiersz + 1][index_kolumna] == '.' or mapa[index_wiersz + 1][index_kolumna] == '$':
                            if mapa[index_wiersz + 1][index_kolumna] == '$':
                                return '$'
                            mapa[index_wiersz + 1][index_kolumna] = 'k'
                            current_path += 1
                        elif mapa[index_wiersz - 1][index_kolumna] == '.' or mapa[index_wiersz - 1][index_kolumna] == '$':
                            if mapa[index_wiersz - 1][index_kolumna] == '$':
                                return '$'
                            mapa[index_wiersz - 1][index_kolumna] = 'k'
                            current_path += 1
                        elif mapa[index_wiersz][index_kolumna - 1] == '.' or mapa[index_wiersz][index_kolumna - 1] == '$':
                            if mapa[index_wiersz][index_kolumna - 1] == '$':
                                return '$'
                            mapa[index_wiersz][index_kolumna - 1] = 'k'
                            current_path += 1
                        else:
                            mapa[index_wiersz][index_kolumna] = 'o'
                            if mapa[index_wiersz + 1][index_kolumna] == 'b':
                                mapa[index_wiersz + 1][index_kolumna] = 'k'
                            elif mapa[index_wiersz - 1][index_kolumna] == 'b':
                                mapa[index_wiersz - 1][index_kolumna] = 'k'
                            elif mapa[index_wiersz][index_kolumna - 11] == 'b':
                                mapa[index_wiersz][index_kolumna - 1] = 'k'

                elif mapa[index_wiersz+1][index_kolumna] == '.' or mapa[index_wiersz+1][index_kolumna] == '$':
                    if mapa[index_wiersz+1][index_kolumna] == '$':
                        return '$'
                    mapa[index_wiersz+1][index_kolumna] = 'k'
                    current_path += 1
                elif mapa[index_wiersz-1][index_kolumna] == '.' or mapa[index_wiersz-1][index_kolumna] == '$':
                    if mapa[index_wiersz-1][index_kolumna] == '$':
                        return '$'
                    mapa[index_wiersz-1][index_kolumna] = 'k'
                    current_path += 1
                elif mapa[index_wiersz][index_kolumna+1] == '.' or mapa[index_wiersz][index_kolumna+1] == '$':
                    if mapa[index_wiersz][index_kolumna+1] == '$':
                        return '$'
                    mapa[index_wiersz][index_kolumna+1] = 'k'
                    current_path += 1
                elif mapa[index_wiersz][index_kolumna-1] == '.' or mapa[index_wiersz][index_kolumna-1] == '$':
                    if mapa[index_wiersz][index_kolumna-1] == '$':
                        return '$'
                    mapa[index_wiersz][index_kolumna-1] = 'k'
                    current_path += 1
                # Jezeli brak już korytarza, oznacz drogę jako odwiedzoną i cofnij się
                else:
                    mapa[index_wiersz][index_kolumna] = 'o'
                    if mapa[index_wiersz+1][index_kolumna] == 'b':
                        mapa[index_wiersz+1][index_kolumna] = 'k'
                    elif mapa[index_wiersz-1][index_kolumna] == 'b':
                        mapa[index_wiersz-1][index_kolumna] = 'k'
                    elif mapa[index_wiersz][index_kolumna+1] == 'b':
                        mapa[index_wiersz][index_kolumna+1] = 'k'
                    elif mapa[index_wiersz][index_kolumna-11] == 'b':
                        mapa[index_wiersz][index_kolumna-1] = 'k'
                return str(current_path)


def main():
    ini_keyboard()

    dane = odczytaj_plik()
    sprawdz_poprawnosc_danych(dane)

    tracer(0, 0)
    pokaz_plansze()
    current_path = 0
    zaktualizuj_naglowek(current_path)

    pen = Turtle()
    kolo = Turtle()
    stworz_strukture_planszy(pen, kolo, dane[1:])

    dane_kopia = dane[1:].copy()
    zmien_strukture_mapy(dane_kopia)

    zwroc_indeks_nastepnej_pozycji(dane_kopia, '#')
    zaktualizuj_strukture_planszy(pen, kolo, dane_kopia)
    update()

    wyjscie = False
    while pressed_key != "q":
        if not wyjscie:
            znak = zwroc_indeks_nastepnej_pozycji(dane_kopia, 'k')
            if znak == "$":
                wyjscie = True
            else:
                current_path += int(znak)
                zaktualizuj_naglowek(current_path)
            zaktualizuj_strukture_planszy(pen, kolo, dane_kopia)
            print(current_path)
        update()
        time.sleep(0.2)
    bye()
    done()


main()
