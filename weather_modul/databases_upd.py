import peewee

database_proxy = peewee.DatabaseProxy()


class BaseTable(peewee.Model):
    class Meta:
        database = database_proxy


class Weather(BaseTable):
    """
    Иницилизируем базу данных
    """
    date = peewee.DateTimeField()
    temp_now = peewee.CharField()
    weather = peewee.CharField()


class DataBaseUpdater:
    """
    Обновляем базу данных.
    Проверяем есть ли уже запись в базе по дате, с помощью исключенией, и если нет, то добовляем.
    На вход add_list = список словарей
    """

    def update_db(self, add_list):
        for weather in add_list:
            try:
                date = Weather.get(Weather.date == weather.get('date'))
            except:
                Weather.create(
                    date=weather.get('date'),
                    temp_now=weather.get('temp'),
                    weather=weather.get('weather')
                )


database = peewee.PostgresqlDatabase('mydb', user='avis')
database_proxy.initialize(database)
database.create_tables([Weather])


