
print("Attempting to import discord.ext & other required modules...", end="")

from discord.ext import commands
from os import listdir, path
import modules.utils as utils
#print("Script path", utils.get_script_dir())

try:
    from colorama import Fore
except:
    Fore.GREEN = ""
    Fore.RESET = "" # Define fallbacks

print("done!")
print("Creating bot object...", end="")
bot = commands.Bot(command_prefix="$", description="Wtf")
print("done!")
print("Logging in...", end="")

@bot.event
async def on_ready():
    print("done!")
    print(Fore.GREEN + f"\nLogged into Discord bot account {bot.user.name}#{bot.user.discriminator}.", Fore.RESET)
    print("Loading submodules:")
    for extension_file in listdir(utils.local_filepath("modules")):
        if extension_file.endswith(".py") and extension_file != "utils.py":
            print("  Loading {0}...".format(extension_file), end="")
            bot.load_extension("modules." + extension_file[:-3])  # try and load module from filename (sans extension)
            print("  Loading of module {0} completed.".format(extension_file))
    print("Extension loading complete.\n")

if __name__ == "__main__": # if we're ready to go
    with open (utils.local_filepath("key.txt"), "r") as key_file:
        key = key_file.read()
    bot.run(key)
