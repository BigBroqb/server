from pymongo import MongoClient

from user import User
import config

client = MongoClient(config.MONGO_URL)
db = client.facebook #defines database to use
users = db.users #defines collection within database to use

def add_user_data(user):
    """Creates new user entry from User model."""
    assert isinstance(user, User)
    if get_user_data(user) == None:
        return users.insert_one(user.export_dict()).inserted_id
    else:
        return 409 # HTTP code for conflict

def get_user_data(user):
    """Given unique id, returns the existing entry for that user"""
    assert isinstance(user, User)
    user_dict = users.find_one({"_id": user._id})
    if user_dict == None:
        return None
    return User(user._id, user_dict)

def remove_user_data(user):
    assert isinstance(user, User)
    return users.delete_one({"_id": user._id})

def update_user_data(user):
    assert isinstance(user, User)
    return users.replace_one({"_id": user._id}, user.export_dict())

def num_users():
    """Returns the current number of existing user entries in the db"""
    return users.count()