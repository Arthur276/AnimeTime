import csv
import os
import requests
from bs4 import BeautifulSoup

class Episode():
    # classe des épisodes d'une saison d'un animé
    def __init__(self,anime_id,saison_id,numero_episode,nom_episode):
        self.anime = anime_id
        self.saison = saison_id
        self.numero_episode = numero_episode
        saison_id.dict_episodes[numero_episode] = self
        self.nom_episode = nom_episode


class Saison():
    #classe des saison d'un animé, qui peut contenir des épisodes
    def __init__(self,anime_id, numero_saison, nb_episodes,init = True):
        try :
            self.anime = anime_id
            self.nb_episodes = nb_episodes
            self.saison = numero_saison
            self.dict_episodes = {}
            anime_id.dict_saisons[numero_saison] = self
            anime_id.nb_saisons += 1
            anime_id.nb_episodes += nb_episodes
            if init:
                self.init_episodes()
            print(f"La saison {numero_saison} de {anime_id.nom_complet} a été ajouté")

        except ValueError:
            print("Le numéro de la saison doit être un entier !")

    def init_episodes(self):
        #fonction qui crée automatiquement des épisodes avec comme nom par défaut "Episode XX"
        # STATUS : OK
        for episode in range(1,self.nb_episodes+1):
            globals()[f"episode_{self.anime.id}_{self.saison}_{episode}"] = Episode(self.anime,self,episode,f"Episode {episode}")

    def nom_episode(self,numero_episode,nom):
        # STATUS : OK
        self.dict_episodes[f"E{numero_episode}"].nom_episode = nom
        globals()[f"episode_{self.anime.id}_{self.saison}_{numero_episode}"].nom_episode = nom

    def afficher_episodes_saison(self):
        # STATUS : OK
        list_episodes_saison = {}
        for episode in self.dict_episodes.keys():
            list_episodes_saison[episode] = self.dict_episodes[episode]


class Anime():
    #classe des animés, qui peuvent contenir des saisons et des épisodes
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
        self.id = Anime.nb_anime
        Anime.nb_anime += 1


    @classmethod
    def ajouter_anime(cls,nom_anime):
        # STATUS : OK
        globals()[f"anime_{Anime.nb_anime}"] = Anime(nom_anime)

    def supprimer_anime(self):
        # STATUS : OK
        print(f"Suppresion de l'animé {self.nom_complet}")
        del Anime.instances_anime[self.nom_complet]
        Anime.nb_anime -= 1
        print(f"L'animé {self.nom_complet} à été supprimé")

    @classmethod
    def afficher_anime(cls):
        # STATUS : OK
        list_anime = []
        print("Voici les animés ajoutés : ")
        for instance in Anime.instances_anime.values():
            list_anime.append(instance.nom_complet)
        return list_anime


    def ajouter_saison(self,numero_saison,nb_episodes,init = True):
        # STATUS : OK
        globals()[f"saison_{self.id}_{numero_saison}"] = Saison(self,numero_saison,nb_episodes)

    def supprimer_saison(self,nom_saison):
        # STATUS : OK
        self.nb_saisons -= 1
        self.nb_episodes -= self.dict_saisons[nom_saison].nb_episodes
        del self.dict_saisons[nom_saison]
        print("La saison et ses épisodes ont été supprimés")

    def afficher_saisons(self):
        # STATUS : OK
        affich_saisons = {}
        for saison in self.dict_saisons.keys():
            affich_saisons[saison] = self.dict_saisons[saison].nb_episodes
        return affich_saisons

    def webscrapp_episodes(self):
        # STATUS : BETA
        print("Cette fonction ne fonctionne qu'avec l'animé SNK")
        print("ATTENTION : Fonctions obsolète qui ne fonctionne pas avec le reste des commandes")
        url = "https://attaque-des-titans.fandom.com/fr/wiki/Liste_des_%C3%89pisodes"
        if self.nom_complet == "SNK" :
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')
            globals()[f"saison_{self.id}_1"] = Saison(self,1,87)
            id_saison = self.dict_saisons[1]
            for episode in range(1,87+1):
                resultats = soup.find(title = f"Épisode {episode}")
                globals()[f"episode_{self.id}_1_{episode}"] = Episode(self,id_saison,episode,resultats.string)
                print(resultats.string)
            print(f"Webscrapping effectué depuis {url}")

    def afficher_episodes(self):
        #STATUS : OK
        affich_episode = {}
        for saison in self.dict_saisons.keys():
            id_saison = self.dict_saisons[saison]
            for episode in id_saison.dict_episodes.keys():
                id_episode = id_saison.dict_episodes[episode]
                titre = id_episode.nom_episode
                affich_episode[f"S{saison}-E{episode}"] = id_episode.nom_episode
        return affich_episode


def sauv_anime():
    #STATUS : OK
    print("Enregistrement des animés en cours...")
    header = ["anime","saisons","episodes"]
    with open("anime.csv", "w", newline='', encoding ="utf-8") as main_csv:
        writer = csv.writer(main_csv, delimiter=',')
        writer.writerow(header)
        for anime in Anime.instances_anime.keys():
            id = Anime.instances_anime[anime]
            ligne = [id.nom_complet, id.nb_saisons, id.nb_episodes]
            writer.writerow(ligne)
    print("Les animés ont été enregistrés dans le fichier 'anime.csv'.")

def sauv_episodes():
    #STATUS : OK
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
    print("Enregistrement de toutes les données (Animés et Épisodes)...")
    sauv_anime()
    sauv_episodes()
    print("Toutes les données ont été correctement enregistrées.")

def recup_data():
    #STATUS : OK
    print("ATTENTION : La récupération des données provoque la suppression de toutes les données non enregistrées")
    print("Les animés vont être récupérés s'ils sont présents dans le fichier 'anime.csv'.")
    print("Récupération des données en cours...")
    try:
        with open("anime.csv", "r", encoding ="utf-8") as main_csv:
            reader = csv.DictReader(main_csv, delimiter=',')
            for ligne in reader:
                globals()[f"anime_{Anime.nb_anime}"] = Anime(ligne["anime"])
                globals()[f"anime_{Anime.nb_anime}"].nb_saisons = int(ligne["saisons"])
                globals()[f"anime_{Anime.nb_anime}"].nb_episodes = int(ligne["episodes"])
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
                    globals()[f"saison_{id_anime.id}_{saison}"] = Saison(id_anime,saison,saison_found[saison])
                    id_saison = id_anime.dict_saisons[saison]
                    for ligne in reader_ep:
                        if ligne["saison"] == saison:
                            globals()[f"episode_{id_anime.id}_{id_saison.saison}_{ligne['episode']}"] = Episode(id_anime,id_saison,ligne["episode"],ligne["nom_episode"])
                    print(f"La saison {saison} est ses épisodes de l'animé {anime_to_read} ont été récupérés")
    except FileNotFoundError:
        print("Aucune donnée n'est enregistrée !")


def clean_data(type = "file"):
    #STATUS : OK
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
