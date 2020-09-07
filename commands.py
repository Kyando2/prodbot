from discord.ext import commands
import discord
import re
import json

exp = re.compile("(#\d*)")
# reason_exp = re.compile("([Rr]eason\s{0,1}\:\s{0,2})(.+)")
higherups = [331431342438875137, 569151075651682315, 145753622053912576, 253240617310748674, 219116126116773888]


class Commands(commands.Cog):

    def __init__(self, bot):
       self.bot = bot
       self.case_logs = self.bot.get_channel(751877338135789568)
       with open("silenced.json", "r") as f:
            self.silenced = json.loads(f.read())


    @commands.command()
    async def accept(self, ctx, case_number, limit: int=100):
        if ctx.message.author.id in higherups:
            msg = await self.get_case(case_number, limit)
            if msg:
                await msg.add_reaction("✅")
                await ctx.send("Successfully accepted the case")
            else:
                await ctx.send("Case wasn't found")
    
    @commands.command()
    async def silence(self, ctx, user: discord.User):
        if ctx.message.author.id in higherups:
            if user.id in higherups:
                await ctx.send("No, that's not how you play the game.")
                return
            self.silenced.append(user.id)
            with open("silenced.json", "w") as f:
                f.write(json.dumps(self.silenced))
            for channel in ctx.guild.text_channels:
                await channel.set_permissions(user, send_messages=False)
            try:
                await user.send("You have been silenced by his majesty " + ctx.author.name)
            except Exception as e:
                pass
            await ctx.send("Successfully silenced human being")

    @commands.command()
    async def unsilence(self, ctx, user: discord.User):
        if ctx.message.author.id in higherups:
            for channel in ctx.guild.text_channels:
                await channel.set_permissions(user, send_messages=None)
            self.silenced.remove(user.id)
            with open("silenced.json", "w") as f:
                f.write(json.dumps(self.silenced))
            await ctx.send("Successfully unsilenced human being")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id in self.silenced and message.guild.id == 601796845748092938:
            await message.delete()

    @commands.command()
    async def reason(self, ctx, case_number, limit: int=100):
        if ctx.message.author.id in higherups:
            msg = await self.get_case(case_number, limit)
            if msg:
                reason = await self.get_reason(msg.content)
                await ctx.send(reason)
            else:
                await ctx.send("Case wasn't found")
        await ctx.send('something')

    @commands.command()
    async def accept_all(self, ctx, limit: int=100):
        if ctx.message.author.id in higherups:
            async for message in self.case_logs.history(limit=limit):
                await message.add_reaction("✅")

    async def get_case(self, case_number, limit):
        async for message in self.case_logs.history(limit=limit):
            text = message.content
            x = re.findall(
                exp,
                text
                )[0].replace("#", "")
            if str(x) == str(case_number):
                return message

        return None

    async def get_reason(self, text):
        return reason_exp.findall(
            text
            )[0][1]

def setup(bot):
    bot.add_cog(Commands(bot))