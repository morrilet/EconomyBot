async def buy(message):
    await message.channel.send('BUY')

async def sell(message):
    await message.channel.send('SELL')

async def commit(message):
    await message.channel.send('COMMIT')

async def cancel(message):
    await message.channel.send('CANCEL')

async def list(message):
    await message.channel.send('LIST')

async def give(message):
    await message.channel.send('GIVE')