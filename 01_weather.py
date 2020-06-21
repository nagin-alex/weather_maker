
from weather_modul.engine import update_db, get_data, image_make, view_weather, clear
import argparse


COMMAND = {'upd': update_db, 'get': get_data, 'make': image_make, 'view': view_weather, 'clear': clear}
DESCRIPTION = f'С помощью данного скрипта вы сможете созавать открытки с архивом погоды в Москве(начиная с 2015).\n' \
       'Для начала загрузите в Базу данных нужный промежуток используя команду upd.\n' \
       'По умолчанию в базе храниться архив за последние 7 дней.\n' \
       'Использую get для сохранения в кэше нужного интервала дат и дальнейше работы.\n' \
       'С помощь view вы можете увидеть данные с которыми работаете.\n' \
       'C помощью make вы сможете созданить открытки.\n' \
       'clear очистит базу данных.'


def run():
    pars = argparse.ArgumentParser()
    pars.add_argument('command', choices=COMMAND.keys(), help=DESCRIPTION)
    args = pars.parse_args()
    func = COMMAND[args.command]
    func()


run()

