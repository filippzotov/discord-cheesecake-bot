import discord
from token_file import TOKEN
from discord.ext import commands
import asyncio
import db_logic as db
import random

intents = discord.Intents.all()
intents.members = True
intents.messages = True
bot = commands.Bot(command_prefix="c!", intents=intents)
bot.remove_command("help")


@bot.event
async def on_ready():
    await bot.load_extension("cogs.music_cog")
    await bot.load_extension("cogs.help_cog")
    await bot.load_extension("cogs.roulette_cog")
    await bot.load_extension("cogs.blackjack_cog")
    await bot.load_extension("cogs.slots_cog")
    await bot.load_extension("cogs.currency_cog")
    print("The bot has logged in!")  # outputs to local command line


@bot.event
async def on_guild_available(guild):
    await asyncio.sleep(
        2
    )  # Adjust the delay time if needed to ensure members are fetched properly
    # get all members from every server
    server_db = db.server_exists(session, guild.id)
    if not server_db:
        server_db = db.add_server(session, guild.id)
        print(server_db)
        for member in guild.members:
            print(member.name)

            db.add_user(session, member.id, member.name, server_db)


@bot.command()
async def ping(ctx):
    print("ping")
    await ctx.send("Pong!")  # Responds with "Pong!" when the command !ping is used


@bot.command()
async def hello(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author
    await ctx.send(f"Hello, {member.mention}!")


# takes arguments in message and returns random element from arguments
@bot.command()
async def choice(ctx, *, message_text=""):
    input_words = message_text.split()
    if len(input_words) <= 1:
        await ctx.send("not enough arguments")
    else:
        answer = random.choice(input_words)
        await ctx.send(f"{ctx.author.mention}\nThe result is {answer}")


session = db.connect_db()
bot.run(TOKEN)
