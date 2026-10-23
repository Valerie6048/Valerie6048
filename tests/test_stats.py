import unittest
from xml.etree import ElementTree
from unittest.mock import patch
from scripts.update_stats import collect, render
from scripts import update_stats


class StatsTests(unittest.TestCase):
    def test_pagination_filtering_and_totals(self):
        def repo(name, fork=False, private=False):
            return dict(full_name=name, fork=fork, private=private,
                        stargazers_count=2, forks_count=1)

        calls = []

        def fetch(path):
            calls.append(path)
            if path == "/users/example":
                return {"followers": 7}
            if path.endswith("&page=1"):
                return [repo("example/one"), repo("example/private", private=True)] + [repo("example/fork", fork=True)] * 98
            if path.endswith("&page=2"):
                return [repo("example/two")]
            if path.endswith("/languages"):
                return {"Python": 300, "C++": 100}
            self.fail(f"Unexpected path: {path}")

        self.assertEqual(collect("example", fetch), dict(repositories=2, stars=4,
                         forks=2, followers=7, languages={"Python": 600, "C++": 200}))
        self.assertEqual(len(calls), 5)

    def test_svg_escaping_and_percentages_include_all_languages(self):
        stats = dict(repositories=1, stars=0, forks=0, followers=0,
                     languages={"A&B": 50, "B": 10, "C": 10, "D": 10, "E": 10, "F": 10})
        cards = render(stats, "2026-10-23")
        for svg in cards.values():
            ElementTree.fromstring(svg)
        self.assertIn("A&amp;B", cards["github-languages.svg"])
        self.assertIn("50.0%", cards["github-languages.svg"])
        self.assertEqual(cards["github-languages.svg"].count("10.0%"), 4)

    def test_empty_account(self):
        stats = dict(repositories=0, stars=0, forks=0, followers=0, languages={})
        svg = render(stats, "2026-10-23")["github-languages.svg"]
        self.assertIn("No language data", svg)
        ElementTree.fromstring(svg)

    def test_api_failure_preserves_existing_cards(self):
        with patch.object(update_stats, "collect", side_effect=RuntimeError("API unavailable")):
            with patch.object(update_stats.Path, "write_text") as write:
                with self.assertRaises(RuntimeError):
                    update_stats.main()
                write.assert_not_called()


if __name__ == "__main__":
    unittest.main()
