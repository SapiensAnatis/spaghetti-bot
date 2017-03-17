import discord
from discord.ext import commands
import modules.utils as utils
import os

class TierList:
    # Backing functions

    def load_lists(self, folder):
        for tierlist in os.listdir(folder):
            with open(utils.local_filepath("modules\\tierlists\\"+tierlist), "r") as list_file:
                list_itself = list_file.read().split(",")
                self.lists[tierlist[:-4]] = list_itself
                print(f"[Tierlist.py] Loading: added key {tierlist[:-4]} to dict")

    def save_lists(self):
        for tierlist, list_array in self.lists.items():
            with open(utils.local_filepath("modules\\tierlists\\"+tierlist + ".csv"), "w+") as list_file:
                for entry in list_array:
                    list_file.write(entry + ",")
    
    # init needs the above

    def __init__(self, bot):
        # Initialize:
        self.bot = bot
        self.lists = {}
        self.emoji = ["0⃣", "1⃣", "2⃣", "3⃣", "4⃣", "5⃣", "6⃣", "7⃣", "8⃣", "9⃣"]
        # Make folders:
        list_folder = utils.local_filepath("modules\\tierlists")
        self.load_lists(list_folder)
    
    # Utils functions

    def number_to_emoji(self, num):
        # I'm sorry
        output = ""
        if num < 10: output += "0⃣"
        num_string = str(num)
        digits = list(num_string)

       
        for digit in digits:
            output += self.emoji[int(digit)]
        
        return output
    
    # Functions that will be mapped to a command
    
    def new_list(self, name):
        with open ("modules\\tierlists\\" + name + ".csv", "w+"): # create empty file
            pass
        
        self.lists[name] = []
        self.save_lists()
        return True
        
    
    def add_entry(self, list_name, ranking, entry):
        list_array = self.lists[list_name]
        try:
            list_array[ranking-1] = entry
        except IndexError:
            list_array.append(entry)
        self.save_lists()
    
    def del_entry(self, list_name, ranking):
        list_array = self.lists[list_name]
        list_array.pop(ranking-1)
        self.save_lists()
    
    def read_list(self, list_name):
        response = f"THE MOST AGREED UPON TIER LIST OF {list_name}:\n"
        list_array = self.lists[list_name]
        print("Showing list:", list_array)
        for ranking, entry in enumerate(list_array):
            if entry == "": continue
            response += (f"{self.number_to_emoji(ranking+1)} {entry}\n")
        
        return response

    def delete_list(self, list_name):
        del self.lists[list_name]
        os.remove(utils.local_filepath("modules\\tierlists\\"+list_name + ".csv"))


    # Frontend command mapping
    
    @commands.command(pass_context = True)
    async def listnew(self, ctx, *, list_name: str):
        self.new_list(list_name)
        await self.bot.add_reaction(ctx.message, "👌")
    
    @commands.command(pass_context = True)
    async def listadd(self, ctx, list_name: str, ranking: int, *, entry: str):
        self.add_entry(list_name, ranking, entry)
        await self.bot.add_reaction(ctx.message, "👌")
    
    @commands.command(pass_context = True)
    async def listdelitem(self, ctx, list_name: str, ranking: int):
        self.del_entry(list_name, ranking)
        await self.bot.add_reaction(ctx.message, "👌")
    
    @commands.command(pass_context = True)
    async def listshow(self, ctx, *, list_name: str):
        response = self.read_list(list_name)
        await self.bot.send_message(ctx.message.channel, response)
    
    @commands.command(pass_context = True)
    async def listdel(self, ctx, list_name: str):
        self.delete_list(list_name)
        await self.bot.add_reaction(ctx.message, "👌")



def setup(parent):
    instance = TierList(parent)
    parent.add_cog(instance)