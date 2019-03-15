import discord
import dataset
import asyncio
import os
from os import listdir
from os.path import isfile, join
from discord.ext.commands import Bot

path = 'C:/temp/All_images/'
BOT_PREFIX = "$"
client = Bot(command_prefix=BOT_PREFIX)
db = dataset.connect('sqlite:///bot.db')


@client.event
async def on_ready():
    import discord


@client.event
async def on_ready():
    print("Logged in as " + client.user.name)


@client.command(name='card',
                description="gives random card to user and stores it under their user ID in database.",
                brief="gives random card to user.",
                aliases=['cardplz', '8ball', 'manIcouldUseAcard'],
                pass_context=True)
async def give_card(context):
    data = db.query('SELECT * FROM cardData WHERE cardID IN (SELECT cardID FROM cardData ORDER BY RANDOM() LIMIT 1)')
    for row in data:
        card = (row['cardID'])
        name = db.query('SELECT cardName FROM cardData WHERE cardID=:card;', {'card': card})
        with open(path + card + ".png", 'rb') as fp:
            await context.channel.send(context.message.author.mention + 'Your new card is...')
            await context.channel.send(file=discord.File(fp, card + '.png'))
            table = db['users']
            table.insert(dict(userID=str(context.message.author.id), username=str(context.message.author.id)))
            table = db['collections']
            namec = db.query('SELECT cardName FROM cardData WHERE cardID=:card;', {'card': card})
            for x in namec:
                namey = (x['cardName'])
            table.insert(dict(userID=str(context.message.author.id), cardID=str(card), cardName= namey))


@client.command(name='mycards',
                pass_context=True)
async def get_cards(context):
    user = context.message.author.id
    db = dataset.connect('sqlite:///bot.db')
    usercard = db.query('SELECT cardName From collections WHERE userID=:user;', {'user': user})
    for x in usercard:
        with open('C:/temp/tempNames.txt', 'a') as cwrite:
            cwrite.write(x['cardName'] + '\n')
    with open('C:/temp/tempNames.txt', 'r') as csv:
        em = discord.Embed(title='Inventory for ', description=context.message.author.mention + '\n' + csv.read(), colour=0xDEADBF)
        await context.channel.send(embed=em)
        open('C:/temp/tempNames.txt', 'w').close

   # for row in usercard:
   #     inven = (row['cardID'])
    #    ef = discord.Embed()
    #    ef.set_image(url="https://ygoprodeck.com/pics/" + inven + '.jpg')
    #    await context.channel.send(embed=ef)

@client.command(name='showmycards',
                pass_context=True)
async def show_cards(context):
    user = context.message.author.id
    db = dataset.connect('sqlite:///bot.db')
    usercard = db.query('SELECT cardID From collections WHERE userID=:user;', {'user': user})
    for y in usercard:
        inven = (y['cardID'])
        ef = discord.Embed()
        ef.set_image(url="https://ygoprodeck.com/pics/" + inven + '.jpg')
        await context.channel.send(embed=ef)
    

client.run('NTU0NDE2MjQ2NDAyMDU2MjEz.D2iDBQ.-LL9j6xLPDsQLV0fQkF3abks05U')

