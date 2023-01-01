
class DataBase:

    user_id = 0
    
    def set_id(self, user_id):
        self.user_id = user_id

    @property
    def id(self):
        return self.user_id
