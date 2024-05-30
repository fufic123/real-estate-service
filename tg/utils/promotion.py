import asyncio
from telethon import TelegramClient
from telegraph import Telegraph
import os
from tg.models import BotAdmin

def create_telegraph(title, message, images):
    telegraph = Telegraph()
    telegraph.create_account(short_name='telegraph_api')
    content = []
    for image in images:
        content.append({'tag': 'img', 'attrs': {'src': image}})
    page = telegraph.create_page(
        title=title,
        content=content
    )
    return page['url']

async def send_promotion(message, channel, telegraph_url):
    try:
        # Define your API credentials
        api_id = os.environ.get("TELEGRAM_API_KEY")
        api_hash = os.environ.get("TELEGRAM_API_HASH")
        bot_token = BotAdmin.objects.get(id=1).token
        
        async with TelegramClient('session_name', api_id, api_hash) as client:
            # Initialize the client with the bot token
            await client.start(bot_token=bot_token)

            # Retrieve the channel entity
            channel_entity = await client.get_entity(channel)

            # Send message with Telegraph link
            await client.send_message(channel_entity, f"{message}\n\n{telegraph_url}", link_preview=True)

    except Exception as e:
        print(f"Error sending telegram message: {e}")

async def run_promotion_thread(message, channel, *images):
    try:
        # Create a Telegraph article
        telegraph_url = create_telegraph("Promotion", message, images)

        # Send message with Telegraph link
        await send_promotion(message, channel, telegraph_url)

    except Exception as e:
        print(f"Error sending telegram message in func: {e}")