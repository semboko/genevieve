import pygame
pygame.init()

from pygame import Vector2
from gui.elements import (
    ScreenTitle,
    TextInput,
    Button,
    MessagesList,
    TextInputWHints,
    ElementList,
    DynamicText,
    ResizableTextInput,
)
from gui.screen import Screen
from typing import List, Optional
from storage import storage
from os import listdir
from threading import Thread
from network_loop import network_loop


WINDOW_WIDTH, WINDOW_HEIGHT = 400, 600


class Application:
    def __init__(self, screen_size: Vector2) -> None:
        self.screen_size = screen_size
        self.screens: List[Screen] = []
        # self.screen_idx: Optional[int] = None

        self.main_surface = pygame.display.set_mode(screen_size)
        self.clock = pygame.time.Clock()

        self.last_screen: Optional[Screen] = None

    def before_launch(self):
        if "token.txt" not in listdir("."):
            return
        token_file = open("token.txt", "r")
        token = token_file.readline()
        token_file.close()
        storage["token"] = token
        if not storage.verify_tokey():
            storage["token"] = ""
            return
        storage["active_screen"] = 0
        storage.get_username()

    def add_screen(self, screen: Screen, active: bool = False) -> None:
        self.screens.append(screen)
        screen.post_setup()
        if active:
            storage["active_screen"] = len(self.screens) - 1

    def launch(self) -> None:
        if len(self.screens) == 0 or storage["active_screen"] is None:
            raise Exception("Nothing to show")

        update_thread = Thread(target=storage.update_messages)
        update_thread.start()

        network_thread = Thread(target=network_loop, args=(storage, ))
        network_thread.start()

        while True:
            active_screen: Screen = self.screens[storage["active_screen"]]
            if active_screen != self.last_screen:
                self.last_screen = active_screen
                for callback in active_screen.on_render:
                    callback()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    storage["exit"] = True
                    update_thread.join()
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    active_screen.handle_mouseclick(event)
                if event.type == pygame.KEYDOWN:
                    # if event.key == pygame.K_LCTRL:
                    #     storage.load_messages()

                    active_screen.handle_keypress(event)

            self.main_surface.fill((255, 255, 255))

            active_screen.draw(self.main_surface)

            pygame.display.update()
            self.clock.tick(40)


messenger_screen = Screen()
messenger_screen.add_element(
    ScreenTitle(Vector2(0, 20), "Messages")
)
messenger_screen.add_element(
    DynamicText(Vector2(20, 80), Vector2(0, 0), "chat_with", "No contact was choosen", 20)
)
messenger_screen.add_element(
    ResizableTextInput(Vector2(20, WINDOW_HEIGHT - 40 - 20), Vector2(WINDOW_WIDTH - 2 * 20, 40), "message_txt")
)
messenger_screen.add_element(
    Button(Vector2(WINDOW_WIDTH - 20 - 5 - 70, WINDOW_HEIGHT - 20 - 5 - 30), Vector2(70, 30), "Send", storage.send_message)
)
messenger_screen.add_element(
    MessagesList(Vector2(20, WINDOW_HEIGHT - 80 - 400), Vector2(WINDOW_WIDTH - 40, 400))
)
messenger_screen.add_element(
    Button(Vector2(20, 20), Vector2(100, 40), "Contacts", storage.move_to_contacts)
)
messenger_screen.add_element(
    Button(Vector2(WINDOW_WIDTH - 120, 20), Vector2(100, 40), "Sign Out", storage.logout)
)

signup_screen = Screen()
signup_screen.add_element(
    ScreenTitle(Vector2(0, 20), "Sign Up")
)
signup_screen.add_element(
    TextInput(Vector2(20, 150), Vector2(WINDOW_WIDTH - 40, 40), "signup_username", "Username")
)
signup_screen.add_element(
    TextInput(Vector2(20, 220), Vector2(WINDOW_WIDTH - 40, 40), "signup_password_1", "Password")
)
signup_screen.add_element(
    TextInput(Vector2(20, 290), Vector2(WINDOW_WIDTH - 40, 40), "signup_password_2", "Retype your Password")
)
signup_screen.add_element(
    Button(Vector2(WINDOW_WIDTH/2 - 50, 350), Vector2(100, 40), "Submit", storage.signup)
)
signup_screen.add_element(
    Button(Vector2(WINDOW_WIDTH/2 - 50, 410), Vector2(100, 40), "Sign In", storage.move_to_signin)
)


signin_screen = Screen()
signin_screen.add_element(
    ScreenTitle(Vector2(0, 20), "Sign In")
)
signin_screen.add_element(
    TextInput(Vector2(20, 150), Vector2(WINDOW_WIDTH - 40, 40), "signin_username", "Username")
)
signin_screen.add_element(
    TextInput(Vector2(20, 220), Vector2(WINDOW_WIDTH - 40, 40), "signin_password", "Password")
)
signin_screen.add_element(
    Button(Vector2(WINDOW_WIDTH/2 - 50, 290), Vector2(100, 40), "Submit", storage.signin)
)
signin_screen.add_element(
    Button(Vector2(WINDOW_WIDTH/2 - 50, 350), Vector2(100, 40), "Sign Up", storage.move_to_signup)
)


contacts_screen = Screen()
contacts_screen.add_on_render(storage.load_contacts)
contacts_screen.add_element(
    ScreenTitle(Vector2(0, 20), "Contacts")
)
contacts_screen.add_element(
    Button(Vector2(20, 20), Vector2(100, 40), "Messages", storage.move_to_messages)
)

contacts_screen.add_element(
    ElementList(
        Vector2(20, 140),
        Vector2(WINDOW_WIDTH - 40, 400),
        "contacts",
        storage.load_contacts,
        storage.click_contact,
    )
)

contacts_screen.add_element(
    TextInputWHints(Vector2(20, 80), Vector2(WINDOW_WIDTH - 40, 40), "search", "Search")
)


messenger = Application(Vector2(WINDOW_WIDTH, WINDOW_HEIGHT))
messenger.add_screen(messenger_screen)
messenger.add_screen(signup_screen)
messenger.add_screen(signin_screen, active=True)
messenger.add_screen(contacts_screen)
messenger.before_launch()
messenger.launch()
