import configparser
import logging
import os

import yaml
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from db_requests import DBConnector
from src import catching, storage, stats, leaderboard, selling


class FishingBot:
    def __init__(self):
        self.token = None
        self.messages = self.read_texts()
        self.application = self.get_application()
        self.application = self.setup_application(self.application)
        self.create_logs_directory()  # Добавляем создание каталога
        self.setup_logging()
        self.db_connector = DBConnector()
        print("Bot inited!")

    def create_logs_directory(self):
        logs_directory = '../logs'
        if not os.path.exists(logs_directory):
            os.makedirs(logs_directory)

    def read_texts(self):
        with open("text/parsed_texts.yml", "r", encoding="utf-8") as file:
            texts = yaml.safe_load(file)
        return texts

    async def send_message(self, user_id, message):
        await self.application.bot.send_message(chat_id=user_id, text=message, parse_mode="Markdown")

    async def send_cooldown_message(self, user_id, cooldown, tool="rod"):
        tool_name = None
        reply_markup = None
        if tool == "rod":
            reply_markup = ReplyKeyboardMarkup([[KeyboardButton('/fish')]], resize_keyboard=True,
                                               one_time_keyboard=True)
            tool_name = "удочки"
        elif tool == "net":
            tool_name = "сети"
            reply_markup = ReplyKeyboardMarkup([[KeyboardButton('/net')]], resize_keyboard=True,
                                               one_time_keyboard=True)
        await self.application.bot.send_message(chat_id=user_id,
                                                text=f"Перезарядка {tool_name}: {cooldown:.0f} секунд(ы)!",
                                                parse_mode="Markdown",
                                                reply_markup=reply_markup)

    def get_text(self, var):
        return self.messages[var]

    def read_config(self):
        config = configparser.ConfigParser()
        config.read("settings/config.ini")
        return config

    async def start(self, update: Update, context):
        user = update.effective_user
        print(f"Trying to insert player {user.id}, {user.username}")
        self.db_connector.insert_player(user.id, user.username)
        keyboard = [[KeyboardButton('/fish')]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
        await update.message.reply_html(
            self.get_text("bot_start").format(user.mention_html()),
            reply_markup=reply_markup,
        )

    async def fish(self, update: Update, context):
        user = update.effective_user
        result = await catching.get_player_catch_fish(user.id, update.message.date, self, tool="rod")
        if result:
            keyboard = [[KeyboardButton('/fish')]]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
            await update.message.reply_text(result, parse_mode="Markdown", reply_markup=reply_markup)

    async def net(self, update: Update, context):
        user = update.effective_user
        result = await catching.get_player_catch_fish(user.id, update.message.date, self, tool="net")
        if result:
            keyboard = [[KeyboardButton('/net')]]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
            await update.message.reply_text(result, parse_mode="Markdown", reply_markup=reply_markup)

    async def storage(self, update: Update, context):
        user = update.effective_user
        result = storage.get_player_storage(user.id, self)
        await update.message.reply_text(result, parse_mode="Markdown", reply_markup=None)

    async def stats(self, update: Update, context):
        user = update.effective_user
        result = stats.player_stats(user.id)
        await update.message.reply_text(result, parse_mode="Markdown", reply_markup=None)

    async def leaderboard(self, update: Update, context):
        user = update.effective_user
        result = leaderboard.get_leaderboard(user.id, self)
        await update.message.reply_text(result, parse_mode="Markdown", reply_markup=None)

    async def sell(self, update: Update, context):
        user = update.effective_user
        result = selling.sell_all(user.id, self)
        await update.message.reply_text(result, parse_mode="Markdown", reply_markup=None)

    async def help_command(self, update: Update, context):
        await update.message.reply_text("Help!")

    async def echo(self, update: Update, context):
        await update.message.reply_text("Не понимаю. Блокирую!")

    def get_application(self):
        config = self.read_config()
        self.token = config["Bot"]["token"]
        return Application.builder().token(self.token).build()

    def setup_application(self, application):
        application.add_handler(CommandHandler("start", self.start))
        application.add_handler(CommandHandler("help", self.help_command))
        application.add_handler(CommandHandler("fish", self.fish))
        application.add_handler(CommandHandler("net", self.net))
        application.add_handler(CommandHandler("storage", self.storage))
        application.add_handler(CommandHandler("stats", self.stats))
        application.add_handler(CommandHandler("leaderboard", self.leaderboard))
        application.add_handler(CommandHandler("sell", self.sell))
        application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.echo)
        )
        return application

    def setup_logging(self):
        logging.basicConfig(
            filename="../logs/bot.log",
            filemode='a',
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
        )

    def run(self):
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)
