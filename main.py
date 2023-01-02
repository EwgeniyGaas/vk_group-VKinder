from chat_bot import ChatBot
from data_base import DataBase
from search_engine import SearchEngine

from pprint import pprint                   # ВРЕМЕННО


if __name__ == "__main__":

    my_id = 14783152                     # ВРЕМЕННО
    my_wife = 35384195                     # ВРЕМЕННО
    many_photos = 984334                    # ВРЕМЕННО профиль где много фоток

    user = DataBase()
    print("start**************")                          # ВРЕМЕННО
    bot = ChatBot(user)
    search_criterion = bot.listen()
 

    '''search_criterion = {                          # ВРЕМЕННО
                        "hometown": "Абакан",
                        "sex": 2,
                        "age_from": 26,
                        "age_to": 35
                        }'''
    
    offset = 0 # сдвиг поиска, чтобы рез-ы не повторялись
    count = 10 # кол-во акк-ов в рез-ах == увеличение offset
    
    while True:
        searcher = SearchEngine(search_criterion, offset, count, user)
        search_result = searcher.search()
        pprint(search_result)                           # ВРЕМЕННО
        bot.present_results(search_result)
        offset += count

