# -*- coding: utf-8 -*-
from sys import argv

from configuration import Configuration


def main(args):
    configuration = Configuration()
    configuration.parse(args)
    if configuration.config is None:
        return 0
    print configuration.config
    return 0

if __name__ == '__main__':
    exit(main(argv[1:]))
