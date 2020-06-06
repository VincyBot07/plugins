import discord
from discord.ext import commands
from core import checks
from core.models import PermissionLevel

counter = 0
counter = counter + 1

casefile = 'plugins/Vincysuper07/modmail-plugins-2/moderation-master/cases.txt'

trash = "🗑️"
error = "❌"
info = "ℹ️"
check = "✅"
checkmark = check

class Moderazione(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.errorcolor = 0xFF2B2B
        self.blurple = 0x7289DA

    #On channel create set up mute stuff
    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        guild = channel.guild
        role = discord.utils.get(guild.roles, name = "Mutato")
        if role == None:
            role = await guild.create_role(name = "Mutato")
        await channel.set_permissions(role, send_messages = False)

    #Purge command
    @commands.command(aliases = ["clear"])
    @checks.has_permissions(PermissionLevel.MODERATOR)
    async def purge(self, ctx, amount = 10):
        max_purge = 2000
        if amount >= 1 and amount <= max_purge:
            await ctx.channel.purge(limit = amount + 1)
            await ctx.send(f'{trash} | Ho eliminato {amount} messaggi!')
            await ctx.send(embed = embed, delete_after = 5.0)
            modlog = discord.utils.get(ctx.guild.text_channels, name = "vincylog")
            if modlog == None:
                return
            if modlog != None:
                embed = discord.Embed(
                    title = "Messaggi eliminati",
                    description = f"{amount} messaggi sono stati eliminati da {ctx.author.mention} in {ctx.message.channel.mention}",
                    color = self.blurple
                )
                await modlog.send(embed = embed)
        if amount < 1:
            await ctx.send(f'{error} | Non puoi eliminare meno di {amount} messaggi(o)!', delete_after = 5.0)
            await ctx.message.delete()
        if amount > max_purge:
            await ctx.send(f'Non puoi eliminare più di 2000 messaggi!', delete_after = 5.0)
            await ctx.message.delete()

    @purge.error
    async def purge_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'Non hai il permesso per usare questo comando!', delete_after = 5.0)
            await ctx.message.delete()

    #Kick command
    @commands.command()
    @checks.has_permissions(PermissionLevel.MODERATOR)
    async def kick(self, ctx, member : discord.Member = None, *, reason = None):
        """Kicka (espelle) una persona dal server."""
        if member == None:
            await ctx.send(f'{error} | Devi specificare un membro!', delete_after=5.0)
        else:
            if member.id == ctx.message.author.id:
                await ctx.send('{error} | Non puoi kickare te stesso!')
            else:
                if reason == None:
                    with open(casefile,'r') as file:
                       counter = int(file.read())+1
                    with open(casefile,'w') as file:
                       file.write(str(counter))
                    case = open(casefile, 'r').read()
                    await member.kick(reason = f"Moderatore - {ctx.message.author.name}#{ctx.message.author.discriminator}.\nMotivo - Nessun motivo specificato.")
                    await ctx.send(f"{member.name}#{member.discriminator} è stato kickato da {ctx.message.author.mention}, questo è il caso numero {case}.")
                    vincylog = discord.utils.get(ctx.guild.text_channels, name = "vincylog")
                    if vincylog == None:
                        return
                    if vincylog != None:
                        embed = discord.Embed(
                            title = f"Kick",
                            description = f"{member.mention} è stato kickato da {ctx.message.author.mention} in {ctx.message.channel.mention}.",
                            color = self.blurple
                        ).set_footer(text=f'Questo è il caso numero {case}.')
                        await vincylog.send(embed = embed)
                else:
                    with open(casefile,'r') as file:
                        counter = int(file.read())+1
                    with open(casefile,'w') as file:
                        file.write(str(counter))
                    case = open(casefile, 'r').read()
                    await member.kick(reason = f"Moderatore - {ctx.message.author.name}#{ctx.message.author.discriminator}.\nMotivo - {reason}")
                    embed = discord.Embed(
                        title = "Kick",
                        description = f"{member.mention} è stato kickato da {ctx.message.author.mention} per {reason}.",
                        color = self.blurple
                    ).set_footer(text=f'Questo è il caso numero {case}.')
                    await ctx.send(embed = embed)
                    vincylog = discord.utils.get(ctx.guild.text_channels, name = "vincylog")
                    if vincylog == None:
                        return
                    if vincylog != None:
                        embed = discord.Embed(
                            title = "Kick",
                            description = f"{member.name}#{member.discriminator} è stato kickato da {ctx.message.author.mention} in {ctx.message.channel.mention} per {reason}",
                            color = self.blurple
                        ).set_footer(text=f'Questo è il caso numero {case}.')
                        await vincylog.send(embed = embed)

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'{error} | Non hai il permesso per usare quel comando.', delete_after = 5.0)

    #Ban command
    @commands.command()
    @checks.has_permissions(PermissionLevel.MODERATOR)
    async def ban(self, ctx, member : discord.Member = None, *, reason = None):
        if member == None:
            await ctx.send(f'{error} | Devi specificare un utente!')
        else:
            if member.id == ctx.message.author.id:
                await ctx.send(f'{error} | Non puoi bannare te stesso!')
            else:
                if reason == None:
                    with open(casefile,'r') as file:
                       counter = int(file.read())+1
                    with open(casefile,'w') as file:
                       file.write(str(counter))
                    case = open(casefile, 'r').read()
                    await member.ban(reason = f"Moderatore - {ctx.message.author.name}#{ctx.message.author.discriminator}.\nMotivo - Nessun motivo dato.")
                    await ctx.send(f'{check} | {member.name}#{member.discriminator} è stato bannato da {ctx.message.author.mention}, questo è il caso numero {case}.\n\nhttps://imgur.com/V4TVpbC')
                    embed = discord.Embed(
                        title = "Ban",
                        description = f"{member.mention} è stato bannato da {ctx.message.author.mention}.",
                        color = self.blurple
                    ).set_footer(text=f'Questo è il caso numero {case}.')

                    vincylog = discord.utils.get(ctx.guild.text_channels, name = "vincylog")
                    if vincylog == None:
                        return
                    if vincylog != None:
                        embed = discord.Embed(
                            title = "Ban",
                            description = f"{member.name}#{member.discriminator} è stato bannato da {ctx.message.author.mention}.",
                            color = self.blurple
                        ).set_footer(text=f'Questo è il caso numero {case}.')
                        await vincylog.send(embed = embed)
                else:
                    with open(casefile,'r') as file:
                       counter = int(file.read())+1
                    with open(casefile,'w') as file:
                       file.write(str(counter))
                    case = open(casefile, 'r').read()
                    await member.ban(reason = f"Moderatore - {ctx.message.author.name}#{ctx.message.author.discriminator}.\nMotivo - {reason}")
                    await ctx.send(f'{check} | {member.name}#{member.discriminator} è stato bannato da {ctx.message.author.mention} per motivo \"{reason}\", questo è il caso numero {case}.\n\nhttps://imgur.com/V4TVpbC')
                    vincylog = discord.utils.get(ctx.guild.text_channels, name = "vincylog")
                    if vincylog == None:
                        return
                    if vincylog != None:
                        embed = discord.Embed(
                            title = "Ban",
                            description = f"{member.mention} è stato bannato da {ctx.message.author.mention}.",
                            color = self.blurple
                        )
                        embed.set_footer(text=f'Questo è il caso numero {case}.')
                        await vincylog.send(embed = embed)
   
    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'{error} | Non hai il permesso per usare questo comando', delete_after = 5.0)

    #Unban command
    @commands.command()
    @checks.has_permissions(PermissionLevel.MODERATOR)
    async def unban(self, ctx, *, member : discord.User = None):
        if member == None:
            await ctx.send(f'{error} | Devi specificare un utente!', delete_after = 5.0)
        else:
            banned_users = await ctx.guild.bans()
            for ban_entry in banned_users:
                user = ban_entry.user

                if (user.name, user.discriminator) == (member.name, member.discriminator):
				
                    with open(casefile,'r') as file:
                       counter = int(file.read())+1
                    with open(casefile,'w') as file:
                       file.write(str(counter))
                    case = open(casefile, 'r').read()
                    await ctx.guild.unban(user)
                    await ctx.send(f'{check} | {member.name}#{member.discriminator} è stato unbannato da {ctx.message.author.mention}')
                    vincylog = discord.utils.get(ctx.guild.text_channels, name = "vincylog")
                    if vincylog == None:
                        return
                    if vincylog != None:
                        embed = discord.Embed(
                            title = "Unban",
                            description = f"{user.name}#{user.discriminator} è stato unbannato da {ctx.message.author.mention} in {ctx.message.channel.mention}.",
                            color = self.blurple
                        ).set_footer(text=f'Questo è il caso numero {case}.')
                        await vincylog.send(embed = embed)


    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'{error} | Non hai il permesso per usare questo comando', delete_after = 5.0)

    #Mute command
    @commands.command()
    @checks.has_permissions(PermissionLevel.MODERATOR)
    async def mute(self, ctx, member : discord.Member = None, *, reason = None):
        if member == None:
            await ctx.send(f'{error} | Devi specificare un utente!', delete_after = 5.0)
        else:
            if member.id == ctx.message.author.id:
                await ctx.send(f'{error} | Non puoi mutare te stesso!', delete_after = 5.0)
            else:
                if reason == None:
                    with open(casefile,'r') as file:
                        counter = int(file.read())+1
                    with open(casefile,'w') as file:
                    	file.write(str(counter))
                    case = open(casefile, 'r').read()
                    role = discord.utils.get(ctx.guild.roles, name = "Mutato")
                    if role == None:
                        role = await ctx.guild.create_role(name = "Mutato")
                        for channel in ctx.guild.text_channels:
                            await channel.set_permissions(role, send_messages = False)
                    await member.add_roles(role)
                    await ctx.send(f'{check} | {member.name}#{member.discriminator} è stato mutato, questo è il caso numero {case}')
                    vincylog = discord.utils.get(ctx.guild.text_channels, name = "vincylog")
                    if vincylog == None:
                        return
                    if vincylog != None:
                        embed = discord.Embed(
                            title = "Muto",
                            description = f"{member.name}#{member.discriminator} è stato mutato da {ctx.message.author.mention} in {ctx.message.channel.mention}.",
                            color = self.blurple
                        ).set_footer(text=f'Questo è il caso numero {case}.')
                        await vincylog.send(embed = embed)
                else:
                    role = discord.utils.get(ctx.guild.roles, name = "Mutato")
                    if role == None:
                        role = await ctx.guild.create_role(name = "Mutato")
                        for channel in ctx.guild.text_channels:
                            await channel.set_permissions(role, send_messages = False)
                    await member.add_roles(role)
                    embed = discord.Embed(
                        title = "Muto",
                        description = f"{member.name}#{member.discriminator} è stato mutato da {ctx.message.author.mention} per {reason}",
                        color = self.blurple
                    ).set_footer(text=f'Questo è il caso numero {case}.')
                    await ctx.send(embed = embed)
                    vincylog = discord.utils.get(ctx.guild.text_channels, name = "vincylog")
                    if vincylog == None:
                        return
                    if vincylog != None:
                        embed = discord.Embed(
                            title = "Muto",
                            description = f"{member.name}#{member.discriminator} è stato mutato da {ctx.message.author.mention} in {ctx.message.channel.mention} per {reason}",
                            color = self.blurple
                        ).set_footer(text=f'Questo è il caso numero {case}.')
                        await vincylog.send(embed = embed)

    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'{error} | Non hai il permesso per usare quel comando')

    #Unmute command
    @commands.command()
    @checks.has_permissions(PermissionLevel.MODERATOR)
    async def unmute(self, ctx, member : discord.Member = None):
        if member == None:
            await ctx.send(f'{error} | Devi specificare un utente!', delete_after = 5.0)
        else:
            role = discord.utils.get(ctx.guild.roles, name = "Mutato")
            if role in member.roles:
                with open(casefile,'r') as file:
                    counter = int(file.read())+1
                with open(casefile,'w') as file:
                    file.write(str(counter))
                case = open(casefile, 'r').read()
                await member.remove_roles(role)
                await ctx.send(f'{check} | {member.name}#{member.discriminator} è stato smutato')
                vincylog = discord.utils.get(ctx.guild.text_channels, name = "vincylog")
                if vincylog == None:
                    return
                if vincylog != None:
                    embed = discord.Embed(
                        title = "Unmute",
                        description = f"{member.name}#{member.discriminator} è stato smutato da {ctx.message.author.mention} in {ctx.message.channel.mention}.",
                        color = self.blurple
                    ).set_footer(text=f'Questo è il caso numero {case}.')
                    await vincylog.send(embed = embed)
            else:
                await ctx.send(f'{error} | Quella persona non è mutata')

    @unmute.error
    async def unmute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'{error} | Non hai il permesso per usare questo comando')
									
    #Nuke command
    @commands.command()
    @checks.has_permissions(PermissionLevel.MODERATOR)
    async def nuke(self, ctx):
        channel_position = ctx.channel.position
        new_channel = await ctx.channel.clone()
        await new_channel.edit(reason = f"Detonato da {ctx.message.author.name}#{ctx.message.author.discriminator}", position = channel_position)
        await ctx.channel.delete()
        embed = discord.Embed(
            title = "Detonazione",
            description  = "Questo canale è stato detonato!",
            color = self.blurple,
        ).set_image(url = "https://cdn.discordapp.com/attachments/600843048724987925/600843407228928011/tenor.gif")
        await new_channel.send(embed = embed, delete_after = 30.0)
        vincylog = discord.utils.get(ctx.guild.text_channels, name = "vincylog")
        if vincylog == None:
            pass
        if vincylog != None:
            embed = discord.Embed(
                title = "Detonazione",
                description = f"{ctx.message.author.mention} ha detonato {new_channel.mention}",
                color = self.blurple,
            )
            await vincylog.send(embed = embed)

    @nuke.error
    async def nuke_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'{error} | Non hai il permesso per usare quel comando')

def setup(bot):
    bot.add_cog(Moderazione(bot))
