import datetime
from discord.ext import commands
import discord
import os
import aiml

description = '''Lithia an assistant built apon python3.6+ to help with a variety of things.
Lithia's Github = https://github.com/nathanlol5/Lithia-AIML
'''
# this specifies what extensions to load when the bot starts up

with open ("./configs/bot.ini", "r") as configfile:
    config=configfile.read().splitlines() 

operator = config[1]
devs = config[2]
prefix = config[3]
PCmention = config[4]
Mobilemention = config[5]
auditchan = config[6]
startup_extensions = []

directory = os.fsencode('./cogs')
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".cog") or filename.endswith(".py"): 
        print(os.path.join(str(filename)))
        startup_extensions.append(str('cogs.'+str(filename)).replace('.py',''))
        continue
    else:
        continue

bot = commands.Bot(command_prefix=commands.when_mentioned_or(prefix), description=description)
bot.prefix = prefix
bot.operator = "175182469656477696"

@bot.event
async def on_ready():
    data[0] = None
    print('Logged in as')
    bot.brain = aiml.Kernel()
    bot.brain.learn('./aiml/Startup.xml')
    bot.brain.respond("LOAD STANDARD LIBRARIES")
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(game=discord.Game(name=str(prefix) + "Commands", type=2))

@bot.command(pass_context=True)
async def load(ctx, extension_name : str):
    """Loads an extension."""
    if ctx.message.author.id == bot.operator:
        try:
            bot.load_extension(extension_name)
        except (AttributeError, ImportError) as e:
            await bot.say("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
            return
        await bot.say("```SubUnit\nLoaded <{}> : ".format(extension_name)+str(datetime.datetime.now())+"z```")

@bot.command(pass_context=True)
async def unload(ctx, extension_name : str):
    """Unloads an extension."""
    if ctx.message.author.id == bot.operator:
        bot.unload_extension(extension_name)
        await bot.say("```SubUnit\nUnloaded <{}> : ".format(extension_name)+str(datetime.datetime.now())+"z```")

if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))
            
    with open ("./configs/bot.token", "r") as myfile:
        data=myfile.readlines()
    bot.run(data[0])