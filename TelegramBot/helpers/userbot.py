from TelegramBot import config
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import InputPeerChannel

from TelegramBot.helpers.local_timezone import bangkok_tz
from TelegramBot import client_userbot

async def get_last_100_messages(): 
    await client_userbot.start()
    # Get the channel entity
    channel = await client_userbot.get_entity(int(config.CHAT_ID))

    # Create an InputPeerChannel which is needed for fetching messages
    input_channel = InputPeerChannel(channel.id, channel.access_hash)
    
    # Fetch the last 100 messages
    result = await client_userbot(GetHistoryRequest(
        peer=input_channel,
        limit=100,
        offset_date=None,
        offset_id=0,
        max_id=0,
        min_id=0,
        add_offset=0,
        hash=0
    ))
    
    result_text = []

    for message in result.messages:
        result = []
        if message.message is not None:
            result.append(str(message.date.now(bangkok_tz)))
            user_name = await client_userbot.get_entity(entity=int(message.from_id.user_id))
            if user_name.last_name is not None:
                result.append(str(user_name.first_name) + ' ' + str(user_name.last_name))
            else:
                result.append(user_name.first_name)
            result.append(message.message)

        result_text.append(result)

    return result_text




