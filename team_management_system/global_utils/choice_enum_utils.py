import inspect

from enum import Enum


class ChoiceEnum(Enum):

    @classmethod
    def int_choices(cls):
        # get all members of the class
        members = inspect.getmembers(cls, lambda m: not(inspect.isroutine(m)))
        # filter down to just properties
        props = [m for m in members if not(m[0][:2] == '__')]
        # format into django choice tuple
        choices = tuple([(int(p[1].value), p[0]) for p in props])
        return choices

    @classmethod
    def str_choices(cls):
        # get all members of the class
        members = inspect.getmembers(cls, lambda m: not (inspect.isroutine(m)))
        # filter down to just proprties
        props = [m for m in members if not (m[0][:2] == '__')]
        # format into django choice tuple
        choices = tuple([(str(p[1].value), str(p[1].value)) for p in props])
        return choices

    @classmethod
    def choices(cls):
        choices = tuple([(v.value, k) for k, v in cls.__members__.items()])
        return choices

    @classmethod
    def key_choices(cls):
        return tuple([(key, key) for key in cls.__members__.keys()])

    @classmethod
    def list_choices(cls):
        # get all members of the class
        members = inspect.getmembers(cls, lambda m: not (inspect.isroutine(m)))
        props = [m for m in members if not (m[0][:2] == '__')]
        # format into django choice tuple
        choices = [p[1].value for p in props]
        return choices
