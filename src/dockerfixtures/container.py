# -*- coding: utf-8; -*-
import logging
import subprocess
import time
from typing import Any, Dict

import docker

from .image import Image

_CONTAINER_DEFAULT_OPTIONS = dict(cap_add=['IPC_LOCK'],
                                  mem_limit='256m',
                                  # privileged=True,
                                  detach=True,
                                  publish_all_ports=True
                                  )

CONTAINER_STATUS_CREATED = 'created'
CONTAINER_STATUS_DEAD = 'dead'
CONTAINER_STATUS_EXITED = 'exited'
CONTAINER_STATUS_PAUSED = 'paused'
CONTAINER_STATUS_RUNNING = 'running'
# Couldn't find those in the docker module... need to look harder

_OK_CONTAINER_STATUSES = (CONTAINER_STATUS_RUNNING,
                          )
_KO_CONTAINER_STATUSES = (CONTAINER_STATUS_DEAD,
                          CONTAINER_STATUS_EXITED,
                          )
_WAIT_CONTAINER_STATUSES = (CONTAINER_STATUS_CREATED,
                            CONTAINER_STATUS_PAUSED,
                            )


class TimeOut(Exception):
    pass


class Container:
    """Represents a container
    """
    __slots__ = ('__client',
                 '__container',
                 '__environment',
                 '__image',
                 '__max_wait',
                 '__options',
                 '__poll_interval',
                 )

    def __enter__(self):
        self.run()
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.__container.kill()
        self.__container.remove()
        if exc_value:
            raise exc_value

    def __init__(self,
                 image: Image,
                 *,
                 dockerclient: docker.client.DockerClient = None,
                 environment: Dict[str, str] = None,
                 max_wait: int = 10,
                 options=None,
                 poll_interval: int = 1,
                 ):
        """

        TODO: Build container from an ID ?
        """
        assert max_wait >= 0
        self.__client = dockerclient
        self.__container = None
        self.__environment = _prune_dict({** image.default_environment, **(environment or dict())})
        self.__image = image
        self.__max_wait = max_wait
        self.__options = options or dict()
        self.__poll_interval = poll_interval

    def check(self):
        """Runs the check command provided by the image.

        If the command fails, the container is assumed to have
        crashed.  If it succeeds the container is assumed to have
        started properly and is running.

        """
        command = self.__image.check_command(self)
        subprocess.check_call(command, shell=False)

    @property
    def address(self):
        """Returns the container's IP address
        """
        try:
            network = self.__container.attrs['NetworkSettings']
            ip = network['IPAddress']
        except KeyError:
            ip = ''

        if not ip:
            ip = 'localhost'  # !!
        return ip

    @property
    def id(self):
        """The identifier of the container, or None.

        The value None is only returnd if the container has not been
        started yet.

        """
        return self.__container.id if self.__container else None

    @property
    def image(self):
        """Returns the Image the container is based upon.
        """
        return self.__image

    def kill(self):
        self.__container.kill()

    @property
    def options(self) -> Dict[str, Any]:
        """Returns the options to use to create the container from the image.

        The value return by this attribute is the union of the default
        options (:var:`_CONTAINER_DEFAULT_OPTIONS`) and the optoins you
        passed upon the :class:`.Container` object construction.

        These are equivalent to the options you would pass to the
        :program:`docker` command line. The options in question exclude
        some that have dedicated arguments:

        - `environment` to manage the containers environment variables;
        - `environment` to manage the containers environment variables;

        """
        options = {**_CONTAINER_DEFAULT_OPTIONS, **self.__options}
        return options

    def remove(self) -> None:
        if self.__container is not None:
            self.__container.remove(v=True, force=True)

    def run(self, dockerclient=None):
        """Starts the container

        Raises:
            docker.errors.ImageNotFound: if the image to use to build the container cannot be found.
            docker.errors.APIError: if the docker server returns an Error, any other error.
            RuntimeError: if the container fails to start after
            ValueError: if you failed to

        """
        self.__client = dockerclient or self.__client  # Override client if requested
        if self.__client is None:
            raise ValueError('You did not provide a docker client !')

        try:
            image = self.__client.images.get(self.__image.pullname)
        except docker.errors.ImageNotFound as exc:
            raise ImageNotFound("Image '%s' does not exist", self.__image.pullname) from exc

        logging.getLogger(__name__).debug('Starting container from image: %s', self.__image.name,
                                          extra={'pullname': self.__image.pullname,
                                                 'environment': self.__environment,
                                                 'options': self.options,
                                                 })
        self.__container = self.__client.containers.run(image=image,
                                                        environment=self.__environment,
                                                        **self.options,
                                                        )
        for _ in range(self.__max_wait):
            # Ain't there a synchronous API ?
            self.__container.reload()
            logging.getLogger(__name__).debug('Container %s status is %s',
                                              self.__container.id,
                                              self.__container.status)
            if self.__container.status in _OK_CONTAINER_STATUSES:
                break
            if self.__container.status in _KO_CONTAINER_STATUSES:
                raise RuntimeError('Container exited permaturelly')
            if self.__container.status in _WAIT_CONTAINER_STATUSES:
                time.sleep(self.__poll_interval)  # pylint: disable=expression-not-assigned

        else:
            self.__container.reload()
            if self.__container.status not in _OK_CONTAINER_STATUSES:
                raise TimeOut('Container {} is taking too long to start'.format(self.__container.id))

        return self.__container.id


def _prune_dict(dictionary):
    """Removes None values from possibly nested dict.

    Note: this function does not prune structures others than dict,
      for example print_dict({'k': [None, None]}) will not remove the
      None in the list.

    """
    res = {}
    for key, value in dictionary.items():
        if value is None:
            continue
        elif isinstance(value, dict):
            res[key] = _prune_dict(value)
        else:
            res[key] = value
    return res


# vim: et:sw=4:syntax=python:ts=4:
