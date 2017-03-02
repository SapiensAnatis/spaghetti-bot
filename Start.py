
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

print("Performing pre-login tasks...", end="")
extensions = [filename[:-3]
              for filename in listdir(utils.local_filepath("modules"))
              if filename.endswith(".py") and filename != "utils.py"] # Generate a list of modules to load
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
<<<<<<< HEAD
    for extension in extensions:
        print(f"  Loading {extension}...")
        bot.load_extension("modules." + extension)
        print(f"  Loading of module {extension} completed.")
=======
    for extension_file in listdir(utils.local_filepath("modules")):
        if extension_file.endswith(".py") and extension_file != "utils.py":
            print("  Loading {0}...".format(extension_file), end="")
            bot.load_extension("modules." + extension_file[:-3])  # try and load module from filename (sans extension)
            print("  Loading of module {0} completed.".format(extension_file))
>>>>>>> f5f7e4ad017a73025e676524e34cd842c565df9d
    print("Extension loading complete.\n")

@bot.command(aliases=['reload', 'restart'], pass_context=True)
async def _reload(ctx, *, extension_arg: str = None):
    if ctx.message.author.id != "259763709541351426":
        await bot.add_reaction(ctx.message, "😒")
        return



    if extension_arg is None: # generic call
        print("Received call to reload all modules:")
        for extension in extensions:
            print(f"  Reloading {extension}...")
            bot.unload_extension("modules."+extension)
            bot.load_extension("modules."+extension)
            print(f"{extension} successfully reloaded.")
        print("All extensions successfully reloaded.")
        await bot.add_reaction(ctx.message, "👌")
    else:
        extension_arg = extension_arg.title() # All modules are in titlecase and the user may not provide the name like that
        if not (extension_arg in extensions):
            await bot.send_message(":unamused:")
        else:
            print("Received call to reload module {extension_arg}.")
            print(f"Reloading {extension_arg}...")
            bot.unload_extension("modules."+extension_arg)
            bot.load_extension("modules."+extension_arg)
            print(f"Successfully reloaded extension {extension_arg}.")
            await bot.add_reaction(ctx.message, "👌")


if __name__ == "__main__": # if we're ready to go
    with open (utils.local_filepath("key.txt"), "r") as key_file:
        key = key_file.read()
    bot.run(key)
