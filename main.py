import discord
from discord.ext import commands

import os
import asyncio
import webserver
from dotenv import load_dotenv
import time
import requests
import cache
import service
import re  

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)
user_id = 1458918001477685374
channel_id = 1501032896218267679




async def send_message():
    channel = bot.get_channel(channel_id)

    if not channel:
        channel = await bot.fetch_channel(channel_id)

    payment_key, payment_details = cache.find_first("payment_details_")

    if payment_details:
        value = payment_details.get("value", {})

        amount = value.get("amount")
        currency = value.get("currency")
        if amount and currency:
            message = (
                f"<@{user_id}> você recebeu um novo pagamento!\n"
                f"{amount} {currency} 💸"
            )
        else:
            message = f"<@{user_id}> pagamento recebido (dados incompletos) ⚠️"
    else:
        message = f"<@{user_id}> Mensagem vinda de HTTP 🚀"

    await channel.send(message)

    if payment_key:
        cache.delete_cache(payment_key)

def trigger_from_http():
    future = asyncio.run_coroutine_threadsafe(send_message(), bot.loop)
    future.result()  # opcional (espera terminar)




webserver.keep_alive(trigger_from_http)
bot.run(token)



