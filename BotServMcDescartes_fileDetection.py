import discord
from discord.ext import commands
import csv
import os.path
import asyncio

#####################################################################################################################################
def lecture_fichier(nom_fichier:str):
    with open(nom_fichier, mode='r') as fichier_ouvert:
        return list(csv.reader(fichier_ouvert, delimiter=","))

#####################################################################################################################################
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all(), help_command=None)
liste=list(lecture_fichier('liste_eleves_premiere.csv'))

#####################################################################################################################################
@bot.event
async def on_ready():
    print("------>>> Bot ready")
    print("------>>> Checking for a file")
    while True:
        if os.path.isfile("/home/gabanger/files/ip_reject.txt"):
            liste=list(lecture_fichier('liste_eleves_premiere.csv'))
            await asyncio.sleep(0.1)
            ipReject=open("/home/gabanger/files/ip_reject.txt","r")
            content=ipReject.readlines()
            print("------>>> Ip_reject")
            for i in range(len(liste)):
                if "{}\n".format(liste[i][3])==content[0]:
                    author=bot.get_user(int(liste[i][4]))
                    userIp=open('/home/gabanger/files/userIp.txt','w')
                    userIp.write(content[0])
                    userIp.write(content[1])
                    message=await author.send("Quelqu'un a tenté de se connecter au Serveur Minecraft des premières de Descartes avec votre compte avec l'IP {}, cette IP ne figure pas dans votre liste d'IP autorisées.\nVoulez-vous accepter cette IP ?\nRéagissez ci-dessous.\n:warning: N'acceptez que s'il s'agit de vous.".format(content[1]))
                    await message.add_reaction('\U0000274C')
                    await message.add_reaction('\U00002705')
                    userIp.close()

            ipReject.close()
            os.remove("/home/gabanger/files/ip_reject.txt")
        else:
            await asyncio.sleep(5)

#####################################################################################################################################
bot.run("")         # Your token here
