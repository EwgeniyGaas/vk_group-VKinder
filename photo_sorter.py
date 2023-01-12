import vk_api
from config import token


class PhotoSorter:
    """
    класс PhotoSorter.
    Получает фотографии с запрошенной страницы, отбирает три самые популярные по лайкам и комментам. 
    """
    
    photos = list() # все фотки полученные со страницы Вк. Объявлять локально в функции нельзя,
                    # потому что self.get_photo() вызывается 2 раза для каждого id,
                    # при втором вызове данные из первого вызова стёрлись бы.

    def __init__(self):
        self.vk = vk_api.VkApi(token=token)

    def get_photos(self, params):
        '''
        Получает id фотографий со страницы пользователя Вк
        и вычисляет рейтинг фото по кол-ву лайков и комментов
        -> [{'id': 111111111, 'rating': 11}, {'id': 222222222, 'rating': 22}]
        Вызывается в методе self.select_photos()
        '''    
        raw_photos = self.vk.method("photos.get", params)
        try:
            for photo in raw_photos["items"]:
                current_photo = dict()
                current_photo["id"] = photo["id"]
                current_photo["rating"] = photo["likes"]["count"] + photo["comments"]["count"]
                self.photos.append(current_photo)
        except: # обработано в методе self.get_three_photos_with_max_rating()
            pass

    def get_three_photos_with_max_rating(self):
        '''
        Выбирает три фотографии с максимальным рейтингом, возвращает список их id
        -> [111111111, 222222222, 333333333]
        Вызывается в методе self.select_photos()
        '''
        three_photos = [0, 0, 0]
        rating_buffer = [0, 0, 0]
        if self.photos: # если метод self.get_photos() отработал без ошибки и вернул данные
            for photo in self.photos:
                if photo["rating"] > min(rating_buffer):
                    index = rating_buffer.index(min(rating_buffer))
                    three_photos[index] = photo["id"]
                    rating_buffer[index] = photo["rating"]
        else:
            three_photos = []
        return three_photos

    def select_photos(self, account_id):
        """
        Запускает остальные методы класса.
        Получает фотографии с запрошенной страницы, отбирает три самые популярные по лайкам и комментам.
        -> [1111111, 222222, 333333]
        Вызывается в методе present_results() класса ChatBot
        """
        self.photos = list()  # нужно обнулить, иначе данные сохраняются из предыдущего поиска
        params_profile = {
            "owner_id": account_id,
            "album_id": "profile",
            "extended": 1
            } 
        self.get_photos(params_profile)  # шаг 1 получаем список фотографий профиля + кол-во лайков + кол-во комментов
        params_wall = {
            "owner_id": account_id,
            "album_id": "wall",
            "extended": 1
            }
        self.get_photos(params_wall)  # шаг 2 получаем список фотографий со стены + кол-во лайков + кол-во комментов
        three_photos_id = self.get_three_photos_with_max_rating()  # шаг 3. определяем три фотки с максимальным рейтингом (кол-во лайков + комментов)

        return three_photos_id
