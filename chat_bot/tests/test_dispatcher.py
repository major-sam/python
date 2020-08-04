import unittest
from unittest.mock import patch

from chat_bot.fly_dispatcher import Dispatcher as ds

test_city_dict = "test_cities.json"
test_flights_dict = "test_flights.json"
test_from_city = "Москва"
test_to_city = "Нарния"
test_dispatch_date = "22-07-2020"
expected_search_flight_result = [{'москва - нарния': [
    '25-07-2020 19:15',
    '28-07-2020 19:15',
    '01-08-2020 19:15',
    '04-08-2020 19:15',
    '08-08-2020 19:15',
    '11-08-2020 19:15']
}]
data_list = [["москва - нарния"], ["нарния - онтарио"]]


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.scheduled_flights_dict = test_flights_dict
        self.source_cities_dict = test_city_dict

    def test_search_flight(self):
        result = ds(from_city=test_from_city, to_city=test_to_city, dispatch_date=test_dispatch_date,
                    cities_file=test_city_dict,
                    schedules_file=test_flights_dict).search_flight()
        self.assertEqual(result, expected_search_flight_result)

    def test_create_graph_picks_dict(self):
        result = ds("Москва", "Нарния", "10-10-1910", test_city_dict, test_flights_dict).create_graph_picks_dict()
        print()
        self.assertEqual({'москва': 0, 'нарния': 1, 'онтарио': 2, 'окленд': 3}, result)

    def test_create_graph_fringe_dict(self):
        result = ds("Москва", "Нарния", "10-10-1910", test_city_dict, test_flights_dict).create_graph_fringe_dict()
        print()
        self.assertEqual(({'москва': 0, 'нарния': 1, 'онтарио': 2, 'окленд': 3},
                          [['нарния', 'окленд'], ['онтарио'], ['окленд'], [None]]), result)

    def test_filter_by_date(self):
        result = ds("Москва", "Нарния", "22-07-2020", test_city_dict, test_flights_dict).filter_by_date(data_list)
        self.assertEqual([{'москва - нарния': [
            '25-07-2020 19:15', '28-07-2020 19:15', '01-08-2020 19:15', '04-08-2020 19:15',
            '08-08-2020 19:15', '11-08-2020 19:15']},
            {'нарния - онтарио': ['26-07-2020 05:25']}], result)

    def test_search_non_straight_flight(self):
        result = ds("Москва", "Онтарио", "22-07-2020", test_city_dict, test_flights_dict).search_non_straight_flight()
        self.assertEqual([[{'москва - нарния': ['25-07-2020 19:15',
                                                '28-07-2020 19:15',
                                                '01-08-2020 19:15',
                                                '04-08-2020 19:15',
                                                '08-08-2020 19:15',
                                                '11-08-2020 19:15']},
                           {'нарния - онтарио': ['26-07-2020 05:25']}]], result)


if __name__ == '__main__':
    unittest.main()
