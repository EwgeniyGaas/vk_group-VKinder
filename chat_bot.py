import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from random import randrange


class ChatBot:

    user_name = str()
    user_city = "Москва"
    partner_city = "Москва"
    other_city = "Другой город"
    user_sex = int()  # 0 - не указана, 1 - жен., 2 - муж.
    partner_sex = int()  # 1 - жен., 2 - муж.
    partner_relation = 6  # 6 — в активном поиске
    min_age = 18
    max_age = 120
    first_message = True
    check_point = False  # контроль, что пользователь следует сценарию, иначе начинаем заново
    ages_step = ["от 18 до 25", "от 26 до 35", "от 36 до 45", "от 46 до 55", "от 56 до 65", "от 66 и более"]  # индексы 0-5

    
    def __init__(self):
        with open("group_token.txt", 'r') as file:
            self.token = file.read().strip()
        self.vk = vk_api.VkApi(token=self.token)
        self.longpoll = VkLongPoll(self.vk)

        
    def send_message(self, user_id, message: str, keyboard = None):
        params = {
            "user_id": user_id,
            "message": message,
            "random_id": randrange(10**7)
            }
        if keyboard:
            params["keyboard"] = keyboard.get_keyboard()
        else:
            keyboard = VkKeyboard()
            params["keyboard"] = keyboard.get_empty_keyboard()
        self.vk.method("messages.send", params)


    def set_user_data(self, user_id):
        params = {
            "user_ids": user_id,
            "fields": "sex, city"
            }
        user = self.vk.method("users.get", params)
        self.user_name = user[0]["first_name"]
        if self.user_city:
            self.user_city = user[0]["city"]["title"]
        self.user_sex = user[0]["sex"]


    def get_age_for_search(self, user_id, keyboard):
        blue_key =  VkKeyboardColor.PRIMARY
        keyboard.add_button(self.ages_step[0], blue_key)
        keyboard.add_button(self.ages_step[1], blue_key)
        keyboard.add_button(self.ages_step[2], blue_key)
        keyboard.add_line()
        keyboard.add_button(self.ages_step[3], blue_key)
        keyboard.add_button(self.ages_step[4], blue_key)
        keyboard.add_button(self.ages_step[5], blue_key)
        self.send_message(user_id, "Выберите предпочитаемый возраст", keyboard)


    def set_age_for_search(self, text: str):
        age = list()
        for value in text.split():
            try:
                age.append(int(value))
            except ValueError:
                pass
            
        self.min_age = age[0]
        if len(age) == 1:
            self.max_age = 120;
        else:
            self.max_age = age[1]


    def set_partner_sex(self, user_id):
        if self.user_sex == 1:
            self.partner_sex = 2
        elif self.user_sex == 2:
            self.partner_sex = 1
        else:
            self.send_message(user_id, "Ошибка. У вашего профиля не указан пол. \
                                       Укажите ваш пол в настройках аккаунта и повторите попытку.")


    def set_partner_city(self, user_id, keyboard):
        blue_key =  VkKeyboardColor.PRIMARY
        keyboard.add_button(self.partner_city, blue_key)
        keyboard.add_button(self.other_city, blue_key)
        self.send_message(user_id, f"Место поиска - {self.partner_city}? \
                                    Или выбрать другой населённый пункт? \
                                    Нажмите на соответствующую кнопку внизу.", keyboard)


    def listen(self):
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                
                user_id = event.user_id
                text = event.text.lower()
                keyboard = VkKeyboard()
                start_text = "СТАРТ"
                green_key = VkKeyboardColor.POSITIVE

                if text == start_text.lower():
                    self.get_age_for_search(user_id, keyboard)
                    
                elif text in self.ages_step:
                    self.set_age_for_search(text)
                    self.set_partner_sex(user_id)
                    self.partner_city = self.user_city
                    self.set_partner_city(user_id, keyboard)
                    
                elif text == self.partner_city.lower():
                    self.send_message(user_id, "Мы уже ищем. Нужно чуть-чуть подождать.")
                    return

                elif text == self.other_city.lower():
                    self.send_message(user_id, f"Ведите в ответном сообщении название населённого пункта, \
                                                    где желаете осуществить поиск пары:")
                    self.check_point = True
                
                else:
                    if self.first_message:  # ответ на любое первое сообщение пользователя
                        self.first_message = False
                        self.set_user_data(user_id)
                        keyboard.add_button(start_text, green_key)
                        self.send_message(user_id, f"Приветствую {self.user_name}.\
                                                    Давайте подберём Вам пару.\
                                                    Нажмите кнопку {start_text} внизу, что-бы начать.", keyboard)
                    else:
                        if self.check_point:
                            self.partner_city = event.text
                            self.set_partner_city(user_id, keyboard)
                        else:
                            keyboard.add_button(start_text, green_key)  # если user не следует сценарию начинаем сначала
                            self.send_message(user_id, f"Приветствую {self.user_name}.\
                                                        Давайте подберём Вам пару.\
                                                        Нажмите кнопку {start_text} внизу, что-бы начать.", keyboard)























 













