import csv


class Anime():
    instances_anime = {}

    def __new__(cls, nom_complet):
        instances = cls.instances_anime
        if nom_complet not in instances.keys():
            instances[nom_complet] = super(Anime, cls).__new__(cls)
            print(f"L'animé {nom_complet} à été ajouté !")
        else:
            print(f"L'animé {nom_complet} existe déjà !")
        return instances[nom_complet]

    def __init__(self, nom_complet):
        if self == Anime.instances_anime[nom_complet]:
            self.actif = True
            self.nom_complet = nom_complet
            self.number_seasons = "N/A"
            self.number_of_episode = "N/A"
        else:
            self.actif = False

    def checking(self):
            if self.nom_complet in Anime.instances_anime.keys() and self.actif:
                return True
            else:
                return False

    def supprimer_anime(self):
        if self.checking():
            del Anime.instances_anime[self.nom_complet]
            self.actif = False
            print(f"L'animé {self.nom_complet} à été supprimé")
        else:
            print(f"L'anime {self.nom_complet} n'exise pas !")

    def ajouter_episodes(self):
        if self.checking():
            self.number_episodes = 0
            self.dict_saisons = {}
            self.number_seasons = int(input(f"Combien de saisons compte l'animé \
            {self.nom_complet} ?"))
            for saison in range(1, self.number_seasons+1):
                episodes_in_season = int(input(f"Combien d'épisodes compte la saison {saison} \
                de l'animé {self.nom_complet} ?"))
                self.number_episodes += episodes_in_season
                for episode in range(1, episodes_in_season+1):
                        self.dict_saisons[f"S{saison}_E{episode}"] = input(f"Quel est le nom de l'épisode {episode},\
                         de la saison {saison}, de {self.nom_complet} ?")
        else:
            print(f"L'animé {self.nom_complet} n'existe pas !")


def afficher_anime():
    for instance in Anime.instances_anime.values():
        print(instance.nom_complet)


def sauv_anime():
    header = ["anime", "saisons", "episodes"]
    with open("anime.csv", "w", newline='') as main_csv:
        writer = csv.writer(main_csv, delimiter=',')
        writer.writerow(header)
        for anime in Anime.instances_anime.keys():
            id = Anime.instances_anime[anime]
            ligne = [id.nom_complet, id.number_seasons, id.number_of_episode]
            writer.writerow(ligne)


def recup_anime():
    with open("anime.csv", "r") as main_csv:
        reader = csv.DictReader(main_csv, delimiter=',')
        for ligne in reader:
            instance_number = 0
            globals()[f"instance{instance_number}"] = Anime(ligne["anime"])
            globals()[f"instance{instance_number}"].number_seasons =
            ligne["saisons"]
            globals()[f"instance{instance_number}"].number_episodes =
            ligne["episodes"]
            instance_number += 1
