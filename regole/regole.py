import discord
from discord.ext import commands


class Regole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def regole(self, ctx):
        embed = discord.Embed(
            title="Regole del server",
            url="https://vincybot07.vincysuper07.cf",
            description="Questo server, come tutti gli altri, ha delle regole che __devono__ essere rispettate.",
            color=0x00FF00,
        )
        embed.add_field(
            name="REGOLA D'ORO!",
            value=f"Rispetta, accetta e sii gentile con tutti.\n"
            "Tagga <@&595651372247154729> se vieni molestato. Non reagire.",
            inline=False,
        )
        embed.set_author(
            name="Vincysuper07",
            url="https://vincysuper07.cf",
            icon_url="https://cdn.discordapp.com/attachments/595327251579404298/682915766160588817/img2.png",
        )
        embed.add_field(
            name="1. È vietato alcun tipo di spam, flood, raid e altri tipi di spam.",
            value="Lo spam in questo server è proibito in questo server.\n"
            "Se qualcuno dovesse spammare, verrà kickato.\n"
            "Se qualcuno dovesse raidare, avete il consenso di spammare <@&595651372247154729>,\n"
            "noi prenderemo i provvedimenti necessari.",
            inline=False,
        )
        embed.add_field(
            name="2. È vietato insultare e bestemmiare.",
            value=f"Insulti, bestemmie, drammi e altre cose sono vietate in questo server.\n"
            "Se qualcuno dovesse bestemmiare oppure insultare, taggate <@&595651372247154729>.\n"
            "È consentito dire parolacce, però, solo fino a un certo punto.",
            inline=False,
        )
        embed.add_field(
            name="3. È vietato avere un nome impossibile da menzionare.",
            value="In questo server, i nomi devono essere **__tutti__ taggabili**. Quindi,\n"
            "un solo nome intaggabile, verrà cambiato in qualcos'altro.\n"
            "Se qualcuno dovesse rimettere il nome intaggabile, verrà avvertito, e,\n"
            "se necessario, verrà anche mutato!",
            inline=False,
        )
        embed.add_field(
            name="4. Non inviare NSFW.",
            value="È illegale, sta scritto nei termini di servizio di Discord. [Leggi altro...](http://discord.com/terms)\n"
            "Tornando alle regole, l'invio anche di un solo video/immagine NSFW, vale un __ban istantaneo__!",
            inline=False,
        )
        embed.add_field(
            name="5. Non fare pubblicità.",
            value=f"La pubblicità al di fuori di <#595326853728960523> vale un warn, poi kick e ban!\n"
            "**La pubblicità in privato è __inclusa__!**",
            inline=False,
        )
        embed.add_field(
            name=f"6. Niente minimod nel server.",
            value=f"Lasciate gli <@&595651372247154729> fare il loro lavoro.",
            inline=False,
        )
        embed.add_field(
            name="Nota bene:",
            value=f"•Tutte le regole elencate qui sotto, **valgono __anche__ in chat privata**, quindi,\n"
            "se qualcuno dovesse violare una o più regole nella chat privata, taggate <@&595651372247154729>,\n"
            "provvederemo noi a tutto.\n"
            "•Violazione di una regola: __Warn__\n"
            "4 Warn in 2 settimane: **Mute per __2 giorni__**\n"
            "5 Warn in 2 settimane: **__Ban__**!\n"
            "•Noi consentiamo le persone che hanno meno di 13 anni, quindi,\n"
            "qui potete dire l'età, non la diremo a nessuno.\n"
            "Se qualcuno non dovesse dire la sua vera età (es. qualcuno dice “Ho 22 anni” ma si capisce benissimo che ne ha 12)\n"
            "verrà bannato dal server.\n"
            "•Gli <@&595651372247154729> possono bannarti senza warn in qualsiasi momento!",
            inline=False,
        )
        embed.set_footer(text="Rispettale e non verrai bannato!")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Regole(bot))
