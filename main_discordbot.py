import discord
from discord.ext import commands
import csv
import os
import main_anime as anipy
from main_anime import Anime
bot = commands.Bot(command_prefix = "a!", description = "AnimeTime discord bot, devloped by Arthur")

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
            for saison in range(1,id.number_seasons+1):
                for episode in range(1,id.number_episodes+1):
                    key = f"S{saison}:E{episode}"
                    if key in id.dict_saisons.keys():
                        episode_trouve = id.dict_saisons[key]
                        if episode_trouve != "":
                            await ctx.send(f"Saison {saison}, Episode {episode} : {episode_trouve}")

@bot.command()
async def enregistrer(ctx):
        await ctx.send("Les animés suivants vont être enregistés : ")
        await afficher_anime(ctx = ctx, mode = "only")
        anipy.sauv_anime()
        anipy.sauv_episodes()
        await ctx.send("Les animés et leurs données ont été enregistrés")



bot.run("OTE2Njc0NzAwNDA1NTM4ODY4.Yatl1w.AEXrtRr9kVyyMFoeYHZcfr_tD_I")
