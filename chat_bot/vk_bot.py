from chat_bot.vk_token import token, group_id
import vk_api
import vk_api.bot_longpoll


class Bot:
    def __init__(self, group_id, token):
        self.group_id = group_id
        self.token = token
        self.vk = vk_api.VkApi(token=token)
        self.long_poller = vk_api.bot_longpoll.VkBotLongPoll(self.vk, self.group_id)

    def run(self):
        for event in self.long_poller.listen():
            try:
                self.on_event(event)
            except Exception as exc:
                print(exc)

    def on_event(self, event):
        print(event)


if __name__ == "__main__":
    bot = Bot(group_id, token)
    bot.run()
