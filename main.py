from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
import handlers
import config
import asyncio

bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
dp.include_router(handlers.router)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())