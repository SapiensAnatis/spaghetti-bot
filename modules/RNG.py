print("   [RNG.py] Importing required modules...", end="")
import random
try: import inflect; inflect_imported = True
except: pass
import discord
from discord.ext import commands
print("done!")


class RNG:
    def __init__(self, bot):
        print("   [RNG.py] Initializing...", end="")
        self.bot = bot
        self.eightballresults = ["It is certain",
                            "It is decidedly so",
                            "Without a doubt",
                            "Yes, definitely",
                            "You may rely on it",
                            "As I see it, yes",
                            "Most likely",
                            "Quite possibly",
                            "Yes",
                            "Signs point to yes",
                            "Reply hazy; try again",
                            "Ask again later",
                            "Maybe yes, maybe no",
                            "I don't know",
                            "I'm not sure",
                            "Don't count on it",
                            "I'd say no",
                            "My sources say no",
                            "Probably not",
                            "Very doubtful"]
        print("done!")

    @commands.command(pass_context=True, aliases=['flip', 'cointoss', 'toss', 'flipacoin', 'headsortails', 'flipcoin'])
    async def coinflip(self, ctx):
        if ctx.message.author == ctx.message.server.me: return

        print(f"[RNG.py] User {ctx.message.author.name} has flipped a coin.")
        channel = ctx.message.channel

        result = random.randint(1,6000)
        print(f"[RNG.py] The int result was {result}")

        if result == 6000: # cite: Murray and Teare, The probability of a tossed coin falling on its edge, Phys. Rev. E. 2547-2552 (1993)
            await self.bot.send_message(channel, "The coin landed on its side.")
        elif result == 5999: # Add a second dumb outcome so that it isn't biased (heads/tails still has equal number of possibilities as range is divisible by two)
            await self.bot.send_message(channel, "The coin was flipped with such force that it entered low Earth orbit, never to be seen again.")
        elif result > 5998/2:
            await self.bot.send_message(channel, "Heads.")
        else:
            await self.bot.send_message(channel, "Tails.")

    @commands.command(pass_context=True, aliases=['roll, diceroll', 'dice', 'dieroll'])
    async def die(self, ctx, sides : float = 6):
        if ctx.message.author == ctx.message.server.me: return

        if sides > 1337 or sides <= 0:
            await self.bot.send_message(ctx.message.channel, ":unamused:")
            return

        print(f"[RNG.py] User {ctx.message.author.name} has rolled a {sides}-sided die.")

        if sides.is_integer():
            print(f"[RNG.py] Rolling integer-sided die...")
            result = random.randint(1,int(sides))
            clarify = ""
        else:
            print(f"[RNG.py] Rolling non-integer sided die...")
            result = round(random.random() * sides, len(str(sides)[2:]))
            clarify = f" ({str(result)})"

        if inflect_imported: result = inflect.engine().number_to_words(result) # humanize: "99" -> "ninety-nine"
        await self.bot.send_message(ctx.message.channel, f"🎲 You rolled a {result}{clarify}.")

    @commands.command(pass_context=True, aliases=['8ball', 'magic8ball'])
    async def eightball(self, ctx):
        if ctx.message.author == ctx.message.server.me: return

        result = self.eightballresults[random.randint(0,len(self.eightballresults)-1)]
        await self.bot.send_message(ctx.message.channel, f":8ball: {result}.")

def setup(parent):
    instance = RNG(parent)
    parent.add_cog(instance)
