# -*- coding: utf-8 -*-
from argparse import ArgumentParser
from os.path import abspath
from os.path import dirname
from os.path import exists
from os.path import expanduser
from os.path import expandvars
from os.path import isabs
from os.path import join
from re import compile as regex_compile
from re import error as regex_error

from jsonschema import SchemaError
from jsonschema import validate
from jsonschema import ValidationError
from simplejson import dumps
from simplejson import load


class ConfigurationError(RuntimeError):
    pass


class Configuration:
    _parser = None  # Command line parser
    _json_schema = None  # Json schema for the configuration validation
    config = None  # Validated configuration

    def __init__(self, configuration_schema='configuration.json.schema'):
        self._json_schema = self._read_json(configuration_schema)

    def _read_json(self, json_path):
        with open(json_path) as json_file:
            return load(json_file)

    def _init_parser(self):
        parser = ArgumentParser()
        parser.add_argument('-c', '--config',
                            help='Configuration file. Default: config.json', default='config.json')
        parser.add_argument('-s', '--show-schema',
                            help='Get the Schema of the configuration file', action='store_true')
        parser.add_argument('-v', '--validate-configuration',
                            help='Validate the configuration file', action='store_true')
        self._parser = parser

    @staticmethod
    def _validate_regex(regex):
        # if regex is already a pattern object
        if isinstance(regex, type(regex_compile(''))):
            return regex
        try:
            return regex_compile('^{regex}$'.format(regex=regex))
        except regex_error:
            raise ConfigurationError('Invalid regex: {regex}'.format(regex=regex))

    @staticmethod
    def _validate_repository(repository_path):
        if exists(join(repository_path, '.git')):
            return repository_path
        else:
            raise ConfigurationError('Invalid Repository Path: {repository_path}'.format(repository_path=repository_path))

    def _validate_args(self, argparse_config):
        """
        Validate the configuration file and returns an object containing all the configuration
        defined for each repository.
        Note: the structure of the returned object is the same defined by the json schema with an additional field
        'repository' which will contain the git.Repo object targeted by the path

        :param argparse_config:
        :type argparse_config: Namespace
        :param only_schema_validation:
        :type only_schema_validation: bool
        :returns: None
        """
        raw_config = self._read_json(argparse_config.config)
        configuration_file_directory = dirname(argparse_config.config)
        try:
            validate(instance=raw_config, schema=self._json_schema)
        except ValidationError:
            raise ConfigurationError('Configuration not compliant to schema.')
        except SchemaError:
            raise ConfigurationError('Invalid schema definition.')

        # Checks he validity of the regular expression (it cannot be done by the JSON Schema)
        raw_config['default']['feature_branches'] = self._validate_regex(raw_config['default']['feature_branches'])

        # Checks that each repository path is targeting a git repository and that the override of the
        for repository, r_config in raw_config['repositories'].items():
            repository = expanduser(expandvars(repository))
            # Relative paths are considered starting from the configuration file
            if not isabs(repository):
                repository = abspath(join(configuration_file_directory, repository))
            if not exists(repository):
                raise ConfigurationError(
                    'Repository path "{repository_path}" not found'.format(
                        repository_path=repository,
                    )
                )
            if repository in self.config:
                raise ConfigurationError(
                    'Repository "{repository_path}" already defined'.format(
                        repository_path=repository,
                    )
                )

            # Set for the repository the overridden configurations (if available) otherwise use the default one
            repository_conf = {key: r_config.get(key, raw_config['default'][key]) for key in raw_config['default'].keys()}
            # Get the repository object
            repository_conf['repository'] = self._validate_repository(repository)
            # Check the validity of the regular expression
            repository_conf['feature_branches'] = self._validate_regex(repository_conf['feature_branches'])

            self.config[repository] = repository_conf

    def parse(self, args):
        if self._parser is None:
            self._init_parser()

        try:
            args = self._parser.parse_args(args)
            args.config = abspath(expanduser(expandvars(args .config)))
            if args.show_schema:
                print dumps(self._json_schema, sort_keys=True, indent=4 * ' ')
            else:
                if not exists(args.config):
                    raise ConfigurationError('Configuration file not found')
                self.config = {}
                self._validate_args(args)
                if args.validate_configuration:
                    self.config = None
        except ConfigurationError as e:
            self.config = None
            self._parser.error(e.message)
