from turtle import*
import time

# ---- Stałe ---------
margx = 20
margy = 60
szerokosc_okna = 700
wysokosc_okna = 600


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
    file = open('mapa.txt', 'r')
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

def pokaz_plansze(ilosc_wierszy, ilosc_kolumn):
    screen = Screen()
    screen.setup(szerokosc_okna+margx, wysokosc_okna+margy)
    screen.title("Labirynt")

    pen = Turtle()
    path_length_obj = Turtle()

    current_path_length(path_length_obj, 0)

    odstep_wysokosc = wysokosc_okna / ilosc_wierszy
    odstep_szerokosc = szerokosc_okna / ilosc_kolumn

    a = -szerokosc_okna/2
    b = wysokosc_okna/2
    for i in range(ilosc_wierszy+1):
        # linie w pionie
        pen.penup()
        pen.goto(a + i*odstep_szerokosc, b)
        pen.pendown()
        pen.goto(a + i*odstep_szerokosc, -b)
        # linie w poziomie
        pen.penup()
        pen.goto(a, b - i*odstep_wysokosc)
        pen.pendown()
        pen.goto(-a, b - i*odstep_wysokosc)
    pen.hideturtle()

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
    obj.write(f'Searching for an exit from the labirynth', font=("Arial", 10, "bold"), align='center')
    obj.fillcolor("blue")
    obj.hideturtle()

def main():
    ini_keyboard()

    dane = odczytaj_plik()
    sprawdz_poprawnosc_danych(dane)

    liczba_wierszy, liczba_kolumn = odczytaj_ilosc_wierszy_kolumn(dane)

    tracer(0, 0)
    pokaz_plansze(liczba_wierszy, liczba_kolumn)
    update()

    while pressed_key != "q":
        update()
        time.sleep(0.2)
    bye()
    done()


main()
