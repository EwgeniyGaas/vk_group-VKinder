
class DataBase:
    def __init__(self, user_id):
        self.user_id = user_id

    @property
    def id(self):
        return self.user_id
