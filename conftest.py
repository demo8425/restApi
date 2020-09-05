import pytest
from os import path
import os

#File to write feched User Records
json_file = "user_info.json"


# Function: verify_user_list_data
# Usage: A Fixture with module level scope.
#        Get list of users and verify status_code==200 and Content-Type is application/json
# Returns: Get response data in json format
@pytest.fixture(scope="module")
def verify_user_list_data(request):
    received_data = getattr(request.module, "ra_obj").get_data(getattr(request.module, "getlist_url"))
    # Verify response status code equal to 200
    assert received_data.status_code == 200
    # Verify response Content is of application/json type
    assert "application/json" in received_data.headers['Content-Type']
    return received_data.json()


# Function: json_file_descriptor
# Usage: This is a Fixture to create a file descriptor session for the entire module to write data.
#        File closed after scope ends.
# Returns: File descriptor
@pytest.fixture(scope='session')
def json_file_descriptor(request):
    if path.exists(json_file):
        os.remove(json_file)
    jf = open(json_file, 'a+')

    def jf_close():
        jf.close()
    request.addfinalizer(jf_close)
    return jf
