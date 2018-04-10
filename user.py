import json

class User(object):
    """docstring for [object Object]."""
    def __init__(self, id, data=None):
        self._id = id
        self.generate_from_dict(data)

    def generate_from_dict(self, data):
        if data != None:
            data.pop('id', None)
            self.__dict__.update(data)

    def export_json(self):
        return json.dumps(self.__dict__)

    def export_dict(self):
        result = self.__dict__
        return result

    def __repr__(self):
        return(str(self.__dict__))