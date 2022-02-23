import discord
from discord.abc import User
from discord.ext import commands, tasks
import datetime
from discord.ext.commands.converter import Greedy
import requests
import json
import os
import random as rd
from typing import Optional

if os.path.exists(os.getcwd() + "\config.json"):
    # print("Current working directory:", os.getcwd()) 
    with open("./config.json") as f:
        configData = json.load(f)
else:
    # print("Current working directory:", os.getcwd()) 
    configTemplate = {"Token": "", "Prefix": "!"}
    with open(os.getcwd() + "/config.json", "w+") as f:
        json.dump(configTemplate, f) 

token = configData["Token"]
prefix = configData["Prefix"]

bot = commands.Bot(command_prefix=prefix, intents = discord.Intents.all())

@bot.event
async def on_ready():
    print("ready")
    current_time.start()
    
@bot.event
async def on_message(message):
    s = str(message.content)
    if message.author == bot.user:
        return
    if "Eu amo o Frodo".upper() in s.upper():
        await message.channel.send(f"Eu também amo o Frodo, {message.author.name}.")
    if "Oi".upper() == s.upper():
        await message.channel.send(f"Oi, {message.author.name}.")
    await bot.process_commands(message)

@bot.event
async def on_raw_reaction_add(payload):
    msg_id = payload.message_id
    if msg_id == 911901505546756197:
        guild = bot.get_guild(payload.guild_id)

        if payload.emoji.name == 'sage':
            role = discord.utils.get(guild.roles, name='valorant')  
        else:
            role = discord.utils.get(guild.roles, name=payload.emoji.name)

    if role is not None:
        member = guild.get_member(payload.user_id)
        if member is not None:
            await member.add_roles(role)
            print("role added")
        else:
            print("user not found")
    else:
        print("role not found")

@bot.event
async def on_raw_reaction_remove(payload):
    msg_id = payload.message_id
    if msg_id == 911901505546756197:
        guild = bot.get_guild(payload.guild_id)

        if payload.emoji.name == 'sage':
            role = discord.utils.get(guild.roles, name='valorant')  
        else:
            role = discord.utils.get(guild.roles, name=payload.emoji.name)

    if role is not None:
        member = guild.get_member(payload.user_id)
        if member is not None:
            await member.remove_roles(role)
            print("role removed")
        else:
            print("user not found")
    else:
        print("role not found")
          
@bot.command(name="oi")
async def greet_user(ctx):
    resp = "Oi, " + ctx.author.name + "."
    await ctx.send(resp)
    
@bot.command()
async def price(ctx, coin, base):
    try:
        resp = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={coin.upper()}{base.upper()}")
        price = resp.json().get("price")
        
        if price:
            await ctx.send(f"{coin.upper()}: {float(price):,.2f} {base.upper()}" )
        else:
            await ctx.send("invalido")
    except Exception as e:
        await ctx.send(e)

@bot.command(name="randbg")
async def generate_rand_bg(ctx): 

    img_id = rd.randint(1,1000)
    w=1920
    h=1080
    url = "http://picsum.photos/id/"+str(img_id)+"/"+str(w)+"/"+str(h)+"/"

    embed = discord.Embed(
        title = "Background",
        description = "Lorem Ipsum",
        color = 0x9D5AB8
    )
    embed.set_author(name=bot.user.name, url="https://github.com/qedrohenrique/Bot-discord", icon_url=bot.user.avatar_url)
    embed.set_footer(text="Aproveite " + ctx.author.name)
    embed.add_field(name="Width", value=str(w))
    embed.add_field(name="Height",value=str(h))
    embed.add_field(name="Link", value=url, inline=False)
    embed.set_image(url = url)
    await ctx.send(embed=embed)

@bot.command(name="randimg")
async def generate_rand_img(ctx, w=0, h=0): 
    if w == 0 and h == 0:
        w = rd.randint(200,3840)
        h = rd.randint(200, 2160)
        
    img_id = rd.randint(1,1060)

    url = "http://picsum.photos/id/"+str(img_id)+"/"+str(w)+"/"+str(h)+"/"

    embed = discord.Embed(
        title = "Background",
        description = "Lorem Ipsum",
        color = 0x9D5AB8
    )
    embed.set_author(name=bot.user.name, url="https://github.com/qedrohenrique/Bot-discord", icon_url=bot.user.avatar_url)
    embed.set_footer(text="Aproveite " + ctx.author.name)
    embed.add_field(name="Width", value=str(w))
    embed.add_field(name="Height",value=str(h))
    embed.add_field(name="Link", value=url, inline=False)
    embed.set_image(url = url)
    await ctx.send(embed=embed)

@bot.command(name="cc")
async def clear_chat(ctx, targets: Greedy[User], limit= 1):
    def _check(message):
        return not len(targets) or message.author in targets
    if 0 < limit <= 100:
        with ctx.channel.typing():
            await ctx.message.delete()
            deleted = await ctx.channel.purge(limit=limit, check=_check)
            await ctx.send(f"deletei {len(deleted):,} mensagens.", delete_after=15)
    else:
        await ctx.send("numero de mensagens invalido")

@bot.command(name="clist")
async def command_list(ctx):
    embed = discord.Embed(
        title = "Lista de comandos",
        description = "**!clist** ➜ lista de comandos\n"
                      "**!oi** ➜ olá\n"
                       "**!cc [usuários] [quant. msgs]** ➜ limpa o chat\n"
                       "**!randimg [larg] [altura]** ➜ imagem aleatória\n"
                       "**!randbg** ➜ plano de fundo aleatório\n"
                       "**!price [moeda] [moeda]** ➜ cotação crypto\n",
        color = 0x9D5AB8
    )
    await ctx.send(embed=embed)

@bot.command(name="pfp")
async def embed_profile_picture(ctx, target: Optional[User]):
    if target is None:
        target = ctx.message.author
    mention = int(target.id)
    embed = discord.Embed(
        title = ctx.message.author,
        description = f"**baixe** [**aqui**]({target.avatar_url}).",
        color = 0x9D5AB8
    )
    embed.set_image(url = target.avatar_url)
    await ctx.send(f"<@{mention}>",embed=embed)
    
@tasks.loop(hours = 1)
async def current_time():
    now = datetime.datetime.now().strftime("%d-%m-%Y, %H:%M:%S")
    await bot.get_channel(911532765286117416).send("Data atual: " + now)
    
bot.run(token)