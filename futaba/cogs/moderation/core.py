#
# cogs/moderation/core.py
#
# futaba - A Discord Mod bot for the Programming server
# Copyright (c) 2017-2018 Jake Richardson, Ammon Smith, jackylam5
#
# futaba is available free of charge under the terms of the MIT
# License. You are free to redistribute and/or modify it under those
# terms. It is distributed in the hopes that it will be useful, but
# WITHOUT ANY WARRANTY. See the LICENSE file for more details.
#

'''
Collection of moderation commands such as Ban/Kick
'''

import asyncio
import logging

import discord
from discord.ext import commands

from futaba import permissions
from futaba.converters import MemberConv, UserConv
from futaba.enums import Reactions
from futaba.utils import escape_backticks, user_discrim

logger = logging.getLogger(__name__)

__all__ = [
    'Moderation',
]

class Moderation:
    '''
    Staff moderation commands
    '''

    __slots__ = (
        'bot',
        'journal',
    )

    def __init__(self, bot):
        self.bot = bot
        self.journal = bot.get_broadcaster('/moderation')

    @commands.command(name='kick')
    @commands.guild_only()
    @permissions.check_mod()
    async def kick(self, ctx, member: MemberConv, *, reason: str):
        '''
        Kicks the user from the guild with a reason
        If guild has moderation logging enabled, it is logged
        '''

        try:
            embed = discord.Embed(description='Done! User Kicked')
            embed.add_field(name='Reason', value=reason)

            await asyncio.gather(
                ctx.guild.kick(member, reason=f'{reason} - {user_discrim(ctx.author)}'),
                ctx.send(embed=embed),
            )

        except discord.errors.Forbidden:
            await asyncio.gather(
                ctx.send("Can't do that user has higher role than me"),
                Reactions.DENY.add(ctx.message)
            )

    @commands.command(name='ban')
    @commands.guild_only()
    @permissions.check_admin()
    async def ban(self, ctx, member: MemberConv, *, reason: str):
        '''
        Bans the user from the guild with a reason
        If guild has moderation logging enabled, it is logged
        '''

        try:
            embed = discord.Embed(description='Done! User Banned')
            embed.add_field(name='Reason', value=reason)

            mod = user_discrim(ctx.author)
            banned = user_discrim(member)
            clean_reason = escape_backticks(reason)
            content = f'{mod} banned {member.mention} ({banned}) with reason: `{clean_reason}`'

            await asyncio.gather(
                ctx.guild.ban(member, reason=f'{reason} - {mod}'),
                ctx.send(embed=embed),
            )

            self.journal.send('member/ban', ctx.guild, content, icon='ban')

        except discord.errors.Forbidden:
            await asyncio.gather(
                ctx.send("Can't do that user has higher role than me"),
                Reactions.DENY.add(ctx.message)
            )

    @commands.command(name='softban', aliases=['soft', 'sban'])
    @commands.guild_only()
    @permissions.check_admin()
    async def softban(self, ctx, member: MemberConv, *, reason: str):
        '''
        Soft-bans the user from the guild with a reason.
        If guild has moderation logging enabled, it is logged

        Soft-ban is a kick that cleans up the chat
        '''

        try:
            embed = discord.Embed(description='Done! User Soft-banned')
            embed.add_field(name='Reason', value=reason)

            mod = user_discrim(ctx.author)
            banned = user_discrim(member)
            clean_reason = escape_backticks(reason)
            content = f'{mod} soft-banned {member.mention} ({banned}) with reason: `{clean_reason}`'

            # TODO add to tracker and add handler to journal event to prevent ban/softban event
            await asyncio.gather(
                ctx.guild.ban(member, reason=f'{reason} - {mod}', delete_message_days=1),
                ctx.send(embed=embed),
            )

            await ctx.guild.unban(member, reason=f'{reason} - {mod}')

            self.journal.send('member/softban', ctx.guild, content, icon='soft',
                    member=member, reason=reason, cause=ctx.author)

        except discord.errors.Forbidden:
            await asyncio.gather(
                ctx.send("Can't do that user has higher role than me"),
                Reactions.DENY.add(ctx.message)
            )

    @commands.command(name='unban', aliases=['pardon'])
    @commands.guild_only()
    @permissions.check_admin()
    async def unban(self, ctx, member: UserConv, *, reason: str):
        '''
        Unbans the id from the guild with a reason.
        If guild has moderation logging enabled, it is logged
        '''

        try:
            embed = discord.Embed(description='Done! User Unbanned')
            embed.add_field(name='Reason', value=reason)

            # TODO add tracker unban event and move this to journal/impl/moderation.py
            mod = user_discrim(ctx.author)
            unbanned = user_discrim(member)
            clean_reason = escape_backticks(reason)
            content = f'{mod} unbanned {member.mention} ({unbanned}) with reason: `{clean_reason}`'

            await asyncio.gather(
                ctx.guild.unban(member, reason=f'{reason} - {mod}'),
                ctx.send(embed=embed),
            )

            self.journal.send('member/unban', ctx.guild, content, icon='unban', member=member)

        except discord.errors.Forbidden:
            await asyncio.gather(
                ctx.send("Can't do that user has higher role than me"),
                Reactions.DENY.add(ctx.message)
            )
