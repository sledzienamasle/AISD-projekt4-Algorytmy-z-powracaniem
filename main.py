import sys
from graph_hamilton import Graf

def main():
    if len(sys.argv) < 2:
        print("Blad: Nie podano argumentu uruchomienia (--hamilton lub --non-hamilton)", file=sys.stderr)
        return

    mode = sys.argv[1]

    if mode == "--hamilton":
        try:
            print("Wybrano tryb: Graf hamiltonowski.")
            print("Podaj liczbe wierzcholkow (wieksza niz 10):")
            nodes = int(input("nodes> "))
            while nodes <= 10:
                print("Blad: Liczba wierzcholkow musi byc wieksza niz 10.", file=sys.stderr)
                nodes = int(input("nodes> "))
        except ValueError:
            print("Blad: zle podana liczba wierzcholkow.", file=sys.stderr)
            return

        try:
            print("Podaj wspolczynnik nasycenia (30 lub 70):")
            saturation = float(input("saturation [%]> "))
            while saturation not in [30, 70]:
                print("Blad: Wspolczynnik nasycenia musi wynosic 30 lub 70.", file=sys.stderr)
                saturation = float(input("saturation [%]> "))
        except ValueError:
            print("Blad: Niepoprawna wartosc nasycenia.", file=sys.stderr)
            return

        # Generowanie oraz testowanie algorytmów
        graph = Graf(nodes)
        graph.generowanie_hamiltona(saturation)
        graph.wyswietl_macierz()
        graph.znajdz_cykl_eulera()
        graph.znajdz_cykl_hamiltona()

    elif mode == "--non-hamilton":
        print("Wybrano tryb: Graf nie-hamiltonowski.")
        print("(Logika pominieta w kodzie zrodlowym zgodnie z wytycznymi).")
        # Miejsce na logikę generowania grafów nie-hamiltonowskich (np. poprzez izolację wierzchołka)

    else:
        print("Blad: Nieznany argument. Uzyj '--hamilton' lub '--non-hamilton'.", file=sys.stderr)

if __name__ == "__main__":
    main()