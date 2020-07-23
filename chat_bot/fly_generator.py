import json
import random
import datetime

CITIES_FILE = "json/avia_yandex_cites_id.json"
RESULT_FILE = "json/result.json"
EXCLUDE_FLIGHT_TRACKS = ["москва-мельбурн", "санкт-петербург-мельбурн", "мельбурн-москва", "мельбурн-санкт-петербург"]


def get_json(json_file):
    """:param json_file json file with cities
     :returns dict('city':yandex_params)"""
    with open(json_file, 'r', encoding='utf-8') as file:
        s = file.read()
        match_dict = json.loads(s)
    return match_dict


def write_to_json(source_dict):
    """:param source_dict json json file with result dict"""
    with open(RESULT_FILE, 'w', encoding='utf-8') as fp:
        json.dump(source_dict, fp, indent=4, ensure_ascii=False)


def generate_sch_flights(count, from_town, to_town, week_days=None, month_days=None):
    """:param count - int count of iteration for flight
    :param from_town - str departure town
    :param to_town - str target town
    :param week_days - list of days of week for scheduled
    :param month_days - list of day of month for schedule
    :returns dict of scheduled flights"""
    key = f"{from_town}-{to_town}"
    result = {key: []}
    time = f"{random.randrange(0, 24):02d}:{random.randrange(0, 60, 5):02d} "
    date = datetime.datetime.now().replace(day=1)
    while count > 0:
        if key in EXCLUDE_FLIGHT_TRACKS:
            break
        val = result.get(key)
        if week_days is not None and date.isoweekday() in week_days:
            weekday_val = f"{date.day:02d}-{date.month:02d}-{date.year} {time}"
            count -= 1
        else:
            weekday_val = None
        if month_days is not None and date.day in month_days:
            month_val = f"{date.day:02d}-{date.month:02d}-{date.year} {time}"
            count -= 1
        else:
            month_val = None
        if weekday_val == month_val is not None:
            val.append(weekday_val)
        elif weekday_val is not None:
            val.append(weekday_val)
        elif month_val is not None:
            val.append(month_val)
        result[key] = val
        date = date + datetime.timedelta(days=1)
    return result


def generate_random_flights(count, c_list):
    """:param count - int count of iteration for flight
    :param c_list - list of towns
    :returns dict of random flights"""
    result = {}
    while count > 0:
        from_city, to_city = random.sample(set(c_list), 2)
        key = f"{from_city}-{to_city}"
        if key in EXCLUDE_FLIGHT_TRACKS:
            break
        time = f"{random.randrange(0, 24):02d}:{random.randrange(0, 60, 5):02d} "
        additional_val = f"2020-{random.randrange(1, 12):02d}-{random.randrange(1, 30):02d} {time}"
        if key in result.keys():
            val = result.get(key)
            val.append(additional_val)
            result[key] = val
        else:
            result.update({key: [additional_val]})
        count -= 1
    return result


def generate_flight_dict(cites_list, weekly_scheduled_flight_count,
                         monthly_scheduled_flight_count, random_flight_count):
    """:param cites_list - list of cities
    :param monthly_scheduled_flight_count - list [[int, [int, int,...]],...] fly count,
            [fly days of week (iso week days)]
    :param  weekly_scheduled_flight_count - list [[int, [int, int,...]],...] fly count, [fly days of month]
    :param random_flight_count - int count for random flight
    :returns mixed dict of flights"""
    result = generate_random_flights(random_flight_count, cites_list)
    for flight_count in weekly_scheduled_flight_count:
        from_city, to_city = random.sample(set(cities_list), 2)
        result.update(generate_sch_flights(flight_count[0], from_city, to_city, week_days=flight_count[1]))
    for flight_count in monthly_scheduled_flight_count:
        from_city, to_city = random.sample(set(cities_list), 2)
        result.update(generate_sch_flights(flight_count[0], from_city, to_city, month_days=flight_count[1]))
    return result


yandex_dict = get_json(CITIES_FILE)
cities_list = list(map(lambda x: x.lower(), [*yandex_dict]))
# lists [[count,[week day\ month day, ...]],...]
w_sch_fl_count = [[10, [1, 4]], [12, [2, 6]], [30, [1]], [5, [1, 3, 6]]]
m_sch_fl_count = [[5, [5, 15, 25]], [4, [10, 20]], [6, [7]]]
dict_to_json = generate_flight_dict(cites_list=cities_list, weekly_scheduled_flight_count=w_sch_fl_count,
                                    monthly_scheduled_flight_count=m_sch_fl_count, random_flight_count=100)
write_to_json(dict_to_json)
