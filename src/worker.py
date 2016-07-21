# -*- coding: utf-8 -*-
import logging
import subprocess
from abc import ABCMeta
from abc import abstractmethod
from sys import stderr

import return_codes
from autologging import TRACE
from autologging import traced
from configuration import Configuration
from git_commands import GitCmd

logging.basicConfig(level=TRACE, stream=stderr,
                    format='%(levelname)s | %(name)s | %(funcName)s:%(lineno)s | %(message)s')


class AbstractWorker:
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def _start(self):
        pass

    @abstractmethod
    def _join(self):
        pass

    @abstractmethod
    def _pre_start(self):
        pass

    def run(self):
        """
        Start and wait the execution of the RepositoryWorkers
        :return: return code specifying the exit status. WorkerSuccess() is returned if everything if the process is
            successfully completed, other extensions of WorkerReturnCode are returned in case of error
        :rtype: WorkerReturnCode
        """
        self._pre_start()
        if not self._start():  # problems to start the executions? kill everything
            return return_codes.StartError()
        if not self._join():  # problems to wait the RepositoryWorkers? report a log
            return return_codes.JoinError()
        return return_codes.Success()


class RepositoryWorker(AbstractWorker):
    """
    The class is handling the flow described on the
    `How it works <https://github.com/macisamuele/git-worker/#how-it-works>`_
    section of the README
    """

    configuration = None
    repository_cmds = None

    def __init__(self, configuration):
        super(RepositoryWorker, self).__init__()
        self.configuration = configuration
        if configuration is not None:
            self.repository_cmds = GitCmd(configuration['repository'])

    def _is_master_branch(self):
        return self.repository_cmds.current_branch() == self.configuration['master_branch']

    def _is_your_feature_branch(self):
        return self.configuration['feature_branches'].match(self.repository_cmds.current_branch()) is not None

    def _merge_rebase(self):
        if self.configuration['update_strategy'] == 'merge':
            return self.repository_cmds.merge(self.configuration['master_branch'])
        elif self.configuration['update_strategy'] == 'rebase':
            return self.repository_cmds.rebase(self.configuration['master_branch'])

    def _merge_rebase_abort(self):
        if self.configuration['update_strategy'] == 'merge':
            return self.repository_cmds.merge_abort()
        elif self.configuration['update_strategy'] == 'rebase':
            return self.repository_cmds.rebase_abort()

    @traced(logging.getLogger('RepositoryWorker'))
    def _start(self):
        if self._is_master_branch():
            return self.repository_cmds.pull('{remote} {branch}'.format(
                remote=self.configuration['git_remote'],
                branch=self.configuration['master_branch'],
            ))
        elif self._is_your_feature_branch():
            if not self.repository_cmds.fetch('{remote} {branch}'.format(
                remote=self.configuration['git_remote'],
                branch=self.configuration['master_branch'],
            )):
                return False
            self.repository_cmds.fetch(self.configuration['master_branch'])
            if not self._merge_rebase():
                self._merge_rebase_abort()
                return False
            try:
                subprocess.check_call(self.configuration['build_command'].split())
                subprocess.check_call(self.configuration['test_command'].split())
            except subprocess.CalledProcessError:
                self._merge_rebase_abort()
                return False

        return True

    @traced(logging.getLogger('RepositoryWorker'))
    def _join(self):
        return True

    @traced(logging.getLogger('RepositoryWorker'))
    def _pre_start(self):
        if self.configuration is None or self.repository_cmds is None:
            return return_codes.ConfigurationError()

    def __repr__(self):
        return str(self.configuration['repository'].git_dir)


class Worker(AbstractWorker):
    """
    The class is handling the whole git-worker process:
        - configuration fetching and validation
        - spinning elaboration for each repository (sequential way or one process per repository

    Basically it acts as a manager for the RepositoryWorkers
    """
    configuration = None

    def __init__(self, args):
        super(Worker, self).__init__()
        worker_configuration = Configuration()
        worker_configuration.parse(args)
        self.configuration = worker_configuration.config

    @traced(logging.getLogger('Worker'))
    def _start(self):
        """
        Start the execution of the RepositoryWorker or every required repository

        NOTE: the execution of the RepositoryWorkers is executed in a sequential way (single process)

        :return: True if the start process is correctly performed, False otherwise
        :type: bool
        """

        for repository_path, repository_config in self.configuration.items():
            print repository_path
            repository_worker = RepositoryWorker(repository_config)
            repository_worker.run()

        return True

    @traced(logging.getLogger('Worker'))
    def _join(self):
        """
        Wait the execution end of all the started RepositoryWorkers

        :return: True if the waiting process is correctly performed, False otherwise
        :type: bool
        """

        # for repository_path, repository_config in self.configuration.items():
        #     print repository_path

        return True

    @traced(logging.getLogger('Worker'))
    def _pre_start(self):
        if self.configuration is None:
            return return_codes.ConfigurationError()
