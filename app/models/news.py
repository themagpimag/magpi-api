from google.appengine.ext import ndb
from datetime import datetime

class News(ndb.Model):
    date = ndb.DateTimeProperty()
    title = ndb.StringProperty()
    content = ndb.StringProperty(indexed=False)

    def maximize(self):
        my_dict = self.to_dict()
        my_dict['date'] = my_dict['date'].strftime("%Y-%m-%d %H:%M:%S")
        return my_dict

    def fill_from_old(self, old_news):
        self.title = old_news['title']
        self.content = old_news['summary']
        #DATE FORMAT Tue, 04 Feb 2014 12:29:32 PST
        self.date = datetime.strptime(old_news['published'][0:-4], "%a, %d %b %Y %H:%M:%S")

    @classmethod
    def generate_key(cls, id):
        return ndb.Key(cls, id)
