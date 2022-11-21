import time
import datetime


class Cache(object):
    # Тут будет хранится сам объект кеша, который будет или создан, или возвращаться при попытке создать новый
    # экземпляр
    _instance = None
    #

