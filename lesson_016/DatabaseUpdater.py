from pprint import pprint

import peewee
from playhouse.db_url import connect
import database as db
from WheatherMaker import WeatherMaker as wm
# TODO Вы всё подготовили для использования коннекта, но решили им не пользоваться?)
# TODO По сути это ещё один способ создать тот же объект, внутри модуля с connect есть ассоциация
# TODO 'sqlite': SqliteDatabase
# TODO т.е. если вы используете путь вроде 'sqlite:///weather.db'
# TODO то он сопоставит первую часть по словарю, и создаст такой же объект по пути, указанному во второй части
sql_lite_database = peewee.SqliteDatabase("python_base\lesson_016\default2.db")
db.proxy.initialize(sql_lite_database)
sql_lite_database.create_tables([db.Date, db.DayStats, db.NightStats], safe=True)


def save_data(input_dict=None):
    """

    :param input_dict: dict from console input or file
    :return:
    """
    if input_dict is None:
        data = wm().get_data()
    else:
        data = input_dict
    for date in data.keys():
        for day_times in data.get(date):
            db.Date.insert(date).on_conflict('REPLACE').execute()
            for day_time in day_times.keys():
                result = day_times.get(day_time)
                result.update({'daytime': day_time})
                result.update({'date': date})
                if day_time == "День":
                    db.DayStats.replace(result).on_conflict(action='REPLACE', conflict_target=db.DayStats.date_id) \
                        .execute()
                elif day_time == "Ночь":
                    db.NightStats.replace(result).on_conflict(action='REPLACE', conflict_target=db.NightStats.date_id) \
                        .execute()


def get_data(date):
    """

    :param date: str in \d\d\d\d-\d\d-\d\d format
    :return: dict
    """
    day, night = None, None
    # TODO В целом тут это ещё терпимо, но если программа работает с объемами данных побольше
    # TODO То ей нужно будет отдельно писать функцию/метод, чтобы тянуть сразу множество записей (не за один день)
    day_result = db.DayStats.select().where(db.DayStats.date == date)
    for result in day_result:
        day = {result.daytime: {'temperature': result.temperature,
                                'sky': result.sky,
                                'temperature_feeling': result.temperature_feeling,
                                'rain_probability': result.rain_probability,
                                'pressure': result.pressure,
                                'humidity': result.humidity}
               }
    night_result = db.NightStats.select().where(db.NightStats.date == date)
    for result in night_result:
        night = {result.daytime: {'temperature': result.temperature,
                                  'sky': result.sky,
                                  'temperature_feeling': result.temperature_feeling,
                                  'rain_probability': result.rain_probability,
                                  'pressure': result.pressure,
                                  'humidity': result.humidity}
                 }
    res = {date: [day, night]}
    return res


#save_data()
#get_data("2020-07-15")
#print(get_data("1234-12-12"))