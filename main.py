import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandObject
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

# =============================================
# КОНФИГУРАЦИЯ - НАСТРОЙТЕ ЭТИ ПАРАМЕТРЫ!
# =============================================

# Токен бота из переменных окружения
BOT_TOKEN = os.getenv("8476199583:AAGIObszhz_ucZvAxlA25NW9f68d-ItUc4g")

# ЕСЛИ ТОКЕН НЕ УСТАНОВЛЕН - ВЫВОДИМ ОШИБКУ И ВЫХОДИМ
if not BOT_TOKEN:
    print("❌ ОШИБКА: BOT_TOKEN не установлен!")
    print("📝 Добавьте переменную окружения BOT_TOKEN в Render")
    print("🔧 Инструкция:")
    print("1. Зайдите в панель Render")
    print("2. Ваш сервис → Environment → Environment Variables")
    print("3. Добавьте: Key: BOT_TOKEN, Value: ваш_токен_от_BotFather")
    exit(1)

# ID ваших каналов для подписки (ЗАМЕНИТЕ НА СВОИ!)
REQUIRED_CHANNELS = ["@Sigma4Script", "@Xleb4ikScript"]

# Ссылки на ваши каналы для кнопок "Подписаться" (ЗАМЕНИТЕ НА СВОИ!)
CHANNEL_LINKS = {
    "channel1": "https://t.me/Sigma4Script",
    "channel2": "https://t.me/Xleb4ikScript",
    "youtube": "https://youtu.be/edUA1lwRFh8?si=fC4L_dsq39sFNITB",  # ЗАМЕНИТЕ на вашу ссылку YouTube
    "script_channel": "https://t.me/+R7DwT69_eHhmMmEy"    # ЗАМЕНИТЕ на канал со скриптами
}

# База данных скриптов (ключ: код скрипта)
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
    """Клавиатура для приветственного сообщения"""
    keyboard = InlineKeyboardBuilder()
    
    # Кнопка для получения скриптов
    keyboard.button(
        text="🎮 Получить скрипты", 
        callback_data="get_scripts"
    )
    
    # Кнопка ссылки на YouTube
    keyboard.button(
        text="📹 YouTube канал", 
        url=CHANNEL_LINKS["youtube"]
    )
    
    # Кнопка канала со скриптами
    keyboard.button(
        text="📢 Канал со скриптами", 
        url=CHANNEL_LINKS["script_channel"]
    )
    
    return keyboard.adjust(1).as_markup()

def get_main_keyboard():
    """Главное меню со всеми скриптами"""
    keyboard = InlineKeyboardBuilder()
    
    # Создаем кнопки для каждого скрипта
    for script_key in SCRIPTS_DB.keys():
        keyboard.button(
            text=f"🎮 {script_key.upper()}", 
            callback_data=f"script_{script_key}"
        )
    
    # Кнопка помощи
    keyboard.button(text="❓ Помощь", callback_data="help")
    
    # Кнопка назад в приветствие
    keyboard.button(text="🔙 Назад", callback_data="back_to_welcome")
    
    return keyboard.adjust(2).as_markup()

def get_subscription_keyboard(script_key):
    """Клавиатура для подписки на каналы"""
    keyboard = InlineKeyboardBuilder()
    
    # Кнопки подписки на каналы
    keyboard.button(
        text="📢 Подписаться 1", 
        url=CHANNEL_LINKS["channel1"]
    )
    keyboard.button(
        text="📢 Подписаться 2", 
        url=CHANNEL_LINKS["channel2"]
    )
    
    # Кнопка проверки подписки
    keyboard.button(
        text="✅ Я ПОДПИСАЛСЯ", 
        callback_data=f"check_{script_key}"
    )
    
    # Кнопка назад в меню
    keyboard.button(
        text="🔙 Назад", 
        callback_data="back_to_menu"
    )
    
    return keyboard.adjust(1).as_markup()

# =============================================
# ПРОВЕРКА ПОДПИСКИ
# =============================================

async def check_subscription(user_id: int):
    """
    Проверяет, подписан ли пользователь на все обязательные каналы
    Возвращает True если подписан на все, False если нет
    """
    for channel in REQUIRED_CHANNELS:
        try:
            chat_member = await bot.get_chat_member(
                chat_id=channel, 
                user_id=user_id
            )
            
            if chat_member.status == 'left':
                logging.info(f"Пользователь {user_id} не подписан на {channel}")
                return False
                
        except Exception as e:
            logging.error(f"Ошибка проверки подписки на {channel}: {e}")
            return False
    
    logging.info(f"Пользователь {user_id} подписан на все каналы")
    return True

# =============================================
# ОБРАБОТЧИКИ КОМАНД И СООБЩЕНИЙ
# =============================================

@dp.message(Command("start"))
async def cmd_start(message: types.Message, command: CommandObject):
    """Обработчик команды /start"""
    user_id = message.from_user.id
    username = message.from_user.first_name
    
    # ПРИВЕТСТВЕННОЕ СООБЩЕНИЕ
    welcome_text = (
        f"👋 Приветствую, {username}!\n\n"
        "🤖 **Данный бот создан для получения скриптов а также ключей**\n\n"
        "📹 **Чтобы получить ключ перейдите по ссылке:**\n"
        "[Посмотрите видео туториал](https://youtu.be/edUA1lwRFh8?si=-xoOLb2QEvAlLZnc)\n\n"
        "🎮 **Получите побольше скриптов на этом канале:**\n"
        "[Наш канал со скриптами](https://t.me/+R7DwT69_eHhmMmEy)\n\n"
        "👇 **Нажмите кнопку ниже чтобы получить скрипты:**"
    )
    
    # Проверяем есть ли параметр после start (прямая ссылка на скрипт)
    if command.args:
        script_key = command.args.lower()
        await process_script_direct(message, script_key, user_id)
    else:
        # Показываем приветственное сообщение
        await message.answer(
            welcome_text, 
            parse_mode="Markdown",
            reply_markup=get_welcome_keyboard(),
            disable_web_page_preview=True
        )

@dp.callback_query(F.data == "get_scripts")
async def show_scripts_menu(callback: types.CallbackQuery):
    """Показывает меню со скриптами"""
    menu_text = (
        "🎮 **Выберите скрипт из списка ниже:**\n\n"
        "⚠️ **Для доступа необходимо подписаться на наши каналы**\n\n"
        "🔗 **Также вы можете использовать прямые ссылки:**\n"
        "`t.me/your_bot?start=fvdlisnvl`\n"
        "`t.me/your_bot?start=darkhub`"
    )
    
    await callback.message.edit_text(
        menu_text,
        parse_mode="Markdown",
        reply_markup=get_main_keyboard()
    )
    await callback.answer()

@dp.callback_query(F.data == "back_to_welcome")
async def back_to_welcome(callback: types.CallbackQuery):
    """Возврат в приветственное сообщение"""
    welcome_text = (
        "👋 **С возвращением!**\n\n"
        "🤖 **Данный бот создан для получения скриптов а также ключей**\n\n"
        "📹 **Чтобы получить ключ перейдите по ссылке:**\n"
        "[Наш YouTube канал](https://youtu.be/edUA1lwRFh8?si=-xoOLb2QEvAlLZnc)\n\n"
        "🎮 **Получите побольше скриптов на этом канале:**\n"
        "[Наш канал со скриптами](https://t.me/+R7DwT69_eHhmMmEy)\n\n"
        "👇 **Нажмите кнопку ниже чтобы получить скрипты:**"
    )
    
    await callback.message.edit_text(
        welcome_text,
        parse_mode="Markdown",
        reply_markup=get_welcome_keyboard(),
        disable_web_page_preview=True
    )
    await callback.answer()

async def process_script_direct(message: types.Message, script_key: str, user_id: int):
    """Обработка прямого запроса скрипта через ссылку"""
    
    if script_key in SCRIPTS_DB:
        if await check_subscription(user_id):
            script_code = SCRIPTS_DB[script_key]
            success_text = (
                f"🎉 **Скрипт активирован!**\n\n"
                f"**Ключ:** `{script_key}`\n\n"
                f"```lua\n{script_code}\n```\n\n"
                "💡 Скопируйте код и вставьте в исполнитель Roblox.\n\n"
                f"🔗 **Прямая ссылка:** \n`t.me/{(await bot.get_me()).username}?start={script_key}`"
            )
            await message.answer(success_text, parse_mode="Markdown")
        else:
            warning_text = (
                f"🔒 **Доступ к скрипту `{script_key}` закрыт**\n\n"
                "⚠️ **Для получения скрипта необходимо подписаться на наши каналы:**\n\n"
                "1. 📢 **Becon Script**\n"
                "2. 📢 **Second Channel**\n\n"
                "▶️ **Подпишитесь на оба канала и нажмите кнопку «✅ Я ПОДПИСАЛСЯ»**"
            )
            await message.answer(
                warning_text, 
                parse_mode="Markdown",
                reply_markup=get_subscription_keyboard(script_key)
            )
    else:
        await message.answer(
            "❌ **Скрипт не найден!**\n\n"
            f"Ключ `{script_key}` не существует или устарел.\n\n"
            "📜 Используйте меню ниже чтобы выбрать доступные скрипты:",
            parse_mode="Markdown",
            reply_markup=get_main_keyboard()
        )

@dp.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: types.CallbackQuery):
    """Возврат в главное меню"""
    menu_text = (
        "🎮 **Выберите скрипт из списка ниже:**\n\n"
        "⚠️ **Для доступа необходимо подписаться на наши каналы**"
    )
    await callback.message.edit_text(
        menu_text, 
        parse_mode="Markdown", 
        reply_markup=get_main_keyboard()
    )
    await callback.answer()

@dp.callback_query(F.data == "help")
async def show_help(callback: types.CallbackQuery):
    """Показывает справку"""
    help_text = (
        "❓ **Помощь по использованию бота:**\n\n"
        "📜 **Как получить скрипт:**\n"
        "1. Выберите скрипт из меню\n"
        "2. Подпишитесь на наши каналы\n"
        "3. Нажмите «✅ Я ПОДПИСАЛСЯ»\n"
        "4. Получите код скрипта\n\n"
        "🔗 **Прямые ссылки:**\n"
        "Используйте ссылки вида:\n"
        "`t.me/your_bot?start=ключ`\n\n"
        "📹 **Наш YouTube:**\n"
        "Получайте ключи и обучающие видео\n\n"
        "📢 **Наши каналы:**\n"
        "• Becon Script\n"
        "• Second Channel\n\n"
        "🆘 **Проблемы?**\n"
        "Если бот не работает, проверьте что вы подписались на ВСЕ каналы"
    )
    
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="🔙 Назад в меню", callback_data="back_to_menu")
    
    await callback.message.edit_text(
        help_text,
        parse_mode="Markdown",
        reply_markup=keyboard.as_markup()
    )
    await callback.answer()

@dp.callback_query(F.data.startswith("script_"))
async def process_script_request(callback: types.CallbackQuery):
    """Обработка нажатия на кнопку скрипта в меню"""
    script_key = callback.data.replace("script_", "")
    user_id = callback.from_user.id
    
    if await check_subscription(user_id):
        script_code = SCRIPTS_DB.get(script_key, "Скрипт временно недоступен.")
        success_text = (
            f"🎉 **Скрипт: {script_key.upper()}**\n\n"
            f"```lua\n{script_code}\n```\n\n"
            "💡 Скопируйте код и вставьте в исполнитель Roblox.\n\n"
            f"🔗 **Прямая ссылка:** \n`t.me/{(await bot.get_me()).username}?start={script_key}`"
        )
        await callback.message.edit_text(success_text, parse_mode="Markdown")
    else:
        warning_text = (
            f"🔒 **Доступ к скрипту `{script_key}` закрыт**\n\n"
            "⚠️ **Для получения скрипта необходимо подписаться на наши каналы:**\n\n"
            "1. 📢 **Becon Script**\n"
            "2. 📢 **Second Channel**\n\n"
            "▶️ **Подпишитесь на оба канала и нажмите кнопку «✅ Я ПОДПИСАЛСЯ»**"
        )
        await callback.message.edit_text(
            warning_text,
            parse_mode="Markdown",
            reply_markup=get_subscription_keyboard(script_key)
        )
    await callback.answer()

@dp.callback_query(F.data.startswith("check_"))
async def process_subscription_check(callback: types.CallbackQuery):
    """Проверка подписки после нажатия 'Я ПОДПИСАЛСЯ'"""
    script_key = callback.data.replace("check_", "")
    user_id = callback.from_user.id
    
    if await check_subscription(user_id):
        script_code = SCRIPTS_DB.get(script_key, "Скрипт временно недоступен.")
        success_text = (
            f"🎉 **Спасибо за подписку! Скрипт: {script_key.upper()}**\n\n"
            f"```lua\n{script_code}\n```\n\n"
            "💡 Скопируйте код и вставьте в исполнитель Roblox.\n\n"
            f"🔗 **Прямая ссылка:** \n`t.me/{(await bot.get_me()).username}?start={script_key}`"
        )
        await callback.message.edit_text(success_text, parse_mode="Markdown")
    else:
        warning_text = (
            "❌ **Вы все еще не подписаны на все каналы!**\n\n"
            "Убедитесь, что вы подписались на **ОБА** канала, "
            "и затем нажмите кнопку «✅ Я ПОДПИСАЛСЯ» еще раз.\n\n"
            "⚠️ **Проверьте:**\n"
            "• Becon Script ✅\n" 
            "• Second Channel ✅"
        )
        await callback.answer(warning_text, show_alert=True)
    await callback.answer()

@dp.message(Command("links"))
async def cmd_links(message: types.Message):
    """Показывает все прямые ссылки на скрипты"""
    bot_username = (await bot.get_me()).username
    links_text = "🔗 **Прямые ссылки на все скрипты:**\n\n"
    
    for script_key in SCRIPTS_DB.keys():
        links_text += f"• `t.me/{bot_username}?start={script_key}`\n"
    
    links_text += "\n💡 *Используйте эти ссылки для быстрого доступа*"
    
    await message.answer(links_text, parse_mode="Markdown")

# =============================================
# ЗАПУСК БОТА
# =============================================

async def main():
    """Основная функция запуска бота"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )
    
    if not BOT_TOKEN:
        logging.error("BOT_TOKEN не установлен! Добавьте его в переменные окружения.")
        return
    
    logging.info("Бот запускается...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
