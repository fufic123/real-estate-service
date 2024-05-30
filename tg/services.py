import asyncio
from telegram import Bot, InputMediaPhoto
from .models import BotAdmin
from asgiref.sync import sync_to_async

@sync_to_async
def get_bot_token():
    token = BotAdmin.objects.get(id=1).token
    return token

async def send_promotion(channel, message, *images):
    token = await get_bot_token()
    bot = Bot(token=token)
    
    media = [InputMediaPhoto(open(image_path, 'rb')) for image_path in images]
    await bot.send_media_group(chat_id=channel, media=media, caption=message)
    
    return 'Success'

def send_promotion_thread(channel, message, *images):
    asyncio.run(send_promotion(channel, message, *images))

def get_username(link):
    username = link.split("t.me/")[-1]
    return f"@{username}"
