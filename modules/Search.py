print("\n   [Search.py] Loading necessary modules...", end="")
import discord
from discord.ext import commands
from random import choice
import json
import aiohttp
loc = "uk"
print("done!")

class Search:
    def __init__(self, bot):
        print("   [Search.py] Initializing", end="")
        self.bot = bot
        self.api_key = ""
        print("...done!")

        print("   [Search.py] Locating API key in SearchAPIKey.txt",end="")
        with open(r"C:\Users\Jay\PycharmProjects\spaghetti-bot\modules\SearchAPIKey.txt", "r") as file_in:
            self.api_key = file_in.read()
            print(f"loaded api key {self.api_key}")

        print("...done!")


    def generate_search_url(self, query, num):
        url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={self.api_key}&cx=011947631902407852034:gq02yx0e1mq&gl={loc}&num={num}"
        return url

    @commands.command(pass_context = True)
    async def search(self, ctx, query : str, count : int = 5):
        # Rule out horseplay (input validation)
        if ctx.message.author == ctx.message.server.me:
            return
        if count > 10 or count < 1: # google-imposed limits
            await self.bot.send_message(ctx.message.channel, ":unamused:")
            return
        print(f"[Search.py] User {ctx.message.author.name} has made a search with query {query}.")
        search_message = await self.bot.send_message(ctx.message.channel, "Searching...")

        query_formatted = query.replace(" ", "+")
        search_url = self.generate_search_url(query_formatted, count)

        # Create our embed, to be stylized later...
        search_embed = discord.Embed()

        async with aiohttp.ClientSession() as client:
            async with client.get(search_url) as q:
                # Get results from webrequest
                print("[Search.py] Grabbing data from", search_url)
                print("[Search.py] Received request status", q.status)
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
                    url = result["link"]
                    desc = result["snippet"]
                    search_embed.add_field(name=f"{title} ({url})", value=desc)
                    embed_field_counter += 1
                    print("Adding embed field no", embed_field_counter)
                    if embed_field_counter >= 24:
                        break

        # Embed styling (misc)
        search_embed.colour = choice([discord.Colour.blue(), discord.Colour.gold(), discord.Colour.green(), discord.Colour.red()])
        search_embed.set_footer(text="Plugin by SapiensAnatis, using Google APIs", icon_url="http://i.imgur.com/2UhmSpf.png")
        search_embed.set_author(name=f"Google search (click to view indepth)", url=f"https://www.google.com/search?q={query_formatted}")
        search_embed.set_thumbnail(url="http://i.imgur.com/JFYsOlc.png")
        await self.bot.edit_message(search_message, new_content="Search complete:", embed=search_embed)
        #await self.bot.edit_message(search_message, new_content=":thinking:")

def setup(parent):
    instance = Search(parent)
    parent.add_cog(instance)
