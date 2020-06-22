import discord
from discord.ext import commands
import json
import os

class StatoMC(commands.Cog):
      def __init__(self, bot):
            self.bot = bot

      @commands.command(aliases=["stato"])
      async def statomc(self, ctx):
            """Mostra lo stato del server Minecraft."""
            mc_url = os.getenv("MINECRAFT_SERVER")
            request = await self.bot.session.get(f'https://api.mcsrvstat.us/2/{mc_url}')
            response = await request.content.readline()
            status = json.loads(response)
            online = status["online"]
            players = status["players"]["online"]
            max = status["players"]["max"]
            version = status["version"]
            if online == True:
                if players == 0:
                    e = discord.Embed(title = f"Server Minecraft: {mc_url}", description = "Al momento il server è **online**.")
                elif players == 1:
                    e = discord.Embed(title = f"Server Minecraft: {mc_url}", description = f"Al momento il server è **online**. **1** persona sta giocando sul massimo di {max}.")
                else:
                    e = discord.Embed(title = f"Server Minecraft: {mc_url}", description = f"Al momento il server è **online**. **{players}** persone stanno giocando sul massimo di **{max}**.")

                e.color = discord.Color.green()
                e.set_footer(text=f"La versione è {version}.")

            elif online == False:
                e = discord.Embed(title = f"Server Minecraft: {mc_url}", description = "Al momento il server è **offline**.", color=discord.Color.red()).set_footer(text="Non posso sapere la versione, dato che il server è offline.")
            await ctx.send(embed=e)

def setup(bot):
      bot.add_cog(StatoMC(bot))
