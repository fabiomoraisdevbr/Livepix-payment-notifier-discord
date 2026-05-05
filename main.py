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
        user_name = value.get("user_name")
        message_content = value.get("message")

        # Converter centavos para reais
        if amount:
            reais = amount / 100
            formatted_amount = f"R$ {reais:.2f}"
        else:
            formatted_amount = "Valor não disponível"

        if amount and currency and user_name and message_content:
            message = (
                f"<@{user_id}> "
                f"você recebeu um novo pagamento!\n "
                f"\n"
                f"🥸   •**usuário:** {user_name} \n\n"
                f"💸   •**valor:** {formatted_amount} {currency} \n\n"
                f"💬   •**Mensagem:** {message_content}\n"
            )
        else:
            message = f"<@{user_id}> pagamento recebido (dados incompletos) ⚠️"

    await channel.send(message)

    if payment_key:
        cache.delete_cache(payment_key)

def trigger_from_http():
    future = asyncio.run_coroutine_threadsafe(send_message(), bot.loop)
    future.result()  # opcional (espera terminar)




webserver.keep_alive(trigger_from_http)
bot.run(token)



