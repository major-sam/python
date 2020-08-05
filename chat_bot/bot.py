from random import randint

from pony.orm import db_session

from vk_token import token, group_id
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import logging
import scenarios as sc
import bot_handlers as handlers
from models import UserState, Registration

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


# class UserState:
#    def __init__(self, scenario_name, step_name, context=None):
#        self.scenario_name = scenario_name
#        self.step_name = step_name
#        self.context = context or {}


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
        self.sub_states = {
            'Registration': 1,
            'No straight flight yes/no state': 2,
            'Change Data': 3,
            'Change Data yes/no state': 30,
        }

    #        self.no_straight_flight_switcher_user_states = dict()
    #        self.registration_user_states = dict()
    #        self.switcher_check = dict()
    #        self.change_user_data = dict()

    def run(self):
        for event in self.long_poller.listen():
            try:
                self.on_event(event)
            except Exception:
                log.exception("Ошибка в обработке события")

    @db_session
    def on_event(self, event):
        """on_event method for scenarios
         :arg event """
        if event.type != VkBotEventType.MESSAGE_NEW:
            log.debug("not supported type %s", event.type)
            return
        text = event.object.message['text'].lower()
        user_id = str(event.object.message['peer_id'])
        state = UserState.get(user_id=user_id)
        if state:
            if text in sc.DEFAULT_EXIT[0]:
                text_to_send = sc.DEFAULT_EXIT[1]
                state.delete()
            elif text in sc.DEFAULT_HELP:
                text_to_send = sc.DEFAULT_ANSWER
            elif state.sub_scenario_id is self.sub_states['Change Data']:
                for intent in sc.CHANGE_DATA:
                    if any(_token in text for _token in intent['tokens']):
                        state.step_name = intent['next_step']
                        state.sub_scenario_id = self.sub_states['Registration']
                        text_to_send = intent['answer']
                        break
                else:
                    text_to_send = f"{sc.DEFAULT_WRONG_FIELD}\n{text}"
            elif state.sub_scenario_id is self.sub_states['Change Data yes/no state']:
                for intent in sc.CHECK_SWITCHER:
                    if any(_token in text for _token in intent['tokens']):
                        if intent['name'] == 'yes':
                            text_to_send = intent['answer']
                            state.step_name = intent['next_step']
                            state.sub_scenario_id = self.sub_states['Change Data']
                        else:
                            state.step_name = intent['next_step']
                            state.sub_scenario_id = self.sub_states['Registration']
                            text_to_send = self.continue_scenario(text, state)
                        break
                else:
                    text_to_send = sc.DEFAULT_WRONG_INPUT
            elif state.sub_scenario_id is self.sub_states['No straight flight yes/no state']:
                for intent in sc.NO_STRAIGHT_FLIGHT_SWITCHER:
                    if any(_token in text for _token in intent['tokens']):
                        if intent['next_step']:
                            state.step_name = intent['next_step']
                            state.context['straight_flight'] = False
                            state.sub_scenario_id = self.sub_states['Registration']
                            text_to_send = self.continue_scenario(text, state)
                        else:
                            state.delete()
                            text_to_send = intent['answer']
                        break
                else:
                    text_to_send = f"Неопознаный ввод.\n{sc.DEFAULT_NO_STRAIGHT_FLIGHT_SWITCHER_ANSWER}"
            else:
                text_to_send = self.continue_scenario(text, state)
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
        UserState(user_id=user_id, scenario_name=scenario_name, step_name=first_step, context={}, sub_scenario_id=0)
        return text_to_send

    @db_session
    def continue_scenario(self, text, state):
        steps = sc.SCENARIOS[state.scenario_name]['steps']
        step = steps[state.step_name]
        handler = getattr(handlers, step['handler'])
        handler_result = handler(text=text, context=state.context)
        if handler_result[0]:
            if step['next_step']:
                next_step = steps[step['next_step']]
                text_to_send = next_step['text'].format(**state.context) + handler_result[1]
                state.step_name = step['next_step']
                if next_step['next_step'] is None:
                    context = dict(state.context)
                    if context['straight_flight']:
                        Registration(
                            from_city=context['from_city'],
                            to_city=context['to_city'],
                            straight_flight=['straight_flight'],
                            phone=context['phone'],
                            sits_count=context['sits_count'],
                            comment=context['comment'],
                            flight_date=context['flight_date']
                        )
                    else:
                        Registration(
                            from_city=context['from_city'],
                            to_city=context['to_city'],
                            straight_flight=context['straight_flight'],
                            phone=context['phone'],
                            sits_count=context['sits_count'],
                            comment=context['comment'],
                            flight_to_date=context['flight_to_date'],
                            flight_from_date=context['flight_from_date']
                        )
                    state.delete()
                    text_to_send = f'{sc.DEFAULT_EXIT[1]}\n{text_to_send}'
            else:
                text_to_send = ''
                state.delete()
        else:
            if step['switcher'] == 'no_straight_chooser' and handler_result[2]:
                state.sub_scenario_id = self.sub_states['No straight flight yes/no state']
                text_to_send = f"{state.context['from_city'].capitalize()} > {state.context['to_city'].capitalize()} " \
                               f"{sc.DEFAULT_NO_STRAIGHT_FLIGHT_SWITCHER_ANSWER} "
            elif step['switcher'] == "switcher_check":
                next_step = steps[step['next_step']]
                state.sub_scenario_id = self.sub_states['Change Data yes/no state']
                text_to_send = next_step['text'].format(**state.context) + handler_result[1]
            else:
                text_to_send = step['failure_text'].format(**state.context) + handler_result[1]
        return text_to_send


if __name__ == "__main__":
    config_logs()
    bot = Bot(group_id, token)
    bot.run()
