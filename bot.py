import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

BOT_TOKEN = "8747359640:AAE3EeP3xYkMInNfjHjTHEuPKLBL18loll8"
ADMIN_ID = 911879981

from aiogram.client.session.aiohttp import AiohttpSession

# Если твой VPN поднимает локальный SOCKS5 (обычно порт 1080, 10808 или 7890)
# Либо используем встроенную сессию с системными настройками
session = AiohttpSession(proxy="socks5://127.0.0.1:10808")  # Укажи порт своего VPN, если знаешь

bot = Bot(token=BOT_TOKEN, session=session)
dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer("Привет! Напишите ваше сообщение, и админ вам ответит.")


@dp.message(lambda msg: msg.from_user.id == ADMIN_ID and msg.reply_to_message)
async def reply_to_user(message: types.Message):
    try:
        first_line = message.reply_to_message.text.split("\n")[0]
        user_id = int(first_line.split(":")[1].strip())

        await bot.send_message(
            chat_id=user_id,
            text=f"👨‍💻 **Ответ от администратора:**\n\n{message.text}",
            parse_mode="Markdown",
        )
        await message.answer("✅ Ответ успешно отправлен!")
    except (IndexError, ValueError):
        await message.answer(
            "❌ Не удалось определить ID пользователя. Отвечайте на оригинальное сообщение с ID."
        )
    except Exception as e:
        await message.answer(f"❌ Ошибка при отправке: {e}")


@dp.message()
async def forward_to_admin(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer(
            "Чтобы ответить пользователю, используйте функцию 'Ответить' (Reply) на его сообщение."
        )
        return

    user = message.from_user
    username = f"@{user.username}" if user.username else "нет юзернейма"

    text_to_admin = (
        f"ID: {user.id}\n"
        f"📩 **Новое сообщение!**\n\n"
        f"👤 **От:** {user.full_name} ({username})\n"
        f"💬 **Текст:** {message.text}"
    )

    await bot.send_message(chat_id=ADMIN_ID, text=text_to_admin, parse_mode="Markdown")
    await message.answer("Ваше сообщение отправлено администратору!")


async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())