from telegram import ForceReply, Update
from telegram.ext import CommandHandler, ContextTypes, Application
from checkEdgevana import request
import asyncio


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}! I'm checking for you free server in this moment | start: /check",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    link = 'https://srv.edgevana.com/solana-validator-servers'
    await update.message.reply_html(f'Using this link you can come and check the availability of servers manually: <a href="{link}">Check Servers</a>')


async def check_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    while True:
        servers_generator = format_servers()

        # Список для хранения ID отправленных сообщений
        message_ids = []

        for server in servers_generator:
            # Отправляем сообщение и добавляем его ID в список
            message = await update.message.reply_html(f"{server}")
            message_ids.append(message.message_id)

        # Ждем 30 секунд
        await asyncio.sleep(1800)

        # Удаляем все сообщения
        for message_id in message_ids:
            await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=message_id)


def format_servers() -> str:
    servers = request()
    for server in servers:
        yield server


def main() -> None:
    application = Application.builder().token("Your bot token").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command)) # /help
    application.add_handler(CommandHandler("check", check_command)) # /check

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()