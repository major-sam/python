import unittest
from copy import deepcopy
from unittest.mock import Mock, patch
from vk_api.bot_longpoll import VkBotMessageEvent
from chat_bot.bot import Bot
import chat_bot.fly_dispatcher as dispatcher
from chat_bot.tests.test_scenarios import INPUTS, EXPECTED_OUTPUTS

cities_dict = dispatcher.load_source('tests/test_cities.json')
flights_dict = dispatcher.load_source('tests/test_flights.json')


class MyTestCase(unittest.TestCase):
    TEST_EVENT = {
        'group_id': 179047423,
        'type': 'message_new',
        'object': {
            'message': {
                'date': 1596444772, 'from_id': 00000000, 'id': 2442,
                'out': 0, 'peer_id': 00000000, 'text': 'тест',
                'conversation_message_id': 2442, 'fwd_messages': [],
                'important': False, 'random_id': 0, 'attachments': [],
                'is_hidden': False
            }
        }
    }

    def test_run(self):
        run_count = 2
        event = [{"1": "1"}]
        events = [event] * run_count
        long_poller_mock = Mock(return_value=events)
        long_poller_listen_mock = Mock()
        long_poller_listen_mock.listen = long_poller_mock

        with patch("chat_bot.bot.vk_api.VkApi"), \
             patch("chat_bot.bot.VkBotLongPoll", return_value=long_poller_listen_mock), \
             patch("chat_bot.bot_handlers.CITIES_FILE", return_value="test_cities.json"), \
             patch("chat_bot.fly_dispatcher.DEFAULT_SCHEDULE_FILE", return_value="test_flights.json"):
            bot = Bot("", "")
            bot.on_event = Mock()
            bot.run()
            bot.on_event.assert_called()
            bot.on_event.assert_any_call(event)
            self.assertEqual(bot.on_event.call_count, run_count)

    def test_on_event(self):
        def patcher(arg):
            if arg == 'json/avia_yandex_cites_id.json':
                return cities_dict
            if arg == 'json/result.json':
                return flights_dict

        send_mock = Mock()
        api_mock = Mock()
        api_mock.massages.send = send_mock
        events = []
        for input_text in INPUTS[0]:
            event = deepcopy(self.TEST_EVENT)
            event['object']['message']['text'] = input_text
            events.append(VkBotMessageEvent(event))

        long_poller_mock = Mock()
        long_poller_mock.listen = Mock(return_value=events)
        with patch('chat_bot.bot.VkBotLongPoll', return_value=long_poller_mock), \
             patch('chat_bot.fly_dispatcher.load_source', side_effect=patcher):
            bot = Bot("", "")
            bot.api = api_mock
            bot.run()
        assert len(api_mock.mock_calls) == len(INPUTS[0])

    def test_on_event_0_with_params(self, expected_inputs=None, expected_outputs=None):
        if expected_outputs is None:
            expected_outputs = EXPECTED_OUTPUTS[0]
        if expected_inputs is None:
            expected_inputs = INPUTS[0]

        def patcher(arg):
            if arg == 'json/avia_yandex_cites_id.json':
                return cities_dict
            if arg == 'json/result.json':
                return flights_dict

        send_mock = Mock()
        api_mock = Mock()
        api_mock.massages.send = send_mock
        events = []
        for input_text in expected_inputs:
            event = deepcopy(self.TEST_EVENT)
            event['object']['message']['text'] = input_text
            events.append(VkBotMessageEvent(event))
        long_poller_mock = Mock()
        long_poller_mock.listen = Mock(return_value=events)
        with patch('chat_bot.bot.VkBotLongPoll', return_value=long_poller_mock), \
             patch('chat_bot.fly_dispatcher.load_source', side_effect=patcher):
            bot = Bot("", "")
            bot.api = api_mock
            bot.run()
        result_list = []
        real_outputs = []
        for call in api_mock.mock_calls:
            real_outputs.append(call.kwargs['message'])
        for row in real_outputs:
            string = expected_outputs[real_outputs.index(row)]
            if string in row:
                result_list.append(True)
            else:
                result_list.append(False)
        return False not in result_list

    def test_on_event_1(self):
        result = self.test_on_event_0_with_params(expected_inputs=INPUTS[1], expected_outputs=EXPECTED_OUTPUTS[1])
        self.assertTrue(result)

    def test_on_event_2(self):
        result = self.test_on_event_0_with_params(expected_inputs=INPUTS[2], expected_outputs=EXPECTED_OUTPUTS[2])
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
