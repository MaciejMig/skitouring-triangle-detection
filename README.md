# Skitouring — triangle detection in an undirected graph (Python)

Course project for **Algorithms & Data Structures**.

The program models a network of shelters and ski routes as an **undirected graph** and determines which competitors (starting in shelters `1..K`) can finish the stage.  
A competitor starting at vertex `i` finishes if and only if there exist distinct vertices `u, v` such that edges `(i, u)`, `(i, v)` and `(u, v)` exist — i.e. `i` belongs to at least one **triangle** (a 3-cycle).

## What’s inside

- **Triangle detection with early-exit**: for each `i = 1..K` checks pairs of neighbors and stops after finding the first triangle.
- **Robust input validation** (ranges, duplicates, self-loops) + **connectivity check** for interactive input.
- **Two modes**
  - interactive input from keyboard
  - random connected graph generation (spanning tree + extra edges)
- Optional **Windows executable** (`dist/skitouring.exe`) built with PyInstaller.

## Repository structure

```
src/                # main program (CLI)
tests/              # minimal unit tests (unittest)
examples/           # sample stdin sessions
reports/report.pdf  # project report (PL)
dist/skitouring.exe # compiled Windows binary (optional)
```

## Quickstart (Python)

Requires **Python 3.8+** (standard library only).

```bash
# run interactive mode (menu)
python src/skitouring.py
```

Run using prepared sample inputs:

```bash
# K5 - everyone qualifies
python src/skitouring.py < examples/sample_k5.txt

# a tree - nobody qualifies
python src/skitouring.py < examples/sample_tree.txt
```

## Tests

```bash
python -m unittest -v
```

## Build a Windows .exe (optional)

If you want to rebuild the binary yourself:

```bash
pip install pyinstaller
pyinstaller --onefile --console --name skitouring src/skitouring.py
```

The executable will be created in `dist/`.

## Notes

- The original course constraints assumed small graphs (e.g., `N ≤ 20`), but the approach generalizes well to sparse graphs.
- This repository intentionally **does not** ship any external datasets (inputs are entered interactively or generated randomly).

---

**Author (implementation):** Maciej Migasiuk  
**Report (documentation & analysis):** Kacper Mocarski
