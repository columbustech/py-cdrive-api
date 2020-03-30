import os, requests

class CDriveClient:
    def __init__(self, domain, username, token):
        self.domain = domain
        self.api_url = "https://api." + domain + "/"
        self.token = token
        self.username = username
        self.home = "users/" + username
    def upload(self, local_path, cdrive_path):
        if os.path.isdir(local_path):
            data = {
                "path": cdrive_path,
                "name": os.path.basename(local_path)
            }
            requests.post(self.api_url + "create/", data=data, headers={"Authorization": "Bearer " + self.token})
            for obj_name in os.listdir(local_path):
                self.upload(os.path.join(local_path, obj_name), cdrive_path + "/" + data["name"])
        elif os.path.isfile(local_path):
            f = open(local_path, "rb")
            file_name = os.path.basename(local_path)
            file_arg = {"file": (file_name, f), "path": (None, cdrive_path)}
            requests.post(self.api_url + "upload/", files=file_arg, headers={"Authorization": "Bearer " + self.token})
            f.close()
    def list(self, cdrive_path, recursive=False):
        pass
    def delete(self, cdrive_path):
        pass
    def download(self, cdrive_path):
        pass
    def share(self, cdrive_path, permission, target_name="", target_type="user"):
        data = {
            "path": cdrive_path,
            "permission": permission,
            "targetType": target_type,
            "name": target_name
        }
        response = requests.post(self.api_url + "share/", data=data, headers={"Authorization": "Bearer " + self.token})
    def install_app(self, app_url):
        response = requests.post(self.api_url + "install-application/", data={"app_docker_link": app_url}, headers={"Authorization": "Bearer " + self.token})
        if response.status_code == 201:
            app_name = response.json()["appName"]
            while(True):
                res = requests.get(self.api_url + "app-status/?app_name=" + app_name, headers={"Authorization": "Bearer " + self.token})
                if res.status_code == 200 and res.json()["appStatus"] == "Available":
                    break
            return app_name
    def app_token(self, app_name):
        response = requests.post(self.api_url + "app-token/", data={"app_name": app_name}, headers={"Authorization": "Bearer " + self.token})
        if response.status_code == 200:
            return response.json()["app_token"]
