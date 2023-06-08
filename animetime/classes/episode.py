from animetime.common.instances import instance_exist
from animedata.common.metadata import ad_table

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
                 season_object: object,
                 episode_number: int,
                 episode_name: str = None,
                 episode_duration: int = None,
                 episode_release_date: list = None) -> None:
        """Initialize an Episode instance and add it to its season's index.

        Args:
            anime_object (object): anime object related to the episode.
            season_object (object): season object related to the episode.
            episode_number (int): episode number.
            episode_name (str, optional): episode name. Defaults to None.
            episode_duration (int, optional): episode duration in minutes.
                Defaults to None
            episode_release_date (list): episode release date in format
                [DD,MM,YYYY]. Default to None
        """
        instance_exist(episode_number,
                       season_object.episodes_index,
                       True,
                       "presence")
        self.anime_object = anime_object
        self.season_object = season_object
        self.number = episode_number
        self.duration = episode_duration
        self.release_date = episode_release_date
        self.name = episode_name
        season_object.episodes_index[episode_number] = self

    def export_episode(self) -> dict:
        """Export the episode and its data into a AnimeData friendly dict.

        Returns:
            dict: contains episode data
        """
        episode_dict = {}
        episode_dict[ad_table["episode_name"]] = self.name
        episode_dict[ad_table["episode_duration"]] = self.duration
        episode_dict[ad_table["episode_release_date"]] = self.release_date
        return episode_dict

    def import_episode(self, episode_dict: dict) -> None:
        """Import and replace the data of an episode with the dict data.

        Args:
            episode_dict (dict): contains episode data.
        """
        self.duration = episode_dict[ad_table["episode_duration"]]
        self.name = episode_dict[ad_table["episode_name"]]
        self.release_date = episode_dict[ad_table["episode_release_date"]]