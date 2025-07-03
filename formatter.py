def format_anime(title: str, description: str) -> str:
    return f"<b>{title}</b>\n\n{description}"

def format_top(top_list: list) -> str:
    return "<b>Топ 10 аниме:</b>\n" + "\n".join(top_list)