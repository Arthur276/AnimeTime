import warnings
from animetime.common.instances import instance_exist, delete_instance
from animetime.classes.episode import Episode

class Season():
    """A class to create seasons.

    Attributes:
        anime_object (object): anime object related to the season
        number_of_episodes (int): number of episodes in the season
        number (int): season number
        episodes_index (dict): index of every episode instance of the season,
            binding episode number and its object
    """

    def __init__(self,
                 anime_object: object,
                 season_number: int) -> None:
        """Initialize an Season instance and add itself to its anime's index.

        Args:
            anime_object (object): anime object related to the season
            season_number (int): season number
        """
        instance_exist(season_number,
                       anime_object.seasons_index,
                       True,
                       "presence")
        self.anime_object = anime_object
        self.number = season_number
        self.episodes_index = {}
        anime_object.seasons_index[season_number] = self
        

    def add_episode(self, episode_number: int) -> None:
        """Add an episode to the season.

        Args:
            episode_number (int): number of the episode
        """
        Episode(self.anime_object, self, episode_number)

    def delete_episodes(self, episodes_list: list = None) -> None:
        """Delete an episode.

        Args:
            episodes_list (int): list of the episodes to delete
        """
        delete_instance(self.episodes_index, episodes_list)

    def edit_episode_data(self,
                          episode_number: int,
                          modified_attribute: str,
                          new_value) -> None:
        """Edit a specific attribute of an episode.

        Args:
            episode_number (int): number of the episode to be modified
            modified_attribute (str): attribute to be modified
            new_value (any): new value of the modified attribute
        """
        if modified_attribute == "episode_name":
            self.episodes_index[episode_number].episode_name = new_value
        elif modified_attribute == "episode_duration":
            self.episodes_index[episode_number].episode_duration = new_value
        elif modified_attribute == "release_date":
            self.episodes_index[episode_number].release_date = new_value

    def export_season(self) -> dict:
        """Export a season and its data.

        Returns:
            dict: episode's data
        """
        season_dict = {}
        for episode in self.episodes_index.keys():
            season_dict[episode] = \
                self.episodes_index[episode].export_episode()
        return season_dict

    def import_season(self, season_dict: dict) -> None:
        """Import the episodes of the season from an AD dictionnary.

        Args:
            season_dict (dict): _description_
        """
        if len(self.episodes_index) > 0:
            warnings.warn("The season already contains episode, \
they will be replaced.")
            self.delete_episodes()
        for episode in season_dict.keys():
            self.add_episode(episode)
            self.episodes_index[episode].import_episode(season_dict[episode])