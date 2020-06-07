import asyncio
import emoji
import re
import typing

import discord
from discord.ext import commands

from core import checks
from core.models import PermissionLevel

class UnicodeEmoji(commands.Converter):
    async def convert(self, ctx, argument):
        if argument in emoji.UNICODE_EMOJI:
            return discord.PartialEmoji(name=argument, animated=False)
        raise commands.BadArgument('Unknown emoji')

Emoji = typing.Union[discord.PartialEmoji, discord.Emoji, UnicodeEmoji]

class RuoliReazione(commands.Cog):
    """Assegna ruoli ai tuoi membri con reazioni"""

    def __init__(self, bot):
        self.bot = bot
        self.db = bot.plugin_db.get_partition(self)
        
    @commands.group(name="reactionrole", aliases=["rr"], invoke_without_command=True)
    @checks.has_permissions(PermissionLevel.ADMINISTRATOR)
    async def reactionrole(self, ctx: commands.Context):
        """Assegna ruoli ai tuoi membri con reazioni"""
        await ctx.send_help(ctx.command)
        
    @reactionrole.command(name="add", aliases=["make"])
    @checks.has_permissions(PermissionLevel.ADMINISTRATOR)
    async def rr_add(self, ctx, message: str, role: discord.Role, emoji: Emoji,
                     ignored_roles: commands.Greedy[discord.Role] = None):
        """
        Imposta il ruolo a reazione.
        - Nota/e:
        Puoi usare l'emoji solo una volta, non puoi usare l'emoji multiple volte.
        """
        emote = emoji.name if emoji.id is None else str(emoji.id)
        message_id = int(message.split("/")[-1])
        
        for channel in ctx.guild.text_channels:
            try:
                message = await channel.fetch_message(message_id)
            except (discord.NotFound, discord.HTTPException, discord.Forbidden):
                message = None
                continue
            else:
                break
                
        if not message:
            return await ctx.send("Il messaggio non è stato trovato.")
        
        if ignored_roles:
            blacklist = [role.id for role in ignored_roles]
        else:
            blacklist = []
            
        await self.db.find_one_and_update(
            {"_id": "config"}, {"$set": {emote: {"role": role.id, "msg_id": message.id, "ignored_roles": blacklist, "state": "unlocked"}}},
            upsert=True)
        
        await message.add_reaction(emoji)
        await ctx.send("Ruolo a reazione impostato con successo!")
        
    @reactionrole.command(name="remove", aliases=["delete"])
    @checks.has_permissions(PermissionLevel.ADMINISTRATOR)
    async def rr_remove(self, ctx, emoji: Emoji):
        """Rimuovi qualcosa dal ruolo a reazione."""
        emote = emoji.name if emoji.id is None else str(emoji.id)
        config = await self.db.find_one({"_id": "config"})
        
        valid, msg = self.valid_emoji(emote, config)
        if not valid:
            return await ctx.send(msg)
            
        await self.db.find_one_and_update({"_id": "config"}, {"$unset": {emote: ""}})
        await ctx.send("Ruolo dal ruolo a reazione rimosso con successo.")
        
    @reactionrole.command(name="lock", aliases=["pause", "stop"])
    @checks.has_permissions(PermissionLevel.ADMINISTRATOR)
    async def rr_lock(self, ctx, emoji: Emoji):
        """
        Blocca un ruolo a reazione per disattivarlo temporaneamente.
         - Esempio/i:
        `{prefix}rr lock 👀`
        """
        emote = emoji.name if emoji.id is None else str(emoji.id)
        config = await self.db.find_one({"_id": "config"})
        
        valid, msg = self.valid_emoji(emote, config)
        if not valid:
            return await ctx.send(msg)
        
        config[emote]["state"] = "locked"
        
        await self.db.find_one_and_update(
        {"_id": "config"}, {"$set": {emote: config[emote]}}, upsert=True)
        await ctx.send("Ruolo a reazione bloccato con successo.")
        
    @reactionrole.command(name="unlock", aliases=["resume"])
    @checks.has_permissions(PermissionLevel.ADMINISTRATOR)
    async def rr_unlock(self, ctx, emoji: Emoji):
        """
        Sblocca un ruolo precedentemente disattivato.
         - Esempio/i:
        `{prefix}rr unlock 👀`
        """
        emote = emoji.name if emoji.id is None else str(emoji.id)
        config = await self.db.find_one({"_id": "config"})
        
        valid, msg = self.valid_emoji(emote, config)
        if not valid:
            return await ctx.send(msg)

        config[emote]["state"] = "unlocked"
        
        await self.db.find_one_and_update(
        {"_id": "config"}, {"$set": {emote: config[emote]}}, upsert=True)
        await ctx.send("Ruolo a reazione sbloccato con successo.")
            

    @reactionrole.group(name="blacklist", aliases=["ignorerole"], invoke_without_command=True)
    @checks.has_permissions(PermissionLevel.ADMINISTRATOR)
    async def blacklist(self, ctx):
        """Ignora alcuni ruoli nel reagire al ruolo a reazione."""
        await ctx.send_help(ctx.command)
        
    @blacklist.command(name="add")
    @checks.has_permissions(PermissionLevel.ADMINISTRATOR)
    async def blacklist_add(self, ctx, emoji: Emoji, roles: commands.Greedy[discord.Role]):
        """Ignora alcuni ruoli nel reagire."""
        emote = emoji.name if emoji.id is None else str(emoji.id)
        config = await self.db.find_one({"_id": "config"})
        valid, msg = self.valid_emoji(emote, config)
        if not valid:
            return await ctx.send(msg)
        
        blacklisted_roles = config[emote]["ignored_roles"] or []
        
        new_blacklist = [role.id for role in roles if role.id not in blacklisted_roles]
        blacklist = blacklisted_roles + new_blacklist
        config[emote]["ignored_roles"] = blacklist
        await self.db.find_one_and_update(
            {"_id": "config"}, {"$set": {emote: config[emote]}}, upsert=True)
        
        ignored_roles = [f"<@&{role}>" for role in blacklist]
        
        embed = discord.Embed(title="Ruoli messi in lista nera con successo.", color=discord.Color.green())
        try:
            embed.add_field(name=f"Ruoli correntemente ignorati per {emoji}", value=" ".join(ignored_roles))
        except HTTPException:
            pass
        await ctx.send(embed=embed)
        
    @blacklist.command(name="remove")
    @checks.has_permissions(PermissionLevel.ADMINISTRATOR)
    async def blacklist_remove(self, ctx, emoji: Emoji, roles: commands.Greedy[discord.Role]):
        """Consenti alcuni ruoli a reagire al ruolo a reazione precedentemente messo in lista nera per loro."""
        emote = emoji.name if emoji.id is None else str(emoji.id)
        config = await self.db.find_one({"_id": "config"})
        valid, msg = self.valid_emoji(emote, config)
        if not valid:
            return await ctx.send(msg)
        
        blacklisted_roles = config[emote]["ignored_roles"] or []
        blacklist = blacklisted_roles.copy()
        
        [blacklist.remove(role.id) for role in roles if role.id in blacklisted_roles]
        config[emote]["ignored_roles"] = blacklist
        
        await self.db.find_one_and_update(
            {"_id": "config"}, {"$set": {emote: config[emote]}}, upsert=True)
        
        ignored_roles = [f"<@&{role}>" for role in blacklist]
        
        embed = discord.Embed(title="Ruoli rimossi con successo.", color=discord.Color.green())
        try:
            embed.add_field(name=f"Ruoli al momento ignorati per {emoji}", value=" ".join(ignored_roles))
        except:
            pass
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if not payload.guild_id:
            return
        
        config = await self.db.find_one({"_id": "config"})
        
        emote = payload.emoji.name if payload.emoji.id is None else str(payload.emoji.id)
        emoji = payload.emoji.name if payload.emoji.id is None else payload.emoji
        
        guild = self.bot.get_guild(payload.guild_id)
        member = discord.utils.get(guild.members, id=payload.user_id)
        
        if member.bot:
            return
        
        try:
            msg_id = config[emote]["msg_id"]
        except (KeyError, TypeError):
            return
        
        if payload.message_id != int(msg_id):
            return
        
        ignored_roles = config[emote].get("ignored_roles")
        if ignored_roles:
            for role_id in ignored_roles:
                role = discord.utils.get(guild.roles, id=role_id)
                if role in member.roles:
                    await self._remove_reaction(payload, emoji, member)
                    return
        
        state = config[emote].get("state", "unlocked")
        if state and state == "locked":
            await self._remove_reaction(payload, emoji, member)
            return
        
        rrole = config[emote]["role"]
        role = discord.utils.get(guild.roles, id=int(rrole))

        if role:
            await member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.guild_id is None:
            return
        
        config = await self.db.find_one({"_id": "config"})
        emote = payload.emoji.name if payload.emoji.id is None else str(payload.emoji.id)
        
        try:
            msg_id = config[emote]["msg_id"]
        except (KeyError, TypeError):
            return
                                                              
        if payload.message_id == int(msg_id):
            guild = self.bot.get_guild(payload.guild_id)
            rrole = config[emote]["role"]
            role = discord.utils.get(guild.roles, id=int(rrole))

            if role:
                member = discord.utils.get(guild.members, id=payload.user_id)
                await member.remove_roles(role)
                
    async def _remove_reaction(self, payload, emoji, member):
        channel = self.bot.get_channel(payload.channel_id)
        msg = await channel.fetch_message(payload.message_id)
        reaction = discord.utils.get(msg.reactions, emoji=emoji)
        await reaction.remove(member)
                                  
    def valid_emoji(self, emoji, config):
        try:
            emoji = config[emoji]
            return True, None
        except (KeyError, TypeError):
            return False, "Non c'è nessun ruolo a reazione impostato con quella emoji!"
                
def setup(bot):
    bot.add_cog(RuoliReazione(bot))
