from facebook import GraphAPI
import config


def create_test_user(app_id, graph):
	test_user = graph.request(app_id + '/accounts/test-users', {}, {}, method='POST')
	return test_user

def delete_test_user(graph, id):
	graph.request(id, {}, None, method='DELETE')
	
	
# Ex: create and then delete a test user
if __name__ == "__main__":
	graph = GraphAPI(access_token=config.FB_APP_SECRET)
	print("Creating test user ...")
	test_user = create_test_user(config.FB_APP_ID, graph)
	print("Test user: " + str(test_user))
	print("Deleting test user ...")
	delete_test_user(graph, test_user['id'])
	print("Done")
	