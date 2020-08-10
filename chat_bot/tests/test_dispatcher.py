import unittest
from unittest.mock import patch

from tests.test_context import EXPECTED_SEARCH_FLIGHT_RESULT, EXPECTED_FILTERED_FLIGHT_RESULT
from fly_dispatcher import Dispatcher as ds

test_city_dict = "tests/test_cities.json"
test_flights_dict = "tests/test_flights.json"
test_from_city = "Москва"
test_to_city = "Нарния"
test_dispatch_date = "22-07-2020"
data_list = [["москва - нарния"], ["нарния - онтарио"]]


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.scheduled_flights_dict = test_flights_dict
        self.source_cities_dict = test_city_dict

    def test_search_flight(self):
        result = ds(from_city=test_from_city, to_city=test_to_city, dispatch_date=test_dispatch_date,
                    cities_file=test_city_dict,
                    schedules_file=test_flights_dict).search_flight()
        self.assertEqual(result, EXPECTED_SEARCH_FLIGHT_RESULT)

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
        self.assertEqual(EXPECTED_FILTERED_FLIGHT_RESULT, result)

    def test_search_non_straight_flight(self):
        result = ds("Москва", "Онтарио", "22-07-2020", test_city_dict, test_flights_dict).search_non_straight_flight()
        self.assertEqual([EXPECTED_FILTERED_FLIGHT_RESULT], result)


if __name__ == '__main__':
    unittest.main()
