from random import randint, sample
from datetime import datetime, timedelta

import ticket_generator as tg
import requests
from pony.orm import db_session
import rstr
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


@db_session
def register_no_straight(state, context):
    Registration(
        user_id=state.user_id,
        from_city=context['from_city'],
        to_city=context['to_city'],
        straight_flight=context['straight_flight'],
        phone=context['phone'],
        sits_count=context['sits_count'],
        comment=context['comment'],
        transfer_city=context['transfer_city'],
        flight_to_date=context['flight_to_date'],
        flight_from_date=context['flight_from_date'],
        plane_to=context['plane_to'],
        plane_from=context['plane_from'],
    )


@db_session
def register_straight(state, context):
    Registration(
        user_id=state.user_id,
        from_city=context['from_city'],
        to_city=context['to_city'],
        straight_flight=['straight_flight'],
        phone=context['phone'],
        sits_count=context['sits_count'],
        comment=context['comment'],
        plane=context['plane'],
        flight_date=context['flight_date']
    )


@db_session
def start_scenario(scenario_name, user_id):
    scenario = sc.SCENARIOS[scenario_name]
    first_step = scenario['first_step']
    step = scenario['steps'][first_step]
    text_to_send = step['text']
    UserState(user_id=user_id, scenario_name=scenario_name, step_name=first_step, context={}, sub_scenario_id=0)
    return text_to_send


@db_session
def handle_state_none(text, user_id):
    for intent in sc.INTENTS_MAIN:
        if any(_token in text for _token in intent['tokens']):
            if intent['answer']:
                text_to_send = intent['answer']
            else:
                text_to_send = start_scenario(intent['scenario'], user_id)
            break
    else:
        text_to_send = sc.DEFAULT_ANSWER
    return text_to_send


def get_images(state):
    row = randint(1, 20)
    context = state.context
    images = []
    time_pattern = '%H:%M'
    if context['straight_flight']:
        date_time = context['flight_date'].split(' ')
        date = date_time[0]
        time = date_time[1]
        start_seat = (datetime.strptime(time, time_pattern) - timedelta(minutes=45)).strftime(time_pattern)
        places = sample(range(1, 8), int(context['sits_count']))
        for place in places:
            params = {
                'user_id': state.user_id,
                'departure': context['from_city'],
                'destination': context['to_city'],
                'plane_id': state.context['plane'],
                'row': row,
                'place': place,
                'date': date,
                'time_seat': start_seat,
                'time_departure': time
            }
            images.append(tg.make_ticket(**params))
    else:
        row_to = randint(1, 20)
        date_time_to = context['flight_to_date'].split(' ')
        date_to = date_time_to[0]
        time_to = date_time_to[1]
        start_seat_to = (datetime.strptime(time_to, time_pattern) - timedelta(minutes=45)).strftime(time_pattern)
        date_time_from = context['flight_from_date'].split(' ')
        date_from = date_time_from[0]
        time_from = date_time_from[1]
        start_seat_from = (datetime.strptime(time_from, time_pattern) - timedelta(minutes=45)).strftime(
            time_pattern)
        places = sample(range(1, 8), int(context['sits_count']))
        for place in places:
            params_to = {
                'user_id': state.user_id,
                'departure': context['transfer_city'],
                'destination': context['to_city'],
                'plane_id': state.context['plane_to'],
                'row': row_to,
                'place': place,
                'date': date_to,
                'time_seat': start_seat_to,
                'time_departure': time_to
            }
            params_from = {
                'user_id': state.user_id,
                'departure': context['from_city'],
                'destination': context['transfer_city'],
                'plane_id': state.context['plane_from'],
                'row': row,
                'place': place,
                'date': date_from,
                'time_seat': start_seat_from,
                'time_departure': time_from
            }
            images.append(tg.make_ticket(**params_from))
            images.append(tg.make_ticket(**params_to))
    return images


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
            'Send Ticket': 4
        }

    def run(self):
        for event in self.long_poller.listen():
            try:
                self.on_event(event)
            except Exception:
                log.exception("Ошибка в обработке события")

    def change_flight_data(self, text, state):
        for intent in sc.CHANGE_DATA:
            if any(_token in text for _token in intent['tokens']):
                state.step_name = intent['next_step']
                state.sub_scenario_id = self.sub_states['Registration']
                text_to_send = intent['answer']
                break
        else:
            text_to_send = f"{sc.DEFAULT_WRONG_FIELD}\n{text}"
        return text_to_send

    def change_data_switcher(self, text, state):
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
        return text_to_send

    def switch_send_ticket(self, text, state):
        for intent in sc.PRINT_TICKET:
            if any(_token in text for _token in intent['tokens']):
                if intent['name'] == 'yes':
                    state.step_name = intent['next_step']
                    images = get_images(state)
                    self.send_image(images, state.user_id)
                    state.sub_scenario_id = self.sub_states['Registration']
                    text_to_send = self.continue_scenario(text, state)
                else:
                    state.step_name = intent['next_step']
                    state.sub_scenario_id = self.sub_states['Registration']
                    text_to_send = self.continue_scenario(text, state)
                break
        else:
            text_to_send = f"{sc.DEFAULT_WRONG_INPUT}\n Ведите \"да\" или \"нет\""
        return text_to_send

    def switch_no_straight_flight(self, text, state):
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
        return text_to_send

    def send_image(self, images, user_id):
        if len(images) == 1:
            upload_url = self.api.photos.getMessagesUploadServer()['upload_url']
            upload_data = requests.post(url=upload_url, files={'photo': ('image.png', images[0], 'image/png')}).json()
            image_data = self.api.photos.saveMessagesPhoto(**upload_data)[0]
            owner_id = image_data['owner_id']
            media_id = image_data['id']
            attachment_id = f"photo{owner_id}_{media_id}"
            self.api.messages.send(attachment=attachment_id,
                                   random_id=randint(0, 2 ** 24),
                                   peer_id=user_id)
        elif len(images) > 1:
            attachments_id = []
            for image in images:
                upload_url = self.api.photos.getMessagesUploadServer()['upload_url']
                upload_data = requests.post(url=upload_url,
                                            files={'photo': ('image.png', image, 'image/png')}).json()
                image_data = self.api.photos.saveMessagesPhoto(**upload_data)[0]
                owner_id = image_data['owner_id']
                media_id = image_data['id']
                attachments_id.append(f"photo{owner_id}_{media_id}")
            self.api.messages.send(attachment=','.join(attachments_id),
                                   random_id=randint(0, 2 ** 24),
                                   peer_id=user_id)
        else:
            raise Exception("empty image list")

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
                text_to_send = self.change_flight_data(text, state)
            elif state.sub_scenario_id is self.sub_states['Change Data yes/no state']:
                text_to_send = self.change_data_switcher(text, state)
            elif state.sub_scenario_id is self.sub_states['No straight flight yes/no state']:
                text_to_send = self.switch_no_straight_flight(text, state)
            elif state.sub_scenario_id is self.sub_states['Send Ticket']:
                text_to_send = self.switch_send_ticket(text, state)
            else:
                text_to_send = self.continue_scenario(text, state)
        else:
            text_to_send = handle_state_none(text, user_id)

        log.info(event.type)
        self.api.messages.send(message=text_to_send,
                               random_id=randint(0, 2 ** 24),
                               peer_id=user_id)

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
                        register_straight(state, context)
                    else:
                        register_no_straight(state, context)
                    state.delete()
                    text_to_send = f'{sc.DEFAULT_EXIT[1]}\n{text_to_send}'
            else:
                text_to_send = step['text'].format(**state.context)
                context = dict(state.context)
                if context['straight_flight']:
                    register_straight(state, context)
                else:
                    register_no_straight(state, context)
                state.delete()
                text_to_send = f'{sc.DEFAULT_EXIT[1]}\n{text_to_send}'

        else:
            if step['switcher'] == 'no_straight_chooser' and handler_result[2]:
                state.sub_scenario_id = self.sub_states['No straight flight yes/no state']
                text_to_send = f"{state.context['from_city'].capitalize()} > {state.context['to_city'].capitalize()} " \
                               f"{sc.DEFAULT_NO_STRAIGHT_FLIGHT_SWITCHER_ANSWER} "
            elif step['switcher'] == "switcher_check":
                next_step = steps[step['next_step']]
                state.sub_scenario_id = self.sub_states['Change Data yes/no state']
                text_to_send = next_step['text'].format(**state.context) + handler_result[1]
            elif step['switcher'] == "switcher_ticket_copy" and handler_result[2]:
                next_step = steps[step['next_step']]
                state.sub_scenario_id = self.sub_states['Send Ticket']
                text_to_send = next_step['text'].format(**state.context) + handler_result[1]
            else:
                text_to_send = step['failure_text'].format(**state.context) + handler_result[1]
        return text_to_send


if __name__ == "__main__":
    config_logs()
    bot = Bot(group_id, token)
    bot.run()
