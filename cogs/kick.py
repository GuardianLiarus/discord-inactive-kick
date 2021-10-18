import discord
from discord.ext import commands, tasks
import random
from discord.ext.commands import has_permissions
import traceback
import datetime
import asyncio

# async def generate_message(ctx, days):
#
#     activeMember = []
#     oldestDate = datetime.datetime.now() - datetime.timedelta(int(days))
#
#     for member in ctx.guild.members:
#         print(member)
#         for channel in ctx.guild.text_channels:
#             fetchMessage = await channel.history().find(lambda m: m.author.id == member.id)
#             print(fetchMessage)
#             if fetchMessage is None:
#                 continue
#
#             if fetchMessage.created_at.timestamp() > oldestDate.timestamp():
#                 activeMember.append(member.id)
#                 print(member.id)
#                 break
#
#     print(len(activeMember))



async def generate_stats(ctx, days):
    all_members = set(m.id for m in ctx.guild.members)
    active_members = set()

    # Iterate over all text channels within the guild (that the bot can see)
    for channel in ctx.guild.text_channels:
        # Go back in time

        i = 0
        async for message in channel.history(limit=40000, after=datetime.datetime.now() - datetime.timedelta(int(days))):
            i += 1
            active_members.add(message.author.id)
        print(i)

    inactive_members = all_members.difference(active_members)
    banned_members = active_members.difference(all_members)

    all_mem = len(all_members)
    act_mem = len(active_members)
    ina_mem = len(inactive_members)
    ban_mem = len(banned_members)
    string = f'**Here are the following statistics for the past {days} day(s):**\n' \
             f'```ALL: {all_mem}\nACTIVE: {act_mem}\nINACTIVE: {ina_mem}\nACTIVE BUT BANNED: {ban_mem}\n```'
    return inactive_members, string

class Kick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def kick(self, ctx, days=None):

        msg = await ctx.send(
            f"<a:loading:863890402855223317> "
            f"**Kicking inactive members that has not messaged for the last **{days}** days from the server..** "
            f"<a:loading:863890402855223317> ")
        inactive_members, string = await generate_stats(ctx, days)
        for member in inactive_members:
            member_object = ctx.guild.get_member(member)
            if member_object:
                try:
                    await member_object.kick()
                    await asyncio.sleep(2)
                except:
                    continue

        await msg.edit(content=f"Successfully kicked **{len(inactive_members)}** from the server.")

    @commands.command()
    async def stat(self, ctx, days=None):

        msg = await ctx.send(
            f"<a:loading:863890402855223317> "
            f"**Generating stats..** "
            f"<a:loading:863890402855223317> ")

        async with ctx.typing():
            if (not days):
                await ctx.send('You need to specify the amount of days.')
            else:
                inactive_members, string = await generate_stats(ctx, days)

                for member in inactive_members:
                    user = self.bot.get_user(member)
                await msg.delete()
                await ctx.send(string)




def setup(bot):
    bot.add_cog(Kick(bot))
