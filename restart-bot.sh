#!/bin/bash

BOT_PATH="./src/main.py"

check_bot_status() {
    ps aux | grep "$BOT_PATH" | grep -v grep
}

start_bot() {
    echo "Запуск бота..."
    cd $(dirname "$BOT_PATH")
    python3 "$(basename "$BOT_PATH")"
}

restart_bot() {
    stop_bot
    start_bot
    echo "Бот перезапущен."
}

stop_bot() {
    echo "Остановка бота..."
    pkill -f "$BOT_PATH"
    sleep 2
}

if check_bot_status; then
    restart_bot
else
    start_bot
    echo "Бот запущен"
fi
