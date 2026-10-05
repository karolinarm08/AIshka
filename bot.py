import google.generativeai as genai
import os

from telegram import (
    Update,
    ReplyKeyboardMarkup
)

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-3.1-flash-lite")

keyboard = [
    ["Студент"],
    ["IT-технології"],
    ["Контакти"],
    ["Prompt AI"]
]

reply_markup = ReplyKeyboardMarkup(
    keyboard,
    resize_keyboard=True
)


async def start(update: Update,
                context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "Оберіть пункт меню:",
        reply_markup=reply_markup
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    if text == "Студент":

        await update.message.reply_text(
            "Прізвище: Рудих\n"
            "Група: ІС-32"
        )

    elif text == "IT-технології":

        await update.message.reply_text(
            "Frontend\n"
            "Backend\n"
            "Web Technologies\n"
            "Telegram Bot"
        )

    elif text == "Контакти":

        await update.message.reply_text(
            "Телефон: +380662688888\n"
            "Email: karolina8888@gmail.com"
        )

    elif text == "Prompt AI":

        await update.message.reply_text(
            "Напишіть запит для AI..."
        )

        context.user_data["ai_mode"] = True

    else:

        if context.user_data.get("ai_mode"):

            response = model.generate_content(
    "Відповідай коротко, без Markdown, без символів *, #, ```.\n\n" + text
            )

            await update.message.reply_text(
                response.text
            )

            context.user_data["ai_mode"] = False

        else:

            await update.message.reply_text(
                "Оберіть пункт меню:"
            )


def main():

    app = Application.builder() \
        .token(TELEGRAM_TOKEN) \
        .build()

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message
        )
    )

    print("Бот запущений")

    app.run_polling()


if __name__ == "__main__":
    main()