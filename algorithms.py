import random
from graph import Graph

def generate_hamiltonian_graph(graph: Graph, target_saturation: int):
    """Generuje graf spójny nieskierowany z gwarantowanym cyklem Hamiltona."""
    n = graph.num_vertices
    vertices = list(range(n))
    
    random.shuffle(vertices)
    current_edges = 0

    for i in range(n):
        u = vertices[i]
        v = vertices[(i + 1) % n]
        graph.add_edge(u, v)
        current_edges += 1

    max_edges = (n * (n - 1)) // 2
    target_edges = (max_edges * target_saturation) // 100

    while current_edges + 3 <= target_edges:
        u, v, w = random.sample(range(n), 3)
        if not graph.has_edge(u, v) and not graph.has_edge(v, w) and not graph.has_edge(w, u):
            graph.add_edge(u, v)
            graph.add_edge(v, w)
            graph.add_edge(w, u)
            current_edges += 3

def is_safe_to_add(v: int, graph: Graph, path: list, pos: int) -> bool:
    """Sprawdza, czy wierzchołek v może zostać bezpiecznie dodany do ścieżki."""
    if not graph.has_edge(path[pos - 1], v):
        return False
    if v in path:
        return False
    return True

def find_hamiltonian_cycle_util(graph: Graph, path: list, pos: int) -> bool:
    """Rekurencyjny algorytm z powracaniem (backtracking)."""
    n = graph.num_vertices
    if pos == n:
        return graph.has_edge(path[pos - 1], path[0])

    for v in range(1, n):
        if is_safe_to_add(v, graph, path, pos):
            path[pos] = v
            if find_hamiltonian_cycle_util(graph, path, pos + 1):
                return True
            path[pos] = -1
    return False

def find_and_print_hamiltonian_cycle(graph: Graph) -> bool:
    """Inicjuje przeszukiwanie i wyświetla wynik."""
    path = [-1] * graph.num_vertices
    path[0] = 0

    if not find_hamiltonian_cycle_util(graph, path, 1):
        print("Cykl Hamiltona nie istnieje.\n")
        return False

    path.append(path[0])
    cycle_str = " -> ".join(map(str, path))
    print(f"Znaleziono Cykl Hamiltona: {cycle_str}\n")
    return True

# --- Sekcja: Cykl Eulera (Algorytm Hierholzera) ---

def find_and_print_eulerian_cycle(graph: Graph) -> bool:
    """Znajduje cykl Eulera używając algorytmu Hierholzera."""
    n = graph.num_vertices
    
    # Kopiujemy macierz, ponieważ algorytm Hierholzera "niszczy" krawędzie podczas przechodzenia
    adj_copy = [row[:] for row in graph.adjacency_matrix]
    
    # Sprawdzenie warunku koniecznego (parzyste stopnie)
    for i in range(n):
        degree = sum(adj_copy[i])
        if degree % 2 != 0:
            print("Graf nie posiada cyklu Eulera (istnieje wierzchołek o nieparzystym stopniu).\n")
            return False

    # Stos do śledzenia ścieżki i lista wynikowa
    stack = [0]
    circuit = []

    while stack:
        u = stack[-1]
        has_neighbor = False
        
        # Szukamy pierwszego dostępnego sąsiada
        for v in range(n):
            if adj_copy[u][v]:
                # Usuwamy krawędź, by nie przejść nią drugi raz
                adj_copy[u][v] = False
                adj_copy[v][u] = False
                stack.append(v)
                has_neighbor = True
                break
        
        # Jeśli utknęliśmy (brak nieodwiedzonych sąsiadów), zdejmujemy wierzchołek
        if not has_neighbor:
            circuit.append(stack.pop())

    # Wynik odwracamy, by pokazać poprawną kolejność
    circuit.reverse()
    cycle_str = " -> ".join(map(str, circuit))
    print(f"Znaleziono Cykl Eulera (Algorytm Hierholzera):\n{cycle_str}\n")
    return True