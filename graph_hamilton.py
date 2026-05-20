import random

class Graf:
    def __init__(self, ilosc_wierzcholkow: int):
        self.ilosc_wierzcholkow = ilosc_wierzcholkow
        # Inicjalizacja macierzy sąsiedztwa
        self.macierz_sasiedztwa = [[0] * ilosc_wierzcholkow for _ in range(ilosc_wierzcholkow)]
    
    def generowanie_hamiltona(self, procent_saturacji: float):
        # generuje spójny graf hamiltonowski, w którym każdy wierzchołek ma parzysty stopień

        # 1. Tworzenie początkowego cyklu Hamiltona (losowa permutacja)
        wierzcholki = list(range(self.ilosc_wierzcholkow))
        random.shuffle(wierzcholki)

        for i in range(self.ilosc_wierzcholkow):
            u = wierzcholki[i]
            v = wierzcholki[(i + 1) % self.ilosc_wierzcholkow]
            self.macierz_sasiedztwa[u][v] = 1
            self.macierz_sasiedztwa[v][u] = 1
        
        # 2. Obliczanie docelowej liczby krawędzi na podstawie nasycenia
        max_krawedzi = (self.ilosc_wierzcholkow * (self.ilosc_wierzcholkow - 1)) // 2
        targetowane_krawedzie = int(max_krawedzi * (procent_saturacji / 100.0))
        obecne_krawedzie = self.ilosc_wierzcholkow  # Cykl Hamiltona ma n krawędzi

        # 3. Dopełnianie grafu losowymi 3 wierzchołkowymi krawędziami, aż osiągniemy docelową liczbę krawędzi,
        #    to dba o parzysty stopień każdego wierzchołka
        while obecne_krawedzie < targetowane_krawedzie:
            u,v,w = random.sample(range(self.ilosc_wierzcholkow), 3)

            # odwracanie stanu krawedzi trojkata (np 1 -> 0, 0 -> 1) aby zachowac parzystosc stopni
            self.macierz_sasiedztwa[u][v] = 1 - self.macierz_sasiedztwa[u][v]
            self.macierz_sasiedztwa[v][u] = 1 - self.macierz_sasiedztwa[v][u]

            self.macierz_sasiedztwa[v][w] = 1 - self.macierz_sasiedztwa[v][w]
            self.macierz_sasiedztwa[w][v] = 1 - self.macierz_sasiedztwa[w][v]

            self.macierz_sasiedztwa[w][u] = 1 - self.macierz_sasiedztwa[w][u]
            self.macierz_sasiedztwa[u][w] = 1 - self.macierz_sasiedztwa[u][w]
            
            # przeliczanie krawedzi
            obecne_krawedzie = sum(sum(row) for row in self.macierz_sasiedztwa) // 2