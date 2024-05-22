from math import log

import matplotlib.pyplot as plt
import numpy as np


def calculate_rod_price(i):
    return 20 * (1.15) ** (i - 1)


def calculate_new_rod_price(i):
    return 20 * np.exp(i / 7)


def calculate_level_time(i):
    return 20 * 1.05 ** (i - 1)


def calculate_rod_cooldown(i):
    return 20 * (0.97) ** i


def calculate_new_rod_cooldown(i, start_y, denom):
    return pow(log((i + denom * 10 ** (1 / start_y)) / denom, 10), -1)


def calculate_net_price(i):
    return calculate_new_rod_price(i) * 3


def calculate_net_cooldown(i):
    return 100


def calculate_new_net_cooldown(i, start_y, denom):
    return pow(log((i + denom * 10 ** (1 / start_y)) / denom, 10), -1)


def calculate_net_catch_coef(i):
    return 1 + i * 0.1


def get_avg_catch(i):
    return 5 + i - 1


def get_fish_chances(count):
    fish_chances = {}
    old_fish_id = -2
    mid_fish_id = -1
    new_fish_id = 0
    old_fish_chance = 0.0
    mid_fish_chance = 0.0
    new_fish_chance = 0.0
    fish_types = 20  # Предположим, что у нас 10 разных типов рыб

    for i in range(count + 1):
        if i % 5 == 0 and (i // 5 + 1) <= fish_types:
            old_fish_id += 1
            mid_fish_id += 1
            new_fish_id += 1

            if i == 5:
                new_fish_chance = 0.85
                mid_fish_chance = 0.15
            elif i >= 10:
                old_fish_chance = 0.2
                mid_fish_chance = 0.75
                new_fish_chance = 0.05
        else:
            if i < 5:
                old_fish_chance = 0.0
                mid_fish_chance = 0.0
                new_fish_chance = 1.0
            elif i < 10:
                old_fish_chance = 0
                mid_fish_chance = 1.0 - 0.15 * (i - 4)
                new_fish_chance = 0.15 * (i - 4)
            else:
                old_fish_chance = max(0, old_fish_chance * 0.8)
                mid_fish_chance = max(0, mid_fish_chance * 0.9)
                new_fish_chance = 1.0 - old_fish_chance - mid_fish_chance

        if i == 0:
            new_fish_chance = 1

        if i < 5:
            fish_chances[new_fish_id] = new_fish_chance
        elif i < 10:
            fish_chances[new_fish_id] = new_fish_chance
            fish_chances[mid_fish_id] = mid_fish_chance
        else:
            fish_chances[new_fish_id] = new_fish_chance
            fish_chances[mid_fish_id] = mid_fish_chance
            fish_chances[old_fish_id] = old_fish_chance

    return fish_chances


def get_fish_profit(i):
    return (i - 1) ** 2


def get_fish_exp(i):
    return i ** 2


def calculate_avg_exp(i):
    total_rod_exp = 0
    total_net_exp = 0
    fish_chances = get_fish_chances(i)

    for key, value in fish_chances.items():
        total_rod_exp += value * get_avg_catch(i) * get_fish_exp(i)
        total_net_exp += value * get_avg_catch(i) * get_fish_exp(i) * calculate_net_catch_coef(i)

    rod_avg_exp_per_second = total_rod_exp / calculate_rod_cooldown(i)
    net_avg_exp_per_second = total_net_exp / calculate_net_cooldown(i)

    return rod_avg_exp_per_second, net_avg_exp_per_second


def calculate_new_avg_exp(i):
    total_rod_exp = 0
    total_net_exp = 0
    fish_chances = get_fish_chances(i)

    for key, value in fish_chances.items():
        total_rod_exp += value * get_avg_catch(i) * get_fish_exp(i)
        total_net_exp += value * get_avg_catch(i) * get_fish_exp(i) * calculate_net_catch_coef(i)

    rod_avg_exp_per_second = total_rod_exp / calculate_new_rod_cooldown(i, 10, 30)
    net_avg_exp_per_second = total_net_exp / calculate_new_net_cooldown(i, 300, 1000)

    return rod_avg_exp_per_second, net_avg_exp_per_second


def calculate_new_avg_profit(i):
    total_rod_profit = 0
    total_net_profit = 0
    fish_chances = get_fish_chances(i)

    for key, value in fish_chances.items():
        total_rod_profit += value * get_avg_catch(i) * get_fish_profit(i)
        total_net_profit += value * get_avg_catch(i) * get_fish_profit(i) * calculate_net_catch_coef(i)

    rod_avg_profit_per_second = total_rod_profit / calculate_new_rod_cooldown(i, 10, 30)
    net_avg_profit_per_second = total_net_profit / calculate_new_net_cooldown(i, 300, 100)

    return rod_avg_profit_per_second, net_avg_profit_per_second


def calculate_required_level_exp(level_time, rod_avg_exp_per_second, net_avg_exp_per_second):
    required_level_exp = []
    for i in range(len(level_time)):
        required_level_exp.append((rod_avg_exp_per_second[i] + net_avg_exp_per_second[i]) / level_time[i])
    return required_level_exp



# Создание массива значений i
i_values = np.arange(0, 150)

# Вычисление значений переменных для каждого значения i
rod_price_values = [calculate_rod_price(i) for i in i_values]
new_rod_price_values = [calculate_new_rod_price(i) for i in i_values]
rod_cooldown_values = [calculate_rod_cooldown(i) for i in i_values]
new_rod_cooldown_values = [calculate_new_rod_cooldown(i, start_y=10, denom=300) for i in i_values]
level_time = [calculate_level_time(i) for i in i_values]
rod_avg_exp_per_second = [calculate_avg_exp(i)[0] for i in i_values]
new_rod_avg_exp_per_second = [calculate_new_avg_exp(i)[0] for i in i_values]
net_avg_exp_per_second = [calculate_avg_exp(i)[1] for i in i_values]
new_net_avg_exp_per_second = [calculate_new_avg_exp(i)[1] for i in i_values]
new_required_level_exp = calculate_required_level_exp(level_time, new_rod_avg_exp_per_second, new_net_avg_exp_per_second)
required_level_exp = calculate_required_level_exp(level_time, rod_avg_exp_per_second, net_avg_exp_per_second)

# Создание графиков
# plt.figure(figsize=(10, 10))  # Увеличение размера фигуры

plt.plot(i_values, level_time)
plt.title('Потраченное время для нового уровня')
plt.xlabel('Уровень')
plt.ylabel('Время, с')
plt.grid(True)  # Добавление сетки

# plt.plot(i_values, required_level_exp, label='было')
# plt.plot(i_values, new_required_level_exp, label='стало')
# plt.title('Необходимый опыт для нового уровня')
# plt.xlabel('Уровень')
# plt.ylabel('Кол-во опыта')
# plt.grid(True)  # Добавление сетки
# plt.legend()  # Добавление легенды
# plt.savefig('../img/plots/required_level_exp_plot.pdf')

# plt.subplot(3, 1, 1)
# plt.plot(i_values, new_rod_avg_exp_per_second, label='удочка')
# plt.plot(i_values, new_net_avg_exp_per_second, label='сеть')
# plt.title('Средний опыт')
# plt.xlabel('Уровень (игрока и сети/удочки)')
# plt.ylabel('Кол-во опыта, exp/sec')
# plt.grid(True)  # Добавление сетки
# plt.legend()  # Добавление легенды
# plt.savefig('../img/plots/avg_exp_per_second_plot.pdf')
#
# plt.subplot(3, 1, 2)
# plt.plot(i_values, rod_avg_exp_per_second, label='было')
# plt.plot(i_values, new_rod_avg_exp_per_second, label='стало')
# plt.title('Средний опыт с удочки')
# plt.xlabel('Уровень (игрока и удочки)')
# plt.ylabel('Кол-во опыта, exp/sec')
# plt.grid(True)  # Добавление сетки
# plt.legend()  # Добавление легенды
# plt.savefig('../img/plots/avg_rod_exp_per_second_plot.pdf')
#
# plt.subplot(3, 1, 3)
# plt.plot(i_values, net_avg_exp_per_second, label='было')
# plt.plot(i_values, new_net_avg_exp_per_second, label='стало')
# plt.title('Средний опыт с сети')
# plt.xlabel('Уровень (игрока и сети)')
# plt.ylabel('Кол-во опыта, exp/sec')
# plt.grid(True)  # Добавление сетки
# plt.legend()  # Добавление легенды
# plt.savefig('../img/plots/avg_net_exp_per_second_plot.pdf')

# ---

# plt.subplot(3, 1, 1)
# plt.plot(i_values, rod_price_values, label='Было')
# plt.plot(i_values, new_rod_price_values, label='Стало')
# plt.title('Цена удочки')
# plt.xlabel('Уровень')
# plt.ylabel('Цена, $')
# plt.grid(True)  # Добавление сетки
# plt.legend()  # Добавление легенды
#
# plt.subplot(3, 1, 2)
# plt.plot(i_values, rod_cooldown_values, label='Было')
# plt.plot(i_values, new_rod_cooldown_values, label='Стало')
# plt.title('Перезарядка удочки')
# plt.xlabel('Уровень')
# plt.ylabel('Перезарядка, с')
# plt.grid(True)  # Добавление сетки
# plt.legend()  # Добавление легенды
# plt.savefig('../img/plots/rod_cooldown_plot.pdf')
#
# plt.subplot(3, 1, 3)
# plt.plot(i_values, level_time)
# plt.title('Время до нового уровня')
# plt.xlabel('Уровень')
# plt.ylabel('Среднее время, с')
# plt.grid(True)  # Добавление сетки
# plt.savefig('../img/plots/level_time_plot.pdf')

plt.tight_layout()
plt.show()
