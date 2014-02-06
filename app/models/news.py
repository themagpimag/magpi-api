from google.appengine.ext import ndb

class News(ndb.Model):
    date = ndb.StringProperty()
    title = ndb.StringProperty()
    content = ndb.StringProperty(indexed=False)

    def minimize(self):
        my_dict = self.to_dict()
        del my_dict['content']
        return my_dict

    def maximize(self):
        my_dict = self.to_dict()
        return my_dict

    def fill_from_old(self, old_news):
        self.title = old_news['title']
        self.content = old_news['summary']
        self.date = old_news['published']

    @classmethod
    def generate_key(cls, id):
        return ndb.Key(cls, id)
