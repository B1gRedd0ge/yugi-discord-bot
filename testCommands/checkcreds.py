import discord
import dataset
import asyncio
import os
from os import listdir
from os.path import isfile, join
from discord.ext.commands import Bot
from discord.ext import commands

BOT_PREFIX = "$"
client = Bot(command_prefix=BOT_PREFIX)
db = dataset.connect('sqlite:////home/doge/yugi-bot/yugibot.db')
client.remove_command('help')


@client.event
async def on_ready():
    import discord


@client.event
async def on_ready():
    print("Logged in as " + client.user.name)


@client.event
async def on_message(context):
    if client.user.id == context.author.id:
        return
    person = context.author.id
    table = db['economy']
    table.insert(dict(userID=str(person)))
    cur = db.query('SELECT points FROM economy WHERE userID=:person;', {'person': person})
    for row in cur:
        increase = (row['points']) + 1
        print(increase)
        person = context.author.id
        data = dict(points=int(increase), userID=str(person))
        table.update(data, ['economy'])

    await client.process_commands(context)


@client.command(name='daily',
                brief='- Adds ¥100 and one mystery card to your inventory once every 24 hours.',
                pass_context=True)
@commands.cooldown(1, 86400, commands.BucketType.user)
async def on_daily(context):
    user = context.author.id
    table = db['economy']
    table.insert(dict(userID=str(user)))
    cur = db.query('SELECT points FROM economy WHERE userID=:user;', {'user': user})
    for row in cur:
        increase = (row['points']) + 100
        print(increase)
        data = dict(points=int(increase), userID=str(user))
        table.update(data, ['economy'])
    data = db.query('SELECT * FROM cardData WHERE cardID IN (SELECT cardID FROM cardData ORDER BY RANDOM() LIMIT 1)')
    for row in data:
        card = (row['cardID'])
        name = db.query('SELECT cardName FROM cardData WHERE cardID=:card;', {'card': card})      
        em = discord.Embed(title='Daily', description=context.author.mention + ' you recieved ¥100 and one free card!', colour=0xDEADBF)
        em.set_image(url="https://ygoprodeck.com/pics/" + card + ".jpg")
        await context.channel.send(embed=em)
        table = db['collections']
        namec = db.query('SELECT cardName FROM cardData WHERE cardID=:card;', {'card': card})
        for x in namec:
            namey = (x['cardName'])
        table.insert(dict(userID=str(context.message.author.id), cardID=str(card), cardName= namey))



@client.command(name='buycard',
                description="gives random card to user and stores it under their user ID in database.",
                brief="- Adds mystery card to your inventory.",
                aliases=['cardplz', '8ball', 'manIcouldUseAcard'],
                pass_context=True)
async def buy_card(context):
    user = context.author.id
    purchase = db.query('SELECT points FROM economy WHERE userID=:user;', {'user': user})
    for row in purchase:
        price = (row['points'])
        if int(price) > 50:
            data = db.query('SELECT * FROM cardData WHERE cardID IN (SELECT cardID FROM cardData ORDER BY RANDOM() LIMIT 1)')
            for row in data:
                card = (row['cardID'])
                name = db.query('SELECT cardName FROM cardData WHERE cardID=:card;', {'card': card})      
                em = discord.Embed(description= context.message.author.mention + ' your new card is...', colour=0xDEADBF)
                em.set_image(url="https://ygoprodeck.com/pics/" + card + ".jpg")
                await context.channel.send(embed=em)
                newbal = int(price) - 50
                print(newbal)
                table = db['economy']
                data = dict(points=int(newbal), userID=str(user))
                table.update(data, ['economy'])
                table = ['collections']
                namec = db.query('SELECT cardName FROM cardData WHERE cardID=:card;', {'card': card})
                for x in namec:
                    namey = (x['cardName'])
                    table = db['collections']
                    table.insert(dict(userID=str(context.message.author.id), cardID=str(card), cardName= namey))
        if int(price) < 50:
            en = discord.Embed(title='Insufficient Funds', colour=0xDEADBF)
            await context.channel.send(embed=en)
        # table = db['economy']
        # table.insert(dict(userID=str(user)))
        # table = db['users']
        # table.insert(dict(userID=str(context.message.author.id), username=str(context.message.author)))
        # table = db['collections']
        

@client.command(name='mycards',
                brief='- Lists all the cards in your inventory',
                pass_context=True)
async def get_cards(context):
    user = context.message.author.id
    usercard = db.query('SELECT cardName From collections WHERE userID=:user;', {'user': user})
    for x in usercard:
        with open('./tempNames.txt', 'a') as cwrite:
            cwrite.write(x['cardName'] + '\n')
    with open('./tempNames.txt', 'r') as csv:
        em = discord.Embed(title='Inventory for ', description=context.message.author.mention + '\n' + csv.read(), colour=0xDEADBF)
        await context.channel.send(embed=em)
        open('./tempNames.txt', 'w').close


@client.command(name='deckpics',
                description='- Shows the images for all cards currently in your inventory, use sparingly as it can be a lot of images',
                brief='- Shows the images for all the cards in your inventory',
                pass_context=True)
async def show_cards(context):
    user = context.message.author.id
    usercard = db.query('SELECT cardID From collections WHERE userID=:user;', {'user': user})
    for y in usercard:
        inven = (y['cardID'])
        ef = discord.Embed()
        ef.set_image(url="https://ygoprodeck.com/pics/" + inven + '.jpg')
        await context.channel.send(embed=ef)


@client.command(name='viewcard',
                description='- View any card image by typing $viewcard followed by the card name you with to view',
                brief='- View the image for any card',
                pass_context=True)
async def view_card(context, message):
    msgcard = context.message.content
    cardtosend = msgcard.replace('$viewcard','')
    with open('./tempreq.txt', 'a') as fw:
        fw.write(cardtosend.lstrip())
        fw.close()
    with open('./tempreq.txt', 'r') as fr:
        sendcard = db.query('SELECT cardID FROM cardData WHERE cardName=:cardtosend;', {'cardtosend': fr.read()})
        for row in sendcard:
            x = (row['cardID'])
            with open('./tempreq2.txt', 'a') as ff:
                ff.write(row['cardID'])
                ff.close()
    
        with open('./tempreq2.txt', 'r') as fq:
            em = discord.Embed()
            em.set_image(url="https://ygoprodeck.com/pics/" + fq.read() + '.jpg')
            await context.channel.send(embed=em)
            open('./tempreq2.txt', 'w').close
            open('./tempreq.txt', 'w').close


@client.command(name='credits',
                brief='- Shows current balance',
                pass_context=True)
async def show_credits(context):
    user = context.author.id
    usercred = db.query('SELECT points FROM economy WHERE userID=:user;', {'user':user})
    for row in usercred:
        balance = (row['points'])
        em = discord.Embed(title='Current Balance: ' + '¥' + str(balance),  colour=0xDEADBF)
        await context.channel.send(embed=em)


@client.command(name='help')
async def help(context):
    em = discord.Embed(title='Commands:', description='$mycards --- Displays a list of all cards in your inventory' + '\n' + '\n' + '$daily --- Adds ¥100 and one mystery card to your inventory once per day.' + '\n' + '\n' + '$buycard --- Purchase a mystery card for ¥50' + '\n' + '\n' + '$viewcard [cardnamehere] --- Displays card image, case sensitive.' + '\n' + '\n' '$credits --- Displays your current balance.', colour=0xDEADBF)
    await context.channel.send(embed=em)


client.run('NTU0MTMwOTU0NTYyNTY4MTkz.D28kow.7Lg-wLsbLl45MhT3nAoIhf_7ffg')

