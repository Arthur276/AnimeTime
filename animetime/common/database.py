import animedata.common.lib_interactions as adlib
import animedata.common.metadata as admeta
from animetime.classes.anime import Anime
from animetime.common.instances import instance_exist, select_all_instances

def import_database(animes_list: list = None, ad_online: bool = True) -> None:
    """Import one or several animes from AnimeData.

    Args:
        animes_list (list, optional): List of animes to load. Defaults to None.
        ad_online (bool, optional): _description_. Defaults to True.
    """
    if ad_online:
        adlib.get_ad_lib()
    dict_ad = adlib.get_ad_lib_content(ad_online)
    if animes_list == None:
        animes_list = []
    for element in dict_ad.values():
        if element["type"] == "anime":
            anime_name = element[admeta.ad_table["anime_name"]]
            if anime_name in animes_list or len(animes_list)==0:
                if instance_exist(anime_name, Anime.animes_index, True, "presence"):
                    Anime.animes_index[anime_name].delete_seasons()
                else:
                    Anime.add_anime(anime_name)
                Anime.animes_index[anime_name].import_anime(element)

def export_database(animes_list: list = None) -> dict:
    """Merge several anime dict in a dict in order to be used by AnimeData.

    Args:
        animes_list (list, optional): contains the list of animes to export.
        Default to None.

    Returns:
        dict: contains the dictionnaries of the animes.
    """
    ad_dict = {}
    animes_list = select_all_instances(Anime.animes_index, animes_list)
    animes_ignored = []
    for anime_to_export in animes_list:
        if not instance_exist(anime_to_export,
                          Anime.animes_index,
                          True,
                          "missing"):
            animes_ignored.append(anime_to_export)
        else:
            ad_dict[anime_to_export] = \
                Anime.animes_index[anime_to_export].export_anime()
    return ad_dict