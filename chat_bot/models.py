from pony.orm import Database, Required, Json, Optional

from vk_token import DB_CONFIG

db = Database()
db.bind(**DB_CONFIG)


class UserState(db.Entity):
    user_id = Required(str, unique=True)
    scenario_name = Required(str)
    step_name = Required(str)
    context = Required(Json)
    sub_scenario_id = Required(int)


# {'comment': 'щл',
# 'flights':
# [{'москва - ливерпуль': ['21-10-2020 03:10']}],
# 'to_city': 'ливерпуль',
# 'from_city': 'москва',
# 'input_date': '10-08-2020',
# 'sits_count': '1',
# 'flight_date': '21-10-2020 03:10',
# 'straight_flight': True,
# 'phone': '+71234561212'}

# {'comment': '1',
# 'flights': [[{'москва - ливерпуль':
#                   ['21-10-2020 03:10']},
#            {'ливерпуль - мельбурн':
#                   ['24-08-2020 20:00', '07-09-2020 20:00', '21-09-2020 20:00', '05-10-2020 20:00', '19-10-2020 20:00',
#                   '26-10-2020 20:00', '02-11-2020 20:00', '09-11-2020 20:00', '16-11-2020 20:00', '23-11-2020 20:00',
#                   '30-11-2020 20:00', '07-12-2020 20:00', '14-12-2020 20:00', '21-12-2020 20:00', '28-12-2020 20:00',
#                   '04-01-2021 20:00', '11-01-2021 20:00', '18-01-2021 20:00', '25-01-2021 20:00']}]],
# 'to_city': 'мельбурн',
# 'from_city': 'москва',
# 'input_date': '10-08-2020',
# 'sits_count': '1',
# 'transfer_city': 'ливерпуль',
# 'flight_to_date': '24-08-2020 20:00',
# 'straight_flight': False,
# 'flight_from_date': '21-10-2020 03:10',
# 'phone': '+71231239090'}

class Registration(db.Entity):
    from_city = Required(str)
    to_city = Required(str)
    straight_flight = Required(bool)
    phone = Required(str)
    sits_count = Required(str)
    comment = Required(str)
    flight_date = Optional(str)
    flight_to_date = Optional(str)
    flight_from_date = Optional(str)


db.generate_mapping(create_tables=True)
