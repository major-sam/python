from playhouse.db_url import connect
import database as db
from WheatherMaker import WeatherMaker as wm

db_url = 'sqlite:///lesson_016/default2.db'
sql_lite_database = connect(db_url)
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


def get_data(dates):
    """
    :param dates:list of str in \d\d\d\d-\d\d-\d\d format
    :return: dict
    """
    res = {}
    day, night = None, None
    if len(dates) > 1:
        day_result = db.DayStats.select().where(db.DayStats.date.in_(dates))
        night_result = db.NightStats.select().where(db.NightStats.date.in_(dates))
    else:
        day_result = db.DayStats.select().where(db.DayStats.date == dates[0])
        night_result = db.NightStats.select().where(db.NightStats.date == dates[0])
    for result in day_result:
        day = {result.daytime: {'temperature': result.temperature,
                                'sky': result.sky,
                                'temperature_feeling': result.temperature_feeling,
                                'rain_probability': result.rain_probability,
                                'pressure': result.pressure,
                                'humidity': result.humidity}
               }
    for result in night_result:
        night = {result.daytime: {'temperature': result.temperature,
                                  'sky': result.sky,
                                  'temperature_feeling': result.temperature_feeling,
                                  'rain_probability': result.rain_probability,
                                  'pressure': result.pressure,
                                  'humidity': result.humidity}
                 }
    for date in dates:
        res.update({date: [day, night]})
    return res

# save_data()
# pprint(get_data(["2020-07-15", "2020-07-16", "2020-07-17"]))
# print(get_data("1234-12-12"))
