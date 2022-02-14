import json

import easygui
import requests

import config


class Connection:
    def __init__(self, auth):
        self.js = {}
        self.auth = auth
        self.lobby_id = None

    def registrtion(self, data):
        js = json.dumps({"login": data[0], "password": data[1]})
        try:
            res = requests.post(config.SERVER + "/reg", data=js)
        except:
            easygui.exceptionbox("Connection error", "Requests exception")
            return 404
        if res.text == "Login exist":
            easygui.exceptionbox("Login exist", "Registration")
        self.auth = json.loads(js)
        print(js)
        return res

    def authorization(self, data):
        js = json.dumps({"login": data[0], "password": data[1]})
        try:
            res = requests.post(config.SERVER + "/auth", data=js)
        except:
            easygui.exceptionbox("Connection error", "Requests exception")
            return 404
        if res.text == "Login or password is not correct":
            easygui.exceptionbox("Login or password is not correct", "Authorization")
        elif res.text == "authorized":
            print(js)
            self.auth = json.loads(js)
            return res.text
        return res

    def set_new_game(self, battlefield):
        js = json.dumps({"name": self.auth["login"], "new_player": False, "deleted": False, "battlefield": battlefield})
        status_code = 200
        try:
            res = requests.post(config.SERVER + "/setnew", data=js)
        except:
            easygui.exceptionbox("Connection error", "Requests exception")
            return 404
        if res.status_code != 200 or res.text == "wait":
            status_code = res.status_code
            return "wait"
        else:
            self.js = res.json()
            self.lobby_id = self.js["id"]
            return self.js

    def get_new_game(self, search_name):
        print(self.auth)
        js = json.dumps({"name": self.auth["login"], "search": search_name})
        print(js)
        status_code = 200
        try:
            res = requests.post(config.SERVER + "/getnew", data=js)
        except:
            easygui.exceptionbox("Connection error", "Requests exception")
            return 404
        if res.status_code != 200 or res.text == "wait":
            status_code = res.status_code
        else:
            print(res.json())
            self.js = res.json()
            return res.json()
        return easygui.exceptionbox("Connection error", "Status code " + str(status_code))

    def set_game(self, moves):
        js = json.dumps({"name": self.auth["login"], "id": self.lobby_id, "moves": moves})
        status_code = 200
        try:
            res = requests.post(config.SERVER + "/setgame", data=js)
        except:
            easygui.exceptionbox("Connection error", "Requests exception")
            return 404
        if res.status_code == 200 or res.text == "game is set":
            return res.text
        else:
            return res.status_code

    def get_game(self):
        js = json.dumps({"login": self.auth["login"], "id": self.lobby_id})
        status_code = 200
        try:
            res = requests.post(config.SERVER + "/get", data=js)
        except:
            easygui.exceptionbox("Connection error", "Requests exception")
            return 404
        if res.text == "waiting enemy turn":
            return res.text
        elif res.status_code != 200:
            return easygui.exceptionbox("Connection error", "Status code " + str(res.status_code))
        else:
            print(res.json())
            self.js = res.json()
            return res.json()

    def win(self):
        js = json.dumps({"winner": self.js["name"], "loser": self.js["enemy"], "id": self.lobby_id})
        status_code = 200
        try:
            res = requests.post(config.SERVER + "/rating", data=js)
        except:
            easygui.exceptionbox("Connection error", "Requests exception")
            return 404
        if res.text == "you are winner":
            return res.text
        elif res.status_code != 200:
            return res.status_code

    def get_json(self):
        return self.js

    def get_auth(self):
        return self.auth

    def delete_lobby(self):
        js = json.dumps({"id": self.lobby_id})
        status_code = 200
        try:
            res = requests.post(config.SERVER + "/dellobby", data=js)
        except:
            easygui.exceptionbox("Connection error", "Requests exception")
            return 404
        if res.text == "Lobby is deleted":
            return res.text
        elif res.status_code != 200:
            return res.status_code
