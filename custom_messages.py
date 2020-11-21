from discord.ext import commands


class CustomMessageCog:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="blind", help="Because Blind wanted a Command")
    async def blind(self, context):
        await context.send("`Blind volunteered to do every Mechanic in Shadowlands raiding`")