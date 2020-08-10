import unittest
from copy import deepcopy
from unittest.mock import Mock, patch
import requests
from pony.orm import db_session, rollback
from vk_api.bot_longpoll import VkBotMessageEvent
from bot import Bot
import fly_dispatcher as dispatcher
from tests.test_scenarios import INPUTS, EXPECTED_OUTPUTS

cities_dict = dispatcher.load_source('tests/test_cities.json')
flights_dict = dispatcher.load_source('tests/test_flights.json')

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


def test_on_event_with_params(expected_inputs, expected_outputs):
    def patcher(arg):
        if arg == 'json/avia_yandex_cites_id.json':
            return cities_dict
        if arg == 'json/result.json':
            return flights_dict

    def patcher_request(*args, **kwargs):
        return Mock(json=lambda: {'owner_id': 'test_owner_id', 'media_id': 'test_media_id'})

    def patcher_json(*args, **kwargs):
        return args

    send_mock = Mock()
    photos_mock = Mock(return_value={'upload_url': 'http://test_url'})
    api_mock = Mock()
    save_mock = Mock(return_value=[{'owner_id': 'test_owner_id', 'id': 'test_media_id'}])
    api_mock.massages.send = send_mock
    api_mock.photos.saveMessagesPhoto = save_mock
    api_mock.photos.getMessagesUploadServer = photos_mock
    events = []
    for input_text in expected_inputs:
        event = deepcopy(TEST_EVENT)
        event['object']['message']['text'] = input_text
        events.append(VkBotMessageEvent(event))
    long_poller_mock = Mock()
    long_poller_mock.listen = Mock(return_value=events)
    with patch('bot.VkBotLongPoll', return_value=long_poller_mock), \
         patch('requests.post', side_effect=patcher_request), \
         patch('fly_dispatcher.load_source', side_effect=patcher):
        bot = Bot("", "")
        bot.api = api_mock
        bot.run()
    result_list = []
    real_outputs = []
    for call in api_mock.messages.mock_calls:
        if 'message' in call.kwargs:
            real_outputs.append(call.kwargs['message'])
    for row in real_outputs:
        string = expected_outputs[real_outputs.index(row)]
        if string in row:
            result_list.append(True)
        else:
            result_list.append(False)
    return False not in result_list


def isolate_db(test_func):
    def wrapper(*args, **kwargs):
        with db_session:
            test_func(*args, **kwargs)
            rollback()

    return wrapper


class MyTestCase(unittest.TestCase):
    def test_run(self):

        run_count = 2
        event = [{"1": "1"}]
        events = [event] * run_count
        long_poller_mock = Mock(return_value=events)
        long_poller_listen_mock = Mock()
        long_poller_listen_mock.listen = long_poller_mock
        with patch("bot.vk_api.VkApi"), \
             patch("bot.VkBotLongPoll", return_value=long_poller_listen_mock), \
             patch("bot_handlers.CITIES_FILE", return_value="test_cities.json"), \
             patch("fly_dispatcher.DEFAULT_SCHEDULE_FILE", return_value="test_flights.json"):
            bot = Bot("", "")
            bot.on_event = Mock()
            bot.run()
            bot.on_event.assert_called()
            bot.on_event.assert_any_call(event)
            a = bot.on_event.call_count, run_count
            self.assertEqual(bot.on_event.call_count, run_count)

    @isolate_db
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
            event = deepcopy(TEST_EVENT)
            event['object']['message']['text'] = input_text
            events.append(VkBotMessageEvent(event))
        long_poller_mock = Mock()
        long_poller_mock.listen = Mock(return_value=events)
        with patch('bot.VkBotLongPoll', return_value=long_poller_mock), \
             patch('fly_dispatcher.load_source', side_effect=patcher):
            bot = Bot("", "")
            bot.api = api_mock
            bot.run()
        self.assertEqual(api_mock.messages.send.call_count, len(INPUTS[0]))

    @isolate_db
    def test_on_event_0(self):
        result = test_on_event_with_params(expected_inputs=INPUTS[0], expected_outputs=EXPECTED_OUTPUTS[0])
        self.assertTrue(result)

    @isolate_db
    def test_on_event_1(self):
        result = test_on_event_with_params(expected_inputs=INPUTS[1], expected_outputs=EXPECTED_OUTPUTS[1])
        self.assertTrue(result)

    @isolate_db
    def test_on_event_2(self):
        with patch('ticket_generator.get_name_by_id', return_value="тест тестович"):
            result = test_on_event_with_params(expected_inputs=INPUTS[2], expected_outputs=EXPECTED_OUTPUTS[2])
            self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
