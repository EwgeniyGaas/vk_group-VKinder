import vk_api
from data_base import DataBase # пользовательский тип данных
from chat_bot import ChatBot # пользовательский тип данных
import common_function # пользовательская библиотека
from config import token


class SearchEngine:
    '''
    класс SearchEngine.
    Осуществляет поиск аккаунтов пользователей Вконтакте по заданным параметрам
    '''

    search_result = dict() # результат поиска, аккаунты соответствующие требованиям юзера
    accounts_with_access = list() # аккаунты с открытым доступом просмотра страниц, отобранные из search_result
    
    def __init__(self, search_criterion, offset, count, user: DataBase):
        '''
        формирует параметры поиска аккаунтов Вк, на основе входных данных полученных от чат бота:
        search_criterion = {
                        "hometown": partner_city,
                        "sex": partner_sex,
                        "age_from": min_age,
                        "age_to": max_age
                        }
        '''
        self.params = search_criterion
        self.vk = vk_api.VkApi(token=token)

        self.params["count"] = count  # кол-во аккаунтов сколько надо найти
        self.params["offset"] = offset  # сдвиг поиска, чтобы рез-ы не повторялись
        self.params["status"] = 6   # 6 - в активном поиске
        self.params["online"] = 1   # 1 - online, 0 - всех
        self.params["has_photo"] = 1  # 1 - с фото, 0 - всех
        self.params["fields"] = "bdate" # дата рождения владельца аккаунта

        bot = ChatBot(user)
        bot.send_message("Идёт поиск подходящих анкет. Нужно немного подождать.")

    def select_accounts_with_access(self):
        '''
        Отбирает аккаунты с открытой для просмотра страницей.
        Формирует из них список ->
        [{'age': 18, 'first_name': 'Имя', 'id': 000000000 'last_name': 'Фамилия'}, {}]
        Вызывается в методе self.search()
        '''
        try:
            for account in self.search_result["items"]:
                if account["can_access_closed"]:
                    params = {
                        "id": account["id"],
                        "first_name": account["first_name"],
                        "last_name": account["last_name"],
                        "age": common_function.get_age(account["bdate"])  # вернёт число лет, либо пустую строку
                        }                
                    self.accounts_with_access.append(params)
                else:
                    pass
        except:  # отсутствие результатов обработано в файле main.py
            pass

    def search(self):
        """
        Запускает остальные методы класса.
        Ищет аккаунты Вконтакте, в соответствии с параметрами запроса.
        Отбирает из них открытые для посещения страницы.
        Возвращает список с результатами работы в виде ->
        [{'age': 18, 'first_name': 'Имя', 'id': 00000000, 'last_name': 'Фамилия'}, {}]
        Вызывается в main.py
        """
        self.search_result = dict() # нужно обнулить, иначе данные сохраняются из предыдущего поиска
        self.accounts_with_access = list() # нужно обнулить, иначе данные сохраняются из предыдущего поиска

        self.search_result = self.vk.method("users.search", self.params) # шаг 1. ищем профили соответствующие требованиям юзера
        self.select_accounts_with_access() # шаг 2. отбираем из них те, что с открытым доступом
   
        return self.accounts_with_access # отсутствие результатов обработано в файле main.py























    


