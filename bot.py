

import disnake
from disnake.ext import commands

bot = commands.Bot(command_prefix=".", help_command=None, intents=disnake.Intents.all())

CENSORED_WORDS = ["hack", "fook"]


@bot.event
async def on_ready():
	print(f"Bot {bot.user} is ready to work!")


@bot.event
async def on_member_join(member):
	channel = bot.get_channel(1113908061346734232)

	role = disnake.utils.get(member.guild.roles, id=1115006547714642000)

	await member.add_roles( role )


@bot.event
async def on_message(message):
	await bot.process_commands(message)

	for content in message.content.split(" "):
		for censored_word in CENSORED_WORDS:
			if content.lower() == censored_word:
				await message.delete()
				await message.channel.send(f"{message.author.mention} можно покультурнее?")



@bot.event
async def on_command_error(ctx, error):
	print (error)

	if isinstance(error, commands.MissingPermissions):
		await ctx.send(f"{ctx.author.mention}, у вас недостаточно прав для выполнения данной команды!")
	elif isinstance(error, commands.UserInputError):
		await ctx.send(embed=disnake.Embed(
			description=f"Правильное использование команды: `{ctx.prefix}{ctx.command.name}` ({ctx.command.brief})\nE"
		))


@bot.command()
@commands.has_permissions(kick_members=True, administrator=True)
async def kick(ctx, member: disnake.Member, *, reason="Нарушение правил"):
	await ctx.send(f"Админ {ctx.author.mention} исключил пользователя {member.mention}", delete_after=2)
	await member.kick(reason=reason)
	await ctx.message.delete()


@bot.command()
@commands.has_permissions(ban_members=True, administrator=True)
async def ban(ctx, member: disnake.Member, *, reason="Нарушение правил"):
		await ctx.send(f"Админ {ctx.author.mention} забанил пользователя {member.mention}", delete_after=2)
		await member.ban(reason=reason)
		await ctx.message.delete()


@bot.command()
@commands.has_permissions(administrator=True)
async def mute(ctx, member: disnake.Member, *, reason="Нарушение правил"):
		await ctx.send(f"Админ {ctx.author.mention} Замутил пользователя {member.mention}")
		role = disnake.utils.get(member.guild.roles, id=1116249784232202260)
		await ctx.message.delete()


@bot.command( pass_context = True )

async def clear( ctx, amount = 100 ):
	await ctx.channel.purge( limit = amount )


bot.run("MTExNjIyOTEwODA3MDg5NTcwNw.GVami5.Cbq63jRQwOscqywqqwW8pUrdO6xPP1UXk-ldwg")
