#Statut : BETA
import discord
from discord.ext import commands
import csv
import os
import main_anime as anipy
from main_anime import Anime
bot = commands.Bot(command_prefix = "a!", description = "AnimeTime discord bot, developed by Arthur")

discord_file_version = "DV0.1"
print("Version du fichier du bot discord :" + discord_file_version)

@bot.event
async def on_ready():
        anipy.recup_data()
        print("AnimeTime est prêt !")

@bot.command()
async def afficher_anime(ctx,mode = "list"):
        if mode != "only":
            await ctx.send("Les animés ajoutés sont: ")
        if mode == "number":
            number_anime = {}
            nb_anime = 1
        for instance in Anime.instances_anime.values():
            if mode == "number":
                number_anime[nb_anime] = instance.nom_complet
                await ctx.send(f" {nb_anime} : {instance.nom_complet} ")
                nb_anime += 1
            else:
                await ctx.send(instance.nom_complet)
        if mode == "number":
            return number_anime

@bot.command()
async def afficher_episodes(ctx):
        await ctx.send("De quel animé souhaitez-vous afficher les épisodes ? (Entrez le numéro associé)")
        def check_message(message):
            return message.author == ctx.message.author and message.channel == ctx.message.channel
        dict_number = await afficher_anime(ctx,mode = "number")
        message = await bot.wait_for("message", timeout = 10, check = check_message)
        number_selec = int(message.content)
        if number_selec in dict_number.keys():
            id = Anime.instances_anime[dict_number[number_selec]]
            await ctx.send(id.nom_complet)
            message_discord = ""
            for saison in range(1,id.number_seasons+1):
                for episode in range(1,id.number_episodes+1):
                    key = f"S{saison}:E{episode}"
                    if key in id.dict_saisons.keys():
                        episode_trouve = id.dict_saisons[key]
                        if episode_trouve != "":
                            message_episode = (f"Saison {saison}, Episode {episode} : {episode_trouve} \n")
                            if len(message_discord) + len(message_episode) >= 1650:
                                await ctx.send(message_discord)
                                message_discord = message_episode
                            else:
                                message_discord += message_episode
            await ctx.send(message_discord)

@bot.command()
async def enregistrer(ctx):
        await ctx.send("Les animés suivants vont être enregistés : ")
        await afficher_anime(ctx = ctx, mode = "only")
        anipy.sauv_anime()
        anipy.sauv_episodes()
        await ctx.send("Les animés et leurs données ont été enregistrés")

@bot.command()
async def print_episodes_SNK(ctx):
        episodes_snk = Anime.instances_anime["SNK"].afficher_episodes()
        message_discord = ""
        for episode in episodes_snk.keys():
            message_episode = episode + ":" + episodes_snk[episode]
            if len(message_discord) + len(message_episode) >= 1650:
                await ctx.send(message_discord)
                message_discord = message_episode
            else:
                message_discord += message_episode + "\n"
        await ctx.send(message_discord)


bot.run("OTE2Njc0NzAwNDA1NTM4ODY4.GpV3qh.IfB0sPqy2W63muauHzXbN5tt78V3zpoQmOD86E")
