import unittest

from resources.lib.matching import (
    build_tmdbh_queries,
    normalize_title,
    score_episode_result,
    score_movie_result,
)


class MatchingTests(unittest.TestCase):
    def test_movie_query_generation(self):
        params = {"mediatype": "movie", "title": "Dune", "originaltitle": "Duna", "year": "2021"}
        queries = build_tmdbh_queries(params)
        self.assertEqual(queries[0], "Dune 2021")
        self.assertIn("Duna 2021", queries)

    def test_episode_query_generation(self):
        params = {"mediatype": "episode", "showname": "Silo", "show_originaltitle": "Silo", "season": "1", "episode": "2", "episode_title": "The Engineer"}
        queries = build_tmdbh_queries(params)
        self.assertIn("Silo S01E02", queries)
        self.assertIn("Silo 1x02", queries)


    def test_episode_query_generation_from_tvshowtitle_alias(self):
        params = {"mediatype": "episode", "tvshowtitle": "Andor", "season": "1", "episode": "3", "title": "Reckoning"}
        queries = build_tmdbh_queries(params)
        self.assertIn("Andor S01E03", queries)

    def test_movie_scoring_year_and_title(self):
        params = {"title": "Dune", "originaltitle": "Dune", "year": "2021"}
        good = score_movie_result({"name": "Dune.2021.1080p.WEB-DL.mkv"}, params)
        bad = score_movie_result({"name": "Dune.1984.1080p.mkv"}, params)
        self.assertGreater(good, bad)

    def test_episode_sxe_preferred_over_x(self):
        params = {"showname": "Silo", "season": "1", "episode": "2"}
        sxe = score_episode_result({"name": "Silo.S01E02.1080p.mkv"}, params)
        xfmt = score_episode_result({"name": "Silo.1x02.1080p.mkv"}, params)
        self.assertGreater(sxe, xfmt)

    def test_accent_normalization(self):
        self.assertEqual(normalize_title("Příliš_žluťoučký.kůň"), "prilis zlutoucky kun")

    def test_bad_penalty(self):
        params = {"title": "Dune", "year": "2021"}
        normal = score_movie_result({"name": "Dune.2021.1080p.WEB-DL.mkv"}, params)
        trailer = score_movie_result({"name": "Dune.2021.trailer.1080p.mkv"}, params)
        self.assertGreater(normal, trailer)


if __name__ == "__main__":
    unittest.main()
