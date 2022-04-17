class Data:
    def __init__(self):
        self.userid = -1

    def test(self):
        self.userid = 3
        self.teacherid = 1

    def set_userid(self, userid):
        self.userid = userid

    def get_userid(self):
        return self.userid

    def set_teacherid(self, teacherid):
        self.teacherid = teacherid

    def get_teacherid(self):
        return self.teacherid

    def set_studentid(self, studentid):
        self.studentid = studentid

    def get_studentid(self):
        return self.studentid


data_dict = {'userid': 2,
             'flashcardid': -1,
             'setid': -1,
             'setcode': 'zzzz'}



# data = Data()
# data.set_teacherid()
# print(data.get_teacherid())

