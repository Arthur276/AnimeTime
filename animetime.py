"""Module that provides tools to manage its anime or tv series."""

import animedata as ad
import tomllib
import os.path
import warnings


dir_path = os.path.dirname(__file__)


with open(os.path.join(dir_path, ".\\pyproject.toml"), mode="rb") as pypr:    
    at_version = tomllib.load(pypr)["project"]["version"]
print("AnimeTime script version : ", at_version)


class Episode():
    """A class to create episodes.

    Attributes:
        anime_object (object): anime object related to the episode
        season_object (object): season object related to the episode
        episode_number (int): episode number
        episode_name (str): episode name
        episode_duration (int): episode duration (in seconds)
        release_date (dict): dictionnary contaning episode's release date
    """

    def __init__(self,
                 anime_object: object,
                 season_object:object,
                 episode_number: int,
                 episode_name: str = None,
                 episode_duration: int = None,
                 episode_release_date: list = None):
        """Initialize an Episode instance and add it to its season's index.

        Args:
            anime_object (object): anime object related to the episode
            season_object (object): season object related to the episode
            episode_number (int): episode number
            episode_name (str): episode name. Defaults to None.
            episode_duration (int): episode duration in minutes. 
                Defaults to None
            episode_release_date (list): episode release date in format
                [DD,MM,YYYY]. Default to None
        """
        self.anime_object = anime_object
        self.season_object = season_object
        self.number = episode_number
        self.duration = episode_duration
        self.release_date = episode_release_date
        self.name = episode_name
        season_object.episodes_index[episode_number] = self
    
    def export_episode(self)-> dict:
        """Export the episode and its data into a AnimeData friendly dict.

        Returns:
            dict: contains episode data
        """
        episode_dict = {}
        episode_dict[ad.ad_table["episode_name"]] = self.name
        episode_dict[ad.ad_table["episode_duration"]] = self.duration
        episode_dict[ad.ad_table["episode_release_date"]] = self.release_date
        return episode_dict
    
    def import_episode(self, episode_dict:dict):
        """Import and replace the data of an episode with the dict data.

        Args:
            episode_dict (dict): contains episode data.
        """
        self.duration = episode_dict[ad.ad_table["episode_duration"]]
        self.name = episode_dict[ad.ad_table["episode_name"]]
        self.release_date = episode_dict[ad.ad_table["episode_release_date"]]


class Season():
    """A class to create seasons.

    Attributes:
        anime_object (object): anime object related to the season
        number_of_episodes (int): number of episodes in the season
        season_number (int): season number
        episodes_index (dict): index of every episode instance of the season,
            binding episode number and its object
    """

    def __init__(self,
                 anime_object: object,
                 season_number: int):
        """Initialize an Season instance and adds itself to its anime's index.

        Args:
            anime_object (object): anime object related to the season
            season_number (int): season number
        """
        self.anime_object = anime_object
        self.season_number = season_number
        self.episodes_index = {}
        anime_object.seasons_index[season_number] = self


    def add_episode(self,episode_number: int,episode_name: str = None):
        globals()[f"episode_{self.anime_object.local_id}_ \
                      {self.season_number}_{episode_number}"] \
                      = Episode(self.anime_object,self,episode_number,episode_name)
        
    def delete_episode(self,episode_number: int):
        del self.episodes_index[episode_number]
        print(f"The episode number {episode_number} has been deleted.")
        

    def edit_episode_data(self,
                          episode_number: int,
                          modified_attribute: str,
                          new_value):
        """Edit a specific attribute of an episode.

        Args:
            episode_number (int): number of the episode to be modified
            modified_attribute (str): attribute to be modified
            new_value (any): new value of the modified attribute
        """
        # STATUS : OK
        if modified_attribute == "episode_name":
            self.episodes_index[episode_number].episode_name = new_value
        elif modified_attribute == "episode_duration":
            self.episodes_index[episode_number].episode_duration = new_value
        elif modified_attribute == "release_date":
            self.episodes_index[episode_number].release_date = new_value

    def export_season(self)-> dict:
        """Export

        Returns:
            dict: _description_
        """
        season_dict = {}
        for episode in self.episodes_index.keys():
            season_dict[episode] = \
                self.episodes_index[episode].export_episode()
        return season_dict
    
    
    def import_season(self,season_dict: dict):
        if len(self.episodes_index) >= 0:
            warnings.warn("The season already contains episode, they will be replaced.")
        self.episodes_index = {}
        for episode in season_dict.keys():
            self.add_episode(episode)
            self.episodes_index[episode].import_episode(season_dict[episode])
            
            

class Anime():
    """A class to create animes.

    Attributes:
        animes_index (dict, class attribute): index of every Anime instance
            binding anime name and its object
        animes_number (int, class attribute): number of animes instanced,
            used to create unique anime instances
        name(str) : anime name
        seasons_index (dict) : index of every Season instance of the anime,
            binding season number and its object
        local_id (int): anime number, only depending of animes_number when
            instanced and only used for instance name
    """

    animes_index = {}
    animes_number = 0

    def __new__(cls, anime_name: str):
        """Check if an Anime instance already has the same name as anime_name.

        Args:
            anime_name (str): anime name

        Raises:
            RuntimeError: if an Anime instance has the exact same name
                as anime_name

        """
        instances = cls.animes_index
        if anime_name not in instances.keys():
            instances[anime_name] = super(Anime, cls).__new__(cls)
            print(f"{anime_name} has been added !")
            return instances[anime_name]
        else:
            raise RuntimeError(
                "An Anime instance with the exact same name already exists")

    def __init__(self, anime_name: str):
        """Initialize an Anime instance and increase by one animes_number.

        Args:
            anime_name (str): anime_name
        """
        self.name = anime_name
        self.seasons_index = {}
        self.local_id = Anime.animes_number
        Anime.animes_number += 1

    @classmethod
    def add_anime(cls,
                  anime_name: str,
                  load: bool = False,
                  ad_source: bool = False):
        """Add an anime by creating an Anime instance.

        Args:
            anime_name (str): anime name
            load (bool, optional): defines if the anime should be loaded from
                animedata or not. Defaults to False.
            ad_source (bool, optional): definies if the load file is
                the animedata file or a custom one. Defaults to False.
        """
        # STATUS : OK
        if load:
            if ad_source:
                load_anime(anime_name, ad_source=True)
            else:
                load_anime(anime_name, ad_source=False)
        else:
            globals()[f"anime_{Anime.animes_number-1}"] = Anime(anime_name)

    def delete_anime(self):
        """Delete the anime of the Anime index."""
        # STATUS : OK
        del Anime.animes_index[self.name]
        print(f"{self.name} has been deleted")

    @classmethod
    def export_anime_list(cls) -> list:
        """Return a list containing every anime in the Anime index.

        Returns:
            list: contains the animes of the Anime index
        """
        # STATUS : OK
        list_anime = []
        for instance in Anime.animes_index.values():
            list_anime.append(instance.name)
        return list_anime

    def add_season(self, season_number: int):
        """Add a season to an anime.

        Args:
            season_number (int): the number of the season to be added
            number_of_episodes (int): the number of episodes in the season
        """
        # STATUS : OK
        globals()[f"season_{self.local_id}_{season_number}"] = \
            Season(self, season_number)
        print(f"The season number {season_number} of {self.name} \
have been added.")

    def delete_season(self, season_number: int):
        """Delete a season and its episodes of the season anime index.

        Args:
            season_number (int): number of the season to be deleted
        """
        # STATUS : OK
        del self.seasons_index[season_number]
        print(f"The season number {season_number} of {self.name} \
              and its episodes have been deleted")
        

    def export_dict(self) -> dict:
        """Export a dictionnary containing all the data of the anime.

        Returns:
            dict: contains anime data
        """
        # STATUS : OK
        dict_seasons = {}
        for season in self.seasons_index.keys():
            dict_seasons[season] = \
                self.seasons_index[season].export_season()
        anime_dict = {"type": "anime",
                     ad.ad_table["anime_name"]: self.name,
                     ad.ad_table["seasons"]: dict_seasons}
        return anime_dict


def load_anime(anime: str, ad_source: bool = True):
    """Load an anime using animedata from a json file.

    Args:
        anime (str): anime name to be loaded
        ad_source (bool, optional): defines if the load file :
            the animedata file or a custom one. Defaults to True.
    """
    # STATUS : OK
    if ad_source:
        ad.get_ad_lib()
    dict_ad = ad.get_ad_lib_content(ad_source)
    anime_data = dict_ad[anime]
    if anime not in Anime.animes_index.keys():
        Anime.add_anime(anime, load=False, ad_source=False)
    id_anime = Anime.animes_index[anime]
    for season in anime_data[ad.ad_table["seasons"]].keys():
        dict_season = anime_data[ad.ad_table["seasons"]][season]
        id_anime.add_season(int(season), len(dict_season))
        id_season = id_anime.seasons_index[int(season)]
        for episode in dict_season.keys():
            id_episode = id_season.episodes_index[int(episode)]
            dict_episode = dict_season[episode]
            id_episode.episode_duration = dict_episode[ad.ad_table[
                "episode_duration"]]
            id_episode.release_date = dict_episode[ad.ad_table[
                "episode_release_date"]]
            id_episode.episode_name = dict_episode[ad.ad_table[
                "episode_name"]]
    if ad_source:
        print(f"{anime} has been loaded from AnimeData source file")
    else:
        print(f"{anime} has been loaded from a custom file")


def export_anime(list_anime: list) -> dict:
    """Merge several anime dict in a dict in order to be used by AnimeData

    Args:
        list_anime (list): contains the list of animes to export

    Returns:
        dict: contains the dictionnaries of the animes.
    """
    animes_dict = {}
    for anime_to_export in list_anime:
        if anime_to_export not in Anime.animes_index.keys():
            warnings.warn(
                f"{anime_to_export} is not added to AnimeTime, ingoring it.")
        else:
            animes_dict[anime_to_export] = \
                Anime.animes_index[anime_to_export].export_dict()
            print(f"{anime_to_export} has been exported successfully")
    return animes_dict
    