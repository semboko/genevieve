from time import sleep
import requests
from requests import Request
from typing import List, Callable
from threading import Thread
from dataclasses import dataclass


@dataclass
class Message:
    req: Request
    callback: Callable


network_queue: List[Message] = []


error_handlers = []


def network_loop(storage):
    session = requests.Session()
    while True:
        if storage["exit"] is True:
            print("Exiting from the network loop...")
            return
        if len(network_queue) > 0:
            message = network_queue.pop()
            prep = message.req.prepare()
            res = session.send(prep)

            if res.status_code != 200 and len(error_handlers) > 0:
                for handler in error_handlers:
                    handler(res)

            message.callback(res)

        print("Network loop step...")
        sleep(0.2)
