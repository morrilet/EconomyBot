import config
import discord

client = discord.Client()

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$buy'):
        await message.channel.send(f'Okeydoke, mister {message.author}')

client.run(config.DISCORD_KEY)