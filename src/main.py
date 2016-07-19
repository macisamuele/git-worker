# -*- coding: utf-8 -*-
from sys import argv

from worker import Worker


def main(args):
    worker = Worker(args)
    if worker.configuration is None:
        return 0
    print worker.configuration
    return 0

if __name__ == '__main__':
    exit(main(argv[1:]))
