import csv
import os
import json
import urllib.request

python_script_version = "ATV 1.0-beta"
print("Version du script python d'AnimeTime :" + python_script_version)
animedata = {"url" : "https://raw.githubusercontent.com/Arthur276/AnimeData/main/",
            "nom_fichier_distant" : "main_anime_list.json",
            "nom_fichier_local" : "animedata_list.json",
            "dict_nom_anime_clé" : "nom_anime",
            "dict_episodes_clé" : "saisons_episodes"}

class Episode():
    def __init__(self,anime_id_memoire,saison_id_memoire,numero_episode,nom_episode):
        self.anime_id_memoire = anime_id_memoire
        self.saison_id_memoire = saison_id_memoire
        self.numero_episode = numero_episode
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
            anime_id_memoire.nb_saisons += 1
            anime_id_memoire.nb_episodes += nb_episodes
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

    def edit_nom_episode(self,numero_episode,nom):
        # STATUS : OK
        """Renomme un épisode"""
        self.dict_episodes[numero_episode].nom_episode = nom

    def afficher_episodes_saison(self):
        # STATUS : OK
        """Affiche les episode d'une saison"""
        list_episodes_saison = {}
        for episode in self.dict_episodes.keys():
            list_episodes_saison[episode] = self.dict_episodes[episode]


class Anime():
    instances_anime = {}
    nb_anime = 0

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
        self.nb_saisons = 0
        self.nb_episodes = 0
        self.episodes_par_saison = {}
        self.dict_saisons = {}
        self.id_local = Anime.nb_anime
        Anime.nb_anime += 1


    @classmethod
    def ajouter_anime(cls,nom_anime,en_ligne = True):
        # STATUS : OK
        """Ajoute un animé"""
        if not en_ligne:
            globals()[f"anime_{Anime.nb_anime-1}"] = Anime(nom_anime)
        else:
            maj_anime_liste()
            charger_anime(nom_anime,maj = False)


    def supprimer_anime(self):
        # STATUS : OK
        """Supprime un animé"""
        del Anime.instances_anime[self.nom_complet]
        Anime.nb_anime -= 1
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


    def ajouter_saison(self,numero_saison,nb_episodes,init = True):
        # STATUS : OK
        """Ajoute une saison a un animé"""
        globals()[f"saison_{self.id_local}_{numero_saison}"] = Saison(self,numero_saison,nb_episodes, init = init)

    def supprimer_saison(self,numero_saison):
        # STATUS : OK
        """Supprime une saison d'un animé"""
        self.nb_saisons -= 1
        self.nb_episodes -= self.dict_saisons[str(numero_saison)].nb_episodes
        del self.dict_saisons[str(numero_saison)]
        print(f"La saison {numero_saison} de l'anime {self.nom_complet} et ses épisodes ont été supprimés")

    def afficher_saisons(self):
        # STATUS : OK
        """Retourne un dictionnaire contenant les saisons d'un animé"""
        affich_saisons = {}
        for saison in self.dict_saisons.keys():
            affich_saisons[saison] = self.dict_saisons[saison].nb_episodes
        return affich_saisons

    def afficher_episodes(self):
        #STATUS : OK
        """Retourne un dictionnaire contenant les noms d'épisode aux numéro d'épisodes associés"""
        affich_episode = {}
        for saison in self.dict_saisons.keys():
            id_saison = self.dict_saisons[saison]
            for episode in id_saison.dict_episodes.keys():
                id_episode = id_saison.dict_episodes[episode]
                titre = id_episode.nom_episode
                affich_episode[f"S{saison}-E{episode}"] = id_episode.nom_episode
        return affich_episode

    def export_dict(self):
        """Exporte toutes les données d'un animé vers un dictionnaire"""
        #STATUS : BETA
        json_anime = {}
        for saison in self.dict_saisons.keys():
            saison_instance = self.dict_saisons[saison]
            json_episodes = {}
            for episode in saison_instance.dict_episodes.keys():
                episode_instance = saison_instance.dict_episodes[episode]
                json_episodes[str(episode_instance.numero_episode)] = episode_instance.nom_episode
            json_saisons_episodes[str(saison_instance.numero_saison)] = json_episodes
        json_dict ={animedata["dict_nom_anime_clé"]: self.nom_complet,animedata["dict_episodes_clé"] : json_episodes}
        return json_dict

def maj_anime_liste():
    """Télécharge le fichier source d'AnimeData contenant les données des animés"""
    #STATUS : OK
    urllib.request.urlretrieve(animedata["url"] + animedata["nom_fichier_distant"],animedata["nom_fichier_local"])
    with open(animedata["nom_fichier_local"],"r",encoding = "utf-8") as animedata_json:
        animedata_json_dict = json.load(animedata_json)
        print("Données d'AnimeData téléchargées !")
        print("Version AnimeData :" + animedata_json_dict["ANIMEDATA-METADATA"]["animedata_version"])
        print("Voici les animés disponible en ligne :")
        for element in animedata_json_dict.values():
            if element["type"] == "anime":
                print(element[animedata["dict_nom_anime_clé"]])

def charger_anime(nom_anime,maj = False):
    """Charge ou met a jour un animé depuis le fichier local d'AnimeData"""
    #STATUS : OK
    with open(animedata["nom_fichier_local"],"r",encoding ="utf-8") as animedata_json:
        animedata_json_dict = json.load(animedata_json)
        for element in animedata_json_dict.values():
            if element["type"] == "anime" and nom_anime == element[animedata["dict_nom_anime_clé"]]:
                if not maj:
                    Anime.ajouter_anime(nom_anime,en_ligne = False)
                id_memoire_anime = Anime.instances_anime[nom_anime]
                for saison in element[animedata["dict_episodes_clé"]].keys():
                    id_memoire_anime.ajouter_saison(int(saison),len(element[animedata["dict_episodes_clé"]][saison]))
                    id_memoire_saison = id_memoire_anime.dict_saisons[int(saison)]
                    for episode in element[animedata["dict_episodes_clé"]][saison].keys():
                        id_memoire_saison.edit_nom_episode(int(episode),element[animedata["dict_episodes_clé"]][saison][episode])
                print("L'animé a bien été téléchargé")

def sauv_anime():
    #STATUS : OBSOLETE
    """Enregistre les animés dans le fichier anime.csv"""
    print("Enregistrement des animés en cours...")
    header = ["anime","saisons","episodes"]
    with open("anime.csv", "w", newline='', encoding ="utf-8") as main_csv:
        writer = csv.writer(main_csv, delimiter=',')
        writer.writerow(header)
        for anime_to_save in Anime.instances_anime.keys():
            id_anime_to_save = Anime.instances_anime[anime_to_save]
            ligne = [id_anime_to_save.nom_complet, id_anime_to_save.nb_saisons, id_anime_to_save.nb_episodes]
            writer.writerow(ligne)
    print("Les animés ont été enregistrés dans le fichier 'anime.csv'.")

def sauv_episodes():
    #STATUS : OBSOLETE
    """Enregistre les episodes des animés présents dans le fichier anime.csv dans un fichier 'nom_anime'"""
    print("Enregistrement des noms d'épisodes des animés...")
    for anime_to_save in Anime.instances_anime.keys():
        id_anime = Anime.instances_anime[anime_to_save]
        with open("anime.csv","r",newline='', encoding ="utf-8") as verif_csv:
            reader = csv.DictReader(verif_csv,delimiter = ',')
            anime_saved = []
            for ligne in reader:
                anime_saved.append(ligne["anime"])
        if anime_to_save in anime_saved:
            with open(f"{anime_to_save}.csv", "w", newline = '', encoding ="utf-8") as main_csv:
                writer = csv.writer(main_csv, delimiter='|')
                header = ["saison","episode","nom_episode"]
                writer.writerow(header)
                for saison in id_anime.dict_saisons.keys():
                    id_saison = id_anime.dict_saisons[saison]
                    for episode in id_saison.dict_episodes.keys():
                        id_episode = id_saison.dict_episodes[episode]
                        ligne = [id_saison.saison,id_episode.numero_episode,id_episode.nom_episode]
                        writer.writerow(ligne)
            print(f"Les noms des épisodes de {anime_to_save} ont été enregistrés dans {anime_to_save}.csv .")
        else :
            print("L'animé n'est pas enregistré dans le fichier principal 'anime.csv', il ne pourra pas être récupéré.")
            print("Veuillez utiliser la fonction sauv_anime avant de rééxécuter cette fonction ou alors utilisez la fonction sauv_data")

def sauv_data():
    #STATUS : OBSOLETE
    """Combine les deux fonctions de sauvegarde"""
    print("Enregistrement de toutes les données (Animés et Épisodes)...")
    sauv_anime()
    sauv_episodes()
    print("Toutes les données ont été correctement enregistrées.")

def recup_data():
    #STATUS : OBSOLETE
    """Récupère les données des animés dans le fichier anime.csv s'il est présent, puis récupère les fichiers par animé pour obtenir les épisodes"""
    print("Les animés vont être récupérés s'ils sont présents dans le fichier 'anime.csv'.")
    print("Récupération des données en cours...")
    try:
        with open("anime.csv", "r", encoding ="utf-8") as main_csv:
            reader = csv.DictReader(main_csv, delimiter=',')
            for ligne in reader:
                Anime.ajouter_anime(ligne["anime"],online = False)
        print("Les noms des épisodes des animés présents dans le fichier 'anime.csv' vont être récupérés")
        for anime_to_read in Anime.instances_anime.keys():
            id_anime = Anime.instances_anime[anime_to_read]
            with open(f"{anime_to_read}.csv", encoding ="utf-8") as anime_csv:
                reader = csv.DictReader(anime_csv, delimiter='|')
                saison_found = {}
                for ligne in reader :
                    if ligne["saison"] in saison_found.keys():
                        saison_found[ligne["saison"]] = saison_found[ligne["saison"]] + 1
                    else:
                        saison_found[ligne["saison"]] = 1
            with open(f"{anime_to_read}.csv", encoding ="utf-8") as episode_csv:
                reader_ep = csv.DictReader(episode_csv, delimiter='|')
                for saison in saison_found.keys():
                    globals()[f"saison_{id_anime.id_local}_{saison}"] = Saison(id_anime,saison,saison_found[saison])
                    id_saison = id_anime.dict_saisons[saison]
                    for ligne in reader_ep:
                        if ligne["saison"] == saison:
                            globals()[f"episode_{id_anime.id_local}_{id_saison.numero_saison}_{ligne['episode']}"] = Episode(id_anime,id_saison,ligne["episode"],ligne["nom_episode"])
                    print(f"La saison {saison} est ses épisodes de l'animé {anime_to_read} ont été récupérés")
    except FileNotFoundError:
        print("Aucune donnée n'est enregistrée !")


def clean_data(type = "file"):
    #STATUS : OBSOLETE
    """Nettoie les fichiers ou la mémoire des animés chargés"""
    try:
        if type == "file" or type == "all" :
            print("Suppression de toutes les données enregistrées...")
            for anime_to_delete in Anime.instances_anime.keys():
                id_anime = Anime.instances_anime[anime_to_delete]
                os.remove(f"{anime_to_delete}.csv")
            os.remove("anime.csv")
            print("Les données des fichiers ont été correctement supprimées.")
        if type == "memoire" or type == "all" :
            for anime_instance in Anime.instances_anime.keys():
                del Anime.instances_anime[anime_instance]
            print("Les données de la mémoire ont été supprimées")
    except FileNotFoundError:
        print("Il n'y a aucune donnée à supprimer !")
