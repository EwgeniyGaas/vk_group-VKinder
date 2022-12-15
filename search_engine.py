import vk_api
from datetime import *

from pprint import pprint                           # ВРЕМЕННО

class SearchEngine:

    search_result = dict()

    def __init__(self, search_criterion):
        '''
        данные от чат бота
        search_criterion = {
                        "hometown": self.partner_city,
                        "sex": self.partner_sex,
                        "age_from": self.min_age,
                        "age_to": self.max_age
                        }
        '''
        with open("token.txt", 'r') as file:
            self.token = file.read().strip()
        self.params = search_criterion
        self.vk = vk_api.VkApi(token=self.token)

        self.params["count"] = 1
        self.params["offset"] = 0
        self.params["status"] = 6   # 6 - в активном поиске
        self.params["online"] = 1   # 1 - online, 0 - всех
        self.params["has_photo"] = 1  # 1 - с фото, 0 - всех

        self.params["fields"] = "about, city, sex, bdate, photo_id, relation"                          # ЧАСТИЧНО ВРЕМЕННО


    def start_search(self):
        self.search_result = self.vk.method("users.search", self.params)


    def get_age(self, bdate_str: str) -> int:
        today = datetime.date(datetime.today()) # -> yyyy-mm-dd
        bdate = datetime.date(datetime.strptime(bdate_str, "%d.%m.%Y")) # "dd.mm.yyyy" -> yyyy-mm-dd
        delta = str(today - bdate).split()  # -> ['365', 'days,', '0:00:00']
        age = int(int(delta[0]) // 365.25)
        return age
        


    def print(self):                          # ВРЕМЕННО
        pprint(self.search_result)

    def primary_selection(self):
        ''' is_closed: False - профиль не закрытый
        год рождения может быть скрыт, только день и месяц
        relation - 6, не всегда
        '''
        

        



















