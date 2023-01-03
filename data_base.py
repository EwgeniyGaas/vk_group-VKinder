from config import DSN
import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


class VkinderDB(Base):
    """
    класс VkinderDB является наследуемым от шаблона класса Base библиотеки sqlalchemy
    Используется для создания в базе данных таблицы и её атрибутов (заголовков столбцов)
    Переменные - атрибуты:
    id - primary key
    user_id - id юзера, для которого осуществляется поиск аккаунтов
    account_id - id аккаунта, показанного юзеру в чате
    """
    
    __tablename__ = "vkinder"
    
    # три атрибута таблицы
    id = sq.Column(sq.Integer, primary_key=True)
    user_id = sq.Column(sq.Integer, nullable=False) 
    account_id = sq.Column(sq.Integer, nullable=False)

    def __str__(self):
        """
        Возвращает только номер аккаунта потенциальной пары, показанного юзеру в чате
        """
        return str(self.account_id)


class DataBase:
    """
    класс DataBase. Управляет базой данных.
    Создает таблицы, заполняет данные, читает данные.
    """
    
    user_id = 0

    def __init__(self):
        self.engine = sq.create_engine(DSN) 
        Base.metadata.create_all(self.engine) # if not exist create all tables (class VkinderDB)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def __del__(self):
        self.session.close()

    def set_id(self, user_id):
        """
        Сохраняем id юзера, для которого осуществляется поиск аккаунтов
        Вызывается в методе listen класса ChatBot
        """
        self.user_id = user_id
        
    @property
    def id(self):
        """
        Возвращает id юзера, для которого осуществляется поиск аккаунтов
        """
        return self.user_id

    def save_account_id(self, account_id):
        """
        Сохраняет в базу данных id текущего юзера и id аккаунта, показанного юзеру в чате
        Вызывается в методе present_results() класса ChatBot
        """
        proposal = VkinderDB(user_id=self.user_id, account_id=account_id)
        self.session.add(proposal)
        self.session.commit()

    def check_account_id(self, account_id):
        """
        Проверяет по базе данных показывался ли уже текущий аккаунт юзеру,
        что бы не повторяться
        Вызывается в методе present_results() класса ChatBot
        """
        for db_account in self.session.query(VkinderDB).filter(VkinderDB.user_id == self.user_id).all():
            if str(db_account) == str(account_id):
                return False
        return True


