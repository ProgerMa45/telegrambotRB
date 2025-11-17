import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandObject
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

# =============================================
# ПРОСТО ВСТАВЬТЕ СВОЙ ТОКЕН ЗДЕСЬ ↓
# =============================================
BOT_TOKEN = "8476199583:AAGIObszhz_ucZvAxlA25NW9f68d-ItUc4g"  

# ID ваших каналов для подписки
REQUIRED_CHANNELS = ["@Sigma4Script", "@Xleb4ikScript"]

# Ссылки на ваши каналы
CHANNEL_LINKS = {
    "channel1": "https://t.me/Sigma4Script",
    "channel2": "https://t.me/Xleb4ikScript",
    "youtube": "https://youtu.be/edUA1lwRFh8?si=fC4L_dsq39sFNITB",
    "script_channel": "https://t.me/+R7DwT69_eHhmMmEy"
}

# База данных скриптов
SCRIPTS_DB = {
    "fvdlisnvl": "loadstring(game:HttpGet('https://raw.githubusercontent.com/EdgeIY/infiniteyield/master/source'))()",
    "darkhub": "loadstring(game:HttpGet('https://raw.githubusercontent.com/RandomAdamYT/DarkHub/master/Init'))()",
    "owlhub": "loadstring(game:HttpGet('https://raw.githubusercontent.com/CriShoux/OwlHub/master/OwlHub.txt'))()",
    "script1": "loadstring(game:HttpGet('https://example.com/script1.lua'))()",
    "cheat1": "loadstring(game:HttpGet('https://example.com/cheat1.lua'))()",
    "bypass": "loadstring(game:HttpGet('https://example.com/bypass.lua'))()",
}

# =============================================
# ИНИЦИАЛИЗАЦИЯ БОТА
# =============================================

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# =============================================
# КЛАВИАТУРЫ
# =============================================

def get_welcome_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="🎮 Получить скрипты", callback_data="get_scripts")
    keyboard.button(text="📹 YouTube канал", url=CHANNEL_LINKS["youtube"])
    keyboard.button(text="📢 Канал со скриптами", url=CHANNEL_LINKS["script_channel"])
    return keyboard.adjust(1).as_markup()

def get_main_keyboard():
    keyboard = InlineKeyboardBuilder()
    for script_key in SCRIPTS_DB.keys():
        keyboard.button(text=f"🎮 {script_key.upper()}", callback_data=f"script_{script_key}")
    keyboard.button(text="❓ Помощь", callback_data="help")
    keyboard.button(text="🔙 Назад", callback_data="back_to_welcome")
    return keyboard.adjust(2).as_markup()

def get_subscription_keyboard(script_key):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="📢 Подписаться 1", url=CHANNEL_LINKS["channel1"])
    keyboard.button(text="📢 Подписаться 2", url=CHANNEL_LINKS["channel2"])
    keyboard.button(text="✅ Я ПОДПИСАЛСЯ", callback_data=f"check_{script_key}")
    keyboard.button(text="🔙 Назад", callback_data="back_to_menu")
    return keyboard.adjust(1).as_markup()

# =============================================
# ПРОВЕРКА ПОДПИСКИ
# =============================================

async def check_subscription(user_id: int):
    for channel in REQUIRED_CHANNELS:
        try:
            chat_member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
            if chat_member.status == 'left':
                return False
        except Exception as e:
            logging.error(f"Ошибка проверки подписки: {e}")
            return False
    return True

# =============================================
# ОБРАБОТЧИКИ
# =============================================

@dp.message(Command("start"))
async def cmd_start(message: types.Message, command: CommandObject):
    user_id = message.from_user.id
    username = message.from_user.first_name
    
    welcome_text = (
        f"👋 Приветствую, {username}!\n\n"
        "🤖 **Данный бот создан для получения скриптов а также ключей**\n\n"
        "📹 **Чтобы получить ключ перейдите по ссылке:**\n"
        "[Получить ключ](https://youtu.be/edUA1lwRFh8?si=fC4L_dsq39sFNITB)\n\n"
        "🎮 **Получите побольше скриптов на этом канале:**\n"
        "[Наш канал со скриптами](https://t.me/+R7DwT69_eHhmMmEy)\n\n"
        "👇 **Нажмите кнопку ниже чтобы получить скрипты:**"
    )
    
    if command.args:
        script_key = command.args.lower()
        await process_script_direct(message, script_key, user_id)
    else:
        await message.answer(welcome_text, parse_mode="Markdown", reply_markup=get_welcome_keyboard(), disable_web_page_preview=True)

async def process_script_direct(message: types.Message, script_key: str, user_id: int):
    if script_key in SCRIPTS_DB:
        if await check_subscription(user_id):
            script_code = SCRIPTS_DB[script_key]
            success_text = f"🎉 **Скрипт активирован!**\n\n**Ключ:** `{script_key}`\n\n```lua\n{script_code}\n```\n\n💡 Скопируйте код и вставьте в исполнитель Roblox."
            await message.answer(success_text, parse_mode="Markdown")
        else:
            warning_text = f"🔒 **Доступ к скрипту `{script_key}` закрыт**\n\n⚠️ **Для получения скрипта необходимо подписаться на наши каналы:**\n\n1. 📢 **Becon Script**\n2. 📢 **Second Channel**\n\n▶️ **Подпишитесь на оба канала и нажмите кнопку «✅ Я ПОДПИСАЛСЯ»**"
            await message.answer(warning_text, parse_mode="Markdown", reply_markup=get_subscription_keyboard(script_key))
    else:
        await message.answer("❌ **Скрипт не найден!**\n\nИспользуйте меню ниже:", parse_mode="Markdown", reply_markup=get_main_keyboard())

@dp.callback_query(F.data == "get_scripts")
async def show_scripts_menu(callback: types.CallbackQuery):
    menu_text = "🎮 **Выберите скрипт из списка ниже:**\n\n⚠️ **Для доступа необходимо подписаться на наши каналы**"
    await callback.message.edit_text(menu_text, parse_mode="Markdown", reply_markup=get_main_keyboard())
    await callback.answer()

@dp.callback_query(F.data == "back_to_welcome")
async def back_to_welcome(callback: types.CallbackQuery):
    welcome_text = "👋 **С возвращением!**\n\n🤖 **Данный бот создан для получения скриптов а также ключей**\n\n👇 **Нажмите кнопку ниже чтобы получить скрипты:**"
    await callback.message.edit_text(welcome_text, parse_mode="Markdown", reply_markup=get_welcome_keyboard(), disable_web_page_preview=True)
    await callback.answer()

@dp.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: types.CallbackQuery):
    menu_text = "🎮 **Выберите скрипт из списка ниже:**\n\n⚠️ **Для доступа необходимо подписаться на наши каналы**"
    await callback.message.edit_text(menu_text, parse_mode="Markdown", reply_markup=get_main_keyboard())
    await callback.answer()

@dp.callback_query(F.data == "help")
async def show_help(callback: types.CallbackQuery):
    help_text = "❓ **Помощь:**\n\n1. Выберите скрипт\n2. Подпишитесь на каналы\n3. Нажмите «✅ Я ПОДПИСАЛСЯ»\n4. Получите код"
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="🔙 Назад в меню", callback_data="back_to_menu")
    await callback.message.edit_text(help_text, parse_mode="Markdown", reply_markup=keyboard.as_markup())
    await callback.answer()

@dp.callback_query(F.data.startswith("script_"))
async def process_script_request(callback: types.CallbackQuery):
    script_key = callback.data.replace("script_", "")
    user_id = callback.from_user.id
    
    if await check_subscription(user_id):
        script_code = SCRIPTS_DB.get(script_key, "Скрипт временно недоступен.")
        success_text = f"🎉 **Скрипт: {script_key.upper()}**\n\n```lua\n{script_code}\n```\n\n💡 Скопируйте код и вставьте в исполнитель Roblox."
        await callback.message.edit_text(success_text, parse_mode="Markdown")
    else:
        warning_text = f"🔒 **Доступ к скрипту `{script_key}` закрыт**\n\n⚠️ **Подпишитесь на каналы и нажмите «✅ Я ПОДПИСАЛСЯ»**"
        await callback.message.edit_text(warning_text, parse_mode="Markdown", reply_markup=get_subscription_keyboard(script_key))
    await callback.answer()

@dp.callback_query(F.data.startswith("check_"))
async def process_subscription_check(callback: types.CallbackQuery):
    script_key = callback.data.replace("check_", "")
    user_id = callback.from_user.id
    
    if await check_subscription(user_id):
        script_code = SCRIPTS_DB.get(script_key, "Скрипт временно недоступен.")
        success_text = f"🎉 **Спасибо за подписку! Скрипт: {script_key.upper()}**\n\n```lua\n{script_code}\n```\n\n💡 Скопируйте код и вставьте в исполнитель Roblox."
        await callback.message.edit_text(success_text, parse_mode="Markdown")
    else:
        await callback.answer("❌ Вы все еще не подписаны на все каналы!", show_alert=True)
    await callback.answer()

# =============================================
# ЗАПУСК БОТА
# =============================================

async def main():
    logging.basicConfig(level=logging.INFO)
    logging.info("🚀 Бот запускается...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
