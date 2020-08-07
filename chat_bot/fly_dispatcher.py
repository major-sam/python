# coding: utf-8
import json
import os
import re
from datetime import datetime, timedelta

DEFAULT_SCHEDULE_FILE = "json/result.json"
DEFAULT_CITIES_FILE = "json/avia_yandex_cites_id.json"
DEFAULT_VARIANT_COUNT = 5
DEFAULT_NON_STRAIGHT_FLIGHT_BREAK = 5


def load_source(json_file):
    """:param json_file path to json file
    :type json_file str
    :return source_dict dict from json file
    :rtype source_dict dict"""
    if os.path.isfile(json_file):
        with open(json_file, 'r', encoding='utf-8') as file:
            s = file.read()
            source_dict = json.loads(s)
    else:
        print("use fly_generator to create source data")
        exit('-1')
    return source_dict


class Dispatcher:

    def __init__(self, from_city, to_city, dispatch_date,
                 cities_file=DEFAULT_CITIES_FILE, schedules_file=DEFAULT_SCHEDULE_FILE):
        self.dispatch_date = dispatch_date.lower()
        self.source_cities_dict = load_source(cities_file)
        self.scheduled_flights_dict = load_source(schedules_file)
        self.graph_picks = []
        self.cities_list = list(k.lower() for k in self.source_cities_dict.keys())
        self.from_city = from_city.lower()
        self.to_city = to_city.lower()
        self.date_pattern = re.compile(r"(0[1-9]|[12]\d|3[01])-(0[1-9]|1[0-2])-[12]\d{3}")

    def search_flight(self):
        """get straight flight
        :returns straight flights list
        :rtype list
        """
        straight_flight = f"{self.from_city} - {self.to_city}"
        if straight_flight in self.scheduled_flights_dict.keys():
            result = self.filter_by_date([[straight_flight]])
            for k, v in result[0].items():
                if v[0] is None:
                    return None
            return result
        else:
            return None

    def search_non_straight_flight(self):
        """:returns possible_tracks list of list of  possible fly tracks
        :rtype list"""
        result = []
        possible_tracks = []
        picks, fringes = self.create_graph_fringe_dict()
        current_from_fringes = fringes[picks[self.from_city]]
        for track_list in fringes:
            if self.to_city in track_list:
                fringe_index = fringes.index(track_list)
                transfer_city = None
                for _name, _id in picks.items():
                    if _id == fringe_index:
                        transfer_city = _name
                        break
                if transfer_city in current_from_fringes:
                    new_track = [[f"{self.from_city} - {transfer_city}"], [f"{transfer_city} - {self.to_city}"]]
                    possible_tracks.append(new_track)
                if len(possible_tracks) > DEFAULT_NON_STRAIGHT_FLIGHT_BREAK:
                    continue
        for track in possible_tracks:
            filtered_by_date_track = self.filter_by_date(track)
            # if filtered_by_date_track:
            temp_list = []
            transit_track_out = track[0][0]
            transit_track_in = track[1][0]
            if (filtered_by_date_track[0].get(transit_track_out) is None
                    or filtered_by_date_track[1].get(transit_track_in) is None):
                break
            date_time_pattern = '%d-%m-%Y %H:%M'
            for item in filtered_by_date_track:
                for key, value in item.items():
                    temp_list.append(value[0])
            if None not in temp_list:
                first_departure_datetime = datetime.strptime(filtered_by_date_track[0].get(transit_track_out)[0],
                                                             date_time_pattern)
                second_departure_datetime_list = filtered_by_date_track[1].get(transit_track_in)
                for date in second_departure_datetime_list:
                    second_departure_datetime = datetime.strptime(date, date_time_pattern)
                    if first_departure_datetime > second_departure_datetime + timedelta(hours=2):
                        filtered_by_date_track[1][transit_track_in].remove(date)
                result.append(filtered_by_date_track)
        return result if len(result) > 0 else None

    def create_graph_picks_dict(self):
        """
        :returns dict of graph picks
        :rtype dict"""
        cities = self.source_cities_dict
        graph_picks = {}
        graph_id = 0
        for key in cities.keys():
            graph_picks.update({key.lower(): graph_id})
            graph_id += 1
        return graph_picks

    def create_graph_fringe_dict(self):
        """
        :returns dict of graph fringes
        :rtype dict
        :returns list of fringes
        :rtype list"""
        flight = self.scheduled_flights_dict
        graph_picks_ids = self.create_graph_picks_dict()
        fringe_list = [[None] for i in range(len(graph_picks_ids))]
        for key in flight:
            from_name = list({str(key).split(" - ")[0]})[0]
            to_name = list({str(key).split(" - ")[1]})[0]
            from_name_id = graph_picks_ids.get(from_name)
            temp_val = fringe_list[from_name_id]
            if temp_val[0] is None:
                fringe_list[from_name_id] = [to_name]
            else:
                if temp_val.count(to_name) == 0:
                    temp_val.append(to_name)
                    fringe_list[from_name_id] = temp_val
        return graph_picks_ids, fringe_list

    def filter_by_date(self, data_list):
        result = []
        for schedule_list in data_list:
            schedule_val = schedule_list[0]
            date_list = self.scheduled_flights_dict[schedule_val]
            dates_result = []
            for date in date_list:
                date_pattern = '%d-%m-%Y %H:%M'
                flight_dt = datetime.strptime(date, date_pattern)
                req_dt = datetime.strptime(f'{self.dispatch_date} 00:00', date_pattern)
                if req_dt - timedelta(hours=2) < flight_dt:
                    dates_result.append(date)
            if len(dates_result) > 0:
                result.append({schedule_val: dates_result})
            else:
                # result = None
                result.append({schedule_val: [None]})
        return result
