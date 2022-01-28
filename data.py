class Data:
    def __init__(self):
        self.teacherid = -1
        self.userid = -1
        self.studentid = -1

    def set_userid(self, userid):
        self.userid = userid

    def get_userid(self):
        return self.userid

    def set_teacherid(self, teacherid):
        self.teacherid = teacherid

    def get_teacherid(self):
        return self.teacherid

# data = Data()
# data.set_teacherid()
# print(data.get_teacherid())
