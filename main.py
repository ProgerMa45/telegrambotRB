import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandObject
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.client.default import DefaultBotProperties

# =============================================
# НАСТРОЙКИ
# =============================================
BOT_TOKEN = "8476199583:AAGIObszhz_ucZvAxlA25NW9f68d-ItUc4g"
ADMIN_USER_ID = 6283824301  # ← Замени на свой ID пользователя Telegram

# Ссылки на каналы для подписки
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
# Инициализация бота
# =============================================
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

# Хранилище для ожидаемых платежей
pending_payments = {}

# Клавиатуры
def start_kb():
    k = InlineKeyboardBuilder()
    k.button(text="🎮 Получить скрипты", callback_data="menu")
    k.button(text="⭐ Поддержать бота", callback_data="donate")
    k.button(text="📹 YouTube", url=CHANNEL_LINKS["youtube"])
    k.button(text="📢 Канал со скриптами", url=CHANNEL_LINKS["scripts"])
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
    k.button(text="📢 Подписаться 1", url=CHANNEL_LINKS["1"])
    k.button(text="📢 Подписаться 2", url=CHANNEL_LINKS["2"])
    k.button(text="✅ Я подписался", callback_data=f"check_{key}")
    k.adjust(1)
    return k.as_markup()

def donate_kb():
    k = InlineKeyboardBuilder()
    k.button(text="⭐ 5 звезд", callback_data="donate_5")
    k.button(text="⭐ 10 звезд", callback_data="donate_10")
    k.button(text="⭐ 20 звезд", callback_data="donate_20")
    k.button(text="⭐ Другая сумма", callback_data="donate_custom")
    k.button(text="🔙 Назад", callback_data="menu")
    k.adjust(2)
    return k.as_markup()

# Выдача скрипта
async def send_script(target, key: str):
    code = SCRIPTS.get(key, "Скрипт временно недоступен")
    text = f"<b>🎉 Скрипт: {key.upper()}</b>\n\n<code>{code}</code>\n\n💡 Вставь в эксплойт и наслаждайся!"
    if isinstance(target, types.CallbackQuery):
        await target.message.edit_text(text, reply_markup=menu_kb())
    else:
        await target.answer(text, reply_markup=menu_kb())

# Отправка звезд
async def send_stars(user_id: int, amount: int):
    try:
        # Создаем инвойс для перевода звезд
        result = await bot.send_invoice(
            chat_id=user_id,
            title=f"Поддержка бота - {amount} звезд",
            description="Спасибо за вашу поддержку! ❤️",
            payload=f"donation_{amount}",
            provider_token="",  # Для Telegram Stars не нужен
            currency="XTR",  # Telegram Stars
            prices=[types.LabeledPrice(label=f"{amount} звезд", amount=amount * 100)]  # 1 звезда = 100 единиц
        )
        return True
    except Exception as e:
        print(f"Ошибка отправки звезд: {e}")
        return False

# =============================================
# Обработчики
# =============================================
@dp.message(Command("start"))
async def cmd_start(message: types.Message, command: CommandObject):
    user_id = message.from_user.id

    # Прямая ссылка: t.me/bot?start=owlhub
    if command.args and command.args.lower() in SCRIPTS:
        key = command.args.lower()
        await message.answer(
            f"<b>🔒 Для получения {key.upper()} подпишись на каналы:</b>",
            reply_markup=sub_kb(key)
        )
        return

    # Обычный старт
    await message.answer(
        "<b>👋 Привет!</b>\n\n"
        "🎮 Тут самые мощные и свежие скрипты для Roblox\n"
        "📢 Подпишись на каналы → выбирай любой скрипт бесплатно!\n\n"
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
    await cb.message.edit_text("🎮 <b>Выбери скрипт:</b>", reply_markup=menu_kb())
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
            "Например: 15",
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
            if amount < 1 or amount > 1000:
                await message.answer("❌ Сумма должна быть от 1 до 1000 звезд")
                return
            
            success = await send_stars(user_id, amount)
            if success:
                await message.answer(f"✅ Запрос на {amount} звезд отправлен!")
                # Уведомляем админа
                await bot.send_message(
                    ADMIN_USER_ID,
                    f"⭐ Новая поддержка!\n"
                    f"👤 Пользователь: @{message.from_user.username or 'без username'}\n"
                    f"💫 Сумма: {amount} звезд\n"
                    f"🆔 ID: {user_id}"
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
    await cb.message.edit_text(
        f"<b>🔒 Для получения {key.upper()} подпишись на каналы:</b>",
        reply_markup=sub_kb(key)
    )
    await cb.answer()

@dp.callback_query(F.data.startswith("check_"))
async def check_sub(cb: types.CallbackQuery):
    key = cb.data.split("_", 1)[1]
    await send_script(cb, key)
    await cb.answer("🎉 Спасибо за подписку!")

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
        "🎁 Ваша поддержка помогает развивать проект\n\n"
        "🔗 <b>Прямые ссылки:</b>\n"
        "t.me/scriptmajproRB?start=owlhub\n"
        "t.me/scriptmajproRB?start=infiniteyield",
        reply_markup=k.as_markup()
    )
    await cb.answer()

# Обработчик успешных платежей
@dp.pre_checkout_query()
async def process_pre_checkout(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@dp.message(F.successful_payment)
async def process_successful_payment(message: types.Message):
    amount = message.successful_payment.total_amount // 100
    await message.answer(
        f"💫 <b>Спасибо за поддержку!</b>\n\n"
        f"Вы отправили {amount} звезд ❤️\n"
        f"Ваша поддержка помогает развивать бота!\n\n"
        "🎮 Возвращаюсь в меню:",
        reply_markup=menu_kb()
    )
    
    # Уведомление админу
    await bot.send_message(
        ADMIN_USER_ID,
        f"⭐ Успешная поддержка!\n"
        f"👤 Пользователь: @{message.from_user.username or 'без username'}\n"
        f"💫 Сумма: {amount} звезд\n"
        f"🆔 ID: {message.from_user.id}"
    )

# =============================================
# Запуск
# =============================================
async def main():
    logging.basicConfig(level=logging.INFO)
    bot_user = await bot.get_me()
    print("✅ Бот запущен!")
    print(f"🔗 Прямые ссылки:")
    print(f"t.me/{bot_user.username}?start=owlhub")
    print(f"t.me/{bot_user.username}?start=infiniteyield")
    print(f"t.me/{bot_user.username}?start=darkhub")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
