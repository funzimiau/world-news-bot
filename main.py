import asyncio  
import logging
import requests
from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Message
from aiogram.filters import Command

logging.basicConfig(level=logging.INFO)

TOKEN = "7680078478:AAEqviFBOwhaOAaY4Osbcof6li54l6fTIxg"
NEWS_API_KEY = "8f6b05a1fc844e58a8e977cd1465f435"


bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))


dp = Dispatcher()
router = Router()



@router.message(Command("start"))
async def bot_start(message: Message):
    await message.answer(
        f"Привет, {message.from_user.full_name}! Я могу рассказать тебе о последних мировых новостях!\n\n"
        f"Напиши /help, чтобы узнать мои команды!"
    )

@router.message(Command("help"))
async def bot_help(message: Message):
    await message.answer(
        "Все команды бота:\n"
        "/start - старт бота\n"
        "/help - список команд\n"
        "/news <i><b>тема</b></i> - последние новости по указанной теме"
    )

@router.message(Command("news"))
async def cmd_news(message: Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("Пожалуйста, укажите тему новостей после команды /news!")
        return

    topic = args[1]
    try:
        
        response = requests.get(
            f"https://newsapi.org/v2/everything?q={topic}&apiKey={NEWS_API_KEY}"
        )
        response.raise_for_status()
        data = response.json()

        if data["articles"]:
            articles = data["articles"][:3]  # Ограничиваем количество статей
            news = "\n\n".join(
                [
                    f"📰 <b>{article['title']}</b>\n{article['description']}\n"
                    f"Источник: {article['source']['name']}\n"
                    f"Ссылка: {article['url']}"
                    for article in articles
                ]
            )
            await message.answer(news)
        else:
            await message.answer("Извините, новости по данной теме не найдены. Попробуйте указать другую тему.")
    except requests.exceptions.RequestException:
        await message.answer("Не удалось получить данные о новостях. Проверьте тему или попробуйте позже.")

@router.message()
async def echo_message(message: Message):
    await message.answer("Я не понимаю тебя, напиши /help")


dp.include_router(router)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
