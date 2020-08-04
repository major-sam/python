from random import randint

from chat_bot.vk_token import token, group_id
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import logging
import chat_bot.scenarios as sc
import chat_bot.bot_handlers as handlers

log = logging.getLogger("bot")


def config_logs():
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    stream_handler.setLevel(logging.INFO)
    log.addHandler(stream_handler)
    file_handler = logging.FileHandler("log/bot.log", encoding="utf-8")
    file_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    file_handler.setLevel(logging.DEBUG)
    log.addHandler(file_handler)
    log.setLevel(logging.DEBUG)


class UserState:
    def __init__(self, scenario_name, step_name, context=None):
        self.scenario_name = scenario_name
        self.step_name = step_name
        self.context = context or {}


class Bot:
    """
    Bot for flight ticket registration
    Use python 3.8
    """

    def __init__(self, my_group_id, my_token):
        self.group_id = my_group_id
        self.token = my_token
        self.vk = vk_api.VkApi(token=self.token)
        self.long_poller = VkBotLongPoll(self.vk, self.group_id)
        self.api = self.vk.get_api()
        self.no_straight_flight_switcher_user_states = dict()
        self.registration_user_states = dict()
        self.switcher_check = dict()
        self.change_user_data = dict()

    def run(self):
        for event in self.long_poller.listen():
            try:
                self.on_event(event)
            except Exception:
                log.exception("Ошибка в обработке события")

    def on_event(self, event):
        if event.type != VkBotEventType.MESSAGE_NEW:
            log.debug("not supported type %s", event.type)
            return
        text = event.object.message['text'].lower()
        user_id = event.object.message['peer_id']
        if text in sc.DEFAULT_EXIT[0]:
            if user_id in self.no_straight_flight_switcher_user_states:
                self.no_straight_flight_switcher_user_states.pop(user_id)
            if user_id in self.registration_user_states:
                self.registration_user_states.pop(user_id)
            text_to_send = sc.DEFAULT_EXIT[1]
        elif text in sc.DEFAULT_HELP:
            text_to_send = sc.DEFAULT_ANSWER
        elif user_id in self.change_user_data:
            for intent in sc.CHANGE_DATA:
                if any(_token in text for _token in intent['tokens']):
                    self.change_user_data[user_id].step_name = intent['next_step']
                    self.registration_user_states[user_id] = self.change_user_data.pop(user_id)
                    text_to_send = intent['answer']
                    break
            else:
                text_to_send = f"{sc.DEFAULT_WRONG_FIELD}\n{text}"
        elif user_id in self.switcher_check:
            for intent in sc.CHECK_SWITCHER:
                if any(_token in text for _token in intent['tokens']):
                    if intent['name'] == 'yes':
                        text_to_send = intent['answer']
                        self.switcher_check[user_id].step_name = intent['next_step']
                        self.change_user_data[user_id] = self.switcher_check.pop(user_id)
                    else:
                        self.switcher_check[user_id].step_name = intent['next_step']
                        self.registration_user_states[user_id] = self.switcher_check.pop(user_id)
                        text_to_send = self.continue_scenario(user_id, text)
                    break
            else:
                text_to_send = sc.DEFAULT_WRONG_INPUT
        elif user_id in self.no_straight_flight_switcher_user_states:
            for intent in sc.NO_STRAIGHT_FLIGHT_SWITCHER:
                if any(_token in text for _token in intent['tokens']):
                    if intent['next_step']:
                        self.no_straight_flight_switcher_user_states[user_id].step_name = intent['next_step']
                        self.no_straight_flight_switcher_user_states[user_id].context['straight_flight'] = False
                        self.registration_user_states[user_id] = \
                            self.no_straight_flight_switcher_user_states.pop(user_id)
                        text_to_send = self.continue_scenario(user_id, text)
                    else:
                        self.no_straight_flight_switcher_user_states.pop(user_id)
                        text_to_send = intent['answer']
                    break
            else:
                text_to_send = f"Неопознаный ввод.\n{sc.DEFAULT_NO_STRAIGHT_FLIGHT_SWITCHER_ANSWER}"
        elif user_id in self.registration_user_states:
            text_to_send = self.continue_scenario(user_id, text)
        else:
            for intent in sc.INTENTS_MAIN:
                if any(_token in text for _token in intent['tokens']):
                    if intent['answer']:
                        text_to_send = intent['answer']
                    else:
                        text_to_send = self.start_scenario(intent['scenario'], user_id)
                    break
            else:
                text_to_send = sc.DEFAULT_ANSWER
        log.info(event.type)

        self.api.messages.send(message=text_to_send,
                               random_id=randint(0, 2 ** 24),
                               peer_id=user_id)

    def start_scenario(self, scenario_name, user_id):
        scenario = sc.SCENARIOS[scenario_name]
        first_step = scenario['first_step']
        step = scenario['steps'][first_step]
        text_to_send = step['text']
        self.registration_user_states[user_id] = UserState(scenario_name=scenario_name, step_name=first_step)
        return text_to_send

    def continue_scenario(self, user_id, text):
        state = self.registration_user_states[user_id]
        steps = sc.SCENARIOS[state.scenario_name]['steps']
        step = steps[state.step_name]
        handler = getattr(handlers, step['handler'])
        handler_result = handler(text=text, context=state.context)
        if handler_result[0]:
            next_step = steps[step['next_step']]
            text_to_send = next_step['text'].format(**state.context) + handler_result[1]
            if step['next_step']:
                state.step_name = step['next_step']
            else:
                self.registration_user_states.pop(user_id)
        else:
            if step['switcher'] == 'no_straight_chooser' and handler_result[2]:
                self.no_straight_flight_switcher_user_states[user_id] = self.registration_user_states.pop(user_id)
                text_to_send = f"{state.context['from_city'].capitalize()} > {state.context['to_city'].capitalize()} " \
                               f"{sc.DEFAULT_NO_STRAIGHT_FLIGHT_SWITCHER_ANSWER} "
            elif step['switcher'] == "switcher_check":
                next_step = steps[step['next_step']]
                self.switcher_check[user_id] = self.registration_user_states.pop(user_id)
                text_to_send = next_step['text'].format(**state.context) + handler_result[1]
            else:
                text_to_send = step['failure_text'].format(**state.context) + handler_result[1]
        return text_to_send


if __name__ == "__main__":
    config_logs()
    bot = Bot(group_id, token)
    bot.run()
