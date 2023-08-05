import discord
from discord.ext import commands
from games.slots import SlotMachine
import db_logic as db


class slots_cog(commands.Cog):
    def __init__(self, bot) -> None:
        pass

    # slot game
    @commands.command(name="slots")
    async def slots(self, ctx):
        balance = db.get_balance(db.connect_db(), ctx.author.id, ctx.guild.id)
        if balance - 100 < 0:
            await ctx.send(f"{ctx.author.mention}\nYou are broke🍰")
        else:
            game = SlotMachine()
            result = game.roll_machine()
            slot_image = ""
            reward = result[0]
            for line in result[1]:
                slot_image += f"|{line[0]}|{line[1]}|{line[2]}|\n"
            if reward == 1:
                await ctx.send(
                    f"{ctx.author.mention}\nYou've used 100 🍰 to spin the slots...\n"
                    + slot_image
                    + f"You've lost 100 🍰\n"
                )
                reward -= 101
            else:
                await ctx.send(
                    f"{ctx.author.mention}\nYou've used 100 🍰 to spin the slots...\n"
                    + slot_image
                    + f"You've won {result[0]} 🍰\n"
                )
            db.update_balance(db.connect_db(), ctx.author.id, ctx.guild.id, reward)


async def setup(bot):
    await bot.add_cog(slots_cog(bot))
