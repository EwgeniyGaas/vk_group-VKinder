import vk_api
from chat_bot import ChatBot
from datetime import *   # используется в методе self.get_age()


class SearchEngine:
    '''
    класс SearchEngine. Осуществляет поиск аккаунтов пользователей Вконтакте и их фотографий
    '''

    search_result = dict() # результат поиска, аккаунты соответствующие требованиям юзера
    accounts_with_access = list() # аккаунты с открытым доступом просмотра страниц, отобранные из search_result
    photos = list() # все фотки полученные со страницы Вк. Объявлять локально в функции нельзя,
                    # потому что self.get_photo() вызывается 2 раза для каждого id,
                    # при втором вызове данные из первого вызова стёрлись бы.
        

    def __init__(self, search_criterion, offset):
        '''
        формирует параметры поиска аккаунтов Вк, на основе входных данных полученных от чат бота:
        search_criterion = {
                        "hometown": partner_city,
                        "sex": partner_sex,
                        "age_from": min_age,
                        "age_to": max_age
                        }
        '''
        with open("token.txt", 'r') as file:
            self.token = file.read().strip()
        self.params = search_criterion
        self.vk = vk_api.VkApi(token=self.token)

        self.params["count"] = 10  # кол-во аккаунтов сколько надо найти
        self.params["offset"] = offset  # сдвиг поиска, чтобы рез-ы не повторялись
        self.params["status"] = 6   # 6 - в активном поиске
        self.params["online"] = 1   # 1 - online, 0 - всех
        self.params["has_photo"] = 1  # 1 - с фото, 0 - всех
        self.params["fields"] = "bdate" # дата рождения владельца аккаунта
        bot = ChatBot()
        bot.send_message("Мы ищем подходящие варианты. Нужно чуть-чуть подождать.")

        
       

    def get_age(self, bdate_str: str) -> int:
        """
        вычисляет текущий возраст потенциальных партнёров,
        по разности между сегодняшней датой и датой их рождения.
        Используется в методе self.select_accounts_with_access()
        """
        today = datetime.date(datetime.today()) # сегодняшняя дата -> yyyy-mm-dd
        bdate = datetime.date(datetime.strptime(bdate_str, "%d.%m.%Y")) # преобразование даты рождения "dd.mm.yyyy" -> yyyy-mm-dd
        delta = str(today - bdate).split()  # кол-во дней с момента рождения -> ['365', 'days,', '0:00:00']
        age = int(int(delta[0]) // 365.25)
        return age
    

    def select_accounts_with_access(self):
        '''
        Отбирает аккаунты с открытой для просмотра страницей.
        Формирует из них список -> [{'age': 18, 'first_name': 'Имя', 'id': 000000000 'last_name': 'Фамилия'}, {}]
        '''
        for account in self.search_result["items"]:
            if account["can_access_closed"]:
                params = {
                    "id": account["id"],
                    "first_name": account["first_name"],
                    "last_name": account["last_name"],
                    "age": self.get_age(account["bdate"])
                    }                
                self.accounts_with_access.append(params)
            else:
                pass


    def get_photos(self, params):
        '''
        Получает id фотографий со страницы пользователя Вк и вычисляет рейтинг фото по кол-ву лайков и комментов
        -> [{'id': 111111111, 'rating': 11}, {'id': 222222222, 'rating': 22}]
        '''    
        raw_photos = self.vk.method("photos.get", params)
        for photo in raw_photos["items"]:
            current_photo = dict()
            current_photo["id"] = photo["id"]
            current_photo["rating"] = photo["likes"]["count"] + photo["comments"]["count"]
            self.photos.append(current_photo)


    def get_three_photos_with_max_rating(self):
        '''
        Выбирает три фотографии с максимальным рейтингом, возвращает список их id
        -> [111111111, 222222222, 333333333]
        '''
        three_photos = [0, 0, 0]
        rating_buffer = [0, 0, 0]
        for photo in self.photos:
            if photo["rating"] > min(rating_buffer):
                index = rating_buffer.index(min(rating_buffer))
                three_photos[index] = photo["id"]
                rating_buffer[index] = photo["rating"]
        return three_photos


    def search(self):
        """
        Основная функция, запускает остальные методы класса.
        Ищет аккаунты Вконтакте, в соответствии с параметрами запроса.
        Отбирает из них открытые для посещения страницы.
        Получает фотографии с найденных страниц, отбирает самые популярные по лайкам и комментам.
        Возвращает список с результатами работы в виде
        -> [{'age': 18, 'first_name': 'Имя', 'id': 00000000, 'last_name': 'Фамилия', 'photos': [1111111, 222222, 333333]}, {}]
        """

        self.search_result = self.vk.method("users.search", self.params) # шаг 1. ищем профили соответствующие требованиям юзера
        self.select_accounts_with_access() # шаг 2. отбираем из них те, что с открытым доступом

        for account in self.accounts_with_access: # шаг 3. получаем фотки для каждого аккаунта
            params_profile = {
                "owner_id": account["id"],
                "album_id": "profile",
                "extended": 1
                } 
            self.get_photos(params_profile)       # шаг 3.1 получаем список фотографий профиля + кол-во лайков + кол-во комментов
            params_wall = {
                "owner_id": account["id"],
                "album_id": "wall",
                "extended": 1
                }
            self.get_photos(params_wall)       # шаг 3.2 получаем список фотографий со стены + кол-во лайков + кол-во комментов
            account["photos"] = self.get_three_photos_with_max_rating() # шаг 4. определяем три фотки с максимальным рейтингом (кол-во лайков + комментов)
            self.photos = list() # удаляем данные, чтобы не перенеслись на следующего пользователя
        return self.accounts_with_access





















