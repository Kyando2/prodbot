import discord 
from discord.ext.commands import Bot
from secret import token

client = Bot(command_prefix="!!", case_insensitive=True)

initial_extensions = ['commands']


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    
    for extension in initial_extensions:
        client.load_extension(extension)

@client.event
async def on_command_error(ctx, error):
    discord_error = discord.ext.commands.errors
    isinstance_dict = {
        discord_error.MissingPermissions: "Missing permissions to perform that action!",
        discord_error.CommandInvokeError: "There was an error executing that command!",
        discord_error.BadArgument: "One or more arguments are invalid",
        discord_error.MissingRequiredArgument: "Missing required argument"
    }
    for key in isinstance_dict.keys():
        if isinstance(error, key):
            await ctx.send(isinstance_dict[key] + "\n" + str(error))
            # raise error

client.run(token)