from chat_bot import ChatBot
from search_engine import SearchEngine

from pprint import pprint


if __name__ == "__main__":

    bot = ChatBot()
    print("start**************")                          # ВРЕМЕННО
    search_criterion = bot.listen()

    pprint(search_criterion)                         # ВРЕМЕННО

    
'''
    search_criterion = {                          # ВРЕМЕННО
                        "hometown": "Уфа",
                        "sex": 2,
                        "age_from": 26,
                        "age_to": 35
                        }


    
    searcher = SearchEngine(search_criterion)
    searcher.start_search()

    searcher.print()                           # ВРЕМЕННО
    print("finish-----------")                          # ВРЕМЕННО
'''
