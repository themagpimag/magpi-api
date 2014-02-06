from google.appengine.ext import ndb

class Issue(ndb.Model):
    id = ndb.IntegerProperty()
    id_issuu = ndb.StringProperty()
    date = ndb.StringProperty()
    pdf_url = ndb.StringProperty()
    image_url = ndb.StringProperty()
    content = ndb.StringProperty(indexed=False)

    def minimize(self):
        my_dict = self.to_dict()
        del my_dict['content']
        del my_dict['id_issuu']
        return my_dict

    def maximize(self):
        my_dict = self.to_dict()
        return my_dict

    def fill_from_old(self, old_issue):
        self.id = int(old_issue['title'])
        self.id_issuu = old_issue['issuu']
        self.date = old_issue['date']
        self.pdf_url = old_issue['pdf']
        self.image_url = old_issue['cover']
        self.content = old_issue['editorial']

    @classmethod
    def generate_key(cls, id):
        return ndb.Key(cls, id)
