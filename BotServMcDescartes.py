import discord
from discord.ext import commands
import csv
from time import *
import os

#####################################################################################################################################
def lecture_fichier(nom_fichier:str):                                 # Merci qui ? Merci Vincent et Didier !
    with open(nom_fichier, mode='r') as fichier_ouvert: 
        return list(csv.reader(fichier_ouvert, delimiter=","))

def export(tableau:list,fichier:str):
    file = open(fichier, "w", newline='')
    writer = csv.writer(file)
    writer.writerows(tableau)

liste=list(lecture_fichier('students-list.csv'))

#####################################################################################################################################
def withoutEmphasis(a:str):
    correspondence={'à':'a','â':'a','é':'e','ê':'e','è':'e','ë':'e','ì':'i','î':'i','ï':'i','ô':'o','ò':'o','ö':'o','ù':'u','û':'u','ü':'u','ç':'c'}
    a=list(a)
    for i in range(len(a)):
        if a[i] in correspondence.keys():
            a[i]=correspondence[a[i]]
    return "".join(a)

#####################################################################################################################################
def defineK(rank:int,value)->int:
    for j in range(1,len(liste)):
        if str(value)==str(liste[j][rank]):
            return j

#####################################################################################################################################
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all(), help_command=None)
listeId=[]

#####################################################################################################################################
@bot.event
async def on_ready():
    print("------>>> Bot ready")
    
#####################################################################################################################################
@bot.command(name='wh')
async def whitelist(ctx, lastName:str, firstName:str, Class:str, mcNickname:str):
    if ctx.channel.id==1218672398262468720 or ctx.channel.id==1218667473205985340 or ctx.channel.id==804024422146113616:
        covered=False
        print("------>>>",firstName,lastName,"wants to be added to the whitelist as",mcNickname)
        firstNameBis=withoutEmphasis(firstName).lower()
        lastNameBis=withoutEmphasis(lastName).lower()
        Class=Class.upper()
        for k in range(1,len(liste)):
            if lastNameBis==liste[k][0] and firstNameBis==liste[k][1] and Class==liste[k][2] and not ctx.author.id in listeId and len(liste[k][3])==0:
                liste[k][3]=(str(mcNickname))
                liste[k][4]=(str(ctx.author.id))
                listeId.append(ctx.author.id)
                print("accepted")
                botMessage=await ctx.reply(f"Vous etes accepté dans la whitelist **{firstName}** ! Vous pouvez dès à présent vous connecter au serveur.\n\n||Lorsque vous avez terminé, cliquez sur \U00002705||")
                await botMessage.add_reaction('\U00002705')
                if ctx.channel.id==1218672398262468720:
                    channel=bot.get_channel(1218677627313717371)
                    await channel.send(f"***{mcNickname}*** peut être ajouté à la whitelist. \n__Identité :__ *{firstName} {lastName}, {Class}*")
                print("------>>>",firstName,lastName,"approved in the whitelist")
                wh_add=open("/yourpath/wh_add.txt",'w')         # Your path here
                wh_add.write(mcNickname)
                wh_add.close()
                export(liste,'students-list.csv')
                await ctx.message.delete()
                covered=True
                return

            elif lastNameBis==liste[k][0] and firstNameBis==liste[k][1] and Class==liste[k][2] and len(liste[k][3])!=0 or ctx.author.id in listeId:
                print("already in the wh")
                print(firstNameBis, liste[defineK(4,str(ctx.author.id))][3])
                botMessage=await ctx.reply(f"Vous êtes **déjà enregistré** dans la whitelist sous le pseudonyme *{liste[defineK(4,str(ctx.author.id))][3]}*. \nIl est interdit d'utiliser le même compte Discord pour plusieurs comptes Minecraft.\nS'il s'agit d'une erreur, merci de contacter un membre du staff en créant un ticket.\n\n||Lorsque vous avez terminé, cliquez sur \U00002705||")
                await botMessage.add_reaction('\U00002705')
                if ctx.channel.id==1218672398262468720:
                    channel=bot.get_channel(1218677627313717371)
                    await channel.send(f"**{firstName} {lastName}** a tenté de se connecter pour la seconde fois avec le pseudonyme *{liste[defineK(4,str(ctx.author.id))][3]}*.")
                print("------>>>",liste[defineK(4,str(ctx.author.id))][1],liste[defineK(4,str(ctx.author.id))][0],"was already in the whitelist as",liste[defineK(4,str(ctx.author.id))][3])
                await ctx.message.delete()
                covered=True
                return

            elif k==len(liste)-2 and not covered:
                    print("not accepted")
                    print(k)
                    print(covered)
                    botMessage=await ctx.reply("Vous n'apparaissez pas dans les registres des **premières du Lycée Descartes** dont nous disposons, veuillez réessayer en respectant l'ordre `Nom` `Prénom` `Classe` et en les séparant d'**un seul espace** à chaque fois.\nSi le problème persiste, merci de contacter notre équipe en créant un *ticket*.\n\n||Lorsque vous avez terminé, cliquez sur \U00002705||")
                    await botMessage.add_reaction('\U00002705')
                    if ctx.channel.id==1218672398262468720:
                        channel=bot.get_channel(1218677627313717371)
                        await channel.send(f"**{firstName} {lastName}** a tenté de s'ajouter a la whitelist. Il/Elle ne figure pas dans les listes de premières.")
                    print("------>>>",firstName,lastName,"not found on the list")
                    await ctx.message.delete()
                    return

#####################################################################################################################################
@bot.event
async def on_raw_reaction_add(payload):
    if payload.user_id!=1151281965115375656:
        if payload.emoji.name=='✅' and payload.guild_id!=1211423906867707914 and payload.guild_id!=804010977544110100:
            member=bot.get_user(payload.user_id)
            channel = await member.create_dm()
            ip_add=open('/yourpath/ip_add.txt','w')         # Your path here
            userIp=open('/yourpath/userIp.txt','r')         # Your path here
            content=userIp.readlines()
            ip_add.write(content[0])
            ip_add.write(content[1])
            print(f"------>>> New IP allowed to connect to connect to the account {liste[defineK(4,payload.user_id)][3]}")
            userIp.close()
            ip_add.close()
            os.remove("/yourpath/userIp.txt")         # Your path here
            await channel.send(":white_check_mark: Cette IP a bien été **validée**.")

        elif payload.emoji.name=='❌' and payload.guild_id!=1211423906867707914 and payload.guild_id!=804010977544110100:
            member=bot.get_user(payload.user_id)
            channel = await member.create_dm()
            ip_block=open('/yourpath/ip_block.txt','w')         # Your path here
            userIp = open('/yourpath/userIp.txt', 'r')         # Your path here
            content = userIp.readlines()
            ip_block.write(content[0])
            ip_block.write(content[1])
            print(f"------>>> New IP blocked from the account {liste[defineK(4,payload.user_id)][3]}")
            ip_block.close()
            userIp.close()
            os.remove("/yourpath/userIp.txt")         # Your path here
            await channel.send(":x: Cette IP a bien été **bloquée**.")

        elif payload.emoji.name=='✅' and (payload.channel_id==1218672398262468720 or payload.channel_id==804024422146113616):
            channel=bot.get_channel(payload.channel_id)
            botMessage=await channel.fetch_message(payload.message_id)
            await botMessage.delete()

        else:
            return
        return

#####################################################################################################################################
@bot.command(name='get_csv')
async def getCSV(ctx):
    file=discord.File('./students-list.csv')
    await ctx.send(file=file, content='Voici le dossier CSV daté du {}'.format(strftime("%d/%m/%Y à %H:%M UTC%z")))
    await ctx.message.delete()

#####################################################################################################################################
@bot.command(name='aide')
async def help(ctx):
    botMessage=await ctx.reply("Pour vous faire ajouter à la **liste blanche du serveur Minecraft**, il vous suffit de faire la commande `!wh Nom Prénom Classe Pseudo-en-jeu` en remplaçant les informations par les vôtres.\n- Si vous n'êtes pas arrivé en début d'année ou que vous avez changé de classe, **merci d'ouvrir un <#1214682481740222514>**.\n- Si vous avez un nom/prénom composé, remplacez les espaces par des __tirets__ *\"-\"*.\n- Vous devez mettre vos noms et prénoms __complets__.\n\n*Lorsque vous avez terminé, cliquez sur \U00002705*",ephemeral=True)
    await botMessage.add_reaction('\U00002705')
    await ctx.message.delete()
   
#####################################################################################################################################
bot.run("")         # Your token here
