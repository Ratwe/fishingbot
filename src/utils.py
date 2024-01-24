def translate_fish_name(fish_name):
    match fish_name:
        case 'cod':
            fish_name = 'треска'
        case 'salmon':
            fish_name = 'лосось'
        case 'puffer':
            fish_name = 'иглобрюх'

    return fish_name

def help():
    message = "*Команды бота*\n" \
              "/fish - ловить рыбу удочкой\n" \
              "/rod - тоже ловить рыбу удочкой\n" \
              "/net - ловить рыбу сетью\n" \
              "/start - приветственное сообщение\n" \
              "/storage - склад рыбы\n" \
              "/stats - статистика\n" \
              "/leaderboard - таблица лидеров\n" \
              "/sell - продать всю рыбу со склада\n" \
              "/store - магазин сетей и удочек\n" \
              "/up\\_rod - улучшение удочки\n" \
              "/up\\_rod\\_approve - подтвердить улучшение удочки\n" \
              "/up\\_net - улучшение сети\n" \
              "/up\\_net\\_approve - подтвердить улучшение сети\n" \
              "/help - помощь"

    return message