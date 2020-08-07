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


class Registration(db.Entity):
    user_id = Required(str)
    from_city = Required(str)
    to_city = Required(str)
    straight_flight = Required(bool)
    phone = Required(str)
    sits_count = Required(str)
    comment = Required(str)
    plane = Optional(str)
    plane_to = Optional(str)
    plane_from = Optional(str)
    transfer_plane = Optional(str)
    transfer_city = Optional(str)
    flight_date = Optional(str)
    flight_to_date = Optional(str)
    flight_from_date = Optional(str)


db.generate_mapping(create_tables=True)
