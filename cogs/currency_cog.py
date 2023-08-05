import discord
from discord.ext import commands
import db_logic as db
import random


class currency_cog(commands.Cog):
    def __init__(self, bot) -> None:
        pass

    @commands.command(name="balance")
    async def balance(self, ctx):
        balance = db.get_balance(db.connect_db(), ctx.author.id, ctx.guild.id)
        embed = discord.Embed(colour=discord.Colour.green())
        embed.set_author(name=f"{ctx.author.name} balance: {balance} 🍰")
        await ctx.send(embed=embed)

    @commands.command(name="daily")
    async def daily(self, ctx):
        session = db.connect_db()

        res = db.update_daily_time(session, ctx.author.id, ctx.guild.id)
        if res[0]:
            new_balance = db.update_balance(session, ctx.author.id, ctx.guild.id, 1000)
            await ctx.send(
                f"{ctx.author.mention}\nDaily reward received! You've got {new_balance}🍰"
            )
        else:
            await ctx.send(f"{ctx.author.mention}\nYou need to wait {res[1]}")

    @commands.command(name="steal")
    async def steal(self, ctx, member):
        if not member:
            await ctx.send(f"You need to mention someone")
        else:
            member = await commands.MemberConverter().convert(ctx, member)
            session = db.connect_db()
            balance = db.get_balance(session, member.id, ctx.guild.id)
            if random.random() > 0.5:
                if not balance:
                    await ctx.send(f"This user is broke")
                    return
                balance = random.randint(1, balance // 2)
                db.update_balance(session, member.id, ctx.guild.id, -balance)
                db.update_balance(session, ctx.author.id, ctx.guild.id, +balance)
                await ctx.send(
                    f"{ctx.author.mention}\nYou seccessfully stole {balance} 🍰 from {member.mention}"
                )
            else:
                if not balance:
                    await ctx.send(
                        f"This user is broke AND you've got caught, it's certified bruh moment"
                    )
                else:
                    await ctx.send(f"You've got caught, you'll fined with 250 🍰")
                db.update_balance(session, ctx.author.id, ctx.guild.id, -250)


async def setup(bot):
    await bot.add_cog(currency_cog(bot))
