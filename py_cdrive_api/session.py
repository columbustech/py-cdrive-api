import requests

class Session:
    def __init__(self, domain, username=None, password=None):
        self.domain = domain
        self.accessToken = None
        if (username != None and password != None):
            self.accessToken = self.get_token(username, password)
    def get_token(self, username, password):
        response = request.post(url="https://api." + self.domain + "/api-access-token/", data={"username": username, "password": password})

        
    def user_details(self):
        auth_header = "Bearer " + self.accessToken
        response = requests.get(url="https://api." + self.domain + "/user-details/", headers={"Authorization": auth_header})
        return response.json()
