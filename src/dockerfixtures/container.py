# -*- coding: utf-8; -*-
import logging
import socket
import subprocess
import time
from typing import Any, Dict, List, Mapping, Optional, Tuple, Union
import warnings

import docker
import requests.exceptions

from .image import Image

_CONTAINER_DEFAULT_OPTIONS = dict(cap_add=['IPC_LOCK'],
                                  # mem_limit='256m',
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

_CONTAINER_STATUSES_KO = (CONTAINER_STATUS_DEAD,
                          CONTAINER_STATUS_EXITED,
                          )
_CONTAINER_STATUSES_OK = (CONTAINER_STATUS_RUNNING,
                          )
_CONTAINER_STATUSES_WAIT = (CONTAINER_STATUS_CREATED,
                            CONTAINER_STATUS_PAUSED,
                            )
_SUPPORTED_NETWORK_PROTOCOLS = ['tcp', 'udp']

MANIFEST_V2 = 'application/vnd.docker.distribution.manifest.v2+json'
MANIFEST_LIST_V2 = 'application/vnd.docker.distribution.manifest.list.v2+json'
SUPPORTED_MANIFEST_TYPES = (MANIFEST_V2, MANIFEST_LIST_V2)


class TimeOut(Exception):
    """Raised when a container does not start within the alloted time
    """


class ImageNotFound(Exception):
    """Raised when an image cannot be found in the docker registry
    """


class UnsupportedNetworkProtocol(Exception):
    """Raised when a port value contains an invalid protocol name
    """


def _port(port: str) -> Tuple[int, str]:
    """Transforms ports in the '<port>/<proto>' syntax into a tuple.
    """
    if '/' in port:
        port, proto = port.split('/')
    else:
        port, proto = port, None

    if not proto:
        return int(port), 'tcp'
    if proto not in _SUPPORTED_NETWORK_PROTOCOLS:
        raise UnsupportedNetworkProtocol("Protocol '{}' is not supported, only {} are."
                                         .format(proto,
                                                 ' and '.join([
                                                     ', '.join(_SUPPORTED_NETWORK_PROTOCOLS[:-1]),
                                                     *_SUPPORTED_NETWORK_PROTOCOLS[:-1]])))
    return int(port), proto


def _prune_dict(dictionary: Mapping[Any, Optional[Any]]) -> Mapping[Any, Any]:
    """Removes None values from possibly nested dict.

    Note: this function does not prune structures others than dict,
      for example print_dict({'k': [None, None]}) will not remove the
      None in the list.

    """
    res = {}
    for key, value in dictionary.items():
        if value is None:
            continue
        if isinstance(value, dict):
            value = _prune_dict(value)
            if len(value) > 0:
                res[key] = value
        else:
            res[key] = value
    return res


class Container:
    """Represents a container
    """
    __slots__ = ('__client',
                 '__command',
                 '__container',
                 '__environment',
                 '__image',
                 '__max_wait',
                 '__options',
                 '__readyness_poll_interval',
                 '__startup_poll_interval',
                 )

    def __enter__(self):
        self.run()
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.kill()
        self.remove()
        if exc_value:
            raise exc_value

    def __init__(self,
                 image: Image,
                 *,
                 command: Optional[Union[str, List[str]]] = None,
                 dockerclient: docker.client.DockerClient = None,
                 environment: Dict[str, str] = None,
                 max_wait: int = 10,
                 options=None,
                 startup_poll_interval: float = 1,
                 readyness_poll_interval: float = 0.2,
                 ):
        """

        TODO: Build container from an ID ? (restart paused container)
        """
        assert max_wait >= 0
        self.__client = dockerclient
        self.__command = None
        self.__container = None
        self.__environment = _prune_dict({** image.default_environment, **(environment or dict())})
        self.__image = image
        self.__max_wait = max_wait
        self.__options = options or dict()
        self.__readyness_poll_interval = readyness_poll_interval
        self.__startup_poll_interval = startup_poll_interval

    def check(self):
        """Runs the check command provided by the image.

        If the command fails, the container is assumed to have
        crashed.  If it succeeds the container is assumed to have
        started properly and is running.

        """
        command = self.__image.check_command(self)
        subprocess.check_call(command, shell=False)

    @property
    def address(self) -> str:
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
        """Kills the container if still running.

        Equivalent to the `docker stop <ContainerID>` command
        """
        try:
            self.__container.kill()
        except requests.exceptions.HTTPError as exc:
            if exc.response.status_code != 409:
                raise
            # Container was already dead.

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

    @property
    def ports(self) -> Dict[str, Tuple[int, str]]:
        """Try to return the set of ports the container listens on.

        Return value is::

            {'<port>/proto': (<effective port>, 'proto'), }

        """
        if self.__container is not None:
            image = self.__container.image
        else:
            image_meta = self.__client.images.get_registry_data(name=self.__image.pullname)
            assert image_meta.attrs['Descriptor']['mediaType'] in SUPPORTED_MANIFEST_TYPES
            image = image_meta.pull()
        # Get list of exposed ports
        ports = {k: _port(k) for k, v in image.attrs.get('ExposedPorts', {}).items()}
        # Update with the possible port mapping(s)
        ports.update({k: _port(k) for k, v in self.__options.get('ports', {}).items()})
        return ports

    def remove(self) -> None:
        """Removes the container

        Equivalent to the `docker rm <ContainerID>` command
        """
        if self.__container is None:
            warnings.warn('Container was never started!', RuntimeWarning)
            return
        self.__container.remove(v=True, force=True)

    def run(self, command=None, dockerclient=None):
        """Starts the container

        Args:
            dockerclient: a docker client if none were provided on container instanciation
            command: alternate command for the container to run, instead its default CMD or
                ENTRYPOINT

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
            image = self.__client.images.pull(self.__image.pullname)
        except docker.errors.ImageNotFound as exc:
            raise ImageNotFound("Image '{}' does not exist".format(self.__image.pullname)) from exc

        logging.getLogger(__name__).debug('Starting container from image: %s', self.__image.name,
                                          extra={'pullname': self.__image.pullname,
                                                 'environment': self.__environment,
                                                 'options': self.options,
                                                 })
        self.__container = self.__client.containers.run(command=command or self.__command,
                                                        image=image,
                                                        environment=self.__environment,
                                                        **self.options,
                                                        )
        for _ in range(self.__max_wait):
            self.__container.reload()
            logging.getLogger(__name__).debug('Container %s status is %s',
                                              self.__container.id,
                                              self.__container.status)
            if self.__container.status in _CONTAINER_STATUSES_OK:  # pylint: disable=no-else-break
                break
            elif self.__container.status in _CONTAINER_STATUSES_KO:
                raise RuntimeError('Container stopped prematurely')
            elif self.__container.status in _CONTAINER_STATUSES_WAIT:
                time.sleep(self.__startup_poll_interval)  # pylint: disable=expression-not-assigned
            else:
                warnings.warn('Unknown container status!', RuntimeWarning)

        else:
            self.__container.reload()
            if self.__container.status not in _CONTAINER_STATUSES_OK:
                raise TimeOut('Container {} is taking too long to start'
                              .format(self.__container.id))

        return self.__container.id

    def wait(self,
             *ports: Tuple[Tuple[int, str], ...],
             max_wait: float = None,
             readyness_poll_interval: float = 0.1,
             ) -> None:
        """Waits for the container to be listening on some network ports.
        """
        if not ports:
            next_round_ports = list(self.ports.values())
        else:
            next_round_ports = list(ports)
        max_wait = max_wait or self.__image.max_wait

        then = time.time()
        while (time.time() - then) < max_wait:
            ports = next_round_ports
            next_round_ports = []

            for port, proto in ports:
                try:
                    sock_proto = socket.SOCK_STREAM if proto == 'tcp' else socket.SOCK_DGRAM
                    with socket.socket(socket.AF_INET, sock_proto) as sock:
                        sock.connect((self.address, port))
                except ConnectionError:
                    next_round_ports.append((port, proto))
                    time.sleep(readyness_poll_interval)

            if not next_round_ports:
                return True
        raise TimeOut('Container taking too long to become ready (waited {:.2f}s.): {} {}'
                      .format(time.time() - then,
                              self.address,
                              ', '.join(['{}/{}'.format(str(x[0]), x[1])
                                         for x in next_round_ports])))


def fixture(image: Image,
            *ports: Tuple[int, str],
            environment: Optional[Mapping[str, str]] = None,
            max_wait: Optional[float] = None,
            options: Optional[Mapping[str, Any]] = None,
            readyness_poll_interval: Optional[float] = None,
            ) -> None:
    with Container(image, options=options, environment=environment) as cntr:
        cntr.wait(*ports, max_wait=max_wait, readyness_poll_interval=readyness_poll_interval)
        yield  # Do not yield the container, not need if container is reachable through the network


# vim: et:sw=4:syntax=python:ts=4:
