import csv
import os
import requests
from bs4 import BeautifulSoup

file_version = "V1.1 beta-1"
print("Version du fichier de script :" + file_version)
server_url = "https://webserver-ubuntu.ddns.net"

class Episode():
    def __init__(self,anime_id_memory,saison_id_memory,numero_episode,nom_episode):
        self.anime_id_memory = anime_id_memory
        self.saison_id_memory = saison_id_memory
        self.numero_episode = numero_episode
        saison_id_memory.dict_episodes[numero_episode] = self
        self.nom_episode = nom_episode


class Saison():
    def __init__(self,anime_id_memory, numero_saison, nb_episodes,init = True):
        try :
            self.anime_id_memory = anime_id_memory
            self.nb_episodes = nb_episodes
            self.numero_saison = numero_saison
            self.dict_episodes = {}
            anime_id_memory.dict_saisons[numero_saison] = self
            anime_id_memory.nb_saisons += 1
            anime_id_memory.nb_episodes += nb_episodes
            if init:
                self.init_episodes()
            print(f"La saison {numero_saison} de {anime_id_memory.nom_complet} a été ajouté")
        except ValueError:
            print("Le numéro de la saison doit être un entier !")

    def init_episodes(self):
        # STATUS : OK
        """Crée les épisodes d'une saison au format 'Episode XX'"""
        for episode in range(1,self.nb_episodes+1):
            globals()[f"episode_{self.anime_id_memory.id_local}_{self.numero_saison}_{episode}"] = Episode(self.anime_id_memory,self,episode,f"Episode {episode}")

    def edit_nom_episode(self,numero_episode,nom):
        # STATUS : OK
        """Renomme un épisode"""
        self.dict_episodes[f"E{numero_episode}"].nom_episode = nom
        globals()[f"episode_{self.anime.id_local}_{self.numero_saison}_{numero_episode}"].nom_episode = nom

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
    def ajouter_anime(cls,nom_anime):
        # STATUS : OK
        """Ajoute un animé"""
        globals()[f"anime_{Anime.nb_anime-1}"] = Anime(nom_anime)

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
        globals()[f"saison_{self.id_local}_{numero_saison}"] = Saison(self,numero_saison,nb_episodes)

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

    def webscrapp_anime(self):
        # STATUS : BETA
        page = requests.get(server_url,verify = False)
        soup = BeautifulSoup(page.content, 'html.parser')
        for anime in soup.find_all('li'):
            print(anime.string)


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

    def create_html(self):
        #STATUS : BETA
        """Crée un fichier html contenant toutes les informations de l'animé choisi"""
        default_header = f"<!DOCTYPE html>\n<html>\n<head>\n<meta charset='utf-8' />\n<title>{self.nom_complet}</title>\n</head>\n<body>"
        with open(f"{self.nom_complet}.html", "w", newline='', encoding ="utf-8") as html:
            html.write(default_header)
            html.write(f"<h1>{self.nom_complet}</h1>\n")
            for saison in self.dict_saisons.keys():
                saison_id_memory = self.dict_saisons[saison]
                html.write(f"<h2>Saison {saison}</h2>")
                html.write("\n<ul>\n")
                for episode in saison_id_memory.dict_episodes.keys():
                    episode_id_memory = saison_id_memory.dict_episodes[episode]
                    html.write(f"<li>\n<ul>\n")
                    html.write(f"<li>Saison {saison} - Episode {episode}</li>\n")
                    html.write(f"<li id_saison = '{saison}' id_episode = '{episode}'> {episode_id_memory.nom_episode} </li>\n")
                    html.write("</ul>\n</li>\n")
            html.write("</ul>\n</body>\n</html>\n")

def sauv_anime():
    #STATUS : OK
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
    #STATUS : OK
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
    #STATUS : OK
    """Combine les deux fonctions de sauvegarde"""
    print("Enregistrement de toutes les données (Animés et Épisodes)...")
    sauv_anime()
    sauv_episodes()
    print("Toutes les données ont été correctement enregistrées.")

def recup_data():
    #STATUS : OK
    """Récupère les données des animés dans le fichier anime.csv s'il est présent, puis récupère les fichiers par animé pour obtenir les épisodes"""
    print("Les animés vont être récupérés s'ils sont présents dans le fichier 'anime.csv'.")
    print("Récupération des données en cours...")
    try:
        with open("anime.csv", "r", encoding ="utf-8") as main_csv:
            reader = csv.DictReader(main_csv, delimiter=',')
            for ligne in reader:
                Anime.ajouter_anime(ligne["anime"])
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
    #STATUS : OK
    """Nettoie les fichiers ou la mémoire des animés chargés"""
    try:
        if type == "file" or type == "all" :
            print("Suppression de toutes les données enregistrées...")
            for anime_to_delete in Anime.instances_anime.keys():
                id_anime = Anime.instances_anime[anime_to_delete]
                os.remove(f"{anime_to_delete}.csv")
            os.remove("anime.csv")
            print("Les données des fichiers ont été correctement supprimées.")
        if type == "memory" or type == "all" :
            for anime_instance in Anime.instances_anime.keys():
                del Anime.instances_anime[anime_instance]
            print("Les données de la mémoire ont été supprimées")
    except FileNotFoundError:
        print("Il n'y a aucune donnée à supprimer !")
