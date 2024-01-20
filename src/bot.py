import configparser
import logging
import os

import yaml
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from db_requests import DBConnector


class FishingBot:
    def __init__(self):
        self.token = None
        self.messages = self.read_texts()
        self.application = self.setup_bot()
        self.create_logs_directory()  # Добавляем создание каталога
        self.setup_logging()
        self.db_connector = DBConnector()
        print("Im alive!")

    def create_logs_directory(self):
        logs_directory = '../logs'
        if not os.path.exists(logs_directory):
            os.makedirs(logs_directory)

    def read_texts(self):
        with open("text/parsed_texts.yml", "r", encoding="utf-8") as file:
            texts = yaml.safe_load(file)
        return texts

    def get_text(self, var):
        return self.messages[var]

    def read_config(self):
        config = configparser.ConfigParser()
        config.read("settings/config.ini")
        return config

    async def start(self, update: Update, context):
        print("In start")
        user = update.effective_user
        print(" игрока")
        print(f"Create player {user.id}, {user.username}")
        self.db_connector.create_player(user.id, user.username)
        await update.message.reply_html(
            self.get_text("bot_start").format(user.mention_html()),
            reply_markup=None,
        )
        print("Игрок создан")

    async def fish(self, update: Update, context):
        user = update.effective_user

        await update.message.reply_html(
            self.get_text("bot_start").format(user.mention_html()),
            reply_markup=None,
        )

    async def help_command(self, update: Update, context):
        await update.message.reply_text("Help!")

    async def echo(self, update: Update, context):
        await update.message.reply_text("Не понимаю. Блокирую!")


    def setup_bot(self):
        config = self.read_config()
        token = config["Bot"]["token"]

        application = Application.builder().token(token).build()

        application.add_handler(CommandHandler("start", self.start))
        application.add_handler(CommandHandler("help", self.help_command))
        application.add_handler(CommandHandler("fish", self.help_command))
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
