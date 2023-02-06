"""Module that provides tools to manage its anime or tv series."""

import animedata as ad
import tomllib

with open("../animetime/pyproject.toml", mode="rb") as pypr:
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
                 episode_name: str):
        """Initialize an Episode instance and add it to its season's index.

        Args:
            anime_object (object): anime object related to the episode
            season_object (object): season object related to the episode
            episode_number (int): episode number
            episode_name (str): episode name
        """
        self.anime_object = anime_object
        self.season_object = season_object
        self.episode_number = episode_number
        self.episode_duration = 0
        self.release_date = {}
        season_object.episodes_index[episode_number] = self
        self.episode_name = episode_name


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
                 season_number: int,
                 number_of_episodes: int,
                 init_episodes: bool):
        """Initialize an Season instance and adds itself to its anime's index.

        Args:
            anime_object (object): anime object related to the season
            season_number (int): season number
            number_of_episodes (int): number of episodes in the season
            init_episodes (bool): defines if init_episodes() is executed.
        """
        self.anime_object = anime_object
        self.number_of_episodes = number_of_episodes
        self.season_number = season_number
        self.episodes_index = {}
        anime_object.seasons_index[season_number] = self
        if init_episodes:
            self.init_episodes()
        print(f"The season number {season_number} of {anime_object.name} \
have been added")

    def init_episodes(self):
        """Initialize every episode of the season using number_if_episodes \
            with a formatted name."""
        # STATUS : OK
        for episode in range(1, self.number_of_episodes+1):
            globals()[f"episode_{self.anime_object.local_id}_ \
                      {self.season_number}_{episode}"] \
                      = Episode(self.anime_object,
                                self,
                                episode,
                                f"Episode {episode}")

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

    def export_episodes(self) -> dict:
        """Export episodes data of the season.

        Returns:
            dict: dictionnary containing episodes data of the season
        """
        # STATUS : OK
        episodes_data = self.anime_object.export_dict()
        return episodes_data[ad.ad_table[
            "key_seasons_episodes"]][str(self.season_number)]


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

    def add_season(self, season_number: int, number_of_episodes: int):
        """Add a season to an anime.

        Args:
            season_number (int): the number of the season to be added
            number_of_episodes (int): the number of episodes in the season
        """
        # STATUS : OK
        globals()[f"season_{self.local_id}_{season_number}"] = \
            Season(self, season_number, number_of_episodes, init_episodes=True)

    def delete_season(self, season_number: int):
        """Delete a season and its episodes of the season anime index.

        Args:
            season_number (int): number of the season to be deleted
        """
        # STATUS : OK
        del self.seasons_index[season_number]
        print(f"The season number {season_number} of {self.name} \
              and its episodes have been deleted")

    def export_seasons_episodes(self) -> dict:
        """Export a dict containing every seasons and episodes of the anime.

        Returns:
            dict: contains seasons and episodes data of the anime
        """
        # STATUS : OK
        data_seasons = self.export_dict()
        return data_seasons[ad.ad_table["key_seasons_episodes"]]

    def export_dict(self) -> dict:
        """Export a dictionnary containing all the data of the anime.

        Returns:
            dict: contains anime data
        """
        # STATUS : OK
        json_seasons = {}
        for season in self.seasons_index.values():
            json_episodes = {}
            for episode in season.episodes_index.values():
                json_episodes[str(episode.episode_number)] = {
                    ad.ad_table["key_episode_release_date"]:
                        episode.release_date,
                    ad.ad_table["key_episode_duration"]: episode.release_date,
                    ad.ad_table["key_episode_name"]: episode.episode_name}
            json_seasons[str(season.season_number)] = json_episodes
        json_dict = {"type": "anime",
                     ad.ad_table["key_anime_name"]: self.name,
                     ad.ad_table["key_seasons_episodes"]: json_seasons}
        return json_dict


def multi_anime_dict(list_anime: list) -> dict:
    """Put anime dictionnary together in order to exploit this database.

    Args:
        list_anime (list): list containing the anime to export

    Returns:
        dict: contains animes data
    """
    # STATUS : OK
    dict_anime = {}
    for anime_to_format in list_anime:
        dict_anime[anime_to_format] \
             = Anime.animes_index[anime_to_format].export_dict()
    return dict_anime


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
    for season in anime_data[ad.ad_table["key_seasons_episodes"]].keys():
        dict_season = anime_data[ad.ad_table["key_seasons_episodes"]][season]
        id_anime.add_season(int(season), len(dict_season))
        id_season = id_anime.seasons_index[int(season)]
        for episode in dict_season.keys():
            id_episode = id_season.episodes_index[int(episode)]
            dict_episode = dict_season[episode]
            id_episode.episode_duration = dict_episode[ad.ad_table[
                "key_episode_duration"]]
            id_episode.release_date = dict_episode[ad.ad_table[
                "key_episode_release_date"]]
            id_episode.episode_name = dict_episode[ad.ad_table[
                "key_episode_name"]]
    if ad_source:
        print(f"{anime} has been loaded from AnimeData source file")
    else:
        print(f"{anime} has been loaded from a custom file")
