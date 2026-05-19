import sys
from graph import Graph
from algorithms import generate_hamiltonian_graph, find_and_print_hamiltonian_cycle, find_and_print_eulerian_cycle

def main():
    """Główna funkcja zarządzająca interakcją z terminalem."""
    if len(sys.argv) > 1 and sys.argv[1] == "--hamilton":
        try:
            nodes_input = input("nodes> ")
            nodes = int(nodes_input.strip())

            if nodes <= 10:
                print("Błąd: Ilość wierzchołków musi być większa niż 10.")
                return

            saturation_input = input("saturation> ")
            saturation = int(saturation_input.strip())

        except ValueError:
            print("Błąd: Proszę wprowadzić poprawne wartości liczbowe.")
            return

        # Użycie klas i algorytmów z zaimportowanych plików
        graph = Graph(nodes)
        generate_hamiltonian_graph(graph, saturation)
        graph.display()
        
        find_and_print_eulerian_cycle(graph)      # <--- TO JEST TA NOWA LINIJKA
        find_and_print_hamiltonian_cycle(graph)

    elif len(sys.argv) > 1 and sys.argv[1] == "--non-hamilton":
        print("Tryb --non-hamilton w przygotowaniu...")
    else:
        print(f"Użycie: python3 {sys.argv[0]} [--hamilton | --non-hamilton]")

if __name__ == "__main__":
    main()