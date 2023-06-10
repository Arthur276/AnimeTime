import unittest
from animetime.classes.anime import Anime
from animetime.classes.season import Season
from animetime.classes.episode import Episode


class testAnime(unittest.TestCase):
    def test_init(self):
        anime_test = Anime("ANIMETEST")
        if Warning.