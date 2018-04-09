from pymongo import MongoClient
from user import User

client = MongoClient("mongodb://bigbroqb:bigbrother@cluster0-shard-00-00-a4qe4.mongodb.net:27017,cluster0-shard-00-01-a4qe4.mongodb.net:27017,cluster0-shard-00-02-a4qe4.mongodb.net:27017/facebook?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin")
db = client.facebook #defines database to use
users = db.users #defines collection within database to use

def add_user_data(user):
	"""Creates new user entry with specified id if user does not exist, otherwise updates existing user entry with specified id"""
	if get_user_data(user) == None:
		return users.insert_one(user).inserted_id
	else:
		return "User already exists"

def get_user_data(user):
	"""Given unique id, returns the existing entry for that user"""
	user_dict = users.find_one({"_id": user["_id"]})
	if user_dict == None:
		return None
	user = User(None)
	for f in user_dict:
		setattr(user, f, user_dict[f])
	return user

def remove_user_data(user):
	return users.delete_one({"_id": user["_id"]})

def update_user_data(update):
	"""Need to fix"""
	return users.replace_one({"_id": id}, update)

def num_users():
	"""Returns the current number of existing user entries in the db"""
	return users.count()

user = {"_id": 1, "firstname": "Connor", "lastname": "Hebert", "dob": "11/08/1996", "location": "East Longmeadow", "posts": [], "gender": "Male"}

#add_user_data(user)
user = get_user_data(user)
print(user.firstname)