import json
import random
import discord
from discord.ext import commands
colors = [0x6bc7ea, 0xc73650, 0xfdf95b]

class GitHubNews(commands.Cog, name="GitHub News"):
    def __init__(self, bot):
        self.bot = bot
    #
    @commands.command()
    async def testgitnews(self,ctx):
        color = random.choice(colors)
        request = await self.bot.session.get("https://api.github.com/repos/VincyBot07/VincyBot07/releases/latest")
        response = await request.content.readline()
        resp = json.loads(response)
        e = discord.Embed(title="testù", description=f'versione: {resp["tag_name"]}', color=color)
        await ctx.send(embed=e)


def setup(bot):
    bot.add_cog(GitHubNews(bot))
