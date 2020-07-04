import json
import discord
from discord.ext import commands

class GitHubNews(commands.Cog, name="GitHub News"):
  def __init(self, bot):
    self.bot = bot

    
    
    
def setup(bot):
  bot.add_cog(GitHubNews(bot))
