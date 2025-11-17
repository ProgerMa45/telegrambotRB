import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.exceptions import TelegramBadRequest
from aiogram.client.default import DefaultBotProperties

# =============================================
# ЗАМЕНИ ТОЛЬКО ЭТИ СТРОКИ!
# =============================================
BOT_TOKEN = "8476199583:AAGIObszhz_ucZvAxlA25NW9f68d-ItUc4g"   # ← твой токен

# ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←
# ID КАНАЛОВ! (обязательно с -100 в начале)
REQUIRED_CHANNELS = [
    -1002183745123,  # ← замени на реальный ID первого канала
    -1002194857391   # ← замени на реальный ID второго канала
]
# =============================================

CHANNEL_URLS = {
    "1": "https://t.me/Sigma4Script",
    "2": "https://t.me/Xleb4ikScript",
    "youtube": "https://youtu.be/edUA1lwRFh8",
    "scripts": "https://t.me/+R7DwT69_eHhmMmEy"
}

SCRIPTS = {
    "infiniteyield": 'loadstring(game:HttpGet("https://raw.githubusercontent.com/EdgeIY/infiniteyield/master/source"))()',
    "owlhub": 'loadstring(game:HttpGet("https://raw.githubusercontent.com/CriShoux/OwlHub/master/OwlHub.txt"))()',
    "darkhub": 'loadstring(game:HttpGet("https://raw.githubusercontent.com/RandomAdamYT/DarkHub/master/Init"))()',
    "vortex": 'loadstring(game:HttpGet("https://raw.githubusercontent.com/VortexHubScript/VortexHub/main/init"))()',
    "fluxus": 'loadstring(game:HttpGet("https://raw.githubusercontent.com/FluxusHub/Fluxus/main/Loader"))()',
    "electron": 'loadstring(game:HttpGet("https://raw.githubusercontent.com/ElectronTeam/Electron/main/Electron"))()',
}

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

def start_kb():
    k = InlineKeyboardBuilder()
    k.button(text="Получить скрипты", callback_data="menu")
    k.button(text="YouTube", url=CHANNEL_URLS["youtube"])
    k.button(text="Канал со скриптами", url=CHANNEL_URLS["scripts"])
    k.adjust(1)
    return k.as_markup()

def menu_kb():
    k = InlineKeyboardBuilder()
    for name in SCRIPTS: k.button(text=name.upper(), callback_data=f"get_{name}")
    k.button(text="Помощь", callback_data="help")
    k.adjust(2)
    return k.as_markup()

def sub_kb(key): 
    k = InlineKeyboardBuilder()
    k.button(text="Канал 1", url=CHANNEL_URLS["1"])
    k.button(text="Канал 2", url=CHANNEL_URLS["2"])
    k.button(text="Я подписался", callback_data=f"check_{key}")
    k.adjust(1)
    return k.as_markup()

async def check_sub(uid):
    for cid in REQUIRED_CHANNELS:
        try:
            m = await bot.get_chat_member(cid, uid)
            if m.status in ("left", "kicked"): return False
        except: return False
    return True

async def give_script(to, key):
    code = SCRIPTS.get(key, "Ошибка")
    text = f"<b>Скрипт: {key.upper()}</b>\n\n<code>{code}</code>\n\nВставь в эксплойт!"
    if isinstance(to, types.CallbackQuery):
        await to.message.edit_text(text, reply_markup=menu_kb())
    else:
        await to.answer(text, reply_markup=menu_kb())

@dp.message(Command("start"))
async def start(m: types.Message, command: CommandObject):
    uid = m.from_user.id
    args = command.args
    if args and args.lower() in SCRIPTS:
        if await check_sub(uid):
            await give_script(m, args.lower())
        else:
            await m.answer(f"Подпишись на каналы, чтобы получить {args.upper()}", reply_markup=sub_kb(args.lower()))
        return
    await m.answer("<b>Привет!</b>\nТут самые мощные скрипты для Roblox\nПодпишись на каналы → выбирай любой!", reply_markup=start_kb())

@dp.callback_query(F.data == "menu")
async def menu(c): await c.message.edit_text("Выбери скрипт:", reply_markup=menu_kb()); await c.answer()

@dp.callback_query(F.data.startswith("get_"))
async def get(c):
    key = c.data.split("_", 1)[1]
    if await check_sub(c.from_user.id): await give_script(c, key)
    else: await c.message.edit_text("Подпишись на каналы:", reply_markup=sub_kb(key))
    await c.answer()

@dp.callback_query(F.data.startswith("check_"))
async def check(c):
    key = c.data.split("_", 1)[1]
    if await check_sub(c.from_user.id): await give_script(c, key)
    else: await c.answer("Ты не подписан на все каналы!", show_alert=True)

@dp.callback_query(F.data == "help")
async def help(c):
    k = InlineKeyboardBuilder().button(text="Назад", callback_data="menu")
    await c.message.edit_text("1. Подпишись на оба канала\n2. Нажми «Я подписался»\n3. Получай скрипт", reply_markup=k.as_markup())
    await c.answer()

async def main():
    logging.basicConfig(level=logging.INFO)
    print("Бот запущен на Railway!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
