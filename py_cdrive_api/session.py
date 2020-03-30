import requests
from .client import CDriveClient

class Session:
    def __init__(self, domain, username=None, password=None, accessToken=None):
        self.domain = domain
        if accessToken != None:
            self.accessToken = accessToken
        elif (username != None and password != None):
            self.accessToken = self.get_token(username, password)
            self.home = "users/" + username
    def get_token(self, username, password):
        response = requests.post(url="https://api." + self.domain + "/api-access-token/", data={"username": username, "password": password})
        return response.json()['accessToken']
    def user_details(self):
        auth_header = "Bearer " + self.accessToken
        response = requests.get(url="https://api." + self.domain + "/user-details/", headers={"Authorization": auth_header})
        return response.json()
    def create_client(self):
        username = self.user_details()["username"]
        return CDriveClient(self.domain, username, self.accessToken)
