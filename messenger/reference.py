from redis import Redis
from threading import Thread
import pygame


pygame.init()

redis = Redis(host="178.62.216.119", port="4567", decode_responses=True)

if not redis.ping():
    raise Exception("The server does not respond")


# redis.set("message", "hello")
# message = redis.get("message")
# print(message)

def publisher():
    while True:
        redis.publish("messages", input())


def receiver():
    subscriber = redis.pubsub()
    subscriber.subscribe("messages")
    while True:
        received_msg = subscriber.get_message(ignore_subscribe_messages=True)
        if received_msg:
            print(received_msg)


p = Thread(target=publisher)
r = Thread(target=receiver)

p.start()
r.start()
