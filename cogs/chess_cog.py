import discord
from discord.ext import commands
import db_logic as db
from games.chess_game import ChessGame
import random


class currency_cog(commands.Cog):
    def __init__(self, bot) -> None:
        self.games = {}

    @commands.command(name="chess")
    async def chess(self, ctx, member):
        if not member:
            await ctx.send(f"You need to mention someone")
        else:
            member = await commands.MemberConverter().convert(ctx, member)
            self.games[ctx.author.id] = ChessGame()
            self.games[member.id] = ctx.author.id

    @commands.command(name="move")
    async def move(self, ctx, piece_move):
        if ctx.author.id not in self.games:
            await ctx.send("You are not playing")
        else:
            game = self.games[ctx.author.id]
            if piece_move in game.display_legal_moves():
                game.make_move(piece_move)
                await ctx.send(game.display_board())
            else:
                await ctx.send("wrong move")


async def setup(bot):
    await bot.add_cog(currency_cog(bot))
