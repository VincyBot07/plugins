"""
Plugin di Embedder per VincyBot07.

Tradotto da Ergastolator1.
Tutti i diritti riservati.
"""

import re
from datetime import datetime

from discord import Color, Embed, Message
from discord.ext.commands import Bot, Cog, Context, group
from motor.motor_asyncio import AsyncIOMotorCollection
from pyimgur import Imgur

from core.checks import has_permissions
from core.models import PermissionLevel


class Embedder(Cog):
    """Crea facilmente embed per un look più fantastico.
    Più informazioni: [click here](https://github.com/Ergastolator1/fhmail-plugins/tree/master/embedder)
    """

    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.db: AsyncIOMotorCollection = bot.plugin_db.get_partition(self)

    @group(name="embedder", aliases=["embed"], invoke_without_command=True)
    @has_permissions(PermissionLevel.MODERATOR)
    async def embedder(self, ctx: Context) -> None:
        """Crea facilmente embed per una presenza più fantastica."""
        await ctx.send_help(ctx.command)

    @embedder.command(name="color", aliases=["colour"])
    @has_permissions(PermissionLevel.MODERATOR)
    async def color(self, ctx: Context, colorcode: str) -> None:
        """Salva un codice di colore per futuri embed."""
        is_valid = re.search(r"^#(?:[0-9a-fA-F]{3}){1,2}$", colorcode)

        if not is_valid:
            embed = Embed(
                title="Embedder",
                url="https://github.com/Ergastolator1/fhmail-plugins/blob/master/embedder",
                description="Per favore inserisci un valido [codice hex](https://htmlcolorcodes.com/color-picker)",
                color=self.bot.main_color,
            )

            return await ctx.send(embed=embed)

        colorcode = colorcode.replace("#", "0x")

        await self.db.find_one_and_update(
            {"_id": "embedcolor-config"}, {"$set": {"colorcode": colorcode}}, upsert=True,
        )

        embed = Embed(
            title="Embedder",
            url="https://github.com/Ergastolator1/fhmail-plugins/blob/master/embedder",
            description="Questo colore verrà usato per i futuri embed.",
            color=Color(int(colorcode, 0)),
        )

        await ctx.send(embed=embed)

    @embedder.command(name="send", aliases=["make"])
    @has_permissions(PermissionLevel.MODERATOR)
    async def send(self, ctx: Context, title: str, *, message: str) -> None:
        """Invia un embed."""
        try:
            colorcode = (await self.db.find_one({"_id": "embedcolor-config"}))["colorcode"]
        except (KeyError, TypeError):
            colorcode = "0x3498DB"  # blue

        embed = Embed(
            title=title,
            description=message,
            color=Color(int(colorcode, 0)),
            timestamp=datetime.utcnow(),
        )

        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)

        if len(ctx.message.attachments) == 1:
            try:
                imgur = Imgur("0f032be3851849a")
                image_url = ctx.message.attachments[0].url

                uploaded_image = imgur.upload_image(url=image_url, title="Modmail")
                embed.set_image(url=uploaded_image.link)
            except BaseException:
                pass
        elif len(ctx.message.attachments) > 1:
            await ctx.message.delete()

            embed = Embed(
                title="Embedder",
                url="https://github.com/Ergastolator1/fhmail-plugins/blob/master/embedder",
                description="Puoi solo usare un immagine per embed.",
                color=self.bot.main_color,
            )

            error: Message = await ctx.send(embed=embed)
            return await error.delete(5000)

        await ctx.send(embed=embed)
        await ctx.message.delete()


def setup(bot: Bot) -> None:
    """Caricamento bot cog."""
    bot.add_cog(Embedder(bot))
