import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandObject
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.client.default import DefaultBotProperties

# =============================================
# НАСТРОЙКИ
# =============================================
BOT_TOKEN = "8386985377:AAFccrzILjyJ0JMuz2rt-J17xHOeo6Wy_VA"
ADMIN_USER_ID = 6283824301

# Ссылки на каналы для подписки
CHANNEL_LINKS = {
    "channel1": "https://t.me/passByscirpt",
    "channel2": "https://t.me/bekascript",
}

# Username каналов для проверки подписки
CHANNELS_TO_CHECK = [
    "@passByscirpt",
    "@bekascript",
]

# Скрипты
SCRIPTS = {
    "infiniteyield": 'loadstring(game:HttpGet("https://raw.githubusercontent.com/EdgeIY/infiniteyield/master/source"))()',
    "owlhub": 'loadstring(game:HttpGet("https://raw.githubusercontent.com/CriShoux/OwlHub/master/OwlHub.txt"))()',
    "darkhub": 'loadstring(game:HttpGet("https://raw.githubusercontent.com/RandomAdamYT/DarkHub/master/Init"))()',
    "vortex": 'loadstring(game:HttpGet("https://raw.githubusercontent.com/VortexHubScript/VortexHub/main/init"))()',
    "fluxus": 'loadstring(game:HttpGet("https://raw.githubusercontent.com/FluxusHub/Fluxus/main/Loader"))()',
    "electron": 'loadstring(game:HttpGet("https://raw.githubusercontent.com/ElectronTeam/Electron/main/Electron"))()',
    "hydroxide": 'loadstring(game:HttpGet("https://raw.githubusercontent.com/Upbolt/Hydroxide/master/init.lua"))()',
    "scriptware": 'loadstring(game:HttpGet("https://raw.githubusercontent.com/ScriptWare/ScriptWare/main/loader.lua"))()',
}

# =============================================
# Инициализация бота
# =============================================
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

# =============================================
# ПРОВЕРКА ПОДПИСКИ НА КАНАЛЫ
# =============================================
async def check_subscription(user_id: int) -> bool:
    """
    Проверяет, подписан ли пользователь на все каналы
    """
    for channel_username in CHANNELS_TO_CHECK:
        try:
            chat_member = await bot.get_chat_member(chat_id=channel_username, user_id=user_id)
            
            if chat_member.status not in ["member", "administrator", "creator"]:
                return False
                
        except Exception as e:
            print(f"Ошибка проверки канала {channel_username}: {e}")
            return False
    
    return True

# Клавиатура для подписки
def sub_kb(script_key: str):
    k = InlineKeyboardBuilder()
    k.button(text="📢 Подписаться на каналы", callback_data=f"check_{script_key}")
    return k.as_markup()

# Клавиатура со ссылкой на все скрипты
def all_scripts_kb():
    k = InlineKeyboardBuilder()
    k.button(text="📜 Все скрипты", url="https://t.me/bekascript")  # ← Замени на ссылку на канал со скриптами
    return k.as_markup()

# =============================================
# ОБРАБОТЧИКИ
# =============================================
@dp.message(Command("start"))
async def cmd_start(message: types.Message, command: CommandObject):
    user_id = message.from_user.id

    # Прямая ссылка: t.me/bot?start=script_name
    if command.args and command.args.lower() in SCRIPTS:
        script_key = command.args.lower()
        
        # ПРОВЕРЯЕМ ПОДПИСКУ НА КАНАЛЫ
        if await check_subscription(user_id):
            # Выдаем скрипт с кнопкой "Все скрипты"
            code = SCRIPTS.get(script_key, "Скрипт временно недоступен")
            text = f"<b>🎉 Скрипт: {script_key.upper()}</b>\n\n<code>{code}</code>\n\n💡 Вставь в эксплойт и наслаждайся!"
            await message.answer(text, reply_markup=all_scripts_kb())
        else:
            await message.answer(
                f"<b>🔒 Для получения скрипта нужно подписаться на наши каналы</b>\n\n"
                "📢 <b>Каналы для подписки:</b>\n"
                "• PassBy Script\n"
                "• Bekascript\n\n"
                "✅ <b>После подписки нажми кнопку ниже</b>",
                reply_markup=sub_kb(script_key)
            )
        return

    # Обычный старт без меню
    bot_user = await bot.get_me()
    await message.answer(
        "<b>👋 Привет!</b>\n\n"
        "🎮 Тут самые мощные скрипты для Roblox\n\n"
        "🔗 <b>Используй прямые ссылки для получения скриптов:</b>\n"
        f"• t.me/{bot_user.username}?start=infiniteyield\n"
        f"• t.me/{bot_user.username}?start=owlhub\n"
        f"• t.me/{bot_user.username}?start=darkhub\n"
        f"• t.me/{bot_user.username}?start=vortex\n\n"
        "📢 <b>Подпишись на каналы чтобы получить доступ</b>"
    )

@dp.callback_query(F.data.startswith("check_"))
async def check_sub(cb: types.CallbackQuery):
    script_key = cb.data.split("_", 1)[1]
    
    # ПРОВЕРЯЕМ ПОДПИСКУ при нажатии кнопки
    if await check_subscription(cb.from_user.id):
        # Выдаем скрипт с кнопкой "Все скрипты"
        code = SCRIPTS.get(script_key, "Скрипт временно недоступен")
        text = f"<b>🎉 Скрипт: {script_key.upper()}</b>\n\n<code>{code}</code>\n\n💡 Вставь в эксплойт и наслаждайся!"
        await cb.message.edit_text(text, reply_markup=all_scripts_kb())
    else:
        await cb.answer("❌ Вы не подписаны на все каналы! Подпишитесь и нажмите снова.", show_alert=True)

# =============================================
# Запуск
# =============================================
async def main():
    logging.basicConfig(level=logging.INFO)
    bot_user = await bot.get_me()
    print("✅ Бот запущен!")
    print("🔗 Прямые ссылки на скрипты:")
    for name in SCRIPTS.keys():
        print(f"t.me/{bot_user.username}?start={name}")
    print(f"⚠️ Убедись что бот добавлен как администратор в каналы: {CHANNELS_TO_CHECK}")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
