import json


class User(object):
    """docstring for [object Object]."""
    def __init__(self, fbid, firstname=None, lastname=None, gender=None, dob=None, location=None, posts=[]):
        self._id = fbid
        self.first_name = firstname
        self.last_name = lastname
        self.gender = gender
        self.birthday = dob
        self.location = location

        self.posts = posts  # exclude

    def export_json(self):
        return json.dumps(self.__dict__)

    def export_dict(self):
        result = self.__dict__
        return result


