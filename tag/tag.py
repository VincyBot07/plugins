import discord
from datetime import datetime
from discord.ext import commands

from core import checks
from core.models import PermissionLevel

green = discord.Color.green()
red = discord.Color.red()
blurple = discord.Color.blurple()
error = red
success = green

class Tag(commands.Cog):
    def __init__(self, bot):
        self.bot: discord.Client = bot
        self.db = bot.plugin_db.get_partition(self)

    @commands.group(invoke_without_command=True)
    @commands.guild_only()
    @checks.has_permissions(PermissionLevel.REGULAR)
    async def tags(self, ctx: commands.Context):
        """
        Crea, Modifica & Gestisci i Tag
        """
        await ctx.send_help(ctx.command)

    @tags.command()
    async def add(self, ctx: commands.Context, name: str, *, content: str):
        """
        Crea un nuovo tag
        """
        if (await self.find_db(name=name)) is not None:
            await ctx.send(embed=discord.Embed(title='Errore', description=f"Un tag con il nome `{name}` esiste già!", color=red).set_footer(text='Prova a creare un tag con un nome diverso!'))
            return
        else:
            ctx.message.content = content
            await self.db.insert_one(
                {
                    "name": name,
                    "content": ctx.message.clean_content,
                    "createdAt": datetime.utcnow(),
                    "updatedAt": datetime.utcnow(),
                    "author": ctx.author.id,
                    "uses": 0,
                }
            )

            await ctx.send(embed=discord.Embed(
                title='Successo',
                description=f"Il tag `{name}` è stato creato con successo!",
                color=green,
            ).set_footer(text=f'Provalo con {ctx.prefix}{name}!')
            return

    @tags.command()
    async def edit(self, ctx: commands.Context, name: str, *, content: str):
        """
        Modifica un tag esistente

        Solo il proprietario del tag o l'utente con il permesso ''Gestire il server'' può utilizzare questo comando
        """
        tag = await self.find_db(name=name)

        if tag is None:
            await ctx.send(embed=discord.Embed(title='Errore', description=f"Non esiste alcun tag con il nome `{name}`", color=red).set_footer(text='Devi crearlo tu!')
            return
        else:
            ctx.message.content = content
            member: discord.Member = ctx.author
            if ctx.author.id == tag["author"] or member.guild_permissions.manage_guild:
                await self.db.find_one_and_update(
                    {"name": name},
                    {"$set": {"content": ctx.message.clean_content, "updatedAt": datetime.utcnow()}},
                )

                await ctx.send(embed=discord.Embed(
                    title='Successo',    
                    description=f"Il tag `{name}` è stato modificato con successo!",
                    color=green,
                )
            else:
                await ctx.send(embed=discord.Embed(title='Errore', description="Non hai il permesso per modificare quel tag", color=error).set_footer(text='Devi essere il proprietario del tag altrimenti devi avere il permesso "Gestire server"!'))

    @tags.command()
    async def delete(self, ctx: commands.Context, name: str):
        """
        Elimina un tag.

       Solo il proprietario del tag o l'utente con autorizzazioni Manage Server può utilizzare questo comando.
        """
        tag = await self.find_db(name=name)
        if tag is None:
            await ctx.send(embed=discord.Embed(title='Errore', description=f"Non è stato trovato alcun tag con il nome `{name}`.", color=error).set_footer(text='Non c\'è bisogno di eliminarlo!'))
        else:
            if (
                ctx.author.id == tag["author"]
                or ctx.author.guild_permissions.manage_guild
            ):
                await self.db.delete_one({"name": name})

                await ctx.send(embed=discord.Embed(
                    title='Successo',
                    description=f"Il tag `{name}` è stato eliminato con successo!",
                    color=green,
                )
            else:
                await ctx.send(embed=discord.Embed(title='Errore', description="Non hai il permesso per eliminare quel tag", color=error).set_footer(text='Devi essere il proprietario altrimenti devi avere il permesso "Gestire server" per eliminarlo!')

    @tags.command()
    async def claim(self, ctx: commands.Context, name: str):
        """
        Richiedi un tag se il proprietario ha lasciato il server
        """
        tag = await self.find_db(name=name)

        if tag is None:
            await ctx.send(embed=discord.Embed(title='Errore', description=f"Il tag `{name}` non è stato trovato.", color=error).set_footer(text='Puoi crearlo tu!'))
        else:
            member = await ctx.guild.get_member(tag["author"])
            if member is not None:
                await ctx.send(embed=discord.Embed(
                    title='Errore',
                    description=f"Il proprietario del tag è ancora nel server `{member.name}#{member.discriminator}`",
                    color=error
                ).set_footer(text='Il proprietario deve uscire dal server')
                return
            else:
                await self.db.find_one_and_update(
                    {"name": name},
                    {"$set": {"author": ctx.author.id, "updatedAt": datetime.utcnow()}},
                )

                await ctx.send(embed=discord.Embed(
                    title='Successo',
                    description=f"Adesso il proprietario del tag `{name}` è `{ctx.author.name}#{ctx.author.discriminator}`",
                    color=error,
                )

    @tags.command()
    async def info(self, ctx: commands.Context, name: str):
        """
        Ricevi informazioni su un tag
        """
        tag = await self.find_db(name=name)

        if tag is None:
            await ctx.send(embed=discord.Embed(title='Errore', description=f"Il tag `{name}` non è stato trovato.", color=error).set_footer(text='Devi prima crearlo!')
        else:
            user: discord.User = await self.bot.fetch_user(tag["author"])
            embed = discord.Embed()
            embed.colour = discord.Colour.green()
            embed.title = f"Informazioni riguardo il tag \"{name}\""
            embed.add_field(
                name="Creato da", value=f"{user.name}#{user.discriminator}"
            )
            embed.add_field(name="Creato il", value=tag["createdAt"])
            embed.add_field(
                name="Ultima modifica il", value=tag["updatedAt"], inline=False
            )
            embed.add_field(name="Utilizzi", value=tag["uses"], inline=False)
            await ctx.send(embed=embed)
            return

    @commands.command()
    async def tag(self, ctx: commands.Context, name: str):
        """
        Usa un tag!
        """
        tag = await self.find_db(name=name)
        if tag is None:
            await ctx.send(embed=discord.Embed(title='Errore', decscription=f":x: | Il tag {name} non è stato trovato.", color=red)
            return
        else:
            await ctx.send(tag["content"])
            await self.db.find_one_and_update(
                {"name": name}, {"$set": {"uses": tag["uses"] + 1}}
            )
            return

    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        if not msg.content.startswith(self.bot.prefix) or msg.author.bot:
            return
        content = msg.content.replace(self.bot.prefix, "")
        names = content.split(" ")

        tag = await self.db.find_one({"name": names[0]})

        if tag is None:
            return
        else:
            await msg.channel.send(tag["content"])
            await self.db.find_one_and_update(
                {"name": names[0]}, {"$set": {"uses": tag["uses"] + 1}}
            )
            return

    async def find_db(self, name: str):
        return await self.db.find_one({"name": name})


def setup(bot):
    bot.add_cog(Tag(bot))
