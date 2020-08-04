INTENTS_MAIN = [
    {
        "name": "Help",
        "tokens": ("help", "помощь", "привет"),
        "scenario": "",
        "answer": "help intent text"
    },
    {
        "name": "Регистрация",
        "tokens": ("регистр", "рег", "купить", "билет"),
        "scenario": "registration",
        "answer": None
    },
]
CHANGE_DATA = [
    {
        "name": "Рейс",
        "tokens": ("рейс", "РЕЙС", "перелет", "Рейс"),
        "answer": "Введите город отправления",
        "next_step": "step1"
    },
    {
        "name": "Дата",
        "tokens": ("дата", "Дата", "время"),
        "answer": "Введите дату отправления в формате 25-01-2020",
        "next_step": "step3"
    },
    {
        "name": "Количество мест",
        "tokens": ("Количество", "количество", "колич", "Колич", "места", "мест"),
        "answer": "Введите количество мест на рейс:",
        "next_step": "step5"
    },
    {
        "name": "Комментарий",
        "tokens": ("коммен", "Коммен", "Комментарий", "Коментарий", "комментарий", "ком"),
        "answer": "Введите коментарий к рейсу",
        "next_step": "step6"
    },
]
CHECK_SWITCHER = [
    {
        "name": "yes",
        "tokens": ("yes", "да"),
        "answer": "Введите имя поля для изменения\n"
                  "(Рейс, Дата, Количество мест, Комментарий)",
        "next_step": "step07"
    },
    {
        "name": "no",
        "tokens": ("no",  "нет"),
        "answer": None,
        "next_step": "step7"
    }
]
NO_STRAIGHT_FLIGHT_SWITCHER = [
    {
        "name": "yes",
        "tokens": ("yes", "y", "да"),
        "answer": None,
        "next_step": "step03"
    },
    {
        "name": "no",
        "tokens": ("no", "n", "нет"),
        "answer": "Спасибо, что воспользовались нашим сервисом",
        "next_step": None
    }
]
SCENARIOS = {
    "search_flight": {
        "first_step"
    },
    "registration": {
        "first_step": "step1",
        "steps": {
            "step1": {
                "text": "Введите имя города отправления",
                "failure_text": "Такого города отправления нет, попробуйте ввести другой из списка:\n",
                "handler": "handler_from_city",
                "switcher": False,
                "next_step": "step2",
            },
            "step2": {
                "text": "Ведите имя города назначения",
                "failure_text": "Такого города назначения нет, попробуйте ввести другой из списка:\n",
                "handler": "handler_to_city",
                "switcher": "no_straight_chooser",
                "next_step": "step3",
            },
            "step03": {
                "text": "шаг-заглушка для свитчера",
                "failure_text": "",
                "handler": "handler_return_true",
                "switcher": False,
                "next_step": "step3",
            },
            "step3": {
                "text": "Введите дату отправления в формате 25-01-2020 для рейса: ",
                "failure_text": "Нет рейсов на указанную дату",
                "handler": "handler_return_flight_list",
                "switcher": False,
                "next_step": "step4",
            },
            "step4": {
                "text": "Доступны рейсы:",
                "failure_text": "Выберите номер из списка доступных рейсов",
                "handler": "handler_flight_chooser",
                "switcher": False,
                "next_step": "step5",
            },
            "step5": {
                "text": "Введите количество мест на рейс:",
                "failure_text": "Неопознаный ввод, введите количество от 1 до 5",
                "handler": "handler_place_count",
                "switcher": False,
                "next_step": "step6",
            },
            "step6": {
                "text": "Введите коментарий к рейсу",
                "failure_text": "",
                "handler": "handler_comment",
                "switcher": "switcher_check",
                "next_step": "step7",
            },
            "step7": {
                "text": "Проверьте введеные данные",
                "failure_text": "Выберите верное поле",
                "handler": "handler_check_data",
                "switcher": False,
                "next_step": "step8",
            },
            "step8": {
                "text": "Введите номер телефона в формате: +71231234567",
                "failure_text": "Неверный формат номера телефона",
                "handler": "handler_phone_number",
                "switcher": False,
                "next_step": "step9",
            },
            "step9": {
                "text": "В ближайшее время с вами свяжется менеджер",
                "failure_text": "",
                "handler": "handler_end",
                "switcher": False,
                "next_step": None,
            },
            "step07": {
                "text": "",
                "failure_text": "",
                "handler": None,
                "switcher": False,
                "next_step": None,

            }
        }
    }
}
DEFAULT_ANSWER = "Для регистрации на рейс введите слово - \"Регистрация\"\n" \
                 "Завершить процесс регистрации - \"Выход\"\n" \
                 "Чтобы вызвать это сообщение - \"Помощь\""
DEFAULT_NO_STRAIGHT_FLIGHT_SWITCHER_ANSWER = f"прямых рейсов нет.\n Поискать рейсы с одной пересадкой?(да\нет)"
DEFAULT_EXIT = [["exit", "выход"], "Спасибо за то, что воспользовались нашим сервисом"]
DEFAULT_HELP = ["help", "помощь"]
DEFAULT_WRONG_FIELD = "Нет такого поля:"
DEFAULT_WRONG_INPUT = "Неопознаный ввод."

