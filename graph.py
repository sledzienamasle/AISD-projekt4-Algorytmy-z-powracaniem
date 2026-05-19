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