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

    for direction in ["", "q"]:
        onkey(set_direction(direction.lower()), direction)
    hideturtle()
    listen()

# ----------- Obsługa klawiatury - koniec ----------



def odczytaj_plik():
    file = open(nazwa_pliku, 'r')
    mapa = file.read().split('\n')
    file.close()

    return mapa

def sprawdz_poprawnosc_danych(mapa):

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
    assert map(int, mapa[0].split()), "Niepoprawna pierwsza linia w pliku"
    liczba_wierszy, liczba_kolumn = map(int, mapa[0].split())
    return (liczba_wierszy, liczba_kolumn)

def pokaz_plansze():
    screen = Screen()
    screen.setup(szerokosc_okna+margx, wysokosc_okna+margy)
    screen.title("Labirynt")

    path_length_obj = Turtle()

    current_path_length(path_length_obj, 0)
    path_length_obj.hideturtle()

def current_path_length(obj, path_lenth):
    obj.penup()
    obj.goto(0, wysokosc_okna/2+15)
    obj.clear()
    obj.color('navajo white')
    obj.shape('square')
    obj.shapesize(stretch_wid=1, stretch_len=szerokosc_okna/20)
    obj.stamp()
    obj.color('blue')
    obj.goto(0, wysokosc_okna/2+5)
    obj.write(f'Current path length: {path_lenth}', font=(
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

def stworz_strukture_planszy(pen, mapa):
    plansza_slownik = {'x': 'maroon', '.': 'gainsboro',
                       '#': 'orange', '$': 'red'}
    for index_wiersze in range(len(mapa)):
        for index_kolumny in range(len(mapa[index_wiersze])):
            color = plansza_slownik.get(mapa[index_wiersze][index_kolumny])
            dodaj_kwadrat(pen, color, 10, 10, index_wiersze, index_kolumny)


def dodaj_kwadrat(obj, color, ilosc_wierszy, ilosc_kolumn, index_wiersze, index_kolumny):
    odstep_wysokosc = wysokosc_okna / ilosc_wierszy
    odstep_szerokosc = szerokosc_okna / ilosc_kolumn

    # Zamiana indeksów listy na współrzędne (wiersze -> y, kolumny -> x)
    x = index_kolumny
    y = index_wiersze

    x = x * odstep_szerokosc - szerokosc_okna/2
    y = -1 * (y * odstep_wysokosc - wysokosc_okna/2 )

    if (color == "orange") or (color == 'red'):
        kolor_wypelnienia = 'grey'
        kolor_obramowki = color
    else:
        kolor_wypelnienia = color
        kolor_obramowki = 'black'

    szerokosc_obramowki = 4
    narysuj_wypelniony_prostokat(
        obj, x, y, odstep_szerokosc*0.95, odstep_wysokosc*0.95, szerokosc_obramowki, kolor_obramowki, kolor_wypelnienia)
    
    if color == 'orange':
        r_kola = odstep_szerokosc/4
        x_kola = x + odstep_szerokosc/2 + r_kola - szerokosc_obramowki/2
        y_kola = y - odstep_wysokosc/2
        narysuj_kolo(obj, x_kola, y_kola, r_kola)

def narysuj_wypelniony_prostokat(board,x,y,width,height,size,color,fill):
    board.fillcolor(fill)
    board.pencolor(color)
    board.pensize(size)
    board.setheading(0)
    
    board.begin_fill()
    board.up()
    board.goto(x,y)
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
    obj.penup()
    obj.goto(x,y)
    obj.pencolor("red")
    obj.fillcolor("red")
    obj.begin_fill()
    obj.circle(promien)
    obj.end_fill()

def ruch_w_labiryncie():
    pass

def main():
    ini_keyboard()

    dane = odczytaj_plik()
    sprawdz_poprawnosc_danych(dane)

    tracer(0, 0)
    pokaz_plansze()

    pen = Turtle()
    stworz_strukture_planszy(pen, dane[1:])
    update()

    while pressed_key != "q":
        update()
        time.sleep(0.2)
    bye()
    done()


main()
