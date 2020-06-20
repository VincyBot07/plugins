import discord
from discord.ext import commands

from core.paginator import EmbedPaginatorSession


class Comandi(commands.Cog):
    """Lista di comandi by Vincy"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def accetto(self, ctx):
        """<#595319716344758291>"""
        member = ctx.author
        role = discord.utils.find(lambda r: r.name == "Membri", ctx.guild.roles)
        await member.add_roles(role)

    @commands.command(aliases=["help"])
    #async def comandi(self, ctx)
    async def comandi(self, cog, *, no_cog=False, context = ctx):
        """Mostra questo messaggio"""
        bot = self.context.bot
        prefix = self.clean_prefix

        formats = [""]
        for cmd in await self.filter_commands(
            cog.get_commands() if not no_cog else cog,
            sort=True,
            key=lambda c: (bot.command_perm(c.qualified_name), c.qualified_name),
        ):
            perm_level = bot.command_perm(cmd.qualified_name)
            if perm_level is PermissionLevel.INVALID:
                format_ = f"`{prefix + cmd.qualified_name}` "
            else:
                format_ = f"`[{perm_level}] {prefix + cmd.qualified_name}` "

            format_ += f"- {cmd.short_doc}\n"
            if not format_.strip():
                continue
            if len(format_) + len(formats[-1]) >= 1024:
                formats.append(format_)
            else:
                formats[-1] += format_

        embeds = []
        for format_ in formats:
            description = (
                cog.description or "Nessuna descrizione."
                if not no_cog
                else "Svariati comandi senza categoria."
            )
            embed = discord.Embed(description=f"*{description}*", color=bot.main_color)

            embed.add_field(name="Comandi", value=format_ or "Nessun comando.")

            continued = " (Continuato)" if embeds else ""
            name = cog.qualified_name + " - Comandi" if not no_cog else "Comandi vari"
            embed.set_author(name=name + continued, icon_url=bot.user.avatar_url)

            embed.set_footer(
                text=f'Scrivi il comando "{prefix}{self.command_attrs["name"]}" '
                "per informazioni comando specifico."
            )
            embeds.append(embed)
        return embeds

    def help_msg_process(self, help_: str):
        return help_.format(prefix=self.clean_prefix) if help_ else "Nessun messaggio."

    async def bot_help_send(self, mapping):
        embeds = []
        no_cog_commands = sorted(mapping.pop(None), key=lambda c: c.qualified_name)
        cogs = sorted(mapping, key=lambda c: c.qualified_name)

        bot = self.context.bot

        # always come first
        default_cogs = [bot.get_cog("Tag"), bot.get_cog("Divertimento"), bot.get_cog("Utilita"), bot.get_cog("Plugin")]

        default_cogs.extend(c for c in cogs if c not in default_cogs)

        for cog in default_cogs:
            embeds.extend(await self.format_cog_help(cog))
        if no_cog_commands:
            embeds.extend(await self.format_cog_help(no_cog_commands, no_cog=True))

        session = EmbedPaginatorSession(self.context, *embeds, destination=self.get_destination())
        return await session.run()

    async def send_cog_help(self, cog):
        embeds = await self.format_cog_help(cog)
        session = EmbedPaginatorSession(self.context, *embeds, destination=self.get_destination())
        return await session.run()

    async def _get_help_embed(self, topic):
        if not await self.filter_commands([topic]):
            return
        perm_level = self.context.bot.command_perm(topic.qualified_name)
        if perm_level is not PermissionLevel.INVALID:
            perm_level = f"{perm_level.name} [{perm_level}]"
        else:
            perm_level = "NONE"

        embed = discord.Embed(
            title=f"`{self.get_command_signature(topic)}`",
            color=self.context.bot.main_color,
            description=self.help_msg_process(topic.help),
        )
        return embed, perm_level

    async def send_command_help(self, command):
        topic = await self._get_help_embed(command)
        if topic is not None:
            topic[0].set_footer(text=f"Livello di permessi: {topic[1]}")
            await self.get_destination().send(embed=topic[0])

    async def send_group_help(self, group):
        topic = await self._get_help_embed(group)
        if topic is None:
            return
        embed = topic[0]
        embed.add_field(name="Livello di permessi", value=topic[1], inline=False)

        format_ = ""
        length = len(group.commands)

        for i, command in enumerate(
            await self.filter_commands(group.commands, sort=True, key=lambda c: c.name)
        ):
            # BUG: fmt may run over the embed limit
            # TODO: paginate this
            if length == i + 1:  # last
                branch = "└─"
            else:
                branch = "├─"
            format_ += f"`{branch} {command.name}` - {command.short_doc}\n"

        embed.add_field(name="Sotto-comandi", value=format_[:1024], inline=False)
        embed.set_footer(
            text=f'Scrivi il comando "{self.clean_prefix}{self.command_attrs["name"]}" '
            "per più informazioni riguardo un comando."
        )

        await self.get_destination().send(embed=embed)

    async def send_error_message(self, error):
        command = self.context.kwargs.get("command")
        val = self.context.bot.snippets.get(command)
        if val is not None:
            embed = discord.Embed(
                title=f"{command} è uno snippet.", color=self.context.bot.main_color
            )
            embed.add_field(name=f"`{command}` invierà:", value=val)
            return await self.get_destination().send(embed=embed)

        val = self.context.bot.aliases.get(command)
        if val is not None:
            values = utils.parse_alias(val)

            if not values:
                embed = discord.Embed(
                    title="Errore",
                    color=self.context.bot.error_color,
                    description=f"L'alias `{command}` non è valido e verrà eliminato",
                )
                embed.add_field(name=f"{command}` era:", value=val)
                self.context.bot.aliases.pop(command)
                await self.context.bot.config.update()
            else:
                if len(values) == 1:
                    embed = discord.Embed(
                        title=f"{command} è un alias.", color=discord.Color.blurple()
                    )
                    embed.add_field(name=f"`{command}` punta a:", value=values[0])
                else:
                    embed = discord.Embed(
                        title=f"{command} è un alias.",
                        color=self.context.bot.main_color,
                        description=f"**`{command}` punta a i seguenti step:**",
                    )
                    for i, val in enumerate(values, start=1):
                        embed.add_field(name=f"Step {i}:", value=val)

            embed.set_footer(
                text=f'Scrivi l\'alias "{self.clean_prefix}{self.command_attrs["name"]} " '
                "per più dettagli riguardo un alias."
            )
            return await self.get_destination().send(embed=embed)

        logger.warning("CommandNotFound: %s", error)

        embed = discord.Embed(color=self.context.bot.error_color)
        embed.set_footer(text=f'Il comando/La categoria "{command}" non è stato/a trovato/a.')

        choices = set()

        for cmd in self.context.bot.walk_commands():
            if not cmd.hidden:
                choices.add(cmd.qualified_name)

        closest = get_close_matches(command, choices)
        if closest:
            embed.add_field(name="Forse intendevi:", value="\n".join(f"`{x}`" for x in closest))
        else:
            embed.title = "Non è stato possibile trovare il comando o la categoria specificata."
            embed.set_footer(
                text=f'Scrivi "{self.clean_prefix}{self.command_attrs["name"]}" '
                "Per una lista di tutti i comandi disponibili."
            )
        await self.get_destination().send(embed=embed)

        #"""Mostra i comandi del bot"""
        #e = discord.Embed(
        #    title="Tags",
        #    description=f"""{ctx.prefix}tag <nome> - Usa un tag!
        #    {ctx.prefix}tags add <nome> <risposta> - Crea un tag!""",
        #    color=discord.Color.green(),
        #)
        #em = discord.Embed(
        #    title="Divertimento",
        #    description=f"""{ctx.prefix}inspiro(bot) - Mostra un immagine a caso da InspiroBot.me
        #    {ctx.prefix}choose <primo oggetto> <secondo oggetto> Scegli tra 2 oggetti!
        #    {ctx.prefix}roll - Lancia un dado
        #    {ctx.prefix}flip - Lancia una moneta
        #    {ctx.prefix}rps - Sasso, Carta, o Forbici?
        #    {ctx.prefix}8ball <domanda>? - La 8Ball risponderà a ogni tua domanda!
        #    {ctx.prefix}reverse <messaggio> - !otseT out li etrevnI\n{ctx.prefix}meme - Ti da una meme a caso
        #    {ctx.prefix}roast <persona> - Insulta la persona menzionata
        #    {ctx.prefix}smallcaps <messaggio> - ᴄᴏɴᴠᴇʀᴛᴇ ɪʟ ᴛᴜᴏ ᴛᴇꜱᴛᴏ ᴀ ᴜɴ ᴍᴀɪᴜꜱᴄᴏʟᴏ ᴘɪᴄᴄᴏʟᴏ!""",
        #    color=discord.Color.green(),
        #)
        #emb = discord.Embed(
        #    title="Hastebin",
        #    description=f"{ctx.prefix}hastebin <messaggio> - Inserisce il tuo testo su Hastebin",
        #    color=discord.Color.green(),
        #)
        #embe = discord.Embed(
        #    title="Moderazione",
        #    description=f"""{ctx.prefix}purge <numero> - Elimina una quantità da 1 a 100 di messaggi
        #    {ctx.prefix}kick <persona> - Espelle un membro del server
        #    {ctx.prefix}mute <persona> - Muta una persona nel server
        #    {ctx.prefix}unmute <persona> - Smuta una persona nel server
        #    {ctx.prefix}nuke - Eimina tutti i messaggi di una chat
        #    {ctx.prefix}ban <persona> - Banna una persona dal server
        #    {ctx.prefix}unban <persona> - Revoca il ban a una persona del server""",
        #    color=discord.Color.green(),
        #)
        #embed = discord.Embed(
        #    title="Annunci",
        #    description=f"""{ctx.prefix}announcement start - crea un annuncio interattivo
        #    {ctx.prefix}announcement quick <canale> [ruolo] <messaggio> - Un modo alternativo e più veloce per creare un'annuncio""",
        #    color=discord.Color.green(),
        #)
        #embedd = discord.Embed(
        #    title="Musica",
        #    description=f"""{ctx.prefix}join - Entra in un canale vocale
        #    {ctx.prefix}leave - Esce da un canale vocale
        #    {ctx.prefix}now - Mostra la canzone in riproduzione
        #    {ctx.prefix}pause - Mette una canzone in pausa
        #    {ctx.prefix}play <link-canzone> - Riproduce una canzone
        #    {ctx.prefix}queue - mostra la coda
        #    {ctx.prefix}remove - Rimuove una canzone dalla coda
        #    {ctx.prefix}resume - Riprende una canzone dopo averla messa in pausa
        #    {ctx.prefix}shuffle - Attiva la riproduzione casuale
        #    {ctx.prefix}skip - Salta una canzone passando a quella successiva
        #    {ctx.prefix}stop - Ferma la riproduzione della musica, ma pulisce la coda
        #    {ctx.prefix}summon - Lo stesso di v!play, entra in un canale vocale
        #    {ctx.prefix}volume <volume> - Cambia il volume del bot""",
        #    color=discord.Color.green(),
        #)
        #embeddd = discord.Embed(
        #    title="Altro",
        #    description=f"""{ctx.prefix}embed send <titolo> <Descrizione> - Invia un messaggio incorporato
        #    {ctx.prefix}embed color <hexcode> - Cambia il colore del tuo messaggio incorporato
        #    {ctx.prefix}welcomer <chat> <messaggio> - Crea un messaggio di benvenuto!
        #    {ctx.prefix}reactionrole add <id_messaggio> <ruolo> <emoji> - Inserisce una reazione ad un messaggio, che servirà per ricevere un ruolo!
        #    {ctx.prefix}stato - Controlla se il server Minecraft di Vincy è online!
        #    {ctx.prefix}comandi - Mostra questo messaggio!
        #    {ctx.prefix}help - Mostra questo messaggio!""",
        #    color=discord.Color.green(),
        #)
        #embeds = []
        #embed_list = [e, em, emb, embe, embed, embedd, embeddd]
        #for embed in embed_list:
        #    embed.set_footer(text=f"Usa le frecce per cambiare pagina. • Prefix: {ctx.prefix}")
        #    embed.set_author(name="VincyBot07", icon_url=self.bot.user.avatar_url)
        #    embeds.append(embed)
        #session = EmbedPaginatorSession(ctx, *embeds)
        #await session.run()

    @commands.command(aliases=["helpmod", "helpm", "hmod", "hadmin", "helpa", "hm"])
    async def helpadmin(self, ctx):
        await ctx.send_help()


def setup(bot):
    bot.add_cog(Comandi(bot))
