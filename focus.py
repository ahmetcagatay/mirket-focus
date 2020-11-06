#Discordda Belirli bir kanala girildiğinde belirli rolü veren Bot

"""
Örneğin: Resepsiyon kanalına giren birisi için Kayıtsız rolünü verebilirsiniz.
Örneğin: Çalışıyorum odasına giren birisi için Focus Mode rolünü verebilirsiniz.
"""

#Bu botu kanalınıza yükleyerek test edebilirsiniz.

"""Yapmanız gerekenler"""
#1-Botun komutlarına sadece "Kurucu" rolüne sahip olanlar erişebilir. 
"""(İsterseniz kendi sunucunuzda "Kurucu" rolü oluşturmak yerine aşağıdaki adminRoleName'i değiştirerek kendi sunucunuzun yöneticisinin rol adını koyabilirsiniz)"""
adminRoleName="Kurucu"
#2-setFocus fonksiyonu ile  hangi kanala girildiğinde ve hangi rolü vermek istediğinizi belirtmelisiniz.
"""
.setFocus [Kanal Id] [Rol Adı]
.setFocus [78949498798498] [Kayıtsız] (ÖRNEK)
"""

#Ve başlıyoruz...
import discord
import os
import random
import asyncio
import aiohttp
import time as t
import datetime
from discord import Game
from discord.ext.commands import Bot
from discord.ext import commands
from discord.ext.commands import errors

#Buraya kendi tokeninizi girmelisiniz
token = os.environ.get('BOT-TOKEN')

#Botun prefix'i
bot = commands.Bot(command_prefix='.')
#Kanal ve Rol Adı için başlangıç koşulları
channel_id= 0 
role_name = ""

#Bot çalıştığında
@bot.event
async def on_ready():
    now = datetime.datetime.now()
    print(f'{bot.user.name} çalışıyor...' + "-" + str(now.hour) + ":" + str(now.minute) + ":" + str(now.second))
    #await bot.change_presence(activity=discord.Game(name=str(now.hour) + ":" + str(now.minute) + ":" + str(now.second)))

#setFocus komudu çalıştırıldığında
@bot.command()
@commands.has_role(adminRoleName)
async def setFocus(ctx, *args):
    global channel_id
    global role_name
    OutputMessage = "Focus için\n"
    if len(args) <= 0:
        OutputMessage = "Argüman girmediniz"
    elif len(args) >= 3:
        OutputMessage = "Fazla Argüman Girdiniz"
    elif len(args) >= 1:
        channel_id = int(args[0])
        OutputMessage += "Kanal Adı: " + args[0]
        if len(args) >= 2:
            role_name = args[1]
            OutputMessage += "\nRol İsmi: " + args[1]
    await ctx.send(OutputMessage + " \n**...olarak düzenlendi**")

#commands komutu çalıştırıldığında
@bot.command()
@commands.has_role(adminRoleName)
async def commands(ctx, *args):
    await ctx.send(".setFocus [ChannelId] [RoleName]")

#Serverda herhangi birisi herhangi bir kanala girdiğinde
@bot.event
async def on_voice_state_update(member, before, after):
    print(channel_id)
    if  role_name == "" or channel_id == 0:
        print("Henüz bir rol veya kanal atanmadı")
    else:
        #şimdilik id ile çalıştırdım isim ile çalışıyor
        #role = discord.utils.get(member.guild.roles, id=role_name)
        role  = discord.utils.get(member.guild.roles, name=role_name)
        print("log:0")
        if before.channel is None and after.channel is not None:
            print("log:1")
            if after.channel.id == channel_id:
                print("log:11")
                await member.add_roles(role)
            else:
                print("log:12")
                await member.remove_roles(role)

        elif before.channel is not None and after.channel is not None:
            print("log:2")
            if after.channel.id == channel_id:
                print("log:21")
                await member.add_roles(role)
            else:
                print("log:22")
                await member.remove_roles(role)

        elif before.channel is not None and after.channel is None:
            print("log:3")
            if before.channel.id == channel_id:
                print("log:31")
                await member.remove_roles(role)
            else:
                print("log:32")
                pass

bot.run(token)

#Geliştirmelerinizi bekliyorum :)
#Yapılacaklar
"""
#+# Kanallar düzenlenebilir olacak
#-# Tek bir kanal için değil oluşturulan kanal listesi için sorgulama yapacak
#-# Tek bir rol için değil belirli kanalları belirli roller için sorgulama yapacak
"""
