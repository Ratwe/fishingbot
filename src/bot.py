import configparser
import logging
import os

import yaml
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters

import catching
import leaderboard
import selling
import stats
import storage
import store
import utils
from db_requests import DBConnector


class FishingBot:
    def __init__(self):
        self.token = None
        self.admin_ids = self.get_admin_ids()
        self.messages = self.read_texts()
        self.application = self.get_application()
        self.application = self.setup_application(self.application)
        self.create_logs_directory()  # Добавляем создание каталога
        self.setup_logging()
        self.db_connector = DBConnector()
        self.menu_markup = self.get_menu_markup()
        print("Bot inited!")

    def create_logs_directory(self):
        logs_directory = '../logs'
        if not os.path.exists(logs_directory):
            os.makedirs(logs_directory)

    def read_texts(self):
        with open("text/parsed_texts.yml", "r", encoding="utf-8") as file:
            texts = yaml.safe_load(file)
        return texts

    async def send_cooldown_message(self, user_id, cooldown, tool):
        tool_name = None
        reply_markup = None
        if tool == "rod":
            tool_name = "удочки"
            reply_markup = ReplyKeyboardMarkup([[KeyboardButton('Ловить рыбу')], [KeyboardButton('Меню')]],
                                               resize_keyboard=True,
                                               one_time_keyboard=True)
        elif tool == "net":
            tool_name = "сети"
            reply_markup = ReplyKeyboardMarkup([[KeyboardButton('Забросить сеть')], [KeyboardButton('Меню')]],
                                               resize_keyboard=True,
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

    def get_admin_ids(self):
        config = self.read_config()
        return config["Admin"]["admin_ids"]

    def check_admin(self, user):
        if str(user.id) not in self.admin_ids:
            return False
        return True

    async def send_message(self, user_id, message, entities=None, parse_mode="Markdown"):
        await self.application.bot.send_message(chat_id=user_id, text=message, parse_mode=parse_mode,
                                                entities=entities)

    async def send_message_everyone(self, update: Update, context):
        user = update.effective_user
        if not self.check_admin(user):
            await self.send_message(user.id, "Нет прав!")
            return
        message = update.message.text.replace("/send_everyone", "")
        players = self.db_connector.get_all_players()
        for player in players:
            await self.send_message(player["player_id"], message, update.message.entities)

    async def all_users(self, update: Update, context):
        user = update.effective_user
        if not self.check_admin(user):
            await self.send_message(user.id, "Нет прав!")
            return
        players = self.db_connector.get_all_players()
        no_zero_lvl = 0
        for player in players:
            stats = self.db_connector.get_player_stats(player["player_id"])
            total_earning = stats[0]["total_earning"]
            if total_earning > 0:
                no_zero_lvl += 1
        message = f"Всего игроков {len(players)}.\nНенулевого уровня {no_zero_lvl}."
        await self.send_message(user.id, message)

    async def get_utm(self, update: Update, context):
        user = update.effective_user
        if not self.check_admin(user):
            await self.send_message(user.id, "Нет прав!")
            return
        message = "id, name, clicks\n"
        utms = self.db_connector.get_utm()
        for utm in utms:
            message += f"{utm['id']}, {utm['name']}, {utm['clicks']}\n"
        await self.send_message(user.id, message, parse_mode="html")

    async def add_utm(self, update: Update, context):
        user = update.effective_user
        if not self.check_admin(user):
            await self.send_message(user.id, "Нет прав!")
            return
        if len(context.args) != 2:
            await self.send_message(user.id, "Неправильный формат!\nПример: /add\_utm <utm\_name> <clicks>")
            return
        utm_name = context.args[0]
        clicks = context.args[1]
        self.db_connector.add_utm(utm_name, clicks)
        await self.send_message(user.id, f"{utm_name} with {clicks} clicks added!")

    async def start(self, update: Update, context):
        user = update.effective_user
        utm_name = context.args[0] if context.args else None
        stats = self.db_connector.get_player_stats(user.id)
        if not stats:  # пользователь не имеет статистики
            print(f"New player came with utm tag: {utm_name}")
            print(f"Inserting new player {user.id}, {user.username}")
            self.db_connector.insert_player(user.id, user.username)
            if not self.db_connector.get_utm(utm_name):  # если по этой метке перешли впервые
                print(f"Adding new utm: {utm_name}, 0")
                await self.db_connector.add_utm(utm_name, 1)
            self.db_connector.update_utm(utm_name)

        keyboard = [[KeyboardButton('Ловить рыбу')], [KeyboardButton('Продать рыбу')], [KeyboardButton('Меню')]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
        await update.message.reply_text(
            self.get_text("bot_start").format(user.mention_markdown_v2()),
            parse_mode="Markdown",
            reply_markup=reply_markup,
        )

    async def menu(self, update: Update, context):
        await update.message.reply_text("Выберите опцию меню:", parse_mode="Markdown", reply_markup=self.menu_markup)

    async def fish(self, update: Update, context):
        user = update.effective_user
        result = await catching.get_player_catch_fish(user.id, update.message.date, self, tool="rod")
        if result:
            keyboard = [[KeyboardButton('Ловить рыбу')], [KeyboardButton('Продать рыбу')], [KeyboardButton('Меню')]]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
            await update.message.reply_text(result, parse_mode="Markdown", reply_markup=reply_markup)

    async def net(self, update: Update, context):
        user = update.effective_user
        result = await catching.get_player_catch_fish(user.id, update.message.date, self, tool="net")
        if result:
            keyboard = [[KeyboardButton('Забросить сеть')], [KeyboardButton('Продать рыбу')], [KeyboardButton('Меню')]]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
            await update.message.reply_text(result, parse_mode="Markdown", reply_markup=reply_markup)

    async def storage(self, update: Update, context):
        user = update.effective_user
        result = storage.get_player_storage(user.id, self)
        await update.message.reply_text(result, parse_mode="Markdown", reply_markup=self.menu_markup)

    async def stats(self, update: Update, context):
        user = update.effective_user
        result = stats.player_stats(user.id, self)
        await update.message.reply_text(result, parse_mode="Markdown", reply_markup=self.menu_markup)

    async def leaderboard(self, update: Update, context):
        user = update.effective_user
        result = leaderboard.get_leaderboard(user.id, self)
        await update.message.reply_text(result, parse_mode="Markdown", reply_markup=self.menu_markup)

    async def sell(self, update: Update, context):
        user = update.effective_user
        result = selling.sell_all(user.id, self)
        await update.message.reply_text(result, parse_mode="Markdown", reply_markup=self.menu_markup)

    async def store(self, update: Update, context):
        keyboard = [[KeyboardButton("Улучшить удочку")], [KeyboardButton("Улучшить сеть")], [KeyboardButton("Меню")]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)

        await update.message.reply_text("В магазине можно улучшить удочку и сеть до нового уровня\n"
                                        "Улучшить удочку - /up_rod\n"
                                        "Улучшить сеть - /up_net", reply_markup=reply_markup)

    async def up_rod(self, update: Update, context):
        user = update.effective_user
        result = store.up_rod(user.id, self)
        keyboard = [[KeyboardButton('Подтвердить улучшение удочки')], [KeyboardButton("Магазин")],
                    [KeyboardButton("Меню")]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
        await update.message.reply_text(result, parse_mode="Markdown", reply_markup=reply_markup)

    async def up_rod_approve(self, update: Update, context):
        user = update.effective_user
        result = store.up_rod_approve(user.id, self)
        await update.message.reply_text(result, parse_mode="Markdown", reply_markup=self.menu_markup)

    async def up_net(self, update: Update, context):
        user = update.effective_user
        result = store.up_net(user.id, self)
        keyboard = [[KeyboardButton('Подтвердить улучшение сети')], [KeyboardButton("Магазин")],
                    [KeyboardButton("Меню")]]

        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
        await update.message.reply_text(result, parse_mode="Markdown", reply_markup=reply_markup)

    async def up_net_approve(self, update: Update, context):
        user = update.effective_user
        result = store.up_net_approve(user.id, self)
        await update.message.reply_text(result, parse_mode="Markdown", reply_markup=self.menu_markup)

    async def help(self, update: Update, context):
        result = utils.help()
        await update.message.reply_text(result, parse_mode="Markdown", reply_markup=self.menu_markup)

    async def echo(self, update: Update, context):
        await update.message.reply_text("Неизвестная команда. Помощь - /help")

    def get_application(self):
        config = self.read_config()
        self.token = config["Bot"]["token"]
        return Application.builder().token(self.token).build()

    def setup_application(self, application):
        application.add_handler(
            MessageHandler(filters.TEXT & filters.Regex(r'(?i)/send_everyone'), self.send_message_everyone))
        application.add_handler(CommandHandler("all_users", self.all_users))
        application.add_handler(CommandHandler("add_utm", self.add_utm))
        application.add_handler(CommandHandler("get_utm", self.get_utm))
        application.add_handler(CommandHandler("start", self.start))
        application.add_handler(MessageHandler(filters.TEXT & filters.Regex(r'(?i)Старт'), self.start))
        application.add_handler(CommandHandler("menu", self.menu))
        application.add_handler(MessageHandler(filters.TEXT & filters.Regex(r'(?i)Меню'), self.menu))
        application.add_handler(CommandHandler("help", self.help))
        application.add_handler(MessageHandler(filters.TEXT & filters.Regex(r'(?i)Помощь'), self.help))
        application.add_handler(CommandHandler("fish", self.fish))
        application.add_handler(CommandHandler("rod", self.fish))
        application.add_handler(MessageHandler(filters.TEXT & filters.Regex(r'(?i)рыбачить'), self.fish))
        application.add_handler(MessageHandler(filters.TEXT & filters.Regex(r'(?i)Ловить рыбу'), self.fish))

        application.add_handler(CommandHandler("storage", self.storage))
        application.add_handler(MessageHandler(filters.TEXT & filters.Regex(r'(?i)Склад'), self.storage))
        application.add_handler(CommandHandler("stats", self.stats))
        application.add_handler(MessageHandler(filters.TEXT & filters.Regex(r'(?i)Статистика'), self.stats))
        application.add_handler(MessageHandler(filters.TEXT & filters.Regex(r'(?i)Профиль'), self.stats))
        application.add_handler(CommandHandler("leaderboard", self.leaderboard))
        application.add_handler(CommandHandler("top", self.leaderboard))
        application.add_handler(MessageHandler(filters.TEXT & filters.Regex(r'(?i)Топ'), self.leaderboard))
        application.add_handler(CommandHandler("sell", self.sell))
        application.add_handler(MessageHandler(filters.TEXT & filters.Regex(r'(?i)Продать'), self.sell))
        application.add_handler(MessageHandler(filters.TEXT & filters.Regex(r'(?i)Продать рыбу'), self.sell))
        application.add_handler(CommandHandler("store", self.store))
        application.add_handler(MessageHandler(filters.TEXT & filters.Regex(r'(?i)Магазин'), self.store))
        application.add_handler(CommandHandler("up_rod", self.up_rod))
        application.add_handler(MessageHandler(filters.TEXT & filters.Regex(r'(?i)улучшить удочку'), self.up_rod))
        application.add_handler(CommandHandler("up_rod_approve", self.up_rod_approve))
        application.add_handler(
            MessageHandler(filters.TEXT & filters.Regex(r'(?i)подтвердить улучшение удочки'), self.up_rod_approve))
        application.add_handler(CommandHandler("up_net", self.up_net))
        application.add_handler(MessageHandler(filters.TEXT & filters.Regex(r'(?i)улучшить сеть'), self.up_net))
        application.add_handler(CommandHandler("up_net_approve", self.up_net_approve))
        application.add_handler(
            MessageHandler(filters.TEXT & filters.Regex(r'(?i)подтвердить улучшение сети'), self.up_net_approve))
        application.add_handler(CommandHandler("net", self.net))
        application.add_handler(MessageHandler(filters.TEXT & filters.Regex(r'(?i)Забросить сеть'), self.net))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.echo))
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

    def get_menu_markup(self):
        keyboard = [[KeyboardButton('Ловить рыбу'), KeyboardButton('Забросить сеть')],
                    [KeyboardButton('Продать рыбу'), KeyboardButton('Магазин')],
                    [KeyboardButton('Профиль'), KeyboardButton('Склад')],
                    [KeyboardButton('Топ'), KeyboardButton('Помощь')]]
        return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
