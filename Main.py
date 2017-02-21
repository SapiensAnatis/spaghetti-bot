
print("Attempting to import discord.ext & other required modules...", end="")

from discord.ext import commands
from os import listdir

print("done!\nMaking session...", end="")
bot = commands.Bot(command_prefix="$", description="Wtf")
print("done!\nLogging in...", end="")


@bot.event
async def on_ready():
    print("done!\n\nLogged into Discord bot account {0}#{1}.".format(bot.user.name, bot.user.discriminator))
    print("Loading submodules:")
    for extension_file in listdir("modules"):
        if extension_file.endswith(".py"):
            print("\tLoading {0}...".format(extension_file), end="")
            bot.load_extension("modules." + extension_file[:-3])  # try and load module from filename (sans extension)
            print("\tLoading of module {0} completed.".format(extension_file))
    print("Extension loading complete.\n")

if __name__ == "__main__": # if we doing this shit fo real this time
    bot.run(r"MjgzMzM5MTAwOTY1MTc1Mjk3.C4zoSQ.ZFlXQrrnKY1r0YGefEkTHp9b5HM")