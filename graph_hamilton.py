import random
import time

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

    def wyswietl_macierz(self):
        """Wypisuje graf w wybranej reprezentacji macierzowej."""
        print("\nMacierz sasiedztwa grafu:")
        print("   " + " ".join(f"{i}" for i in range(self.ilosc_wierzcholkow)))
        print("   " + "- " * self.ilosc_wierzcholkow)
        for idx, row in enumerate(self.macierz_sasiedztwa):
            print(f"{idx} | " + " ".join(str(wartosc) for wartosc in row))

    
    def znajdz_cykl_eulera(self):
        # kopiowanie macierzy sąsiedztwa, aby nie modyfikować oryginału bo to usuwak krawędzie
        macierz_kopia = [row[:] for row in self.macierz_sasiedztwa]
        cykl = []

        start_time = time.perf_counter()

        # stos zamiast rekurencji zeby uniknąć problemów
        stack = [0] # zaczynamy od wierzchołka 0
        while stack:
            u = stack[-1]
            # szukamy pierwszeego wolnego sasiada
            ma_sasiada = False
            for v in range(self.ilosc_wierzcholkow):
                if macierz_kopia[u][v] == 1: # jest krawędź
                    # usuwamy krawędź z kopii
                    macierz_kopia[u][v] = 0
                    macierz_kopia[v][u] = 0
                    stack.append(v) # idziemy dalej
                    ma_sasiada = True
                    break
            if not ma_sasiada:
                # nie ma już sąsiadów, dodajemy do cyklu i wracamy
                cykl.append(stack.pop())
        
        end_time = time.perf_counter()
        czas_wykonania_ms = (end_time - start_time) * 1000  # konwersja na milisekundy
        print("\n--- CYKL EULERA ---")
        print("Sciezka: " + " -> ".join(map(str, reversed(cykl))))
        print(f"Czas wykonania: {czas_wykonania_ms:.6f} ms")


####################################################### POMOCNICZE DO CYKLU HAMILTONA #######################################################

    def _is_hamilton_safe(self, wierzcholek, pos, sciezka):
        # Sprawdza, czy wierzchołki są połączone
        if self.macierz_sasiedztwa[sciezka[pos - 1]][wierzcholek] == 0:
            return False
        # Sprawdza, czy wierzchołek nie jest już w ścieżce
        if wierzcholek in sciezka[:pos]:
            return False
        return True
    
    def _hamilton_util(self, sciezka, pos):
        # czy ostatni wierzchołek jest połączony z pierwszym
        if pos == self.ilosc_wierzcholkow:
            return self.macierz_sasiedztwa[sciezka[pos - 1]][sciezka[0]] == 1

        for wierzcholek in range(1, self.ilosc_wierzcholkow):
            if self._is_hamilton_safe(wierzcholek, pos, sciezka):
                sciezka[pos] = wierzcholek
                if self._hamilton_util(sciezka, pos + 1):
                    return True
                sciezka[pos] = -1 # backtrack
        return False
    
#######################################################################################################################################

    def znajdz_cykl_hamiltona(self):
        sciezka = [-1] * self.ilosc_wierzcholkow
        sciezka[0] = 0 # zaczynamy od wierzchołka 0

        start_time = time.perf_counter()
        ma_cykl = self._hamilton_util(sciezka, 1)
        end_time = time.perf_counter()
        czas_wykonania_ms = (end_time - start_time) * 1000  # konwersja na milisekundy
        print("\n--- CYKL HAMILTONA ---")
        print(f"Czas wykonania: {czas_wykonania_ms:.6f} ms")
        if ma_cykl:
            print("Sciezka: " + " -> ".join(map(str, sciezka)))
        else:
            print("\nNie znaleziono cyklu Hamiltona.")

# Przykładowe użycie
if __name__ == "__main__":
    ilosc_wierzcholkow = 10
    procent_saturacji = 30.0

    graf = Graf(ilosc_wierzcholkow)
    graf.generowanie_hamiltona(procent_saturacji)
    graf.wyswietl_macierz()
    graf.znajdz_cykl_eulera()
    graf.znajdz_cykl_hamiltona()