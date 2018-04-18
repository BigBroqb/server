import unittest

import sys
sys.path.append('../')

import database as db
from user import User

class TestDatabase(unittest.TestCase):
	test_user = User(-1, {})

	def test_new_user(self):
		self.assertEqual(db.add_user_data(self.test_user), self.test_user._id)
		return

	def test_update_user(self):
		self.assertEqual(db.update_user_data(self.test_user).upserted_id, self.test_user._id)
		return

	def test_get_user(self):
		#self.assertEqual(first, second)
		return

	def test_delete_user(self):
		self.assertEqual(db.remove_user_data(self.test_user).deleted_count, 1)
		return

if __name__ == '__main__':
    unittest.main()