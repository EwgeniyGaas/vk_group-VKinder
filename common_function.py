"""
Общие функции вызываемые в разных классах
"""

from datetime import *


def get_age(bdate_str: str) -> int:
    """
    вычисляет текущий возраст пользователей
    по разности между сегодняшней датой и датой их рождения.
    Вызывается в методе select_accounts_with_access() класса SearchEngine
    И в методе request_age_for_search() класса ChatBot
    """
    if bdate_str:
        try:
            today = datetime.date(datetime.today()) # сегодняшняя дата -> yyyy-mm-dd
            bdate = datetime.date(datetime.strptime(bdate_str, "%d.%m.%Y")) # преобразование даты рождения "dd.mm.yyyy" -> yyyy-mm-dd
            delta = str(today - bdate).split()  # кол-во дней с момента рождения -> ['365', 'days,', '0:00:00']
            age = int(int(delta[0]) // 365.25)
            return age
        except:
            return ""
    else:
        return ""

