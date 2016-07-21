# -*- coding: utf-8 -*-
import os.path

import pytest
from docker import Client

from src.git_commands import GitCommand
# logging.basicConfig(level=TRACE, stream=stderr, format='%(levelname)s | %(name)s | %(funcName)s:%(lineno)s | %(message)s')


@pytest.fixture(scope='module')
def docker_client():
    cli = Client(base_url='unix://var/run/docker.sock')
    return cli


@pytest.fixture(scope='module')
def build_docker_container(docker_client):
    project_root_path = os.path.abspath(os.path.join(
        os.path.dirname(__file__),
        '../',
    ))
    test_dir = os.path.join(project_root_path, 'tests')
    docker_image_tag_name = 'git-worker:{sha}-testing-{user}'.format(
        sha=GitCommand(project_root_path).current_branch_sha(short=True),
        user=os.getenv('USER', 'git-worker-test-user')
    )

    def setup():
        docker_client.build(path=test_dir, tag=docker_image_tag_name)

    def teardown():
        docker_client.remove_image(
            image=docker_image_tag_name,
            force=True,
        )

    setup()
    yield docker_image_tag_name
    teardown()


@pytest.fixture
def start_stop_docker_container(build_docker_container, docker_client):
    """
    Starts and stop a new git server for every test method
    """
    def get_deep(dictionary, path, default=None, delimiter='.'):
        parts = path.split(delimiter)
        if not dictionary or not isinstance(dictionary, dict) or not parts:
            return default
        try:
            result = dictionary.get(parts[0], default)
            for part in parts[1:]:
                result = result.get(part, default)
            return result
        except IndexError:
            return default
    container_info = {}

    def setup():
        container_info['docker-port'] = 8181
        container = docker_client.create_container(
            image=build_docker_container,
            ports=[container_info['docker-port']],
            host_config=docker_client.create_host_config(
                port_bindings={
                    container_info['docker-port']: None,
                }
            ),
        )
        container_info['Id'] = container['Id']
        docker_client.start(container_info['Id'])
        container_info['docker-host'] = get_deep(
            dictionary=docker_client.inspect_container(container_info),
            path='NetworkSettings.Networks.bridge.IPAddress',
        )
        container_info['host-port'] = docker_client.port(
            container,
            container_info['docker-port']
        )[0]['HostPort']

    def teardown():
        docker_client.remove_container(container=container_info, force=True)

    setup()
    yield 'http://{host}:{port}'.format(
        host='localhost',
        port=container_info['host-port'],
    )
    teardown()


@pytest.fixture
def git_server(start_stop_docker_container):

    pass


def test_worker1(git_server):
    assert True


def test_worker2(start_stop_docker_container):
    assert True
