from telethon import TelegramClient
from telethon.tl.types import InputPeerChannel, InputMediaUploadedPhoto
from telethon.tl.functions.messages import SendMediaRequest
import os
from telegram.models import BotAdmin
import asyncio

def send_promotion(message, channel, *images):
    try:
        # Define your API credentials
        api_id = os.environ.get("TELEGRAM_API_KEY")
        api_hash = os.environ.get("TELEGRAM_API_HASH")
        bot_token = BotAdmin.objects.get(id=1).token
        
        async def send_telegram_message():
            async with TelegramClient('session_name', api_id, api_hash) as client:
                # Initialize the client with the bot token
                await client.start(bot_token=bot_token)

                # Retrieve the channel entity
                channel_entity = await client.get_entity(channel)

                # Send images
                for image_path in images:
                    if not os.path.isfile(image_path):
                        print(f"File {image_path} does not exist")
                        continue

                    file = await client.upload_file(image_path)
                    media = InputMediaUploadedPhoto(file)
                    await client(SendMediaRequest(
                        peer=channel_entity,
                        media=media,
                        message=message
                    ))

                # Send message
                await client.send_message(channel_entity, message)

        # Run the coroutine using asyncio's event loop
        asyncio.run(send_telegram_message())

    except Exception as e:
        print(f"Error sending telegram message: {e}")
