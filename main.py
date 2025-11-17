import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.client.default import DefaultBotProperties

# =============================================
# НАСТРОЙКИ — ЗАМЕНИ ТОЛЬКО ЭТИ 3 СТРОЧКИ
# =============================================
BOT_TOKEN = "8476199583:AAGIObszhz_ucZvAxlA25NW9f68d-ItUc4g"   # ← твой токен

# ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←
# ID КАНАЛОВ! Добавь @getidsbot в канал → перешли сообщение → получишь ID
REQUIRED_CHANNELS = [
    -1002183745123,   # ← замени на ID первого канала
    -1002194857391    # ← замени на ID второго канала
]
# =============================================

# Ссылки на каналы (для кнопок)
CHANNEL_LINKS = {
    "1": "https://t.me/Sigma4Script",
    "2": "https://t.me/Xleb4ikScript",
    "youtube": "https://youtu.be/edUA1lwRFh8",
    "scripts": "https://t.me/+R7DwT69_eHhmMmEy"
}

# Скрипты
SCRIPTS = {
    "infiniteyield": 'loadstring(game:HttpGet("https://raw.githubusercontent.com/EdgeIY/infiniteyield/master/source"))()',
    "owlhub": 'loadstring(game:HttpGet("https://raw.githubusercontent.com/CriShoux/OwlHub/master/OwlHub.txt"))()',
    "darkhub": 'loadstring(game:HttpGet("https://raw.githubusercontent.com/RandomAdamYT/DarkHub/master/Init"))()',
    "vortex": 'loadstring(game:HttpGet("https://raw.githubusercontent.com/VortexHubScript/VortexHub/main/init"))()',
    "fluxus": 'loadstring(game:HttpGet("https://raw.githubusercontent.com/FluxusHub/Fluxus/main/Loader"))()',
    "electron": 'loadstring(game:HttpGet("https://raw.githubusercontent.com/ElectronTeam/Electron/main/Electron"))()',
}

# =============================================
# Инициализация бота (aiogram 3.17.0+)
# =============================================
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

# Клавиатуры
def start_kb():
    k = InlineKeyboardBuilder()
    k.button(text="Получить скрипты", callback_data="menu")
    k.button(text="YouTube", url=CHANNEL_LINKS["youtube"])
    k.button(text="Канал со скриптами", url=CHANNEL_LINKS["scripts"])
    k.adjust(1)
    return k.as_markup()

def menu_kb():
    k = InlineKeyboardBuilder()
    for name in SCRIPTS.keys():
        k.button(text=f"{name.upper()}", callback_data=f"get_{name}")
    k.button(text="Помощь", callback_data="help")
    k.adjust(2)
    return k.as_markup()

def sub_kb(key: str):
    k = InlineKeyboardBuilder()
    k.button(text="Канал 1", url=CHANNEL_LINKS["1"])
    k.button(text="Канал 2", url=CHANNEL_LINKS["2"])
    k.button(text="Я подписался", callback_data=f"check_{key}")
    k.adjust(1)
    return k.as_markup()

# Проверка подписки
async def is_subscribed(user_id: int) -> bool:
    for chat_id in REQUIRED_CHANNELS:
        try:
            member = await bot.get_chat_member(chat_id=chat_id, user_id=user_id)
            if member.status in ("left", "kicked"):
                return False
        except:
            return False
    return True

# Выдача скрипта
async def send_script(target, key: str):
    code = SCRIPTS.get(key, "Скрипт временно недоступен")
    text = f"<b>Скрипт: {key.upper()}</b>\n\n<code>{code}</code>\n\nВставь в эксплойт и наслаждайся!"
    if isinstance(target, types.CallbackQuery):
        await target.message.edit_text(text, reply_markup=menu_kb())
    else:
        await target.answer(text, reply_markup=menu_kb())

# =============================================
# Обработчики
# =============================================
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    # Получаем аргументы команды (для прямых ссылок t.me/bot?start=owlhub)
    text_parts = message.text.split(maxsplit=1)
    args = text_parts[1] if len(text_parts) > 1 else None
    user_id = message.from_user.id

    # Прямая ссылка: t.me/bot?start=owlhub
    if args and args.lower() in SCRIPTS:
        key = args.lower()
        if await is_subscribed(user_id):
            await send_script(message, key)
        else:
            await message.answer(
                f"<b>Чтобы получить {key.upper()} — подпишись на каналы:</b>",
                reply_markup=sub_kb(key)
            )
        return

    # Обычный старт
    await message.answer(
        "<b>Привет!</b>\n\n"
        "Тут самые мощные и свежие скрипты для Roblox\n"
        "Подпишись на каналы → выбирай любой скрипт бесплатно!",
        reply_markup=start_kb()
    )

@dp.callback_query(F.data == "menu")
async def show_menu(cb: types.CallbackQuery):
    await cb.message.edit_text("Выбери скрипт ниже:", reply_markup=menu_kb())
    await cb.answer()

@dp.callback_query(F.data.startswith("get_"))
async def get_script(cb: types.CallbackQuery):
    key = cb.data.split("_", 1)[1]
    if await is_subscribed(cb.from_user.id):
        await send_script(cb, key)
    else:
        await cb.message.edit_text("Подпишись на каналы:", reply_markup=sub_kb(key))
    await cb.answer()

@dp.callback_query(F.data.startswith("check_"))
async def check_sub(cb: types.CallbackQuery):
    key = cb.data.split("_", 1)[1]
    if await is_subscribed(cb.from_user.id):
        await send_script(cb, key)
    else:
        await cb.answer("Ты не подписан на все каналы!", show_alert=True)

@dp.callback_query(F.data == "help")
async def help_cmd(cb: types.CallbackQuery):
    k = InlineKeyboardBuilder()
    k.button(text="Назад", callback_data="menu")
    await cb.message.edit_text(
        "<b>Как пользоваться:</b>\n\n"
        "1. Подпишись на <b>оба</b> канала\n"
        "2. Нажми «Я подписался»\n"
        "3. Получишь скрипт мгновенно",
        reply_markup=k.as_markup()
    )
    await cb.answer()

# =============================================
# Запуск
# =============================================
async def main():
    logging.basicConfig(level=logging.INFO)
    print("Бот успешно запущен! Прямые ссылки работают:")
    print("t.me/твойбот?start=owlhub   → сразу OwlHub")
    print("t.me/твойбот?start=infiniteyield → сразу Infinite Yield")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
