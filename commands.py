import db

async def buy(message):
    '''
    Create a buy order. Syntax is as follows: $buy {item} {quantity}@{price}
    '''
    values = _parse_options(message)

    try:
        user_id = message.author.id
        item = values[0]
        quantity = values[1].split('@')[0]
        price = _dollars_to_cents(float(values[1].split('@')[1]))
        total_price = int(quantity) * float(price)

        user = await db.get_user_by_id(user_id)
        if user['money'] >= total_price:
            user['money'] -= total_price
            await db.update_user(user)

            id = await db.create_order(user_id, 'BUY', item, quantity, price)
            await message.channel.send(f'Buy order created!\n[#{id}] BUY {item} {quantity}@{_cents_to_dollars(price)} ({_cents_to_dollars(total_price)})')
        else:
            await message.channel.send(f'You do not have sufficient funds to place this order.')
    except IndexError:
        await message.channel.send(f'Unable to parse buy order - check your syntax!')

async def sell(message):
    '''
    Create a sell order. Syntax is as follows: $sell {item} {quantity}@{price}
    '''
    values = _parse_options(message)

    try:
        user_id = message.author.id
        item = values[0]
        quantity = values[1].split('@')[0]
        price = _dollars_to_cents(float(values[1].split('@')[1]))

        id = await db.create_order(user_id, 'SELL', item, quantity, price)
        await message.channel.send(f'Sell order created!\n[#{id}] SELL {item} {quantity}@{_cents_to_dollars(price)} ({_cents_to_dollars(int(quantity) * float(price))})')
    except IndexError:
        await message.channel.send(f'Unable to parse sell order - check your syntax!')

async def offer(message):
    '''
    Commits to a buy or sell order, creating an interaction. Syntax is as follows: $offer {order_id} {quantity}
    '''
    values = _parse_options(message)

    try:
        user_id = message.author.id
        order_id = values[0]
        quantity = int(values[1])

        order_obj = await db.get_order_by_id(order_id)
        if not order_obj or order_obj['status'] != 'OPEN':
            return await message.channel.send(f'Order #{order_id} not found.')
        
        # We don't enforce whether or not the user can actually afford to buy from sell orders here,
        # because that could change by the time this is approved. Instead we'll handle that in approve.
        # Same logic applies to checking quantity remaining. Best to do that at the time of finalization.
        id = await db.create_interaction(user_id, order_id, quantity)
        order_user = await db.get_user_by_id(order_obj['user'])

        if order_obj['type'] == 'SELL':
            output = f"[#{id}] {message.author.name} has offered to buy {order_obj['item']} x{quantity}@{_cents_to_dollars(order_obj['price'])} from {order_user['name']}."
        if order_obj['type'] == 'BUY':
            output = f"[#{id}] {message.author.name} has offered to sell {order_obj['item']} x{quantity}@{_cents_to_dollars(order_obj['price'])} to {order_user['name']}."
        await message.channel.send(output)
    except IndexError:
        await message.channel.send('Unable to offer - check your syntax!')

async def approve(message):
    pass

async def cancel(message):
    '''
    Cancel an order. Only available to the person the order belongs to. Syntax is as follows: $cancel {order_id}
    '''
    values = _parse_options(message)

    # TODO: return some money to the user if it's a buy order.

    try:
        user_id = message.author.id
        order_id = values[0]
        await db.cancel_order(user_id, order_id)

        await message.channel.send(f'Order #{order_id} has been cancelled.')
    except IndexError:
        await message.channel.send(f'Unable to parse cancellation - check your syntax!')
    except ValueError:
        await message.channel.send(f'Order #{order_id} not found.')
    except PermissionError:
        await message.channel.send(f'Order #{order_id} does not belong to you.')

async def list(message):
    await message.channel.send('LIST')

async def give(message):
    '''
    Give money to a user from your own stash. Syntax is as follows: $give {user_name} {amount}
    '''
    values = _parse_options(message)
    
    try:
        source_id = message.author.id
        target_name = values[0]
        amount = _dollars_to_cents(float(values[1]))

        source_user = await db.get_user_by_id(source_id)
        target_user = await db.get_user_by_name(target_name)

        if amount <= 0:
            return await message.channel.send('Cannot give an amount less than or equal to zero.')

        if not target_user:
            return await message.channel.send(f'Cannot find user with name {target_name} - be sure to use the full syntax, eg: user#1234.)')

        if source_user['money'] - amount < 0:
            return await message.channel.send('You do not have enough money to complete this transaction.')

        source_user['money'] -= amount
        target_user['money'] += amount

        # This is not atomic, but it's fine for the prototype.
        await(db.update_user(source_user))
        await(db.update_user(target_user))

        await message.channel.send(f"You've given {_cents_to_dollars(amount)} to {target_name}.")
    except IndexError:
        await message.channel.send(f'Unable to parse give - check your syntax!')

async def balance(message):
    '''
    Returns the balance of the current user. Syntax is as follows: $balance
    '''
    values = _parse_options(message)

    if values:
        return await message.channel.send(f'Unable to check balance - check your syntax!')
    
    user_obj = await db.get_user_by_id(message.author.id)
    await message.channel.send(f'Hello {message.author.name}, you have a balance of {_cents_to_dollars(user_obj["money"])}')

def _parse_options(message):
    tokens = message.content.split(' ')
    tokens.pop(0)  # Remove the first element - it relates to the command ($buy, $sell, etc.)
    return tokens

# Using cents internally because 2.3 * 100 == 229.9997 for some reason. 
# Rounding cents is less likely to cause an issue than rounding dollars.
def _cents_to_dollars(value):
    return value / 100

def _dollars_to_cents(value):
    return round(value * 100)