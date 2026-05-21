class Graph:
    """
    Reprezentacja grafu nieskierowanego za pomocą macierzy sąsiedztwa.
    Wybrano macierz, ponieważ ułatwia ona szybkie sprawdzanie istnienia krawędzi.
    """
    def __init__(self, num_vertices: int):
        self.num_vertices = num_vertices
        self.vertices = num_vertices
        self.adjacency_matrix = [[False] * num_vertices for _ in range(num_vertices)]

    def add_edge(self, u: int, v: int):
        """Dodaje nieskierowaną krawędź między wierzchołkami u i v."""
        self.adjacency_matrix[u][v] = True
        self.adjacency_matrix[v][u] = True

    def remove_edge(self, u, v):
        self.adjacency_matrix[u][v] = False
        self.adjacency_matrix[v][u] = False

    def has_edge(self, u: int, v: int) -> bool:
        """Sprawdza, czy istnieje krawędź między u i v."""
        return self.adjacency_matrix[u][v]

    def display(self):
        """Wypisuje reprezentację grafu do konsoli z wyrównanymi kolumnami i indeksem."""
        print("\nMacierz sąsiedztwa grafu:")
        
        # Ustalamy szerokość pojedynczej kolumny w znakach (np. 3 znaki wystarczą do czytelności)
        col_width = 3
        
        # 1. Nagłówek - Numeracja kolumn
        header = " " * 4 + " "  # Margines na indeksy wierszy i kreskę separatora
        for i in range(self.num_vertices):
            header += f"{i:>{col_width}}"
        print(header)
        
        # 2. Linia oddzielająca nagłówek od wartości
        separator = " " * 4 + "+" + "-" * (self.num_vertices * col_width)
        print(separator)
        
        # 3. Wiersze macierzy (Indeks wiersza | wartości)
        for idx, row in enumerate(self.adjacency_matrix):
            row_str = f"{idx:>3} | "  # Indeks wiersza wyrównany do prawej + pionowa kreska
            for edge in row:
                val = "1" if edge else "0"
                row_str += f"{val:>{col_width}}"
            print(row_str)
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
