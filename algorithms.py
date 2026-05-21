import random
import time
from graph import Graph

################################# GENEROWANIE GRAFU HAMILTONOWSKIEGO O ZADANYM NASYCENIU ##########################################################

def generate_hamiltonian_graph(graph, target_saturation):
    """
    Generuje spójny graf hamiltonowski o zadanym nasyceniu krawędziami.
    Zapewnia, że każdy wierzchołek ma parzysty stopień.
    """
    import random
    n = graph.vertices
    
    # 1. Tworzenie losowego cyklu Hamiltona
    vertices = list(range(n))
    random.shuffle(vertices)
    
    # Zbiór do przechowywania krawędzi bazowego cyklu (jako posortowane krotki)
    # zapobiegnie to ich przypadkowemu usunięciu podczas dopełniania
    hamilton_edges = set()
    
    for i in range(n):
        u = vertices[i]
        v = vertices[(i + 1) % n]
        graph.add_edge(u, v)
        hamilton_edges.add((min(u, v), max(u, v)))
        
    # 2. Obliczanie docelowej liczby krawędzi
    max_edges = (n * (n - 1)) // 2
    target_edges = int(max_edges * (target_saturation / 100.0))
    
    # Aktualna liczba krawędzi (na starcie jest ich dokładnie n)
    current_edges = n
    
    # Awaryjny licznik iteracji, chroniący przed nieskończoną pętlą
    max_attempts = 100000
    attempts = 0
    
    # 3. Dopełnianie losowymi cyklami 3-wierzchołkowymi (parzystość stopni)
    while current_edges != target_edges and attempts < max_attempts:
        attempts += 1
        u, v, w = random.sample(range(n), 3)
        
        # Tworzymy krawędzie potencjalnego trójkąta (uporządkowane pary)
        e1 = (min(u, v), max(u, v))
        e2 = (min(v, w), max(v, w))
        e3 = (min(w, u), max(w, u))
        
        # Krytyczny warunek: ŻADNA z losowanych krawędzi nie może być krawędzią bazową cyklu Hamiltona!
        if e1 in hamilton_edges or e2 in hamilton_edges or e3 in hamilton_edges:
            continue
            
        # Sprawdzamy, o ile zmieni się liczba krawędzi po odwróceniu stanów w trójkącie
        # (jeśli krawędź istnieje, to zniknie (-1), jeśli jej nie ma, to powstanie (+1))
        delta = 0
        delta += -1 if graph.has_edge(u, v) else 1
        delta += -1 if graph.has_edge(v, w) else 1
        delta += -1 if graph.has_edge(w, u) else 1
        
        # Akceptujemy zmianę tylko jeśli idziemy w stronę celu (target_edges)
        # i nie przekroczymy go w żadną stronę
        if (target_edges - current_edges) * delta > 0:
            if abs(current_edges + delta - target_edges) <= abs(current_edges - target_edges):
                # Odwracamy krawędzie w grafie
                if graph.has_edge(u, v): graph.remove_edge(u, v)
                else: graph.add_edge(u, v)
                    
                if graph.has_edge(v, w): graph.remove_edge(v, w)
                else: graph.add_edge(v, w)
                    
                if graph.has_edge(w, u): graph.remove_edge(w, u)
                else: graph.add_edge(w, u)
                    
                current_edges += delta

################################################# GENEROWANIE GRAFU NIE-HAMILTONOWSKIEGO NASYCENIU 50% ##########################################################

def generate_non_hamiltonian_graph(graph, target_saturation=50):
    """
    Generuje graf nieskierowany nie-hamiltonowski o nasyceniu około 50%
    poprzez wygenerowanie losowego grafu i odizolowanie wierzchołka 0.
    """
    import random
    n = graph.vertices
    
    # 1. Obliczamy ile krawędzi potrzebujemy dla pozostałych (n-1) wierzchołków
    # Cały graf (n) ma mieć docelowo nasycenie 50% z całkowitej liczby krawędzi grafu Kn
    total_max_edges = (n * (n - 1)) // 2
    target_edges = int(total_max_edges * (target_saturation / 100.0))
    
    # Maksymalna liczba krawędzi jaką mogą utworzyć wierzchołki od 1 do n-1
    available_max_edges = ((n - 1) * (n - 2)) // 2
    
    # Zabezpieczenie na wypadek, gdyby matematycznie nie dało się upchać tylu krawędzi bez wierzchołka 0
    actual_target = min(target_edges, available_max_edges)
    
    # 2. Losowo dodajemy krawędzie tylko między wierzchołkami [1, n-1]
    current_edges = 0
    edges_pool = []
    for u in range(1, n):
        for v in range(u + 1, n):
            edges_pool.append((u, v))
            
    random.shuffle(edges_pool)
    
    for i in range(actual_target):
        u, v = edges_pool[i]
        graph.add_edge(u, v)
        
    # Wierzchołek 0 pozostaje całkowicie odizolowany (stopień 0),
    # co gwarantuje, że cykl Hamiltona w tym grafie nie istnieje.

####################################### POMOCNICZE FUNKCJE DLA ZNAJDYWANIA CYKLU HAMILTONA #######################################

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
    start_time = time.perf_counter()
    path = [-1] * graph.num_vertices
    path[0] = 0

    if not find_hamiltonian_cycle_util(graph, path, 1):
        elapsed = time.perf_counter() - start_time
        print("Cykl Hamiltona nie istnieje.\n")
        print(f"Czas wykonania sprawdzenia cyklu Hamiltona: {elapsed:.6f} s\n")
        return False

    path.append(path[0])
    cycle_str = " -> ".join(map(str, path))
    elapsed = time.perf_counter() - start_time
    print(f"Znaleziono Cykl Hamiltona: {cycle_str}\n")
    print(f"Czas wykonania sprawdzenia cyklu Hamiltona: {elapsed:.6f} s\n")
    return True

# --- Sekcja: Cykl Eulera (Algorytm Hierholzera) ---

def find_and_print_eulerian_cycle(graph: Graph) -> bool:
    """Znajduje cykl Eulera używając algorytmu Hierholzera."""
    start_time = time.perf_counter()
    n = graph.num_vertices
    
    # Kopiujemy macierz, ponieważ algorytm Hierholzera "niszczy" krawędzie podczas przechodzenia
    adj_copy = [row[:] for row in graph.adjacency_matrix]
    
    # Sprawdzenie warunku koniecznego (parzyste stopnie)
    for i in range(n):
        degree = sum(adj_copy[i])
        if degree % 2 != 0:
            elapsed = time.perf_counter() - start_time
            print("Graf nie posiada cyklu Eulera (istnieje wierzchołek o nieparzystym stopniu).\n")
            print(f"Czas wykonania sprawdzenia cyklu Eulera: {elapsed:.6f} s\n")
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
    elapsed = time.perf_counter() - start_time
    print(f"Znaleziono Cykl Eulera (Algorytm Hierholzera):\n{cycle_str}\n")
    print(f"Czas wykonania sprawdzenia cyklu Eulera: {elapsed:.6f} s\n")
    return True