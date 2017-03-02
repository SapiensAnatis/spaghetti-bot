print("   [Search.py] Loading necessary modules...", end="")

import discord
from discord.ext import commands
from random import choice
import json
import aiohttp
import time
import modules.utils as utils


def time_since(ref):
	return int(1000*(time.time() - ref))

def tag(start): return f"[Search.py - {time_since(start)}ms]"

loc = "uk"

print("done!")

class Search:
    def __init__(self, bot):
        print("   [Search.py] Initializing", end="")
        self.bot = bot
        self.api_key = ""
        print("...done!")

        print("   [Search.py] Locating API key in SearchAPIKey.txt...",end="")
        with open(utils.local_filepath("SearchAPIKey.txt"), "r") as file_in:
            self.api_key = file_in.readlines()[0]
            print(f"done!")



    def generate_search_url(self, query, num):
        url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={self.api_key}&cx=011947631902407852034:gq02yx0e1mq&gl={loc}&num={num}"
        return url

    @commands.command(pass_context = True)
    async def search(self, ctx, query : str, count : int = 1):
        # Rule out horseplay (input validation)
        start = time.time()
        print(f"{tag(start)} Received command query. Validating...")
        if ctx.message.author == ctx.message.server.me:
            return
        if count > 10 or count < 1: # google-imposed limits
            await self.bot.add_reaction(ctx.message, "😒")
            return

        print(f"{tag(start)} Input validated successfully. User {ctx.message.author.name} has made a search with query {query}. \n{tag(start)} Sending search message:")
        search_message = await self.bot.send_message(ctx.message.channel, "Searching...")

        query_formatted = query.replace(" ", "+")
        search_url = self.generate_search_url(query_formatted, count)
        print(f"{tag(start)} Generated search URL.")
        # Create our embed, to be stylized later...
        search_embed = discord.Embed()
        print(f"{tag(start)} Embed created. Beginning request...")

        async with aiohttp.ClientSession() as client:
            print(f"{tag(start)} aiohttp client defined. Requesting...")
            async with client.get(search_url) as q:
                # Get results from webrequest
                print(f"{tag(start)} Data grabbed from", search_url)
                print(f"{tag(start)} Received request status", q.status)
                if q.status > 300: # probably failed idk lol im not a webmaster
                    await self.bot.edit_message(search_message, new_content=f"Search failed. Web request failed with status {q.status}.")
                    print(await q.text())
                    return
                json_obj = await q.json()
                results_raw = json_obj["items"]

                # Process...
                embed_field_counter = 0
                for result in results_raw:
                    title = result["title"]
                    url = result["link"].replace(")", "%29")
                    desc = result["snippet"].replace("\n", "")
                    search_embed.add_field(name=f"{title} ({url})", value=desc)
                    embed_field_counter += 1
                    print(f"{tag(start)} Adding embed field no", embed_field_counter)
                    if embed_field_counter >= 24:
                        break

        # Embed styling (misc)
        search_embed.colour = choice([discord.Colour.blue(), discord.Colour.gold(), discord.Colour.green(), discord.Colour.red()])
        search_embed.set_footer(text="Plugin by SapiensAnatis, using Google APIs", icon_url="http://i.imgur.com/2UhmSpf.png")
        search_embed.set_author(name=f"Google search (click here to view at google.com)", url=f"https://www.google.com/search?q={query_formatted}")
        search_embed.set_thumbnail(url="http://i.imgur.com/JFYsOlc.png")

        await self.bot.edit_message(search_message, new_content=f"Search completed in {time_since(start)}ms.", embed=search_embed)
        #await self.bot.edit_message(search_message, new_content=":thinking:")
        print(f"{tag(start)} Finished!")

def setup(parent):
    instance = Search(parent)
    parent.add_cog(instance)
