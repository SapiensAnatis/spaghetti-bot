print("\n    Importing discord & other modules...", end="")
import discord
from discord.ext import commands
from asyncio import sleep

print("done!")

cleanup_delay = 6000  # seconds


def role_has_users(role):
    if role.name.startswith("[#"):
        people_with_role = [x.name for x in role.server.members if role in x.roles]
    #   print(f"[debug][Colors.py] Role search complete for role {role.name}: found users {people_with_role}")
        return bool(people_with_role)
    else:
        print(f"[warn][Colors.py] Attempted to check role_has_users status of role {role.name}! "
              f"This role is not owned by this script! It is recommended that you remove this call.")
        return True


class Colors:
    def __init__(self, bot):
        print("    Initializing...", end="")
        self.bot = bot  # there used to be more code here...hence the print statements
        print("done!")

    async def start_background_clean(self):
        await self.bot.wait_until_ready()
        # Clean duplicate and unused roles
        while True:
            print("[Colors.py] Cleaning up unused & duplicate colour roles...")
            deleted_roles = 0
            removed_roles = 0

            for server in self.bot.servers:
                roles = [] # Start collecting role names to identify dupes
                for role in server.roles:
                    if role.name.startswith("[#"):  # make sure it's our business
                        if not role_has_users(role):
                            print(f"  * L O C A T E D redundant role {role} in server {server}. Deleting...")
                            await self.bot.delete_role(server, role)
                            deleted_roles += 1
                        if role.name in roles:
                            print(f"  * L O C A T E D duplicate role {role} in server {server}. Deleting...")
                            await self.bot.delete_role(server, role)
                            deleted_roles += 1

                        roles.append(role.name)

                # Find users with duplicate roles and delete the second role

                for member in server.members:
                    their_role = None
                    for role in member.roles:
                        if role.name.startswith("[#"):
                            if their_role is not None: # if they already have a role
                                print(f"  * L O C A T E D user {member.name} in server {server.name} with second colour role {role.name}. Removing...")
                                await self.bot.remove_roles(member, role)
                                removed_roles += 1

                                # Because we'll soon be checking for redundancy, we need to do that hack again to ensure
                                # roles are actually seen as redundant (fully deleted) before impending cleanup

                                await sleep(1)
                                # now check if that role is redundant:
                                if not role_has_users(role):
                                    print("   * Additionally, this role no longer has users. Deleting...")
                                    await self.bot.delete_role(server, role)
                                    deleted_roles += 1
                            else:
                                their_role = role



            print(f"[Colors.py] Finished cleaning up redundant colour roles; {deleted_roles} roles deleted and {removed_roles} removed from users.")
            await sleep(cleanup_delay)  # async sleep shouldn't slow down the program, hence a while loop is appropriate


    @commands.command(pass_context=True, aliases=['colour'])
    async def color(self, ctx, color_argument_raw: str):  # color is a hex code or should be...

        server = ctx.message.server
        author = ctx.message.author

        if author == self.bot.user:  # No skynet today
            return

        color_argument = color_argument_raw.replace("#", "")  # remove hash; the int(hex, 16) method dislikes hashes

        print(f"[Colors.py on server {server.name}] User {author.name} has requested colour #{color_argument}.")
        # Ensure validity of hex code
        if len(color_argument) != 6:  # Potentially invalid (alpha channels are obviously not supported)
            await self.bot.send_message("Please provide a valid hex code.", ctx.message.channel)
            return
        print("  * The user's input was validated successfully. Removing existing roles...")

        # Find a user's existing colour role if applicable
        old_roles = [x for x in author.roles if x.name.startswith("[#")]

        for old_role in old_roles:
            if old_role is not None:  # if one was found
                print(f"    * Found existing colour role {old_role.name} - removing...")
                await self.bot.remove_roles(author, old_role)
                await sleep(1)  # dirty hack to make sure delete actually goes through before we check for disuse
                print("    * Removed role, checking if still in use...")
                # If that role is now empty, remove it entirely:
                if not role_has_users(old_role):  # if there is nobody with the role
                    print("    * Existing colour role was now empty, deleting...")
                    await self.bot.delete_role(server, old_role)

        print("  * Existing roles successfully cleaned. Applying and possibly creating new role...")
        # Now, apply the new role. First, check if the role already exists
        result = discord.utils.find(lambda role: role.name == f"[#{color_argument}])", server.roles)
        if result is not None:
            print(f"    * Provided colour change to {color_argument} for user {author.name} using pre-existing role.")
            await self.bot.add_roles(author, result)
        else:
            print(f"    * Cannot provide name colour {color_argument} for user {author.name} using current roles. "
                  f"Creating new role...")

            color_int = int(color_argument,
                            16)  # convert our string to a hex int with which we can generate a discord.Color
            discord_color = discord.Color(color_int)
            new_role = await self.bot.create_role(server, name=f"[#{color_argument}]",
                                                  color=discord_color, permissions=discord.Permissions.none())

            ''''"To the top!" - /r/the_donald, literally every day
            # print(f"Created. Moving to pos {server.me.top_role.position - 1}...", end="")
            # await self.Session.move_role(server, new_role, server.me.top_role.position - 1)

            print(f"    * Successfully created role ({color_argument}) for user {author.name}. Applying...")'''

            # The above code causes permission errors for some reason. It is ultimately unimportant;  it seems unlikely
            # to me that admins will make roles that have colours overriding ours without a specific reason in mind.
            # Moreover, a user can only have one at a time. Due to its unimportance, a fix isn't worth pursuing.

            # Apply...
            await self.bot.add_roles(author, new_role)
        print("  * Role changing successful.")


def setup(parent):
    instance = Colors(parent)
    parent.add_cog(instance)
    parent.loop.create_task(Colors.start_background_clean(instance))
