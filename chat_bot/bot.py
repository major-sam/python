from random import randint

from chat_bot.vk_token import token, group_id
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType


class Bot:
    def __init__(self, my_group_id, my_token):
        self.group_id = my_group_id
        self.token = my_token
        self.vk = vk_api.VkApi(token=self.token)
        self.long_poller = VkBotLongPoll(self.vk, self.group_id)
        self.api = self.vk.get_api()

    def run(self):
        for event in self.long_poller.listen():
            try:
                self.on_event(event)
            except Exception as exc:
                print(exc)

    def on_event(self, event):
        if event.type == VkBotEventType.MESSAGE_NEW:
            print(event.object.message['text'])
            print(event.object)
            self.api.messages.send(message=f"yr msg is {event.object.message['text']}",
                                   random_id=randint(0, 2 ** 24),
                                   peer_id=event.object.message['peer_id'],
                                   )
        else:
            print(f'not supported type {event.type}')


if __name__ == "__main__":
    bot = Bot(group_id, token)
    bot.run()