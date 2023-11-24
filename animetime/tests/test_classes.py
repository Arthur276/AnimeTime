import unittest
from animetime.classes.anime import Anime
from animetime.classes.season import Season
from animetime.classes.episode import Episode
from animedata.common.metadata import ad_table as admeta


class testAnime(unittest.TestCase):
    def test_init(self):
        anime_test = Anime("ANIMETEST")
        self.assertEqual(anime_test.name, "ANIMETEST")
        self.assertEqual(anime_test.seasons_index, {})
        self.assertEqual(Anime.animes_index["ANIMETEST"], anime_test)
        Anime.delete_animes(["ANIMETEST"])

    def test_delete_animes(self):
        Anime("ANIMETEST1")
        Anime("ANIMETEST2")
        Anime.delete_animes(["ANIMETEST1", "ANIMETEST2"])
        self.assertFalse("ANIMETEST1" in Anime.animes_index.keys())
        self.assertFalse("ANIMETEST2" in Anime.animes_index.keys())
   
    def test_export_anime_list(self):
        anime_test = Anime("ANIMETEST")
        self.assertEqual(Anime.export_anime_list(), ["ANIMETEST"])
        Anime.delete_animes(["ANIMETEST"])

    def test_add_season(self):
        anime_test = Anime("ANIMETEST")
        anime_test.add_season(1)
        self.assertTrue(1 in anime_test.seasons_index.keys())
        Anime.delete_animes(["ANIMETEST"])

    def test_delete_seasons(self):
        anime_test = Anime("ANIMETEST")
        anime_test.add_season(1)
        anime_test.delete_seasons([1])
        self.assertFalse(1 in anime_test.seasons_index.keys())
        Anime.delete_animes(["ANIMETEST"])

    def test_export_anime(self):
        anime_test = Anime("ANIMETEST")
        export = anime_test.export_anime()
        self.assertEqual(export["type"], "anime")
        self.assertEqual(export[admeta["anime_name"]], "ANIMETEST")
        self.assertEqual(export[admeta["seasons"]], {})
        Anime.delete_animes(["ANIMETEST"])

    def test_import_anime(self):
        anime_test = Anime("ANIMETEST")
        anime_test.import_anime({"type": "anime",
                                 admeta["seasons"]: {1: {}}})
        self.assertTrue(1 in anime_test.seasons_index.keys())
        Anime.delete_animes("ANIMETEST")

class testSeasons(unittest.TestCase):
    def test_init(self):
        anime_test = Anime("ANIMETEST")
        season_test = Season(anime_test, 1)
        self.assertEqual(season_test.anime_object, anime_test)
        self.assertEqual(season_test.number, 1)
        self.assertEqual(season_test.episodes_index, {})
        self.assertEqual(anime_test.seasons_index[1], season_test)
        Anime.delete_animes(["ANIMETEST"])

    def test_add_episode(self):
        anime_test = Anime("ANIMETEST")
        season_test = Season(anime_test, 1)
        season_test.add_episode(1)
        self.assertTrue(1 in season_test.episodes_index.keys())
        Anime.delete_animes(["ANIMETEST"])

    def test_delete_episode(self):
        anime_test = Anime("ANIMETEST")
        season_test = Season(anime_test, 1)
        season_test.add_episode(1)
        season_test.delete_episodes([1])
        self.assertFalse(1 in season_test.episodes_index.keys())
        Anime.delete_animes(["ANIMETEST"])

    def test_edit_episode_data(self):
        pass

    def test_export_season(self):
        anime_test = Anime("ANIMETEST")
        season_test = Season(anime_test, 1)
        export = season_test.export_season()
        self.assertEqual(export, {})
        Anime.delete_animes(["ANIMETEST"])

    def test_import_season(self):
        anime_test = Anime("ANIMETEST")
        season_test = Season(anime_test, 1)
        import_dict = {1: {admeta["episode_duration"]: 12,
                           admeta["episode_release_date"]: (12,7,2007),
                           admeta["episode_name"]: "EPISODETEST"}}
        season_test.import_season(import_dict)
        episode_test = season_test.episodes_index[1]
        self.assertEqual(episode_test.name, "EPISODETEST")
        self.assertEqual(episode_test.duration, 12)
        self.assertEqual(episode_test.release_date, (12,7,2007))




