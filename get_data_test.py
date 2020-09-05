import pytest
from RestAPI import RestApi
import json


getlist_url = "https://reqres.in/api/users?page=2"
getinfo_url = "https://reqres.in/api/users/"
post_url = "https://reqres.in/api/users"

ra_obj = None


# Function: setup_module
# Usage: setup the RestApi object at module level
# Returns: None
def setup_module(module):
    global ra_obj
    ra_obj = RestApi()


# Function: test_display_user_name
# Usage: verify all record has "first_name". Display the first name of all user in the list
# Returns: None
@pytest.mark.userlist
def test_display_user_name(verify_user_list_data):
    received_data = verify_user_list_data['data']
    assert all("first_name" in record.keys() for record in received_data)
    print("User List: {}".format([item['first_name'] for item in received_data]))


# Function: test_validate_keys
# Usage: verify every user records has all keys
# Returns: None
@pytest.mark.userlist
def test_validate_keys(verify_user_list_data):
    received_data = verify_user_list_data['data']
    keys = ["id", "email", "first_name", "last_name", "avatar"]
    assert all(key in keys for record in received_data for key in record.keys())


# Function: test_fetch_user
# Usage: Fetch details of an user by id. verify keys and display user information
# Returns: None
@pytest.mark.singleuser
@pytest.mark.parametrize("user_id", [2, 3, 4, 5])
def test_fetch_user(json_file_descriptor, user_id):
    received_data = ra_obj.get_data(getinfo_url+str(user_id))
    # Verify response status code equal to 200
    assert received_data.status_code == 200
    # Verify response Content is of application/json type
    assert "application/json" in received_data.headers['Content-Type']
    user_data = received_data.json()['data']
    assert len(user_data.keys()) == 5
    keys = ["id", "email", "first_name", "last_name", "avatar"]
    assert all(key in keys for key in user_data.keys())
    # Display Fetched User Information
    print("User Information:")
    for key, value in user_data.items():
        print("{} : {}".format(key, value))
    json.dump(user_data, json_file_descriptor)


# Function: crete_user
# Usage: Create a new user. Verify the Status Code and Content Type. Verify the response data
# Returns: None
@pytest.mark.parametrize("data", [
    {"name": "morpheus", "job": "leader"},
    {"name": "morpheus2", "job": "leader2"},
    {"name": "morpheus3", "job": "leader3"}])
def test_create_user(data):
    received_data = ra_obj.post_data(post_url, data)
    # Verify response status code equal to 201
    assert received_data.status_code == 201
    # Verify response Content is of application/json type
    assert "application/json" in received_data.headers['Content-Type']
    user_data = received_data.json()
    assert user_data['name'] == data['name']
    assert user_data['job'] == data['job']
    assert any(key in ['id', "createdAt"] for key in user_data.keys())
