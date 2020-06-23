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
            value="""Rispetta, accetta e sii gentile con tutti.
            Tagga @Staff se vieni molestato. Non reagire.""",
        )
        embed.set_author(name="Vincysuper07", url="https://vincysuper07.cf")
        embed.add_field(
            name="1. È vietato alcun tipo di spam, flood, raid e altri tipi di spam.",
            value="""
            Lo spam in questo server è proibito in questo server.
            Se qualcuno dovesse spammare, verrà kickato.
            Se qualcuno dovesse raidare, avete il consenso di spammare @Staff,
            noi prenderemo i provvedimenti necessari.
            """,
        )
        embed.add_field(
            name="2. È vietato insultare e bestemmiare.",
            value="""
            Insulti, bestemmie, drammi e altre cose sono vietate in questo server.
            Se qualcuno dovesse bestemmiare oppure insultare, taggate @Staff.
            È consentito dire parolacce, però, solo fino a un certo punto.
            """,
        )
        embed.add_field(
            name="3. È vietato avere un nome impossibile da menzionare.",
            value="""
            In questo server, i nomi devono essere **__tutti__ taggabili**. Quindi,
            un solo nome intaggabile, verrà cambiato in qualcos'altro.
            Se qualcuno dovesse rimettere il nome intaggabile, verrà avvertito, e,
            se necessario, verrà anche mutato!
            """,
        )
        embed.add_field(
            name="4. Non inviare NSFW.",
            value="""
            È illegale, sta scritto nei termini di servizio di Discord. [Leggi altro...](http://discord.com/terms)
            Tornando alle regole, l'invio anche di un solo video/immagine NSFW, vale un __ban istantaneo__!
            """,
        )
        embed.add_field(
            name="5. Non fare pubblicità.",
            value="""
            La pubblicità al di fuori di #pubblicità vale un __ban istantaneo__!
            La pubblicità in privato è inclusa!
            """,
        )
        embed.add_field(
            name="6. Niente minimod nel server.", value="Lasciate gli @Staff fare il loro lavoro.",
        )
        embed.add_field(
            name="Nota bene:",
            value="""
            •Tutte le regole elencate qui sotto, **valgono __anche__ in chat privata**, quindi, se qualcuno dovesse violare una o più regole nella chat privata, taggate @Staff, provvederemo noi a tutto:blobban::yea:
            •Violazione di una regola: __Warn__
            4 Warn in 2 settimane: **Mute per __2 giorni__**
            5 Warn in 2 settimane: **__Ban__**!
            •Noi consentiamo le persone che hanno meno di 13 anni, quindi, qui potete dire l'età, non la diremo a nessuno. Se qualcuno non dovesse dire la sua vera età (es. ualcuno dice “Ho 22 anni” ma si capisce benissimo che ne ha 12) verrà bannato dal server
            •Gli @Staff possono bannarti senza warn in qualsiasi momento!
            """,
            inline=False,
        )
        embed.set_footer(text="Rispettale e non verrai bannato!")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Regole(bot))
