# -*- coding: utf-8 -*-
from configuration import Configuration


class Worker:
    configuration = None

    def __init__(self, args):
        worker_configuration = Configuration()
        worker_configuration.parse(args)
        self.configuration = worker_configuration.config
