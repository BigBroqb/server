import json


class User(object):
    """docstring for [object Object]."""
    def __init__(self, fbid, firstname=None, lastname=None, gender=None, dob=None, location=None, posts=[]):
        self._id = fbid
        self.firstname = firstname
        self.lastname = lastname
        self.gender = gender
        self.dob = dob
        self.location = location

        self.posts = posts  # exclude

    def export_json(self):
        return json.dumps(export_dict())

    def export_dict(self):
        result = self.__dict__
        return result


