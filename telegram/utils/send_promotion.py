# import asyncio
# from asgiref.sync import sync_to_async
# from telegram import Bot, InputMediaPhoto
# import telegram

# from estate.models import Estate
# from .models import BotAdmin

# @sync_to_async
# def get_tgbot_token():
#     return BotAdmin.objects.get(pk=1).token

# @sync_to_async
# def get_tgbot_chat_id(user):
#     return user.telegram_chat_id

# async def send_telegram_message_async(message, images, user):
#     token = await get_tgbot_token()
#     chat_id = await get_tgbot_chat_id(user)
#     bot = Bot(token=token)

#     if images:
#         media = [InputMediaPhoto(media=image.image) for image in images[:9]]
#         await bot.send_media_group(chat_id=chat_id, media=media)
    
#     await bot.send_message(chat_id=chat_id, text=message, parse_mode=telegram.constants.ParseMode.HTML)

# def send_telegram_message(message, images, user):
#     asyncio.run(send_telegram_message_async(message, images, user))
