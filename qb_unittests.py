# Make sure you have Facebook-SDK, Flask, MongoDB and PyMongo installed
# Facebook-SDK http://facebook-sdk.readthedocs.io/en/latest/
# Flask http://flask.pocoo.org/docs/0.12/installation/
# MongoDB https://docs.mongodb.com/manual/installation/
# PyMongo https://api.mongodb.com/python/current/installation.html

# Ex. directory structure:
# root/
#   config.py
#   qb_unittests.py (this file)
#   database.py
#   server.py
#   user.py   

# Information about unittest(Python3) https://docs.python.org/3/library/unittest.html
# PyMongo tutorial http://api.mongodb.com/python/current/tutorial.html
# How to use Mongo shell https://docs.mongodb.com/manual/mongo/

import unittest
from pymongo import MongoClient
import config # User-defined module
import sys
from pymongo.errors import ServerSelectionTimeoutError
from user import User
from database import*
from server import*
from facebook_test_users import create_test_user, delete_test_user

# Test class for user.py
class UserTestCase(unittest.TestCase):
	def setUp(self):
		self.id = 1
		self.args = {"id": self.id, "last name": "Doe", "first name": "Jane", "gender": "Female", "DOB": "1/1/1999", "city" : "Boston"}
		self.expected_dict = {"_id": 1, "last name": "Doe", "first name": "Jane", "gender": "Female", "DOB": "1/1/1999", "city": "Boston"}
	
	def test__init__with_no_data(self):
		user = User(self.id)
		self.assertEqual(1, user._id)
		self.assertNotEqual(0, user._id)
		self.assertEqual({"_id": 1}, user.__dict__)
		
	def test__init__with_data(self):
		user = User(self.id, self.args)
		self.assertEqual(self.expected_dict, user.__dict__)	
		
	def test_generate_from_dict(self):
		user = User(self.id)
		user.generate_from_dict(self.args)
		self.assertEqual(self.expected_dict, user.__dict__)
			
	def test_export_json(self):
		# Export JSON for user with no data
		user = User(self.id)
		self.assertEqual('{"_id": 1}', user.export_json())
		
		# Export JSON for user with data
		user = User(self.id, self.args)
		self.assertEqual('{"_id": 1, "last name": "Doe", "first name": "Jane", "gender": "Female", "DOB": "1/1/1999", "city": "Boston"}',
			(user.export_json()))
			
	def test_export_dict(self):
		# Export dictionary for user with no data
		user = User(self.id)
		self.assertEqual({"_id": 1}, user.export_dict())
		
		# Export dictionary for user with data
		user = User(self.id, self.args)
		self.assertEqual(self.expected_dict, user.__dict__)
		
	def test__repr__(self):
		# User with no data
		user = User(self.id)
		self.assertEqual(str({'_id': 1}), user.__repr__())
		
		# User with data
		user = User(self.id, self.args)
		self.assertEqual(str(self.expected_dict),
			(user.__repr__()))

# Test class for database.py
# A MongoDB instance should be running on config.MONGO_URL 
# config.MONGO_URL can be set to the default host and port
class DatabaseTestCase(unittest.TestCase):
	def setUp(self):
		try:
			# Make a mongo client just to test if the MongoDB instance is running
			# We won't actually use this client
			test_client = MongoClient(config.MONGO_URL, serverSelectionTimeoutMS=1000)
			test_client.server_info() # Force connection on a request
			test_client.close()
		except ServerSelectionTimeoutError:
			# If the client took too long to connect, then the instance isn't running
			test_client.close()
			sys.exit("\nServer on " + config.MONGO_URL + " not available")
		
		# Delete all documents from the collection before starting any test
		users.delete_many({})
		
		self.id = 1
		self.args = {"id": self.id, "last name": "Doe", "first name": "Jane", "gender": "Female", "DOB": "1/1/1999", "city" : "Boston"}
		self.expected_dict = {"_id": 1, "last name": "Doe", "first name": "Jane", "gender": "Female", "DOB": "1/1/1999", "city": "Boston"}
		self.user = User(self.id, self.args)
		self.invalid_user = 0
	
	# Make sure to delete all documents from the collection at the end of each test
	def tearDown(self):
		users.delete_many({}) 
	
	def test_add_user_data(self):
		# Add user with no data
		user_with_no_data = User(2)
		id = add_user_data(user_with_no_data)
		self.assertEqual(2, id)
		self.assertNotEqual(409, id)
		
		# Add same user again
		self.assertEqual(409, add_user_data(user_with_no_data))
		
		# Add user with data
		id = add_user_data(self.user)
		self.assertEqual(1, id)
		self.assertNotEqual(409, id)
		
		# Add same user again
		self.assertEqual(409, add_user_data(self.user))
		
		# Non-User-object as input
		self.assertRaises(AssertionError, add_user_data, self.invalid_user)
	
	def test_get_user_data(self):
		# Get user data when there are no users
		self.assertEqual(None, get_user_data(self.user))
		
		# Get user data from existing user with data
		users.insert_one(self.user.export_dict())
		self.assertEqual(self.expected_dict, get_user_data(self.user).export_dict())
		
		# Get user data from existing user with no data
		user_with_no_data = User(2)
		users.insert_one(user_with_no_data.export_dict())
		self.assertEqual({"_id": 2}, get_user_data(user_with_no_data).export_dict())
		
		# Non-User-object as input
		self.assertRaises(AssertionError, get_user_data, self.invalid_user)
		
	def test_remove_user_data(self):
		# Remove user data when there are no users
		deleted_count = remove_user_data(self.user).deleted_count
		self.assertEqual(0, deleted_count)
		
		# Remove user data when there is a match
		users.insert_one(self.user.export_dict())
		deleted_count = remove_user_data(self.user).deleted_count
		self.assertEqual(1, deleted_count)
		
		# Remove user data when there is no match
		unknown_user = User(2)
		deleted_count = remove_user_data(unknown_user).deleted_count
		self.assertEqual(0, deleted_count)
		
		# Non-User-object as input
		self.assertRaises(AssertionError, remove_user_data, self.invalid_user)
		
	def test_update_user_data(self):
		# Update user data when there are no users
		result = update_user_data(self.user)
		self.assertEqual(0, result.matched_count)
		self.assertEqual(0, result.modified_count)
		
		# Update one user's data with the same data
		users.insert_one(self.user.export_dict())
		result = update_user_data(self.user)
		self.assertEqual(1, result.matched_count)
		self.assertEqual(0, result.modified_count)
		
		# Update one user's data with different data
		updated_args = {"id": self.id, "last name": "Doe", "first name": "Jane", "gender": "Female", "DOB": "1/1/1999", "city" : "New York"}
		updated_user = User(self.id, updated_args)
		result = update_user_data(updated_user)
		self.assertEqual(1, result.matched_count)
		self.assertEqual(1, result.modified_count)
		
		# Update user data when there is no match
		unknown_user = User(2)
		result = update_user_data(unknown_user)
		self.assertEqual(0, result.matched_count)
		self.assertEqual(0, result.modified_count)
		
		# Non-User-object as input
		self.assertRaises(AssertionError, update_user_data, self.invalid_user)
	
	def test_num_users(self):
		# Number of users before adding any user
		self.assertEqual(0, num_users())
		
		# Number of users after adding one user
		users.insert_one(self.user.export_dict())
		self.assertEqual(1, num_users())
		
		# Number of users after deleting one user
		users.delete_one({"_id": self.user._id})
		self.assertEqual(0, num_users())
		
class ServerTestCase(unittest.TestCase):
	def setUp(self):
		self.test_user = create_test_user(config.FB_APP_ID, graph)
		
	def tearDown(self):
		delete_test_user(graph, self.test_user['id'])
		
	def test_get_user_from_fb(self):
		user = get_user_from_fb(self.test_user['id'])
		self.assertEqual(self.test_user['id'], user.export_dict()['_id'])
	
	def test_get_user_by_name(self):
		pass
		
	def test_receive_webhook(self):
		pass
		
	def test_index(self):
		pass
		
		
		
def suite():
	suite = unittest.TestSuite()
	suite.addTest(UserTestCase('test__init__with_no_data'))
	suite.addTest(UserTestCase('test__init__with_data'))
	suite.addTest(UserTestCase('test_generate_from_dict'))
	suite.addTest(UserTestCase('test_export_json'))
	suite.addTest(UserTestCase('test_export_dict'))
	suite.addTest(UserTestCase('test__repr__'))
	suite.addTest(DatabaseTestCase('test_add_user_data'))
	suite.addTest(DatabaseTestCase('test_get_user_data'))
	suite.addTest(DatabaseTestCase('test_remove_user_data'))
	suite.addTest(DatabaseTestCase('test_update_user_data'))
	suite.addTest(DatabaseTestCase('test_num_users'))
	suite.addTest(ServerTestCase('test_get_user_from_fb'))
	return suite
	
if __name__ == '__main__':
	warning = "\nconfig.MONGO_URL is set to " + config.MONGO_URL + "\nTesting will delete all documents from the specified collection '" + str(users.full_name) + "'.\nProceed? Y/N\n"
	while True:
		# Person testing needs to type "Y", "y", "N", or "n" into console
		input_string = input(warning).lower()
		if (input_string == "y"):
			break
		if (input_string == "n"):
			sys.exit()
					
	# Set limit for number of levels of traceback information
	sys.tracebacklimit = 1 
	
	runner = unittest.TextTestRunner()
	runner.run(suite())
		