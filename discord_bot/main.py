import discord
from discord.ext import commands
import json
import csv 
from keep_alive import keep_alive

client = commands.Bot(command_prefix='f')

@client.command(name='register')
async def register(context, faction):
  regEmbed = discord.Embed(title="Registration Info", description="Name: " + str(context.message.author.name) + " ID: " + str(context.message.author.id) + " Faction: " + faction)

  data = [str(context.message.author.name), str(context.message.author.id), faction]
  with open('register.csv', 'a+', encoding='UTF8') as f:
      writer = csv.writer(f)
      writer.writerow(data)

  await context.message.channel.send(embed=regEmbed)
  try:
    if faction == "swarm":
      role = discord.utils.get(context.guild.roles, name="Swarm Warrior")
      user=context.message.author
      await user.add_roles(role)

    if faction == "shadowfen":
      role = discord.utils.get(context.guild.roles, name="Shadowfen Warrior")
      user=context.message.author
      await user.add_roles(role)

    if faction == "ironclad":
      role = discord.utils.get(context.guild.roles, name="Winter Pact Warrior")
      user=context.message.author
      await user.add_roles(role)

    if faction == "winter":
      role = discord.utils.get(context.guild.roles, name="Ironclad Warrior")
      user=context.message.author
      await user.add_roles(role)
  except:
    pass

@client.command(name="config")
async def config(context):
    #variables

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
          filename = "scores.csv"
          # opening the file with w+ mode truncates the file
          floop = open(filename, "w+")
          floop.close()
          data = ["name", "id", "faction", "score"]
          with open('scores.csv', 'a+', encoding='UTF8') as filee:
              writer = csv.writer(filee)
              writer.writerow(data)
          with open('register.csv') as f:  
            reader = csv.reader(f, delimiter=',', quotechar='"')
            for row in reader:
              if row:
                data = [row[0], row[1], row[2], 0]
                with open('scores.csv', 'a+', encoding='UTF8') as filee:
                    writer = csv.writer(filee)
                    writer.writerow(data)
            sf_count = 1
            se_count = 1
            ic_count = 1
            wp_count = 1
            with open("scores.csv", 'r') as csvfile:
              datareader = csv.reader(csvfile)
              for row in datareader:
                print(str(row[2]))
                if str(row[2]) == "swarm":
                  se_count = se_count+1
                elif str(row[2]) == "ironclad":
                  ic_count = ic_count+1
                elif str(row[2]) == "winter":
                  wp_count = wp_count+1
                elif str(row[2]) == "shadowfen":
                  sf_count = sf_count+1
            #maths
            math_count = (sf_count*(ic_count+se_count+wp_count))+(ic_count*(sf_count+se_count+wp_count))+(se_count*(ic_count+sf_count+wp_count))+(wp_count*(ic_count+sf_count+se_count))
            sf_points = round(math_count/(sf_count*(ic_count+se_count+wp_count)), 1)
            ic_points = round(math_count/(ic_count*(sf_count+se_count+wp_count)), 1)
            se_points = round(math_count/(se_count*(ic_count+sf_count+wp_count)), 1)
            wp_points = round(math_count/(wp_count*(ic_count+sf_count+se_count)), 1)
            configEmbed.add_field(name="Player Counts: SF = " + str(sf_count-1) + " SE = " + str(se_count-1) + " IC = " + str(ic_count-1) + " WP = " + str(wp_count-1) + " Point Amounts(Per Faction)", value="SF: " + str(sf_points) + ", IC: " + str(ic_points) + ", SE: " + str(se_points) + ", WP: " + str(wp_points))
            await context.message.channel.send(embed=configEmbed)
            #update points to json 
            with open("points.json", "r") as jsonFile:
              data = json.load(jsonFile)

            data["Swarm"] = se_points
            data["Shadowfen"] = sf_points
            data["Winterpact"] = wp_points
            data["Ironclad"] = ic_points

            with open("points.json", "w") as jsonFile:
              json.dump(data, jsonFile)

            
        else:
            configEmbed.add_field(name="Status:", value="DENIED", inline=False)
            await context.message.channel.send(embed=configEmbed)

keep_alive()



#bot token
client.run("token")
