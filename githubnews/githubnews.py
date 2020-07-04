import json
import random
import discord
from discord.ext import commands
colors = [0x6bc7ea, 0xc73650, 0xfdf95b]

class GitHubNews(commands.Cog, name="GitHub News"):
    def __init(self, bot):
        self.bot = bot
        self.request = await bot.session.get("https://api.github.com/repos/VincyBot07/VincyBot07/releases/latest")
        self.response = await request.content.readline()
        self.resp = json.loads(response)
        self.colors = [0x6bc7ea, 0xc73650, 0xfdf95b]
        self.color = random.choice(colors)
    #
    @commands.command()
    async def qpowieurtyturiewqop(self,ctx):
        e = discord.Embed(title="testù", description=f"versione: {self.resp["tag_name"}")



def setup(bot):
    bot.add_cog(GitHubNews(bot))
