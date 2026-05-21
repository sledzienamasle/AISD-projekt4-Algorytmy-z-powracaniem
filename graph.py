class Graph:
    """
    Reprezentacja grafu nieskierowanego za pomocą macierzy sąsiedztwa.
    Wybrano macierz, ponieważ ułatwia ona szybkie sprawdzanie istnienia krawędzi.
    """
    def __init__(self, num_vertices: int):
        self.num_vertices = num_vertices
        self.adjacency_matrix = [[False] * num_vertices for _ in range(num_vertices)]

    def add_edge(self, u: int, v: int):
        """Dodaje nieskierowaną krawędź między wierzchołkami u i v."""
        self.adjacency_matrix[u][v] = True
        self.adjacency_matrix[v][u] = True

    def has_edge(self, u: int, v: int) -> bool:
        """Sprawdza, czy istnieje krawędź między u i v."""
        return self.adjacency_matrix[u][v]

    def display(self):
        """Wypisuje reprezentację grafu do konsoli."""
        print("\nMacierz sąsiedztwa grafu:")
        for row in self.adjacency_matrix:
            print(" ".join("1" if edge else "0" for edge in row))
        print()

    def export_to_tikz(self, filename="graf.tex"):
        """
        Generuje plik .tex zawierający kod tikzpicture z wizualizacją grafu.
        Wierzchołki są automatycznie rozkładane na okręgu.
        """
        import math

        with open(filename, "w", encoding="utf-8") as f:
            f.write("% Kod do wklejenia do sprawozdania w LaTeXu\n")
            f.write("\\begin{tikzpicture}[scale=2, every node/.style={circle, draw, fill=blue!10, inner sep=2pt, minimum size=6mm}]\n")
            
            # 1. Definiowanie pozycji wierzchołków na okręgu
            r = 2.0  # promień okręgu w cm
            for i in range(self.num_vertices):
                # Obliczanie kąta dla każdego wierzchołka w radianach
                angle = (2 * math.pi * i) / self.num_vertices
                x = r * math.cos(angle)
                y = r * math.sin(angle)
                f.write(f"    \\node ({i}) at ({x:.2f}, {y:.2f}) {{{i}}};\n")
            
            f.write("\n    % Krawędzie grafu\n")
            f.write("    \\begin{scope}[on background layer]\n") # opcjonalne, wymaga \usetikzlibrary{backgrounds}
            
            # 2. Generowanie krawędzi (tylko raz dla każdej pary u-v)
            for i in range(self.num_vertices):
                for j in range(i + 1, self.num_vertices):
                    if self.adjacency_matrix[i][j]:
                        f.write(f"    \\draw ({i}) -- ({j});\n")
                        
            f.write("    \\end{scope}\n")
            f.write("\\end{tikzpicture}\n")
        print(f"\n[Sukces] Wyeksportowano wizualizacje grafu do pliku: {filename}")
