import csv
import os
import requests
from bs4 import BeautifulSoup

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
        self.dict_episodes = {}

    @classmethod
    def ajouter_anime(cls,nom_anime):
        globals()[f"Anime_{Anime.nb_anime}"] = Anime(nom_anime)
        Anime.nb_anime += 1

    def supprimer_anime(self):
        del Anime.instances_anime[self.nom_complet]
        del self.nb_saisons
        del self.nb_episodes
        del self.dict_episodes
        print(f"L'animé {self.nom_complet} à été supprimé")


    def webscrapp_episodes(self):
        print("Cette fonction ne fonctionne qu'avec l'animé SNK")
        url = "https://attaque-des-titans.fandom.com/fr/wiki/Liste_des_%C3%89pisodes"
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        for episode in range(1,self.nb_episodes+1):
            resultats = soup.find(title = f"Épisode {episode}")
            self.dict_episodes[f"S1:E{episode}"] = resultats.string

    def afficher_episodes(self):
        for saison in range(0,self.nb_saisons+1):
            for episode in range(0,self.nb_episodes+1):
                titre_episode = self.dict_episodes.get(f"S{saison}:E{episode}")
                if str(type(titre_episode)) == "<class 'str'>":
                    print(f"Saison {saison} ; Épisode {episode} : {titre_episode}")

    @classmethod
    def afficher_anime(cls):
        print("Voici les animés ajoutés : ")
        for instance in Anime.instances_anime.values():
            print(instance.nom_complet)


def sauv_anime():
    print("Enregistrement des animés en cours...")
    header = ["anime", "saisons", "episodes"]
    with open("anime.csv", "w", newline='', encoding ="utf-8") as main_csv:
        writer = csv.writer(main_csv, delimiter=',')
        writer.writerow(header)
        for anime in Anime.instances_anime.keys():
            id = Anime.instances_anime[anime]
            ligne = [id.nom_complet, id.nb_saisons, id.nb_episodes]
            writer.writerow(ligne)
    print("Les animés ont été enregistrés dans le fichier 'anime.csv'.")

def sauv_episodes():
    print("Enregistrement des noms d'épisodes des animés présents dans le fichier 'animé.csv'...")
    for anime_to_save in Anime.instances_anime.keys():
        id_anime = Anime.instances_anime[anime_to_save]
        with open(f"{anime_to_save}.csv", "w", newline = '', encoding ="utf-8") as main_csv:
            writer = csv.writer(main_csv, delimiter='|')
            header = ["episode","nom_episode"]
            writer.writerow(header)
            for episode in id_anime.dict_episodes:
                ligne =  [episode,id_anime.dict_episodes[episode]]
                writer.writerow(ligne)
        print(f"Les noms des épisodes de {anime_to_save} ont été enregistrés dans {anime_to_save}.csv .")

def sauv_data():
    clean_data()
    print("Enregistrement de toutes les données (Animés et Épisodes)...")
    sauv_anime()
    sauv_episodes()
    print("Toutes les données ont été correctement enregistrées.")

def recup_data():
    print("Les animés vont être récupérés s'ils sont présents dans le fichier 'anime.csv'.")
    print("Récupération des données en cours...")
    try:
        with open("anime.csv", "r", encoding ="utf-8") as main_csv:
            reader = csv.DictReader(main_csv, delimiter=',')
            nb_anime = 0
            for ligne in reader:
                globals()[f"Anime_{Anime.nb_anime}"] = Anime(ligne["anime"])
                globals()[f"Anime_{Anime.nb_anime}"].nb_saisons = int(ligne["saisons"])
                globals()[f"Anime_{Anime.nb_anime}"].nb_episodes = int(ligne["episodes"])
                Anime.nb_anime += 1
        print("Les noms des épisodes des animés présents dans le fichier 'anime.csv' vont être récupérés")
        for anime_to_read in Anime.instances_anime.keys():
            id_anime = Anime.instances_anime[anime_to_read]
            with open(f"{anime_to_read}.csv", encoding ="utf-8") as anime_csv:
                reader = csv.DictReader(anime_csv, delimiter='|')
                for ligne in reader:
                    id_anime.dict_episodes[ligne["episode"]] = ligne["nom_episode"]
            print(f"Les noms des épisodes de {anime_to_read} ont été récupérés.")
    except FileNotFoundError:
        print("Aucune donnée n'est enregistrée !")


def clean_data():
    try:
        print("Suppression de toutes les données enregistrées...")
        for anime_to_delete in Anime.instances_anime.keys():
            id_anime = Anime.instances_anime[anime_to_delete]
            os.remove(f"{anime_to_delete}.csv")
        os.remove("anime.csv")
        print("Les données ont été correctement supprimées.")
    except FileNotFoundError:
        print("Il n'y a aucune donnée à supprimer !")
