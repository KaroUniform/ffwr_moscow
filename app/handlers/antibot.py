import datetime
from aiogram import Router, F, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, BotCommand
from aiogram.types import ChatPermissions

router = Router()
router.message.filter(F.new_chat_members)


@router.message(F.new_chat_members)
async def antibot(message: Message, bot: Bot):
    await message.reply(f'Привет! Для начала пройди проверку на человека. Нажми на креветку! '
                        +'🦐🏖 О, извините, креветка на пенсии. В течение минуты можно писать только текст')
    
    errors = 0
    
    for user in message.new_chat_members:
        until = datetime.datetime.now() + datetime.timedelta(minutes=1)
        try:
            await bot.restrict_chat_member(
                message.chat.id, 
                user.id,
                permissions=ChatPermissions(
                    can_send_messages= True,
                    can_send_audios= False,
                    can_send_documents= False,
                    can_send_photos= False,
                    can_send_videos= False,
                    can_send_video_notes= False,
                    can_send_voice_notes= False,
                    can_send_polls= False,
                    can_send_other_messages= False,
                    can_add_web_page_previews= False,
                    can_change_info= False,
                    can_invite_users= False,
                    can_pin_messages= False,
                    can_manage_topics= False
                ),
                use_independent_chat_permissions=True,
                until_date=until
            )
        except TelegramBadRequest: errors +=1
    if errors > 0: await message.reply(text=f'😢Не имею доступа к этой команде, не хватает прав в чате')
    
    
        

        

        
    
    
