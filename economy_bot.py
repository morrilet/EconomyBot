import config
import discord
import commands
import db

client = discord.Client()

MESSAGE_COMMANDS = {
    '$buy': commands.buy,
    '$sell': commands.sell,
    '$offer': commands.offer,
    '$cancel': commands.cancel,
    '$list': commands.list,
    '$give': commands.give,
    '$balance': commands.balance,
}

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Dispatch the command to the correct function.
    command = message.content.split(' ')[0]
    if MESSAGE_COMMANDS.get(command):
        # If the user isn't currently registered, register them.
        await db.register_user_if_not_found(message.author)
        # Perform the command, passing the message along.
        await MESSAGE_COMMANDS[command](message)
    elif command.startswith('$'):
        await message.channel.send(f'Unrecognized command: `{command}`')

client.run(config.DISCORD_KEY)