import discord
from discord.ext import commands
import requests
import json
import os

class StatoMC(commands.Cog):
      def __init__(self, bot):
            self.bot = bot

      @commands.command(aliases=["stato"])
      async def statomc(self, ctx):
            """Mostra lo stato del server Minecraft."""
            mc_url = os.getenv("MINECRAFT_SERVER")
            response = requests.get(f'https://api.mcsrvstat.us/2/{mc_url')
            status = json.loads(rsp.text)
            #print(load["online"])
            online = status["online"]
            players = status["players"]["online"]
            max = status["players"]["max"]
            version = status["version"]
            #embed = discord.Embed(title = "Server Minecraft: {mc_url}", description = f"Al momento il server è {status}")
            if online == True:
                if players == "1":
                    e = discord.Embed(title = "Server Minecraft: {mc_url}", description = f"Al momento il server è **online**. **1** persona sta giocando sul massimo di {max}.", color = discord.Color.green())
                else:
                    e = discord.Embed(title = "Server Minecraft: {mc_url}", description = f"Al momento il server è **online**. **{players}** persone stanno giocando sul massimo di {max}.")
                if players == "0":
                    e = discord.Embed(title = "Server Minecraft: {mc_url}", description = f"Al momento il server è **online**.")
                e.set_footer(text="La versione è {version}.")
            else:
                e = discord.Embed(title = "Server Minecraft: {mc_url}", description = f"Al momento il server è **offline**.", color=discord.Color.red()).set_footer(text="Non posso sapere la versione, dato che il server è offline.")
            await ctx.send(embed=embed)

def setup(bot):
      bot.add_cog(Comandi(bot))
