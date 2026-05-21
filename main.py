import sys
from graph import Graph
from algorithms import generate_non_hamiltonian_graph, generate_hamiltonian_graph, find_and_print_hamiltonian_cycle, find_and_print_eulerian_cycle

def main():
    """Główna funkcja zarządzająca interakcją z terminalem."""
    if len(sys.argv) > 1 and sys.argv[1] == "--hamilton":
        try:
            print("Tryb --hamilton")
            print("Podaj ilość wierzchołków (większą niż 10):")
            nodes_input = input("nodes> ")
            nodes = int(nodes_input.strip())

            while nodes <= 10:
                print("Błąd: Ilość wierzchołków musi być większa niż 10.")
                nodes_input = input("nodes> ")
                nodes = int(nodes_input.strip())

            print("Podaj nasycenie grafu (30 lub 70):")
            saturation_input = input("saturation[%]> ")
            saturation = int(saturation_input.strip())
            while saturation not in [30, 70]:
                print("Błąd: Proszę wprowadzić nasycenie rowne 30 lub 70.")
                saturation_input = input("saturation[%]> ")
                saturation = int(saturation_input.strip())

        except ValueError:
            print("Błąd: Proszę wprowadzić poprawne wartości liczbowe.")
            return
        
        graph = Graph(nodes)
        generate_hamiltonian_graph(graph, saturation)

    elif len(sys.argv) > 1 and sys.argv[1] == "--non-hamilton":
        try:
            print("Tryb --non-hamilton")
            print("Podaj ilość wierzchołków (większą niż 10):")
            nodes_input = input("nodes> ")
            nodes = int(nodes_input.strip())

            while nodes <= 10:
                print("Błąd: Ilość wierzchołków musi być większa niż 10.")
                nodes_input = input("nodes> ")
                nodes = int(nodes_input.strip())

        except ValueError:
            print("Błąd: Proszę wprowadzić poprawne wartości liczbowe.")
            return
        
        graph = Graph(nodes)
        generate_non_hamiltonian_graph(graph)

    else:
        print(f"Użycie: python3 {sys.argv[0]} [--hamilton | --non-hamilton]")
        return
    
    # loop
    while True:
        print("\nDostępne polecenia:")
        print("1. Wyświetl graf")
        print("2. Eksportuj graf do LaTeX (plik graf.tex)")
        print("3. Sprawdź istnienie cyklu Hamiltona")
        print("4. Sprawdź istnienie cyklu Eulera")
        print("5. Zakończ program")
        
        command = input("command> ").strip().lower()
        print()  # dodajemy pustą linię dla lepszej czytelności

        if command == "1":
            graph.display()
        elif command == "2":
            graph.export_to_tikz()
        elif command == "3":
            if find_and_print_hamiltonian_cycle(graph):
                print()
            else:
                print("Cykl Hamiltona nie istnieje.")
        elif command == "4":
            if find_and_print_eulerian_cycle(graph):
                print()
            else:
                print("Cykl Eulera nie istnieje.")
        elif command == "5" or command == "exit" or command == "q":
            print("Zakończenie programu.")
            break
        else:
            print("Nieznane polecenie. Proszę spróbować ponownie. (Wpisz 1, 2, 3, 4 lub 5)")

if __name__ == "__main__":
    main()