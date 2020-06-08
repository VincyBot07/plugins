import discord
from discord.ext import commands

class StatoMC(commands.Cog):
      def __init__(self, bot):
            self.bot = bot

      @commands.command(aliases=["stato"])
      async def statomc(self, ctx):
            """Mostra lo stato del server Minecraft."""
            response = await self.bot.session.get("http://statomc.vincysuper07.cf/api.php")
            status = (await response.content.readline()).decode('UTF-8')
            embed = discord.Embed(title = "Server Minecraft: mc.Vincysuper07.cf", description = f"Al momento il server è {status}")
            if status == "OFFLINE.":
                embed.color = discord.Color.red()
            else:
                embed.color = discord.Color.green()
            await ctx.send(embed=embed)

def setup(bot):
      bot.add_cog(Comandi(bot))
