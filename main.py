from chat_bot import ChatBot
from search_engine import SearchEngine

from pprint import pprint


if __name__ == "__main__":

    my_id = 14783152                     # ВРЕМЕННО
    my_wife = 35384195                     # ВРЕМЕННО
    many_photos = 984334                    # ВРЕМЕННО профиль где много фоток


    print("start**************")                          # ВРЕМЕННО
    #bot = ChatBot()
    #search_criterion = bot.listen()
 

    search_criterion = {                          # ВРЕМЕННО
                        "hometown": "Абакан",
                        "sex": 2,
                        "age_from": 26,
                        "age_to": 35
                        }


    
    searcher = SearchEngine(search_criterion)
    search_result = searcher.search()

    pprint(search_result)                           # ВРЕМЕННО
    print("finish-----------")                          # ВРЕМЕННО

