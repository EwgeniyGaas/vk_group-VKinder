from chat_bot import ChatBot # пользовательский тип данных
from data_base import DataBase # пользовательский тип данных
from search_engine import SearchEngine # пользовательский тип данных


if __name__ == "__main__":

    print("start**********************************")      #  ВРЕМЕННО

    while True:
        user = DataBase()
        bot = ChatBot(user)
        search_criterion = bot.listen()

        offset = 0 # сдвиг поиска, чтобы результаты не повторялись
        count = 100 # кол-во аккаунтовов в результатах
        end_work = False
        counter_no_result = 0
        
        while not end_work:
            searcher = SearchEngine(search_criterion, offset, count, user)
            search_result = searcher.search()

            if not search_result:
                counter_no_result += 1
                if counter_no_result == 5:
                    bot.no_result()
                    end_work = True
            else:
                counter_no_result = 0
                end_work = bot.present_results(search_result)
            offset += count

