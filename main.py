import discord
from discord.ext import commands

import json # Our dictionary handler. Used to load and save .json files.
import random

intents = discord.Intents.all()

bot = commands.Bot(
	command_prefix="-",
	help_command=None, 
	intents=intents)
# Notice how we use commands.Bot instead of discord.Client. Search the docs for more info. 


# Load/Save functions

def get_data(name):
	with open(f"data/{name}.json", "r") as f:
		return json.load(f)

def _save(data):
	with open(f"data/players.json", "w+") as f:
		json.dump(data, f)



# Events

@bot.event
async def on_ready():
	print(f"Logged in as {bot.user.name}")

@bot.event 
async def on_command(ctx):
	players = get_data("players")
	_id = str(ctx.author.id) # The ID must be a string (not an int) when using json.
	
	if _id not in players: # "account making system"
		players[_id] = {
			"iron": 0,
			"gold": 0,
			"diamond": 0
		}
		_save(players)	
		await ctx.author.send("Welcome to **Creeper Bot**! We\'ve added your account to our database.")



# Commands

@bot.command(aliases=["inv"])
async def inventory(ctx, user:discord.User=None): # Allows you to check other user's inventories.
	players = get_data("players")
	if user == None:
		user = ctx.author

	_id = str(user.id)

	# Discord EMBED 
	inv_embed = discord.Embed(
		title = f"{user.name}\'s inventory",
		description = f"**Iron:** {players[_id]['iron']}\n**Gold:** {players[_id]['gold']}\n**Diamonds:** {players[_id]['diamond']}",
		color = 0x00FF00)
	inv_embed.set_footer(text='Nice inventory.')

	await ctx.send(content="", embed=inv_embed)

@bot.command()
@commands.cooldown(1, 20, commands.BucketType.user) # Change "20" to however long you want. (In seconds)
async def mine(ctx):
	players = get_data('players')
	_id = str(ctx.author.id)
	fate = random.randint(1, 4) 

	if fate < 3:
		iron = random.randint(6,21)
		gold = random.randint(0,10)
		diamond = random.randint(0,6)

		players[_id]['iron'] += iron
		players[_id]['gold'] += gold
		players[_id]['diamond'] += diamond
		_save(players)

		await ctx.send(f'Mining results:\n**+{iron}** Iron\n**+{gold}** Gold\n**+{diamond}** Diamond/s')

	else:
		await ctx.send("You got blown away by a <:3413_Minecraft_Creeper_pixel_art:843064548076158996> creeper while <:4441_MCdiamondpickaxe:843060205134807062> mining.")



# Errors

@inventory.error
async def inv_error(ctx, error):
	if isinstance(error, discord.ext.commands.errors.CommandInvokeError):
		await ctx.send('This user does not have an account. Please try again when they\'ve used the bot.')
	else:
		raise error

@mine.error
async def mine_error(ctx, error):
	if isinstance(error, commands.errors.CommandInvokeError):
		await ctx.message.delete()
	elif isinstance(error, commands.CommandOnCooldown):
		cooldown_embed = discord.Embed(
			title = "You're on cooldown!",
			description = "You can use this command again in **{:.0f}s**".format(error.retry_after),
			color = 0x00FF00)
		cooldown_embed.set_footer(
			text = bot.user.name,
			icon_url = bot.user.avatar_url)
		await ctx.send(content="", embed=cooldown_embed)
	else:
		raise error


bot.run("ODI3MDU0NDE4MzE4OTgzMTk5.YGVccw.g1_6jPtGUFlvCCN7UFL5s3W72fM")