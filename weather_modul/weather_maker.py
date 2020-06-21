from datetime import date, datetime
import re
import requests
from bs4 import BeautifulSoup
from weather_modul.settings import PARSER_URL


class WeatherMaker:
    """
    Парсим нужный сайт, класс рабоает только с определённым сайтом, использоваться другой нельзя
    """
    def __init__(self):
        self.url = PARSER_URL
        self.user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0'
        self.date_now = datetime.now()
        self.list_months = [
            'january',
            'february',
            'march',
            'april',
            'may',
            'june',
            'july',
            'august',
            'september',
            'october',
            'november',
            'december']

    def parser(self, first_date, end_date):
        """
        Ищем даты за указанный диапазон с учётом особенностей сайта.

        :param first_date: дата с которой нужно взять информацию
        :param end_date: дата по которую нужно взять информацию
        :return: список словарей с данными погоды
        """
        list_result = []

        for years in range(first_date.year, end_date.year + 1):
            for month in self.list_months:
                if years == first_date.year and self.list_months.index(month) + 1 < first_date.month:
                    pass
                elif years == end_date.year and self.list_months.index(month) + 1 > end_date.month:
                    pass
                else:
                    response = requests.get(url=f'{self.url}/{month}-{years}/',
                                            headers={'User-Agent': self.user_agent})
                    html_doc = BeautifulSoup(response.text, features='html.parser')
                    for day in range(1, 32):
                        if years == first_date.year and self.list_months.index(
                                month) + 1 == first_date.month and day < first_date.day:
                            pass
                        elif years == end_date.year and self.list_months.index(
                                month) + 1 == end_date.month and day > end_date.day:
                            pass
                        else:
                            temperature_now = html_doc.find_all(href=re.compile(f"{day}-{month}"))
                            if temperature_now:
                                list_result.append({
                                    'date': date(years, self.list_months.index(
                                        month)+1, day),
                                    'weather': temperature_now[0].i['title'],
                                    'temp': temperature_now[0].span.text
                                })
        return list_result
