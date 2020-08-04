import unittest
from copy import deepcopy
from datetime import datetime, timedelta
from unittest.mock import Mock, MagicMock, patch
from chat_bot.tests.test_context import CONTEXT_STRAIGHT, CONTEXT_NO_STRAIGHT
import chat_bot.fly_dispatcher as dp
import chat_bot.bot_handlers as handlers

tests_cities = 'tests/test_cities.json'
test_flights = 'tests/test_flights.json'

cities_dict = dp.load_source('tests/test_cities.json')
flights_dict = dp.load_source('tests/test_flights.json')


def patcher(arg):
    if arg == 'json/avia_yandex_cites_id.json':
        return cities_dict
    if arg == 'json/result.json':
        return flights_dict


class MyTestCase(unittest.TestCase):

    def test_handler_from_city(self):
        wrong_input = '1111'
        right_input = 'моск'
        context = MagicMock()
        self.assertTrue(handlers.handler_from_city(right_input, context)[0])
        self.assertFalse(handlers.handler_from_city(wrong_input, context)[0])

    def test_handler_to_city(self):
        wrong_input = ['1111', 'онтарио']
        right_input = 'нарн'
        mock = Mock(context=deepcopy(CONTEXT_STRAIGHT))
        with patch('chat_bot.fly_dispatcher.load_source', side_effect=patcher):
            self.assertTrue(handlers.handler_to_city(right_input, mock.context)[0])
            self.assertFalse(handlers.handler_to_city(wrong_input[0], mock.context)[0])
            self.assertFalse(handlers.handler_to_city(wrong_input[1], mock.context)[0])
            self.assertFalse(handlers.handler_to_city(wrong_input[0], mock.context)[-1])

    def test_handler_return_flight_list(self):
        wrong_input = ['102002020202012', (datetime.now() - timedelta(days=1)).strftime('%d-%m-%Y')]
        right_input_date = (datetime.now() + timedelta(days=1)).strftime('%d-%m-%Y')
        straight = deepcopy(CONTEXT_STRAIGHT)
        no_straight = deepcopy(CONTEXT_NO_STRAIGHT)
        mock_straight = Mock(context=straight)
        mock_no_straight = Mock(context=no_straight)
        with patch('chat_bot.fly_dispatcher.load_source', side_effect=patcher), \
             patch('chat_bot.bot_handlers.format_flights', return_value=""):
            self.assertTrue(handlers.handler_return_flight_list(right_input_date, mock_straight.context)[0])
            self.assertFalse(handlers.handler_return_flight_list(wrong_input[0], mock_straight.context)[0])
            self.assertFalse(handlers.handler_return_flight_list(wrong_input[1], mock_straight.context)[0])
            self.assertTrue(handlers.handler_return_flight_list(right_input_date, mock_no_straight.context)[0])
            self.assertFalse(handlers.handler_return_flight_list(wrong_input[0], mock_no_straight.context)[0])
            self.assertFalse(handlers.handler_return_flight_list(wrong_input[1], mock_no_straight.context)[0])

    def test_handler_flight_chooser(self):
        straight = deepcopy(CONTEXT_STRAIGHT)
        no_straight = deepcopy(CONTEXT_NO_STRAIGHT)
        mock_straight = Mock(context=straight)
        mock_no_straight = Mock(context=no_straight)
        wrong_input = ['12eqweqweqweqwe', '7', 'Нарния,9,2', '12e1weqwe,1,2']
        right_input_straight = '1'
        right_input_no_straight = 'Нарния,2,2'
        with patch('chat_bot.fly_dispatcher.load_source', side_effect=patcher):
            self.assertTrue(handlers.handler_flight_chooser(right_input_straight, mock_straight.context)[0])
            self.assertTrue(handlers.handler_flight_chooser(right_input_no_straight, mock_no_straight.context)[0])
            for wrong_i in wrong_input:
                self.assertFalse(handlers.handler_flight_chooser(wrong_i, mock_no_straight.context)[0])
                self.assertFalse(handlers.handler_flight_chooser(wrong_i, mock_no_straight.context)[0])

    def test_handler_phone_number(self):
        wrong_input = '123124141414'
        right_input = ['+71112223344', '82223334455']
        mock = Mock(context=deepcopy(CONTEXT_STRAIGHT))
        for right_i in right_input:
            self.assertTrue(handlers.handler_phone_number(right_i, mock.context)[0])
            self.assertEqual(right_i, mock.context['phone'])
        self.assertFalse(handlers.handler_phone_number(wrong_input, mock.context)[0])


if __name__ == '__main__':
    unittest.main()
