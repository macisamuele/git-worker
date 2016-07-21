# -*- coding: utf-8 -*-
from sys import argv

import return_codes
from worker import Worker


def main(args):
    worker = Worker(args)
    return_code = worker.run()
    if not isinstance(return_code, return_codes.Success):
        print return_code
    return return_code.code

if __name__ == '__main__':
    exit(main(argv[1:]))
