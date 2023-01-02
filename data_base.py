from config import DSN
import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


class VkinderDB(Base):
    __tablename__ = "vkinder"

    id = sq.Column(sq.Integer, primary_key=True)
    user_id = sq.Column(sq.Integer, nullable=False)
    account_id = sq.Column(sq.Integer, nullable=False)

    def __str__(self):
        return str(self.account_id)


class DataBase:

    user_id = 0

    def __init__(self):
        self.engine = sq.create_engine(DSN) 
        Base.metadata.create_all(self.engine) # if not exist create all table
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def __del__(self):
        self.session.close()

    def set_id(self, user_id):
        self.user_id = user_id
        
    @property
    def id(self):
        return self.user_id

    def save_account_id(self, account_id):
        proposal = VkinderDB(user_id=self.user_id, account_id=account_id)
        self.session.add(proposal)
        self.session.commit()

    def check_account_id(self, account_id):
        for db_account in self.session.query(VkinderDB).filter(VkinderDB.user_id == self.user_id).all():
            print(1, db_account, account_id)
            if str(db_account) == str(account_id):
                print(2)
                return False
        print(3)
        return True











