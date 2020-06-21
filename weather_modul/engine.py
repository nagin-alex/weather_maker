import datetime

from weather_modul.databases_upd import DataBaseUpdater, Weather
from weather_modul.weather_maker import WeatherMaker
from weather_modul.img_maker import ImageMaker
from weather_modul.settings import CACHE_RESULT


db = DataBaseUpdater()
parser = WeatherMaker()


def update_db():
    try:
        first_date = input(' Введите начальную дату в формате дд.мм.гггг : ').split('.')
        end_date = input(' Введите конечную дату в формате дд.мм.гггг : ').split('.')
        parsing_list = parser.parser(first_date=datetime.date(year=int(first_date[2]),
                                                              month=int(first_date[1]),
                                                              day=int(first_date[0])),
                                     end_date=datetime.date(year=int(end_date[2]),
                                                            month=int(end_date[1]),
                                                            day=int(end_date[0])))
        db.update_db(add_list=parsing_list)
        print(f'\n Обновили базу данных, используй get для извлечения данных \n')
    except:
        print(f'\nЧто-то пошло не так, повторите попытку\n')
        update_db()


def get_data():
    try:
        first_date = input(' Введите начальную дату в формате дд.мм.гггг : ').split('.')
        end_date = input(' Введите конечную дату в формате дд.мм.гггг : ').split('.')
        first_date = datetime.date(year=int(first_date[2]),
                                   month=int(first_date[1]),
                                   day=int(first_date[0]))
        end_date = datetime.date(year=int(end_date[2]),
                                 month=int(end_date[1]),
                                 day=int(end_date[0]))
        with open(CACHE_RESULT, 'w', encoding='utf-8') as file:
            for weather in Weather.select().where((Weather.date >= first_date) & (Weather.date <= end_date)):
                file.write(f'date: {weather.date.date()}\n')
                file.write(f'temp: {weather.temp_now}\n')
                file.write(f'weather: {weather.weather}\n')
                file.write('\n')
        print(
            f'\n Завершили функцию, показатели сохранены, используй view для просмтотра или make для создания '
            f'открыток \n')
    except:
        print(f'\nЧто-то пошло не так, повторите попытку\n')
        get_data()


def image_make():
    with open(CACHE_RESULT, 'r', encoding='utf-8') as file:
        dict_weather = {}
        for line in file:
            if line is '\n':
                make = ImageMaker(dict_weather)
                make.run()
                dict_weather = {}
            else:
                key, val = line.strip().split(':')
                dict_weather[key] = val
    open(CACHE_RESULT, 'w').close()
    print(f'\n Завершили создание картинок, кэш очищен, используй get заново\n')


def view_weather():
    with open(CACHE_RESULT, 'r', encoding='utf-8') as file:
        dict_weather = {}
        for line in file:
            if line is '\n':
                print(f'{dict_weather["date"]} {dict_weather["temp"]} {dict_weather["weather"]}')
                dict_weather = {}
            else:
                key, val = line.strip().split(':')
                dict_weather[key] = val


def clear():
    open(CACHE_RESULT, 'w').close()
    print(f'\nКэш очищен, используй get заново\n')

#  1) Перенесите COMMAND, help_command (лучше назвать "описание" и сделать константой) и run() в главный модуль
#  2) По всему проекту пути к файлам надо вынести в константы, можно даже в отдельный файл настроек проекта


week_back = datetime.timedelta(days=7)
today = datetime.datetime.today()
list_result = parser.parser((today - week_back), today)
db.update_db(add_list=list_result)
