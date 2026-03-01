#!/usr/bin/env python3
"""
Projekt 11: Skitouring
Algorytmy i Struktury Danych

Program:
- wczytuje lub losuje dane wejściowe (N, K, lista szlaków),
- modeluje Góry Bajtockie jako graf nieskierowany,
- dla każdego zawodnika i = 1..K sprawdza, czy istnieje trasa
  w postaci cyklu długości 3:
      i -> u -> v -> i
  gdzie u, v są różnymi schroniskami,
  a wszystkie trzy krawędzie istnieją w grafie.
"""

from dataclasses import dataclass, field
from typing import List, Set, Tuple, Dict, Optional
import random




@dataclass
class SkiGraph:
    """
    Graf nieskierowany reprezentujący sieć szlaków skitourowych.

    Wierzchołki:    1..n  (schroniska)
    Krawędzie:      istniejące szlaki skitourowe
    """
    n: int
    adj: List[Set[int]] = field(init=False)

    def __post_init__(self) -> None:
        self.adj = [set() for _ in range(self.n + 1)]

    def add_edge(self, u: int, v: int) -> None:
        """
        Dodaje szlak pomiędzy schroniskami u i v.
        Pomijamy pętle (u == v) oraz duplikaty.
        """
        if u == v:
            return
        if v in self.adj[u]:
            return

        self.adj[u].add(v)
        self.adj[v].add(u)

    def has_edge(self, u: int, v: int) -> bool:
        """Sprawdza, czy istnieje szlak (u, v)."""
        return v in self.adj[u]

    def edges(self) -> List[Tuple[int, int]]:
        """
        Zwraca listę wszystkich krawędzi (każda tylko raz, (u, v) z u < v).
        Przydaje się w trybie losowym do wypisania grafu.
        """
        result = []
        for u in range(1, self.n + 1):
            for v in self.adj[u]:
                if u < v:
                    result.append((u, v))
        return result

def is_connected(graph: SkiGraph) -> bool:
    """Sprawdza, czy graf jest spójny (DFS od wierzchołka 1)."""
    if graph.n == 0:
        return True
    visited = set()
    stack = [1]
    while stack:
        u = stack.pop()
        if u in visited:
            continue
        visited.add(u)
        for v in graph.adj[u]:
            if v not in visited:
                stack.append(v)
    return len(visited) == graph.n


def candidate_has_triangle(
    graph: SkiGraph,
    start: int
) -> Tuple[bool, Optional[Tuple[int, int, int]]]:
    """
    Sprawdza, czy dla zawodnika startującego ze schroniska 'start'
    istnieje trasa:
        start -> u -> v -> start
    gdzie:
        - u i v są różnymi schroniskami,
        - wszystkie trzy szlaki istnieją w grafie.

    Zwraca:
        (True,  (start, u, v))  jeśli taki trójkąt istnieje,
        (False, None)           w przeciwnym przypadku.
    """
    neighbors = list(graph.adj[start])
    ln = len(neighbors)

    if ln < 2:
        return False, None

    for i in range(ln):
        u = neighbors[i]
        for j in range(i + 1, ln):
            v = neighbors[j]
            if u == v:
                continue
            if graph.has_edge(u, v):
                return True, (start, u, v)

    return False, None


def compute_qualified_candidates(
    graph: SkiGraph,
    k: int
) -> Tuple[List[int], Dict[int, Tuple[int, int, int]]]:
    """
    Dla zawodników o numerach 1..k (i jednocześnie schronisk startowych 1..k)
    sprawdza, kto może ukończyć etap.

    Zwraca:
        - listę numerów zawodników, którzy mają przynajmniej jeden trójkąt,
        - słownik: zawodnik -> przykładowa trasa (start, u, v).
    """
    qualified: List[int] = []
    triangles: Dict[int, Tuple[int, int, int]] = {}

    for start in range(1, k + 1):
        ok, tri = candidate_has_triangle(graph, start)
        if ok and tri is not None:
            qualified.append(start)
            triangles[start] = tri

    return qualified, triangles



def generate_random_connected_graph(
    n: int,
    extra_edge_prob: float = 0.3
) -> SkiGraph:
    """
    Generuje losowy spójny graf nieskierowany na wierzchołkach 1..n.

    - Najpierw tworzymy losowe drzewo rozpinające,
    - potem z pewnym prawdopodobieństwem dokładamy dodatkowe krawędzie.

    Parametr extra_edge_prob decyduje, jak "gęsty" jest graf.
    """
    g = SkiGraph(n)


    vertices = list(range(1, n + 1))
    random.shuffle(vertices)
    for i in range(1, n):
        u = vertices[i]
        v = random.choice(vertices[:i])
        g.add_edge(u, v)

    for u in range(1, n + 1):
        for v in range(u + 1, n + 1):
            if not g.has_edge(u, v) and random.random() < extra_edge_prob:
                g.add_edge(u, v)

    return g




def interactive_input() -> Tuple[SkiGraph, int]:
    while True:
        try:
            n = int(input("Podaj liczbę schronisk N (>= 2, zalecane 6-20): "))
            if n < 2:
                print("N musi być większe lub równe 2.")
                continue
            break
        except ValueError:
            print("To nie jest poprawna liczba całkowita.")

    while True:
        try:
            k = int(input(f"Podaj liczbę zawodników K (1..{n}): "))
            if not 1 <= k <= n:
                print("Musi być 1 <= K <= N.")
                continue
            break
        except ValueError:
            print("To nie jest poprawna liczba całkowita.")

    max_edges = n * (n - 1) // 2
    while True:
        try:
            m = int(input(f"Podaj liczbę dostępnych szlaków M ({n-1}..{max_edges}): "))
            if not n - 1 <= m <= max_edges:
                print(f"M musi być w zakresie {n-1}..{max_edges}.")
                continue
            break
        except ValueError:
            print("To nie jest poprawna liczba całkowita.")

    while True:
        g = SkiGraph(n)
        print("\nPodaj M par wierzchołków (x y), 1 <= x,y <= N, x != y.")
        print("Krawędzie są nieskierowane.")

        for i in range(m):
            while True:
                try:
                    line = input(f"Szlak {i + 1}: ")
                    x_str, y_str = line.strip().split()
                    x = int(x_str)
                    y = int(y_str)

                    if not (1 <= x <= n and 1 <= y <= n):
                        print("Wierzchołki muszą być w zakresie 1..N.")
                        continue
                    if x == y:
                        print("Brak pętli: x i y muszą być różne.")
                        continue
                    if g.has_edge(x, y):
                        print("Taki szlak już istnieje, podaj inną parę.")
                        continue

                    g.add_edge(x, y)
                    break
                except ValueError:
                    print("Podaj dwie liczby całkowite oddzielone spacją.")

        if is_connected(g):
            return g, k

        print("\n❗ Graf jest NIESPÓJNY – nie da się przejść między wszystkimi schroniskami.")
        print("Podaj ponownie wszystkie szlaki (M par), tak aby graf był spójny.\n")



def main() -> None:
    while True:
        print("\n=== Projekt 11: Skitouring ===")
        print("1 - wczytanie danych z klawiatury")
        print("2 - losowanie przykładowych danych")
        print("0 - zakończ program")
        choice = input("Wybierz tryb [0/1/2]: ").strip()

        if choice == "0":
            print("Koniec programu.")
            break

        elif choice == "2":
            random.seed()
            n = random.randint(6, 20)
            k = random.randint(1, n)
            g = generate_random_connected_graph(n, extra_edge_prob=0.4)

            print(f"\nWylosowano N = {n} schronisk, K = {k} zawodników.")
            print("Lista dostępnych szlaków (M par):")
            edges = g.edges()
            print(f"M = {len(edges)}")
            for (u, v) in edges:
                print(u, v)

        elif choice == "1":
            g, k = interactive_input()

        else:
            print("Niepoprawny wybór, spróbuj ponownie.")
            continue

        qualified, triangles = compute_qualified_candidates(g, k)

        print("\nZawodnicy, którzy mogą ukończyć aktualny etap kwalifikacji:")
        if not qualified:
            print("Żaden zawodnik nie spełnia warunków (brak możliwych trójkątów).")
        else:
            for s in qualified:
                start, u, v = triangles[s]
                print(f"- Zawodnik {s}: przykładowa trasa "
                      f"{start} -> {u} -> {v} -> {start}")


if __name__ == "__main__":
    main()

