# -*- coding: utf-8 -*-
class WorkerReturnCode:
    code = None
    message = None

    def __init__(self):
        pass

    def __str__(self):
        return '{code}: {message}'.format(code=self.code, message=self.message)

    def __repr__(self):
        return str(self)


class Success(WorkerReturnCode):
    code = 0
    message = 'Success'


class StartError(WorkerReturnCode):
    code = 1
    message = 'Start Error'


class JoinError(WorkerReturnCode):
    code = 2
    message = 'Join Error'


class ConfigurationError(WorkerReturnCode):
    code = 3
    message = 'Configuration Error'
