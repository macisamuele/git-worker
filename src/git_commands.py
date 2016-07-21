# -*- coding: utf-8 -*-
"""An encapsulation of shelled out git commands."""
import subprocess


class GitCommand:
    repository_path = None

    def __init__(self, repository_path):
        self.repository_path = repository_path

    def _do_command(self, command):
        """Generic command runner."""
        args = command.split()
        try:
            results = subprocess.check_output(args, cwd=self.repository_path)
            success = True
        except subprocess.CalledProcessError:
            results = ''
            success = False

        return results, success

    def current_branch(self):
        command = 'git rev-parse --abbrev-ref HEAD'

        return self._do_command(command)

    def pull(self, options=''):
        command = 'git pull {options}'.format(options=options)
        return self._do_comand(command)

    def fetch(self, options=''):
        command = 'git fetch {options}'.format(options=options)
        return self._do_command(command)

    def merge(self, options=''):
        command = 'git merge {options}'.format(options=options)
        return self._do_command(command)

    def rebase(self, options):
        command = 'git rebase {options}'.format(options=options)
        return self._do_command(command)

    def merge_abort(self):
        command = 'git merge --abort'
        return self._do_command(command)

    def rebase_abort(self):
        command = 'git rebase --abort'
        return self._do_command(command)
