from google.appengine.ext import ndb

class Issue(ndb.Model):
    id = ndb.IntegerProperty()
    date = ndb.StringProperty()
    pdf_url = ndb.StringProperty()
    image_url = ndb.StringProperty()
    content = ndb.StringProperty()

    def minimize(self):
        my_dict = self.to_dict()
        del my_dict['content']
        return my_dict

    def maximize(self):
        my_dict = self.to_dict()
        return my_dict

    def fill_from_old(self, old_issue):
        self.id = int(old_issue['title'])
        self.date = old_issue['date']
        self.pdf_url = old_issue['pdf']
        self.image_url = old_issue['cover']
        self.content = old_issue['editorial']
