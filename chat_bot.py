import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from random import randrange # используется в методе send_message()
from time import sleep # используется в методе listen()
from data_base import DataBase # пользовательский тип данных
from photo_sorter import PhotoSorter # пользовательский тип данных

from config import group_token


class ChatBot:
    """
    класс ChatBot. Общается с юзером в чате группы вКонтакте.
    Получает от юзера параметры поиска, выводит ему найденные результаты.
    """

    user_name = str()
    user_city = "Москва"
    partner_city = "Москва"
    other_city = "Другой город"
    user_sex = int()  # 0 - не указана, 1 - жен., 2 - муж.
    partner_sex = int()  # 1 - жен., 2 - муж.
    min_age = 18
    max_age = 120
    is_check_point = False  # контроль, что пользователь следует сценарию, иначе начинаем заново
    ages_step = ["от 18 до 25", "от 26 до 35", "от 36 до 45", "от 46 до 55", "от 56 до 65", "от 66 и более"]  # индексы 0-5
    
    def __init__(self, user):
        self.vk = vk_api.VkApi(token=group_token)
        self.longpoll = VkLongPoll(self.vk)
        self.user = user # class DataBase

    def send_message(self, message: str, keyboard = None):
        """
        Отправляет клавиатуру и сообщение юзеру в чат вКонтакте.
        """
       
        params = {
            "user_id": self.user.id,
            "message": message,
            "random_id": randrange(10**7)
            }
        if keyboard:
            params["keyboard"] = keyboard.get_keyboard()
        else:
            keyboard = VkKeyboard()
            params["keyboard"] = keyboard.get_empty_keyboard()
        self.vk.method("messages.send", params)

    def set_user_data(self):
        """
        Автоматически получает данные о юзере из его аккаунта вКонтакте - имя, пол и город
        И сохраняет их в переменные класса
        Вызывается в методе self.listen()
        """

        params = {
            "user_ids": self.user.id,
            "fields": "sex, city"
            }
        user = self.vk.method("users.get", params)
        self.user_name = user[0]["first_name"]
        if self.user_city:
            self.user_city = user[0]["city"]["title"]
        self.user_sex = user[0]["sex"]

    def request_age_for_search(self, keyboard):
        """
        Запрашивает у юзера желаемый возраст партнёра.
        Используется клавиатура с задаными в self.ages_step диапазонами
        Вызывается в методе self.listen()
        """
        
        blue_key =  VkKeyboardColor.PRIMARY
        keyboard.add_button(self.ages_step[0], blue_key)
        keyboard.add_button(self.ages_step[1], blue_key)
        keyboard.add_button(self.ages_step[2], blue_key)
        keyboard.add_line()
        keyboard.add_button(self.ages_step[3], blue_key)
        keyboard.add_button(self.ages_step[4], blue_key)
        keyboard.add_button(self.ages_step[5], blue_key)
        self.send_message("Выберите желаемый возраст", keyboard)

    def set_age_for_search(self, text: str):
        """
        Сохраняет диапазон желаемого возраста партнёра для поиска
        Вызывается в методе self.listen()
        """
        
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

    def set_partner_sex(self):
        """
        Сохраняет пол партнёра противоположный полу юзера
        Вызывается в методе self.listen()
        """
        
        if self.user_sex == 1:
            self.partner_sex = 2
        elif self.user_sex == 2:
            self.partner_sex = 1
        else:
            self.send_message("Ошибка. У вашего профиля не указан пол. \
                                Укажите ваш пол в настройках аккаунта, \
                                чтобы мы могли найти вам пару.")

    def set_partner_city(self, keyboard):
        """
        Запрашивает у юзера город для поиска партнёра,
        по умолчанию предлагается город из профиля юзера,
        с возможностью указать другой город
        Вызывается в методе self.listen()
        """
        
        blue_key =  VkKeyboardColor.PRIMARY
        keyboard.add_button(self.partner_city, blue_key)
        keyboard.add_button(self.other_city, blue_key)
        self.send_message(f"Место поиска - {self.partner_city}? \
                            Или выбрать другой населённый пункт? \
                            Нажмите на соответствующую кнопку внизу.", keyboard)

    def listen(self):
        """
        Запускает методы класса, расположенные выше её.
        Управляет чат ботом, обрабатывает сообщения юзера, отвечает ему,
        запрашивает у юзера информацию.
        Вызывается в main.py
        """

        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                
                self.user.set_id(event.user_id) 
                text = event.text.lower()
                keyboard = VkKeyboard()
                green_key = VkKeyboardColor.POSITIVE
                start_text = "СТАРТ" # надпись на стартовой кнопке

                if text == start_text.lower(): # шаг 2. Юзер выбирает возраст партнёра
                    self.request_age_for_search(keyboard)
                    
                elif text in self.ages_step: # шаг 3.1 Присваиваим возраст и пол. Уточняем город поиска
                    self.set_age_for_search(text)
                    self.set_partner_sex()
                    self.partner_city = self.user_city
                    self.set_partner_city(keyboard)
                    
                elif text == self.other_city.lower(): # шаг 3.2 Запрос города, если юзер хочет его сменить
                    self.send_message(f"Ведите в ответном сообщении название населённого пункта, \
                                        где желаете осуществить поиск пары:")
                    self.is_check_point = True
                    
                elif text == self.partner_city.lower(): # шаг 4. Конец первичной работы с юзером. Формируем критерии поиска. Возвращаем результат
                    search_criterion = {
                        "hometown": self.partner_city,
                        "sex": self.partner_sex,
                        "age_from": self.min_age,
                        "age_to": self.max_age
                        }
                    return search_criterion
                
                else:
                    if self.is_check_point:  # шаг 3.3 Сохранение другого города, введённого пользователем
                        self.partner_city = event.text
                        self.set_partner_city(keyboard)
                    else: # шаг 1. Ответ на любое первое сообщение юзера. А также, если юзер не следует сценарию, и пишет в чат, то начинаем сначала
                        self.set_user_data()
                        keyboard.add_button(start_text, green_key)
                        self.send_message(f"Приветствую {self.user_name}.\
                                            Давайте подберём Вам пару.\
                                            Нажмите кнопку {start_text} внизу, что-бы начать.", keyboard)

    def present_results(self, search_result):
        """
        Выводит в чат пользователю найденную информацию (ссылки на три фотографии и на страницу потенциальной пары)
        Вызывается в main.py
        """
        green_key = VkKeyboardColor.POSITIVE
        blue_key =  VkKeyboardColor.PRIMARY
        next_person = "Следующий"
        end_work = "Завершить сеанс"
        photo_sorter = PhotoSorter()
                
        for person in search_result:
            if self.user.check_account_id(person["id"]):
                self.user.save_account_id(person["id"])
                three_photos_id = photo_sorter.select_photos(person["id"])  # -> [1111111, 222222, 333333]
                keyboard = VkKeyboard()
                full_name = f"{person['first_name']} {person['last_name']}"
                url = f"https://vk.com/id{person['id']}"
                photo_1 = f"https://vk.com/photo{person['id']}_{three_photos_id[0]}"
                photo_2 = f"https://vk.com/photo{person['id']}_{three_photos_id[1]}"
                photo_3 = f"https://vk.com/photo{person['id']}_{three_photos_id[2]}"
                
                keyboard.add_openlink_button(full_name, url)
                keyboard.add_button(next_person, green_key)
                keyboard.add_line()
                keyboard.add_button(end_work, blue_key)
                self.send_message(photo_1)
                sleep(1)
                self.send_message(photo_2)
                sleep(1)
                self.send_message(photo_3)
                sleep(1)
                self.send_message(f"{full_name.upper()}, {person['age']} лет \n \
                                    {url} \n \
                                    Нажмите на нужную кнопку внизу, чтобы открыть страницу пользователя \
                                    или посмотреть следующего. Ссылка на страницу сохранится здесь, в чате.", keyboard)
                for event in self.longpoll.listen():
                    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                        text = event.text
                        if text == next_person:
                            break
                        elif text == end_work:
                            self.send_message(f"До свидания {self.user_name}, надеюсь мы смогли вам помочь :) !")
                            return True

    def no_result(self):
        """
        Выводит сообщение, что ничего не удаётся найти
        Вызывается в main.py
        """
        self.send_message(f"К сожалению мы не смогли найти ничего подходящего :( \n \
                            Напишите любое сообщение в чат если хотите изменить параметры поиска.")
                            


