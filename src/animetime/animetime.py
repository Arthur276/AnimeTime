import animedata as ad

at_version = "0.1.5"
print("Version du script python d'AnimeTime : ", at_version)

class Episode():
    def __init__(self,anime_id_memoire,saison_id_memoire,numero_episode,nom_episode):
        self.anime_id_memoire = anime_id_memoire
        self.saison_id_memoire = saison_id_memoire
        self.numero_episode = numero_episode
        self.duree = 0
        self.date_sortie = {}
        saison_id_memoire.dict_episodes[numero_episode] = self
        self.nom_episode = nom_episode


class Saison():
    def __init__(self,anime_id_memoire, numero_saison, nb_episodes,init = True):
        try :
            self.anime_id_memoire = anime_id_memoire
            self.nb_episodes = nb_episodes
            self.numero_saison = numero_saison
            self.dict_episodes = {}
            anime_id_memoire.dict_saisons[numero_saison] = self
            if init:
                self.init_episodes()
            print(f"La saison {numero_saison} de {anime_id_memoire.nom_complet} a été ajouté")
        except ValueError:
            print("Le numéro de la saison doit être un entier !")

    def init_episodes(self):
        # STATUS : OK
        """Crée les épisodes d'une saison au format 'Episode XX'"""
        for episode in range(1,self.nb_episodes+1):
            globals()[f"episode_{self.anime_id_memoire.id_local}_{self.numero_saison}_{episode}"] = Episode(self.anime_id_memoire,self,episode,f"Episode {episode}")

    def edit_info_episode(self,numero_episode,info_modifié,nouvelle_valeur):
        # STATUS : OK
        """Édite les informations d'un épisode"""
        if info_modifié == "nom_episode":
            self.dict_episodes[numero_episode].nom_episode = nouvelle_valeur
        elif info_modifié == "duree_episode":
            self.dict_episodes[numero_episode].duree = nouvelle_valeur
        elif info_modifié == "date_sortie":
            self.dict_episodes[numero_episode].date_sortie = nouvelle_valeur

    def afficher_episodes_saison(self):
        # STATUS : OK
        """Affiche les episode d'une saison"""
        dict_anime = self.anime_id_memoire.export_dict()
        return dict_anime[ad.animedata["dict_episodes_clé"]][str(self.numero_saison)]

class Anime():
    instances_anime = {}
    id_anime = 0

    def __new__(cls, nom_complet):
        instances = cls.instances_anime
        if nom_complet not in instances.keys():
            instances[nom_complet] = super(Anime, cls).__new__(cls)
            print(f"L'animé {nom_complet} à été ajouté !")
        else:
            print(f"L'animé {nom_complet} existe déjà !")
        return instances[nom_complet]

    def __init__(self, nom_complet):
        self.nom_complet = nom_complet
        self.dict_saisons = {}
        self.id_local = Anime.id_anime
        Anime.id_anime += 1


    @classmethod
    def ajouter_anime(cls,nom_anime,load = False, ad_source = False):
        # STATUS : BETA
        """Ajoute un animé"""
        if load:
            if ad_source:
                charger_anime(nom_anime,ad_source = True)
            else:
                charger_anime(nom_anime,ad_source = False)
        else:
            globals()[f"anime_{Anime.id_anime-1}"] = Anime(nom_anime)


    def supprimer_anime(self):
        # STATUS : OK
        """Supprime un animé"""
        del Anime.instances_anime[self.nom_complet]
        print(f"L'animé {self.nom_complet} à été supprimé")

    @classmethod
    def afficher_anime(cls):
        # STATUS : OK
        """Retourne une liste contenant les nom des animés chargés"""
        list_anime = []
        print("Voici les animés ajoutés : ")
        for instance in Anime.instances_anime.values():
            list_anime.append(instance.nom_complet)
        return list_anime


    def ajouter_saison(self,numero_saison,nb_episodes):
        # STATUS : OK
        """Ajoute une saison a un animé"""
        globals()[f"saison_{self.id_local}_{numero_saison}"] = Saison(self,numero_saison,nb_episodes, init = True)

    def supprimer_saison(self,numero_saison):
        # STATUS : OK
        """Supprime une saison d'un animé"""
        del self.dict_saisons[numero_saison]
        print(f"La saison {numero_saison} de l'anime {self.nom_complet} et ses épisodes ont été supprimés")

    def afficher_saisons_episodes(self):
        # STATUS : OK
        """Retourne un dictionnaire contenant les saisons et ses épisodes d'un animé"""
        dict_anime = self.export_dict()
        return dict_anime[ad.animedata["dict_saisons_episodes"]]

    def export_dict(self):
        """Exporte toutes les données d'un animé vers un dictionnaire, utilisable par AnimeData après avoir été formaté"""
        #STATUS : OK
        json_saisons = {}
        for saison in self.dict_saisons.values():
            json_episodes = {}
            for episode in saison.dict_episodes.values():
                json_episodes[str(episode.numero_episode)] = {ad.animedata["dict_date_sortie_episode"] : episode.date_sortie, ad.animedata["dict_duree_episode"] : episode.date_sortie, ad.animedata["dict_nom_episode"] : episode.nom_episode}
            json_saisons[str(saison.numero_saison)] = json_episodes
        json_dict ={"type" : "anime", ad.animedata["dict_nom_anime"]: self.nom_complet,ad.animedata["dict_saisons_episodes"] : json_saisons}
        return json_dict

def format_dict(list_str_anime):
    """Formate les dictionnaires d'animés afin qu'AnimeData puisse les traiter"""
    #STATUS : OK
    dict_anime = {}
    if type(list_str_anime) is list:
        for anime_to_format in list_str_anime:
            dict_anime[anime_to_format] = Anime.instances_anime[anime_to_format].export_dict()
    elif type(list_str_anime) is str:
        dict_anime[list_str_anime] = Anime.instances_anime[list_str_anime].export_dict()
    return dict_anime


def charger_anime(anime,ad_source = True):
    """Charge un animé"""
    #STATUS : OK
    if ad_source:
        ad.maj_anime_lib()
    dict_ad = ad.get_json_dict(ad_source)
    anime_data = dict_ad[anime]
    if anime not in Anime.instances_anime.keys():
        Anime.ajouter_anime(anime,load = False,ad_source = False)
    id_anime = Anime.instances_anime[anime]
    for saison in anime_data[ad.animedata["dict_saisons_episodes"]].keys():
        dict_saison = anime_data[ad.animedata["dict_saisons_episodes"]][saison]
        id_anime.ajouter_saison(int(saison),len(dict_saison))
        id_saison = id_anime.dict_saisons[int(saison)]
        for episode in dict_saison.keys():
            id_episode = id_saison.dict_episodes[int(episode)]
            dict_episode = dict_saison[episode]
            id_episode.duree = dict_episode[ad.animedata["dict_duree_episode"]]
            id_episode.date_sortie = dict_episode[ad.animedata["dict_date_sortie_episode"]]
            id_episode.nom_episode = dict_episode[ad.animedata["dict_nom_episode"]]
    if ad_source:
        print(f"L'animé {anime} a été chargé depuis le fichier local d'AnimeData")
    else:
        print(f"L'animé {anime} a été chargé depuis le fichier personalisé")
