from pygame.event import Event
from time import sleep
import requests
from network_loop import network_queue, Message, error_handlers


# redis = Redis(host="178.62.216.119", port="4567")

host = "0.0.0.0"
port = 8087

base_url = f"http://{host}:{port}"


class Storage(dict):

    def signup(self, event: Event):

        if len(self["signup_username"]) < 3 or len(self["signup_password_1"]) < 3:
            self.error_msg("Username and password must be longer than 3 characters")
            return

        if self["signup_password_1"] != self["signup_password_2"]:
            self.error_msg("Your password is not correctly re-typed")
            return

        request = requests.Request(
            method="GET",
            url=base_url + "/signup",
            params={
                "login": self["signup_username"],
                "password1": self["signup_password_1"],
                "password2": self["signup_password_2"],
            }
        )

        def callback(response: requests.Response):
            if response.status_code == 200:
                self["active_screen"] = 2

        network_queue.append(Message(request, callback))

    def signin(self, event: Event):
        if len(self["signin_username"]) < 3 or len(self["signin_password"]) < 3:
            self.error_msg("Username and password must be longer than 3 characters")
            return

        request = requests.Request(
            method="GET",
            url=base_url + "/signin",
            params={
                "login": self["signin_username"],
                "password": self["signin_password"],
            }
        )

        def callback(response: requests.Response):
            self["token"] = response.json()
            token_file = open("token.txt", "w")
            token_file.write(self["token"])
            token_file.close()
            self["active_screen"] = 0
            self["signin_username"] = ""
            self["signin_password"] = ""

        network_queue.append(Message(request, callback))

    def add_friend(self, friend_id: str) -> None:
        response = requests.post(
            base_url + "/contacts",
            headers={"session-id": self["token"]},
            json={"contact_id": friend_id},
        )

        if response.status_code != 200:
            print(response.text)

    def get_contact_hints(self):
        if len(self["search"]) < 3:
            return

        request = requests.Request(
            method="GET",
            url=base_url + "/search",
            params={"prefix": self["search"]},
            headers={"session-id": self["token"]}
        )

        def callback(response: requests.Response):
            self["contact_hints"] = response.json()

        network_queue.append(Message(request, callback))

    def load_contacts(self):
        req = requests.Request(
            method="GET",
            url=base_url + "/contacts",
            headers={"session-id": self["token"]}
        )

        def callback(res: requests.Response):
            self["contacts"] = res.json()

        network_queue.append(Message(req, callback))

    def verify_tokey(self):
        res = requests.get(base_url + "/contacts", headers={
            "session-id": self["token"]
        })
        return res.status_code == 200

    def get_username(self):
        req = requests.Request(
            method="GET",
            url=base_url + "/username",
            headers={"session-id": self["token"]}
        )

        def callback(res: requests.Response):
            self["username"] = res.json()

        network_queue.append(Message(req, callback))

    def logout(self, event: Event):
        self["token"] = ""
        token_file = open("token.txt", "w")
        token_file.write("")
        token_file.close()
        self.move_to_signin(event)

    def click_contact(self, contact_id: str) -> None:
        self["chat_with"] = contact_id
        self.move_to_messages()

    def delete_contact(self, contact_id: str) -> None:
        res = requests.post(
            base_url + "/contacts/delete",
            json={"contact_id": contact_id},
            headers={"session-id": self["token"]},
        )

        if res.status_code != 200:
            print(res.content)
            return

        self.load_contacts()

    def send_message(self, event: Event):
        if self["message_txt"] == "":
            return
        if self.get("chat_with") is None:
            return

        req = requests.Request(
            method="POST",
            url=base_url + "/message",
            json={
                "contact_id": self["chat_with"],
                "content": self["message_txt"],
            },
            headers={
                "session-id": self["token"]
            },
        )

        def callback(response: requests.Response):
            if response.status_code != 200:
                print(response.content)
                return

            self["message_txt"] = ""

        network_queue.append(Message(req, callback))

    def move_to_signup(self, event: Event):
        self["active_screen"] = 1

    def move_to_signin(self, event: Event):
        self["active_screen"] = 2

    def move_to_contacts(self, event: Event):
        self["active_screen"] = 3

    def move_to_messages(self, event: Event = None):
        self["active_screen"] = 0

    def load_messages(self):
        res = requests.get(
            base_url + "/message",
            params={
                "contact_id": self["chat_with"],
                "start": self["msg_start"],
                "end": self["msg_end"],
            },
            headers={"session-id": self["token"]},
        )
        messages = []
        for item in res.json():
            messages.append(item.split("|"))

        messages.sort(key=lambda item: item[2])

        self["messages"] = messages

    def update_messages(self):
        while True:
            if self["exit"] is True:
                return
            if self["active_screen"] != 0:
                sleep(1)
                continue
            if self.get("chat_with") is None:
                sleep(1)
                continue
            self.load_messages()
            print("Loading messages...")
            sleep(1)

    def error_msg(self, msg: str):
        self["error_msg"] = msg


storage = Storage()


storage["messages"] = []
storage["contact_hints"] = []
storage["contacts"] = []
storage["exit"] = False
storage["message_input_top"] = 540
storage["msg_start"] = 0
storage["msg_end"] = 10
storage["error_msg"] = ""


def alarm_error_handler(res: requests.Response) -> None:
    detail = res.json().get("detail", "Unknown problem")
    storage["error_msg"] = detail


error_handlers.append(alarm_error_handler)
