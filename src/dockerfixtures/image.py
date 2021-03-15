# -*- coding: utf-8; -*-
"""Represents a Docker Image
"""
from typing import Dict, List, Mapping, Optional, Union

from . import placeholders


DEFAULT_IMAGE_TAG = 'latest'


class Image:
    """Represents an image from which a container can be built.

    This image provides meta-data about the image itself and default
    values that should be used to create the container when left
    unspecified.

    """
    __slots__ = ('__name', '__tag', '__hash', '__environment', '__max_wait')

    def __init__(self,
                 name: str,
                 *,
                 hash_: str = None,
                 max_wait: float = 5.0,
                 tag: str = DEFAULT_IMAGE_TAG,
                 environment: Mapping[str, Optional[str]] = None,
                 ) -> None:
        self.__environment = environment or dict()
        self.__hash = hash_
        self.__max_wait = max_wait
        self.__name = name
        self.__tag = tag

    @property
    def default_environment(self) -> Dict[str, str]:
        """The default values of the different environment variables the image declares
        """
        return {k: v for k, v in self.__environment.items() if v is not None}

    @property
    def max_wait(self) -> float:
        return self.__max_wait

    @property
    def name(self):
        """The name of the Image"""
        return self.__name

    @property
    def pullname(self):
        """The name of the image to use to pull the image from a registry
        """
        if self.__hash:
            return "{}@{}".format(self.__name, self.__hash)
        if self.__tag:
            return "{}:{}".format(self.__name, self.__tag)
        return self.__name

    @property
    def tag(self):
        """The tag of the Image"""
        return self.__tag

    # Should be Union[str, placeholders.ContainerIDType]]:
    def check_command(self) -> List[
            Union[str, placeholders._Placeholder]]:  # pylint: disable=no-self-use
        """A command to run to ensure a container build from this image is up and ready


        """
        return ['docker', 'exec', '-ti', placeholders.ContainerID, 'bash', '-c', 'exit 0']


# vim: et:sw=4:syntax=python:ts=4:
