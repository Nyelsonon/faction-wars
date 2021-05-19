import discord
from discord.ext import commands
import json
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import asyncio

client = commands.Bot(command_prefix='f')
scope =["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(r"C:\Users\nealk\OneDrive\Desktop\python_general\faction_wars\creds.json", scope)
client2 = gspread.authorize(creds)
sheet = client2.open("factionwars").sheet1
tp_count = 1
sf_count = 1
ic_count = 1
wp_count = 1
se_count = 1
timer = False

@client.command(name="hello")
async def hello(context):
    await context.message.channel.send('Hello!')

@client.command(name="config")
async def config(context):
    #variables
    global tp_count
    global sf_count
    global se_count
    global ic_count
    global wp_count

    configEmbed=discord.Embed(title=':gear: Configure a New Week! :gear:', description="Type CONFIRM WEEK to confirm your intentions to start a new week and DENY WEEK to cancel.(Please answer in the next 30 seconds!)")
    await context.message.channel.send(embed=configEmbed)
    try:
        message = await client.wait_for("message", check=lambda m: m.author == context.author and m.channel == context.channel, timeout=30)

    except:
        await context.message.channel.send('Question not answered in time, process cancelled...')
    
    else:
        #settings
        if message.content.lower() == "confirm week":
            configEmbed.add_field(name="Status:", value="CONFIRMED", inline=False)
            await context.message.channel.send(embed=configEmbed)
            askEmbed = discord.Embed(title="Setup", description="How many players are participating in this week?")
            await context.message.channel.send(embed=askEmbed)
            Message = await client.wait_for('message')
            tp_count = int(Message.content)
            configEmbed.add_field(name='Total Players', value = str(tp_count))
            await context.message.channel.send(embed=configEmbed)
            askEmbed = discord.Embed(title="Setup", description="How many Shadowfen players are participating in this week?")
            await context.message.channel.send(embed=askEmbed)
            Message = await client.wait_for('message')
            sf_count = int(Message.content)
            configEmbed.add_field(name='Shadowfen Players', value = str(sf_count))
            await context.message.channel.send(embed=configEmbed)
            askEmbed = discord.Embed(title="Setup", description="How many Ironclad players are participating in this week?")
            await context.message.channel.send(embed=askEmbed)
            Message = await client.wait_for('message')
            ic_count = int(Message.content)
            configEmbed.add_field(name='Ironclad Players', value = str(ic_count))
            await context.message.channel.send(embed=configEmbed)
            askEmbed = discord.Embed(title="Setup", description="How many Swarm players are participating in this week?")
            await context.message.channel.send(embed=askEmbed)
            Message = await client.wait_for('message')
            se_count = int(Message.content)
            configEmbed.add_field(name='Swarm Players', value = str(se_count))
            await context.message.channel.send(embed=configEmbed)
            askEmbed = discord.Embed(title="Setup", description="How many Winter players are participating in this week?")
            await context.message.channel.send(embed=askEmbed)
            Message = await client.wait_for('message')
            wp_count = int(Message.content)
            configEmbed.add_field(name='Winter Players', value = str(wp_count))
            await context.message.channel.send(embed=configEmbed)
            #maths
            math_count = (sf_count*(ic_count+se_count+wp_count))+(ic_count*(sf_count+se_count+wp_count))+(se_count*(ic_count+sf_count+wp_count))+(wp_count*(ic_count+sf_count+se_count))
            sf_points = round(math_count/(sf_count*(ic_count+se_count+wp_count)), 1)
            ic_points = round(math_count/(ic_count*(sf_count+se_count+wp_count)), 1)
            se_points = round(math_count/(se_count*(ic_count+sf_count+wp_count)), 1)
            wp_points = round(math_count/(wp_count*(ic_count+sf_count+se_count)), 1)
            configEmbed.add_field(name="Point Amounts(Per Faction)", value="SF: " + str(sf_points) + ", IC: " + str(ic_points) + ", SE: " + str(se_points) + ", WP: " + str(wp_points))
            await context.message.channel.send(embed=configEmbed)
            #update points to sheets
            await asyncio.sleep(60*15)
            try:
                sheet.update_cell(2, 8, tp_count)
                sheet.update_cell(3, 8, 'N/A')
                sheet.update_cell(2, 9, sf_count)
                sheet.update_cell(3, 9, sf_points)
                sheet.update_cell(2, 10, wp_count)
                sheet.update_cell(3, 10, wp_points)
                sheet.update_cell(2, 11, se_count)
                sheet.update_cell(3, 11, se_points)
                sheet.update_cell(2, 12, ic_count)
                sheet.update_cell(3, 12, ic_points)
            except:
                await asyncio.sleep(60*15)
                updated = False
                while updated == False:
                    try:
                        sheet.update_cell(2, 8, tp_count)
                        sheet.update_cell(3, 8, 'N/A')
                        sheet.update_cell(2, 9, sf_count)
                        sheet.update_cell(3, 9, sf_points)
                        sheet.update_cell(2, 10, wp_count)
                        sheet.update_cell(3, 10, wp_points)
                        sheet.update_cell(2, 11, se_count)
                        sheet.update_cell(3, 11, se_points)
                        sheet.update_cell(2, 12, ic_count)
                        sheet.update_cell(3, 12, ic_points)
                        updated = True
                    except:
                        await asyncio.sleep(60*15)
            
        else:
            configEmbed.add_field(name="Status:", value="DENIED", inline=False)
            await context.message.channel.send(embed=configEmbed)


@client.command(name='report')
async def report(context, player1, player2, score, mods="none"):
    brokenScore = list(score)
    player_1_score = int(score[0])
    player_2_score = int(score[2])
    if player_1_score > player_2_score:
        winning_player = player1
        losing_player = player2
    if player_2_score > player_1_score:
        winning_player = player2
        losing_player = player1
    noValues = False
    while noValues == False:
        i=2
        currentCell_NAME = str(sheet.cell(i, 1).value)
        if currentCell_NAME == str(winning_player):
            faction_cell = str(sheet.cell(i, 3).value)
            noValues = True
        elif currentCell_NAME == "None":
            await context.message.channel.send("You are not registered, and therefore cannot enter scores into the scoresheet.")
        else:
            i=i+1
    try:
        if faction_cell == "swarm":
            points = int(sheet.cell(3,11).value)
        if faction_cell == "shadowfen":
            points = int(sheet.cell(3,9).value)
        if faction_cell == "ironclad":
            points = int(sheet.cell(3,12).value)
        if faction_cell == "winter":
            points = int(sheet.cell(3,10).value)
    except:
        await asyncio.sleep(60*10)
        updated=False
        while updated==False:
            try:
                if faction_cell == "swarm":
                    points = int(sheet.cell(3,11).value)
                if faction_cell == "shadowfen":
                    points = int(sheet.cell(3,9).value)
                if faction_cell == "ironclad":
                    points = int(sheet.cell(3,12).value)
                if faction_cell == "winter":
                    points = int(sheet.cell(3,10).value)
                updated = True
            except:
                await asyncio.sleep(60*10)

    reportEmbed=discord.Embed(title='Results: ', description="")
    reportEmbed.add_field(name="Winning Player", value="Gave " + winning_player + " " + str(points) + " points!", inline=False)
    reportEmbed.add_field(name="Losing Player", value="Gave " + losing_player + " 0 points!", inline=False)
    reportEmbed.add_field(name="Score", value="Match Score Recieved as: " + score + ".", inline=False)
    await context.message.channel.send(embed=reportEmbed)
    noValues = False
    while noValues == False:
        await asyncio.sleep(60*15)
        i=2
        currentCell_NAME = str(sheet.cell(i, 1).value)
        if currentCell_NAME == str(winning_player):
            try:
                currentCell_SCORE = int(sheet.cell(i, 2).value)
                sheet.update_cell(i, 2, currentCell_SCORE+points)
            except:
                sheet.update_cell(i, 2, points)
            noValues = True
        elif currentCell_NAME == "None":
            await context.message.channel.send("You are not registered, and therefore cannot enter scores into the scoresheet.")
        else:
            i=i+1

@client.command(name='register')
async def register(context, faction):
    noValues = False
    while noValues == False:
        i = 2
        currentCell_NAME = str(sheet.cell(i, 1).value)
        if currentCell_NAME == "None":
            if faction.lower() == "swarm" or "winter" or "shadowfen" or "ironclad":
                regEmbed = discord.Embed(title="Registration Info:")
                regEmbed.add_field(name="Registered Faction", value=str(faction))
                regEmbed.add_field(name="Registered ID", value=str(context.message.author.id))
                regEmbed.add_field(name="Registered Name", value=str(context.message.author.name))
                regEmbed.add_field(name="Registered Score", value='0')
                await context.message.channel.send(embed=regEmbed)
                await asyncio.sleep(60*15)
                sheet.update_cell(i, 3, str(faction))
                sheet.update_cell(i, 4, str(context.message.author.name))
                sheet.update_cell(i, 1, "<@"+str(context.message.author.id)+">")
                sheet.update_cell(i, 2, 0)
                
                noValues=True

            else:
                await context.message.channel.send("Invalid Faction, please make sure to type the faction identical to these words, 'winter', 'swarm', 'shadowfen', 'ironclad")
        else:
            i=i+1



#bot token
client.run("insert token here")
