import json
from vk_api import VkApi
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor


GROUP_ID = '209553602'
GROUP_TOKEN = "af2980cd8e24db42d444e894c2a8f3e5ec714fd93c980cedac92126c9a36f53141f4e947362d2497b6b7e"
API_VERSION = "5.120"

CALLBACK_TYPES = ("show_snackbar", "open_link", "open_app", "text")


def main():
    vk_session = VkApi(token=GROUP_TOKEN, api_version=API_VERSION)
    vk = vk_session.get_api()
    longpoll = VkBotLongPoll(vk_session, group_id=GROUP_ID)

    keyboard = VkKeyboard()           # Стартовая панель

    keyboard.add_callback_button(label='Интересная и полезная информация', color=VkKeyboardColor.POSITIVE,
                                 payload={"type": "my_own_100500_type_edit"})
    keyboard.add_line()
    keyboard.add_openlink_button(label='Ссылка на Instagram', link='https://www.instagram.com/studfmiat/',
                                 payload={"type": "instagram"})
    keyboard.add_line()
    keyboard.add_openlink_button(label='Ссылка на TikTok', link='https://www.tiktok.com/@studfmiat?lang=ru-RU',
                                 payload={"type": "tiktok"})

    keyboard_2 = VkKeyboard(one_time=True)         # Вторая панель

    keyboard_2.add_callback_button(label="Назад", color=VkKeyboardColor.NEGATIVE,
                                   payload={"type": "my_own_100500_type_edit"})

    keyboard_2.add_line()
    keyboard_2.add_callback_button(label='Кураторы ', color=VkKeyboardColor.POSITIVE,
                                   payload={"type": "kurators", })

    keyboard_2.add_line()
    keyboard_2.add_callback_button(label='Президиум ', color=VkKeyboardColor.POSITIVE,
                                   payload={"type": "krutie_cheli", })

    keyboard_2.add_line()
    keyboard_2.add_callback_button(label='Местонахождение кафедр и контакты ', color=VkKeyboardColor.POSITIVE,
                                   payload={"type": "ucheba", })

    keyboard_2.add_line()
    keyboard_2.add_openlink_button(label='Банк распоряжений ФМИАТа', link='https://disk.yandex.ru/d/CHoy9BQ1YIS_lA',
                                   payload={"type": "bank_fmiat"})

    keyboard_2.add_line()
    keyboard_2.add_openlink_button(label='Банк документов УлГУ', link='https://drive.google.com/drive/folders/1dCHXSoEzZT3sFv6f6QWC5ePRTA0iUBh6',
                                   payload={"type": "bank_oso"})

    f_toggle: bool = False
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            if event.obj.message["text"] != "":
                if event.from_user:
                    if "callback" not in event.obj.client_info["button_actions"]:
                        print(
                            f'Клиент user_id{event.obj.message["from_id"]} не поддерживает callback-кнопки.'
                        )

                    vk.messages.send(
                        user_id=event.obj.message["from_id"],
                        random_id=get_random_id(),
                        peer_id=event.obj.message["from_id"],
                        keyboard=keyboard.get_keyboard(),
                        message="Прив ку это наш фмиатовский бот он оч оч крутой",
                    )

        elif event.type == VkBotEventType.MESSAGE_EVENT:
            if event.object.payload.get("type") in CALLBACK_TYPES:
                r = vk.messages.sendMessageEventAnswer(
                    event_id=event.object.event_id,
                    user_id=event.object.user_id,
                    peer_id=event.object.peer_id,
                    event_data=json.dumps(event.object.payload),
                )

            elif event.object.payload.get("type") == "my_own_100500_type_edit":
                vk.messages.send(
                    user_id=event.object.user_id,
                    random_id=get_random_id(),
                    peer_id=event.object.peer_id,
                    keyboard=(keyboard if f_toggle else keyboard_2).get_keyboard(),
                    message="Прив ку это наш фмиатовский бот он оч оч крутой" if f_toggle else "В этом меню ты можешь найти свои распоряги и посмотреть интересную информацию!",
                )
                f_toggle = not f_toggle

            elif event.object.payload.get("type") == "kurators":
                vk.messages.send(
                    user_id=event.object.user_id,
                    random_id=get_random_id(),
                    peer_id=event.object.peer_id,
                    keyboard=keyboard_2.get_keyboard(),
                    message="Куратор АС: [vlad_glazov|Владислав Глазов] \nКураторы АТПП: [beeeeeeeeb|Павел Авдошин] и [iv.kolesnichenko10|Иван Колесниченко]",
                    # сюда список куряторов
                )

            elif event.object.payload.get("type") == "krutie_cheli":
                vk.messages.send(
                    user_id=event.object.user_id,
                    random_id=get_random_id(),
                    peer_id=event.object.peer_id,
                    keyboard=keyboard_2.get_keyboard(),
                    message="Председатель студенческого актива: [exc9rd|Максим Агибалов]" #сюда список президиума
                )
            elif event.object.payload.get("type") == "ucheba":
                vk.messages.send(
                    user_id=event.object.user_id,
                    random_id=get_random_id(),
                    peer_id=event.object.peer_id,
                    keyboard=keyboard_2.get_keyboard(),
                    message="Кафедра ПМ:\nМестонахождение: 1 корп. ауд. 604 \nКонтактный телефон: 37-24-73" #сюда про кафедры вся инфа на сайте улгу
                )

if __name__=="__main__":
    main()
