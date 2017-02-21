print("\n\t\tImporting discord & other modules...", end="")
import discord
from discord.ext import commands
from asyncio import sleep

print("done!")

default_color = discord.Color(0x74b2ed)
cleanup_delay = 6000  # seconds


def role_has_users(role):
    if role.name.startswith("(#"):
        people_with_role = [x.name for x in role.server.members if role in x.roles]
    #   print("[debug][Colors.py] Role search complete for role {0}: found users {1}".format(role.name, people_with_role))
        return bool(people_with_role)
    else:
        print("[warn][Colors.py] Attempted to check role_has_users status of a role {0}, which is not owned by this script!"
                .format(role.name))
        return True


class Colors():
    def __init__(self, bot):
        print("\t\tInitializing...", end="")
        self.bot = bot  # there used to be more code here
        print("done!")

    async def start_background_clean(self):
        await self.bot.wait_until_ready()
        while True:
            print("[Colors.py] Cleaning up unused & duplicate colour roles..."
                  .format(cleanup_delay))
            count = 0
            for server in self.bot.servers:
                roles = []
                for role in server.roles:
                    if role.name.startswith("(#"):  # make sure it's our business
                        if not role_has_users(role):
                            print("\t* L O C A T E D unused role {0} in server {1}. Deleting..."
                                  .format(role, server))
                            await self.bot.delete_role(server, role)
                            count += 1
                        if role.name in roles:
                            print("\t* L O C A T E D duplicate role {0} in server {1}. Deleting..."
                                  .format(role, server))
                            await self.bot.delete_role(server, role)
                            count += 1

                        roles.append(role.name)
            print("[Colors.py] Finished cleaning up colour roles; {0} roles deleted.".format(count))
            await sleep(6000)

    @commands.command(pass_context=True, aliases=['colour'])
    async def color(self, ctx, color_argument_raw: str):  # color is a hex code or should be...

        server = ctx.message.server
        author = ctx.message.author

        if author == self.bot.user:  # No skynet today
            return

        color_argument = color_argument_raw.replace("#", "")  # remove hash; the int(hex, 16) method dislikes hashes

        print("[Colors.py on server {2}] User {0} has requested a colour change to {1}."
              .format(author.name, color_argument, server.name))
        # Ensure validity of hex code
        if len(color_argument) != 6:  # Potentially invalid (alpha channels are obviously not supported)
            await self.bot.send_message("Please provide a valid hex code.", ctx.message.channel)
            return
        print("\t* Input was validated successfully. Cleaning up old roles...")

        # Find a user's existing colour role if applicable
        old_role = discord.utils.find(lambda role: role.name.startswith("(#"), author.roles)

        if old_role is not None:  # if one was found
            print("\t\t* Found existing colour role {0} - removing..."
                  .format(old_role.name))
            await self.bot.remove_roles(author, old_role)
            await sleep(0.2)  # dirty hack to make sure delete actually goes through before we check for unuse
            print("\t\t* Removed role, checking if still in use...")
            # If that role is now empty, remove it entirely:
            if not role_has_users(old_role):  # if there is nobody with the role
                print("\t\t* Existing colour role was now empty, deleting...")
                await self.bot.delete_role(server, old_role)

        print("\t* Old roles successfully cleaned. Applying and possibly creating new role...")
        # Now, apply the new role. First, check if the role already exists
        result = discord.utils.find(lambda role: role.name == "(#{0})".format(color_argument), server.roles)
        if result is not None:
            print("\t\t* Provided colour change to {0} for {1} using pre-existing role."
                  .format(color_argument, author.name))
            await self.bot.add_roles(author, result)
        else:
            print(
                "\t\t* Cannot provide colour change to hex {0} for {1} using existing roles. Creating new role for them..."
                .format(color_argument, author.name))

            color_int = int(color_argument,
                            16)  # convert our string to a hex int with which we can generate a discord.Color
            discord_color = discord.Color(color_int)
            new_role = await self.bot.create_role(server, name="(#{0})".format(color_argument),
                                                  color=discord_color, permissions=discord.Permissions.none())
            ''''"To the top!" - /r/the_donald, literally every day
            # print("Created. Moving to pos {0}..."
            #      .format(server.me.top_role.position - 1), end="")
            # await self.Session.move_role(server, new_role, server.me.top_role.position - 1)

            print("\t\t* Successfully created role ({0}) for user {1}. Applying..."
                  .format(color_argument, author.name))'''
            # The above code causes permission errors for some reason. It is ultimately unimportant, as it seems unlikely
            # to me that admins will make roles that have colours overriding ours without a specific reason in mind.
            # Moreover, a user can only have one at a time. Due to its unimportance, a fix isn't worth pursuing.

            # Apply...
            await self.bot.add_roles(author, new_role)
        print("\t* Role changing successful.")


def setup(parent):
    instance = Colors(parent)
    parent.add_cog(instance)
    parent.loop.create_task(Colors.start_background_clean(instance))
