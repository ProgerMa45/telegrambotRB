import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandObject
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.client.default import DefaultBotProperties

# =============================================
# НАСТРОЙКИ
# =============================================
BOT_TOKEN = "8386985377:AAHocbav9Pz3dagXRh_WrjGYdUd8DSsNA-o"
ADMIN_USER_ID = 6283824301

# Ссылки на каналы для подписки
CHANNEL_LINKS = {
    "channel1": "https://t.me/passByscirpt",
    "channel2": "https://t.me/bekascript",
}

# Username каналов для проверки подписки
CHANNELS_TO_CHECK = [
    "@passByscirpt",  # ← username первого канала
    "@bekascript",    # ← username второго канала
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
    "krystalkey": 'loadstring(game:HttpGet("https://raw.githubusercontent.com/KrystalTeam/KrystalKey/main/loader.lua"))()',
    "synapse": 'loadstring(game:HttpGet("https://raw.githubusercontent.com/synapse-x/synapse/master/loader.lua"))()',
    "jjsploit": 'loadstring(game:HttpGet("https://raw.githubusercontent.com/jjsploit/jjsploit/master/loader.lua"))()',
    "krnl": 'loadstring(game:HttpGet("https://raw.githubusercontent.com/KRNL/KRNL/master/loader.lua"))()',
}

# =============================================
# Инициализация бота
# =============================================
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

pending_payments = {}

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
                print(f"❌ Пользователь {user_id} не подписан на {channel_username}")
                return False
                
        except Exception as e:
            print(f"🚨 Ошибка проверки канала {channel_username}: {e}")
            return False
    
    print(f"✅ Пользователь {user_id} подписан на все каналы")
    return True

# Клавиатуры
def start_kb():
    k = InlineKeyboardBuilder()
    k.button(text="🎮 Получить скрипты", callback_data="menu")
    k.button(text="⭐ Поддержать бота", callback_data="donate")
    k.adjust(1)
    return k.as_markup()

def menu_kb():
    k = InlineKeyboardBuilder()
    for name in SCRIPTS.keys():
        k.button(text=f"🎮 {name.upper()}", callback_data=f"get_{name}")
    k.button(text="⭐ Поддержать бота", callback_data="donate")
    k.button(text="❓ Помощь", callback_data="help")
    k.adjust(2)
    return k.as_markup()

def sub_kb(key: str):
    k = InlineKeyboardBuilder()
    k.button(text="📢 Подписаться 1", url=CHANNEL_LINKS["channel1"])
    k.button(text="📢 Подписаться 2", url=CHANNEL_LINKS["channel2"])
    k.button(text="✅ Я подписался", callback_data=f"check_{key}")
    k.adjust(1)
    return k.as_markup()

def donate_kb():
    k = InlineKeyboardBuilder()
    k.button(text="⭐ 5 звезд", callback_data="donate_5")
    k.button(text="⭐ 10 звезд", callback_data="donate_10")
    k.button(text="⭐ 50 звезд", callback_data="donate_50")
    k.button(text="⭐ 100 звезд", callback_data="donate_100")
    k.button(text="🔙 Назад", callback_data="menu")
    k.adjust(2)
    return k.as_markup()

# Выдача скрипта (БЕЗ КНОПОК)
async def send_script(target, key: str):
    code = SCRIPTS.get(key, "Скрипт временно недоступен")
    text = f"<b>🎉 Скрипт: {key.upper()}</b>\n\n<code>{code}</code>\n\n💡 Вставь в эксплойт и наслаждайся!"
    if isinstance(target, types.CallbackQuery):
        await target.message.edit_text(text)  # Убрал reply_markup
    else:
        await target.answer(text)  # Убрал reply_markup

# Отправка звезд
async def send_stars(user_id: int, amount: int):
    try:
        # Правильные цены для Telegram Stars (1 звезда = 7 единиц)
        result = await bot.send_invoice(
            chat_id=user_id,
            title=f"Поддержка бота - {amount} звезд",
            description="Спасибо за вашу поддержку! ❤️\nВаши звезды помогают развивать бота.",
            payload=f"donation_{amount}",
            provider_token="",  # Для Telegram Stars не нужен
            currency="XTR",     # Telegram Stars
            prices=[types.LabeledPrice(label=f"{amount} звезд", amount=amount * 7)]  # ПРАВИЛЬНАЯ ЦЕНА
        )
        return True
    except Exception as e:
        print(f"Ошибка отправки звезд: {e}")
        return False

# =============================================
# ОБРАБОТЧИКИ
# =============================================
@dp.message(Command("start"))
async def cmd_start(message: types.Message, command: CommandObject):
    user_id = message.from_user.id

    # Прямая ссылка: t.me/bot?start=owlhub
    if command.args and command.args.lower() in SCRIPTS:
        key = command.args.lower()
        # ПРОВЕРЯЕМ ПОДПИСКУ НА КАНАЛЫ
        if await check_subscription(user_id):
            await send_script(message, key)
        else:
            await message.answer(
                f"<b>🔒 Для получения {key.upper()} нужно подписаться на наши каналы:</b>\n\n"
                "📢 <b>Обязательные подписки:</b>\n"
                "• PassBy Script\n"
                "• Bekascript\n\n"
                "✅ <b>После подписки нажми «Я подписался»</b>",
                reply_markup=sub_kb(key)
            )
        return

    # Обычный старт
    await message.answer(
        "<b>👋 Привет!</b>\n\n"
        "🎮 Тут самые мощные и свежие скрипты для Roblox\n"
        "📢 <b>Подпишись на наши каналы чтобы получить скрипты!</b>\n\n"
        "⭐ <b>Данный бот создан и поддерживается за счет Telegram Stars</b>\n"
        "💫 Поддержи разработчика звездами!",
        reply_markup=start_kb()
    )

@dp.message(Command("donate"))
async def cmd_donate(message: types.Message):
    await message.answer(
        "⭐ <b>Поддержать бота</b>\n\n"
        "💫 Этот бот создан и поддерживается за счет Telegram Stars\n"
        "🎁 Ваша поддержка помогает развивать бота и добавлять новые скрипты\n\n"
        "Выберите сумму для поддержки:",
        reply_markup=donate_kb()
    )

@dp.callback_query(F.data == "menu")
async def show_menu(cb: types.CallbackQuery):
    await cb.message.edit_text(
        "🎮 <b>Выбери скрипт:</b>\n\n"
        "📢 <b>Для получения скрипта нужно подписаться на наши каналы!</b>",
        reply_markup=menu_kb()
    )
    await cb.answer()

@dp.callback_query(F.data == "donate")
async def show_donate(cb: types.CallbackQuery):
    await cb.message.edit_text(
        "⭐ <b>Поддержать бота</b>\n\n"
        "💫 Этот бот создан и поддерживается за счет Telegram Stars\n"
        "🎁 Ваша поддержка помогает развивать бота и добавлять новые скрипты\n\n"
        "Выберите сумму для поддержки:",
        reply_markup=donate_kb()
    )
    await cb.answer()

@dp.callback_query(F.data.startswith("donate_"))
async def process_donation(cb: types.CallbackQuery):
    data = cb.data.replace("donate_", "")
    
    if data == "custom":
        await cb.message.edit_text(
            "⭐ <b>Введите сумму звезд:</b>\n\n"
            "Напишите число - сколько звезд вы хотите отправить\n"
            "Например: 15\n\n"
            "💫 <b>Минимум: 1 звезда</b>\n"
            "💫 <b>Максимум: 1000 звезд</b>",
            reply_markup=InlineKeyboardBuilder().button(text="🔙 Назад", callback_data="donate").as_markup()
        )
        pending_payments[cb.from_user.id] = "waiting_amount"
    else:
        try:
            amount = int(data)
            success = await send_stars(cb.from_user.id, amount)
            if success:
                await cb.answer(f"✅ Запрос на {amount} звезд отправлен!")
            else:
                await cb.answer("❌ Ошибка отправки запроса", show_alert=True)
        except ValueError:
            await cb.answer("❌ Неверная сумма", show_alert=True)
    await cb.answer()

@dp.message(F.text)
async def handle_custom_amount(message: types.Message):
    user_id = message.from_user.id
    
    if user_id in pending_payments and pending_payments[user_id] == "waiting_amount":
        try:
            amount = int(message.text.strip())
            if amount < 1:
                await message.answer("❌ Минимальная сумма - 1 звезда")
                return
            if amount > 1000:
                await message.answer("❌ Максимальная сумма - 1000 звезд")
                return
            
            success = await send_stars(user_id, amount)
            if success:
                await message.answer(f"✅ Запрос на {amount} звезд отправлен!")
                await bot.send_message(
                    ADMIN_USER_ID,
                    f"⭐ Новая поддержка!\n👤 Пользователь: @{message.from_user.username or 'без username'}\n💫 Сумма: {amount} звезд\n🆔 ID: {user_id}"
                )
            else:
                await message.answer("❌ Ошибка отправки запроса")
            
            del pending_payments[user_id]
            await message.answer("🎮 Возвращаюсь в меню:", reply_markup=menu_kb())
            
        except ValueError:
            await message.answer("❌ Введите корректное число")
        except Exception as e:
            await message.answer("❌ Произошла ошибка")
            del pending_payments[user_id]

@dp.callback_query(F.data.startswith("get_"))
async def get_script(cb: types.CallbackQuery):
    key = cb.data.split("_", 1)[1]
    # ПРОВЕРЯЕМ ПОДПИСКУ НА КАНАЛЫ
    if await check_subscription(cb.from_user.id):
        await send_script(cb, key)
    else:
        await cb.message.edit_text(
            f"<b>🔒 Для получения {key.upper()} нужно подписаться на наши каналы:</b>\n\n"
            "📢 <b>Обязательные подписки:</b>\n"
            "• PassBy Script\n"
            "• Bekascript\n\n"
            "✅ <b>После подписки нажми «Я подписался»</b>",
            reply_markup=sub_kb(key)
        )
    await cb.answer()

@dp.callback_query(F.data.startswith("check_"))
async def check_sub(cb: types.CallbackQuery):
    key = cb.data.split("_", 1)[1]
    # ПРОВЕРЯЕМ ПОДПИСКУ при нажатии "Я подписался"
    if await check_subscription(cb.from_user.id):
        await send_script(cb, key)
        await cb.answer("🎉 Спасибо за подписку!")
    else:
        await cb.answer("❌ Вы не подписаны на все каналы! Проверьте подписки.", show_alert=True)

@dp.callback_query(F.data == "help")
async def help_cmd(cb: types.CallbackQuery):
    k = InlineKeyboardBuilder()
    k.button(text="⭐ Поддержать", callback_data="donate")
    k.button(text="🔙 Назад", callback_data="menu")
    
    await cb.message.edit_text(
        "<b>❓ Как пользоваться:</b>\n\n"
        "1. 📢 Подпишись на оба канала\n"
        "2. ✅ Нажми «Я подписался»\n"
        "3. 🎮 Получи скрипт мгновенно\n\n"
        "⭐ <b>Поддержка бота:</b>\n"
        "💫 Бот создан и поддерживается за счет Telegram Stars\n"
        "🎁 Ваша поддержка помогает развивать проект",
        reply_markup=k.as_markup()
    )
    await cb.answer()

# Обработчик платежей
@dp.pre_checkout_query()
async def process_pre_checkout(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@dp.message(F.successful_payment)
async def process_successful_payment(message: types.Message):
    amount = message.successful_payment.total_amount // 7  # Правильный расчет звезд
    await message.answer(
        f"💫 <b>Спасибо за поддержку!</b>\n\nВы отправили {amount} звезд ❤️\n\n🎮 Возвращаюсь в меню:",
        reply_markup=menu_kb()
    )
    
    await bot.send_message(
        ADMIN_USER_ID,
        f"⭐ Успешная поддержка!\n👤 Пользователь: @{message.from_user.username or 'без username'}\n💫 Сумма: {amount} звезд\n🆔 ID: {message.from_user.id}"
    )

# =============================================
# Запуск
# =============================================
async def main():
    logging.basicConfig(level=logging.INFO)
    bot_user = await bot.get_me()
    print("✅ Бот запущен!")
    print(f"🔗 Прямые ссылки:")
    for name in SCRIPTS.keys():
        print(f"t.me/{bot_user.username}?start={name}")
    print(f"⚠️ Убедись что бот добавлен как администратор в каналы: {CHANNELS_TO_CHECK}")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
