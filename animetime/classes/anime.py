from animetime.common.instances import instance_exist, delete_instance
from animetime.classes.season import Season
import warnings
from animedata.common.metadata import ad_table as admeta

class Anime():
    """A class to create animes.

    Attributes:
        animes_index (dict, class attribute): index of every Anime instance
            binding anime name and its object
        animes_id_counter (int, class attribute):animes indentifiers counter,
            used to create unique anime instances
        name(str) : anime name
        seasons_index (dict) : index of every Season instance of the anime,
            binding season number and its object
        local_id (int): anime identifier, depending of animes_id_counter when
            instanced and only used for instance name
    """

    animes_index = {}
    animes_id_counter = 0

    def __init__(self, anime_name: str) -> None:
        """Initialize an Anime instance and increase by one animes_id_counter.

        Args:
            anime_name (str): anime name
        """
        instance_exist(anime_name, Anime.animes_index, True, "presence")
        self.name = anime_name
        self.seasons_index = {}
        self.local_id = Anime.animes_id_counter
        Anime.animes_index[anime_name] = self
        Anime.animes_id_counter += 1

    def __del__(self):
        delete_instance(self.seasons_index)
    
    @classmethod
    def add_anime(cls, anime_name: str) -> None:
        """Add an anime by creating an Anime instance.

        Args:
            anime_name (str): anime name
        """
        globals()[f"anime_{Anime.animes_id_counter-1}"] = Anime(anime_name)

    @classmethod
    def delete_animes(cls, animes_list: list = None) -> None:
        """Delete the selected animes.

        Args:
            animes_list (list, optional): list of the animes to delete.
            Defaults to None.
        """
        delete_instance(cls.animes_index, animes_list)

    @classmethod
    def export_anime_list(cls) -> list:
        """Return a list containing every anime in the Anime index.

        Returns:
            list: contains the animes of the Anime index
        """
        return list(cls.animes_index.keys())

    def add_season(self, season_number: int) -> None:
        """Add a season to an anime.

        Args:
            season_number (int): the number of the season to be added.
        """
        globals()[f"season_{self.local_id}_{season_number}"] = \
            Season(self, season_number)

    def delete_seasons(self, seasons_list: list = None) -> None:
        """Delete a season and its episodes of the season anime index.

        Args:
            seasons_list (list): list of the season to be deleted
        """
        delete_instance(self.seasons_index, seasons_list)

    def export_anime(self) -> dict:
        """Export a dictionnary containing all the data of the anime.

        Returns:
            dict: contains anime data
        """
        dict_seasons = {}
        for season in self.seasons_index.keys():
            dict_seasons[season] = self.seasons_index[season].export_season()
        anime_dict = {"type": "anime",
                      admeta.ad_table["anime_name"]: self.name,
                      admeta.ad_table["seasons"]: dict_seasons}
        return anime_dict

    def import_anime(self, anime_dict: dict) -> None:
        """Import anime's data from a dict.

        Args:
            anime_dict (dict): dict containing anime's data.
        """
        if len(self.seasons_index) > 0:
            warnings.warn("The anime already contains seasons,\
they will be replaced.")
            self.delete_seasons()
        for season in anime_dict[admeta.ad_table["seasons"]].keys():
            self.add_season(season)
            self.seasons_index[season].import_season(
                anime_dict[admeta.ad_table["seasons"]][season])