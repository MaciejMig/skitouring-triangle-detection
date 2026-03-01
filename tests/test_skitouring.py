import os
import sys
import unittest

# Allow "src" imports when running tests from repo root
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)

from src.skitouring import SkiGraph, candidate_has_triangle, compute_qualified_candidates


class TestSkitouring(unittest.TestCase):
    def test_triangle_detected(self):
        g = SkiGraph(3)
        g.add_edge(1, 2)
        g.add_edge(2, 3)
        g.add_edge(1, 3)
        ok, tri = candidate_has_triangle(g, 1)
        self.assertTrue(ok)
        self.assertIsNotNone(tri)
        qualified, triangles = compute_qualified_candidates(g, 3)
        self.assertEqual(set(qualified), {1, 2, 3})

    def test_no_triangle_in_tree(self):
        g = SkiGraph(4)
        g.add_edge(1, 2)
        g.add_edge(2, 3)
        g.add_edge(3, 4)
        qualified, _ = compute_qualified_candidates(g, 4)
        self.assertEqual(qualified, [])

    def test_edge_validation(self):
        g = SkiGraph(3)
        g.add_edge(1, 1)  # ignored
        g.add_edge(1, 2)
        g.add_edge(1, 2)  # duplicate ignored
        self.assertTrue(g.has_edge(1, 2))
        self.assertFalse(g.has_edge(1, 1))


if __name__ == "__main__":
    unittest.main(verbosity=2)
