# -*- coding: utf-8 -*-
class GitCmd:
    repository_path = None

    def __init__(self, repository_path):
        self.repository_path = repository_path

    def current_branch(self):
        # git rev-parse --abbrev-ref HEAD
        pass

    def pull(self):
        pass

    def fetch(self):
        pass

    def merge(self):
        pass

    def rebase(self):
        pass

    def merge_abort(self):
        pass

    def rebase_abort(self):
        pass
