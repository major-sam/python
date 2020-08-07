import itertools
import re
from datetime import datetime, timedelta

import rstr

import fly_dispatcher as fd
from fly_dispatcher import Dispatcher as dp

CITIES_FILE = "json/avia_yandex_cites_id.json"
RE_CITY = re.compile(r'^[\w\-\s]{3,40}')
CITIES_DICT = fd.load_source(CITIES_FILE).keys()
CITIES_dLIST = list(k for k in CITIES_DICT)
CITIES_LIST_LOWER = list(k.lower() for k in CITIES_DICT)
DATE_PATTERN = re.compile(r"^(0[1-9]|[12]\d|3[01])-(0[1-9]|1[0-2])-[12]\d{3}$")
DATE_TIME_PATTERN = '%d-%m-%Y'
DEFAULT_LIST_SIZE = 5
RE_FLIGHT_MATCH = re.compile(r'^\w+\s*,\s*\d{1,2}\s*,\d{1,2}\s*$', flags=re.UNICODE)


def format_context(context):
    if context['straight_flight']:
        return f"\nРейс: {context['from_city'].capitalize()} > {context['to_city'].capitalize()}\n" \
               f"Дата: {context['flight_date']}\n" \
               f"Количество мест:{context['sits_count']}\n" \
               f"Комментарий к рейсу:{context['comment']}"
    else:
        return f"\nРейс: {context['from_city'].capitalize()} > {context['transfer_city'].capitalize()}" \
               f" > {context['to_city'].capitalize()}\n" \
               f"{context['from_city'].capitalize()} > {context['transfer_city'].capitalize()}\n" \
               f"Дата: {context['flight_from_date']}\n" \
               f"{context['transfer_city'].capitalize()} > {context['to_city'].capitalize()}\n" \
               f"Дата: {context['flight_from_date']}\n" \
               f"Количество мест: {context['sits_count']}\n" \
               f"Комментарий к рейсу: {context['comment']}"


def format_flights(flights_list, straight_flight, reverse=False):
    tab = "&#12288;"
    if not straight_flight:
        res = []
        for flights in flights_list:
            lists_to_zip = []
            for flight in flights:
                for key, val in flight.items():
                    r = []
                    if reverse:
                        val = val[-DEFAULT_LIST_SIZE:]
                    else:
                        val = val[:DEFAULT_LIST_SIZE]
                    for i, item in enumerate(val, start=1):
                        r.append(f"{i}. {item}")
                    r.insert(0, key.title())
                    lists_to_zip.append(r)
            for i in itertools.zip_longest(lists_to_zip[0], lists_to_zip[1], fillvalue=tab * 9 + f""):
                res.append((tab * 3).join(i))
            res.append("=" * 40)
        result = f"\n".join(res)
    else:
        lists_to_zip = []
        for flight in flights_list:
            for key, val in flight.items():
                r = []
                if reverse:
                    val = val[-DEFAULT_LIST_SIZE:]
                else:
                    val = val[:DEFAULT_LIST_SIZE]
                for i, item in enumerate(val, start=1):
                    r.append(f"{i}. {item}")
                r.insert(0, key.title())
                lists_to_zip.extend(r)
        result = f"\n".join(lists_to_zip)
    return result


def match_city(text):
    lower_text = text.lower()
    match = [a for a in CITIES_LIST_LOWER if lower_text in a]
    if len(match) == 1:
        return match
    else:
        r_text = re.search("^.{0,3}", lower_text).group(0)
        return [a for a in CITIES_LIST_LOWER if r_text in a]


def handler_from_city(text, context):
    match = match_city(text)
    if len(match) == 1 and len(text) > 3:
        context['from_city'] = match[0]
        context['straight_flight'] = True
        return [True, ""]
    else:
        return [False, f"\n".join(match).title() or f"\n".join(CITIES_LIST_LOWER).title()]


def handler_to_city(text, context):
    match = match_city(text)
    if len(match) == 1:
        context['to_city'] = match[0]
        flights = dp(from_city=context['from_city'], to_city=context['to_city'],
                     dispatch_date='01-01-1900').search_flight()
        if flights:
            return [True, f"{context['from_city'].capitalize()} > {context['to_city'].capitalize()}", True]
        else:
            return [False, "", True]
    else:
        return [False, f"\n".join(match).capitalize() or f"\n".join(CITIES_LIST_LOWER).title(), False]


def handler_return_true(text, context):
    return [True, f"{context['from_city']} > {context['to_city']}"]


def handler_return_flight_list(text, context):
    from_city = context['from_city']
    to_city = context['to_city']
    if DATE_PATTERN.match(text.lower()):
        h = datetime.now().hour
        m = datetime.now().minute
        if datetime.strptime(text, DATE_TIME_PATTERN).replace(hour=h, minute=m) + timedelta(
                minutes=15) > datetime.now():
            context['input_date'] = text
            if context['straight_flight']:
                flights = dp(from_city=from_city,
                             to_city=to_city,
                             dispatch_date=text).search_flight()
                last_flights = dp(from_city=from_city,
                                  to_city=to_city,
                                  dispatch_date="01-01-1914").search_flight()
            else:
                flights = dp(from_city=from_city,
                             to_city=to_city,
                             dispatch_date=text).search_non_straight_flight()
                last_flights = dp(from_city=from_city,
                                  to_city=to_city,
                                  dispatch_date="01-01-1914").search_non_straight_flight()
            if flights:
                context['flights'] = flights
                if context['straight_flight']:
                    transfer = "Выберите по номеру рейса"
                else:
                    transfer = "Введите город пересадки и номера рейсов через запятую " \
                               "\n Например: Владивосток, 1, 1"
                return [True, f"\n\n{format_flights(flights, context['straight_flight'])}\n\n{transfer}"]
            else:
                if last_flights:
                    return [False, f"\nРейсов на эту дату нет. Попробуйте ввести другую\n"
                                   f"Последние рейсы:\n"
                                   f"{format_flights(last_flights, context['straight_flight'], reverse=True)}"]
                else:
                    return [False, "\n Нет рейсов с пересадками"]
        else:
            return [False, f"\n{text} - Дата не может быть прошедшим числом"]
    else:
        return [False, f"\nНеверный формат даты {text}."]


def handler_flight_chooser(text, context):
    text = text.lower().replace(" " and f"\t", "")
    if context["straight_flight"]:
        if re.match(r'^\d{1,2}\s*$', text):
            flight_dates = context['flights'][0].get(f"{context['from_city']} - {context['to_city']}")
            text = int(text) - 1
            if len(flight_dates) > text:
                flight_date = flight_dates[text]
                plane = rstr.xeger("[A-Z] \d\d\d")
                context['plane'] = plane
                context['flight_date'] = flight_date
                return [True, f" {context['from_city'].capitalize()} > {context['to_city'].capitalize()}"]
            else:
                return [False, f" {text} - Такого номера нет в списке"]
        else:
            return [False, "\n Неопознанный ввод"]
    else:
        transfer_city = text.split(",")[0]
        match = match_city(transfer_city)
        if re.match(RE_FLIGHT_MATCH, text) and len(match) == 1:
            transfer_city = match[0]
            context['transfer_city'] = transfer_city
            from_transfer = int(text.split(",")[1]) - 1
            transfer_to = int(text.split(",")[2]) - 1
            flights = context['flights'][0]
            flights_from_dict = flights[0]
            flights_from = f"{context['from_city']} - {transfer_city}"
            flight_from_dates = flights_from_dict.get(flights_from)
            flights_to_dict = flights[1]
            flights_to = f"{transfer_city} - {context['to_city']}"
            flight_to_dates = flights_to_dict.get(flights_to)
            if from_transfer < 5 and transfer_to < 5 and \
                    len(flight_from_dates) > from_transfer and len(flight_to_dates) > transfer_to:
                flight_from_date = flight_from_dates[from_transfer]
                flight_to_date = flight_to_dates[transfer_to]
                plane_to = rstr.xeger(r"[A-Z] \d\d\d")
                context['plane_to'] = plane_to
                plane_from = rstr.xeger(r"[A-Z] \d\d\d")
                context['plane_from'] = plane_from
                context['flight_from_date'] = flight_from_date
                context['flight_to_date'] = flight_to_date
            else:
                return [False, f"\n{text.capitalize()} - Таких номеров рейсов нет в списке"]
            return [True, f"\n{context['from_city'].capitalize()} > {context['transfer_city'].capitalize()} "
                          f"> {context['to_city'].capitalize()}"]
        else:
            return [False, "\n Неопознанный ввод"]


def handler_place_count(text, context):
    if re.match(r'^\s*[1-5]\s*$', text):
        context['sits_count'] = text
        return [True, ""]
    else:
        return [False, "\n Неопознанный ввод"]


def handler_comment(text, context):
    context['comment'] = text
    return [False, format_context(context) + "\n Хотите внести изменения? (да\нет)"]


def handler_check_data(text, context):
    return [True, ""]


def handler_phone_number(text, context):
    text = re.sub(r'\s', "", text)
    if re.match(r'^(\+7|8)\d{10}$', text):
        context['phone'] = text
        return [False, "", True]
    else:
        return [False, "", False]


def handler_ticket_copy(text, context):
    return [True, ""]


def handler_end(text, context):
    context['scenario_success'] = True
    return [True, ""]
