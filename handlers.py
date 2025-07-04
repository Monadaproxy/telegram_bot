from aiogram import Router, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import Command
from scraper import get_random_anime, get_top_10, get_new_episodes

router = Router()

def get_inline_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(
        types.InlineKeyboardButton(
            text="🎲 Случайное аниме",
            callback_data="random_anime"
        ),
        types.InlineKeyboardButton(
            text="🏆 Топ 10 аниме",
            callback_data="top_anime"
        ),
        types.InlineKeyboardButton(
            text="🆕 Новинки",
            callback_data="new_episodes"
        )
    )
    builder.adjust(1)
    return builder.as_markup()


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "🍿 <b>Аниме-бот</b>\n\n"
        "Я могу найти случайное аниме, топовые тайтлы или новинки сезона!",
        reply_markup=get_inline_keyboard()
    )


@router.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(
        "📌 <b>Доступные команды:</b>\n"
        "/start — Главное меню\n"
        "/help — Справка\n\n"
        "Используй кнопки ниже для навигации:",
        reply_markup=get_inline_keyboard()
    )


@router.callback_query(F.data == "random_anime")
async def random_anime(callback: types.CallbackQuery):
    try:
        data = await get_random_anime()

        if "error" in data:
            await callback.answer(data["error"], show_alert=True)
            return

        text = (
            f"<b>🎲 {data['title']}</b>\n\n"
            f"{data['description']}\n\n"
            f"🔗 <a href='{data['url']}'>Подробнее на AniList</a>"
        )

        if data["cover_url"]:
            await callback.message.answer_photo(
                photo=data["cover_url"],
                caption=text,
                reply_markup=get_inline_keyboard(),
                parse_mode="HTML"
            )
            await callback.message.delete()
        else:
            await callback.message.edit_text(
                text,
                reply_markup=get_inline_keyboard(),
                disable_web_page_preview=True
            )

        await callback.answer()

    except Exception as e:
        await callback.answer("😢 Не удалось загрузить аниме", show_alert=True)


@router.callback_query(F.data.in_(["top_anime", "new_episodes"]))
async def handle_other_buttons(callback: types.CallbackQuery):
    try:
        # Удаляем предыдущее сообщение (любое - с фото или текстом)
        await callback.message.delete()

        if callback.data == "top_anime":
            text = await get_top_10()
        else:
            text = await get_new_episodes()

        # Отправляем новое сообщение
        await callback.message.answer(
            text=text,
            reply_markup=get_inline_keyboard(),
            disable_web_page_preview=True
        )

        await callback.answer()

    except Exception as e:
        await callback.answer("⚠️ Ошибка при обработке запроса", show_alert=True)


@router.callback_query(F.data == "top_anime")
async def top_anime(callback: types.CallbackQuery):
    top_list = await get_top_10()
    await callback.message.edit_text(top_list, reply_markup=get_inline_keyboard())

@router.callback_query(F.data == "new_episodes")
async def new_episodes(callback: types.CallbackQuery):
    episodes = await get_new_episodes()
    await callback.message.edit_text(episodes, reply_markup=get_inline_keyboard())