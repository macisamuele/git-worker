# -*- coding: utf-8 -*-
import logging
from abc import ABCMeta
from abc import abstractmethod
from sys import stderr

import return_codes
from autologging import TRACE
from autologging import traced
from configuration import Configuration

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
    repository = None

    def __init__(self, configuration):
        super(RepositoryWorker, self).__init__()
        self.configuration = configuration
        if configuration is not None:
            self.repository = configuration['repository']

    def _is_master_branch(self):
        pass

    def _is_your_feature_branch(self):
        pass

    @traced(logging.getLogger('RepositoryWorker'))
    def _start(self):
        if self._is_master_branch():
            self.repository.remotes[self.configuration['git_remote']].pull()
        elif self._is_your_feature_branch():
            # fetch
            # merge / rebase
            # build
            # test
            pass
        return True

    @traced(logging.getLogger('RepositoryWorker'))
    def _join(self):
        return True

    @traced(logging.getLogger('RepositoryWorker'))
    def _pre_start(self):
        if self.configuration is None or self.repository is None:
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
