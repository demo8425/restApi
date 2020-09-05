import requests


class RestApi:

    # Function: get_data
    # Usage: Execute get request with provided url. On valid response returns the response body.
    # Returns: Response data
    def get_data(self, url):
        response = requests.get(url)
        return response

    # Function: post_data
    # Usage: Executes post request with provided url, data and header body. On valid response returns the response body.
    # Returns: Response data
    def post_data(self, url, data):
        response = requests.post(url, data)
        return response



