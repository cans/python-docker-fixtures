# -*- coding: utf-8; -*-
from dockerfixtures.image import DEFAULT_IMAGE_TAG, Image


def test_image_attributes():
    """Ensures basic attributes are assigned as expected
    """
    # Given
    name = 'tralala'
    tag = 'itou'
    hash_ = 'sha256:0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef'
    img = Image(name, tag=tag, hash_=hash_)

    # When
    assert img.tag == tag
    assert img.name == name


def test_image_environment_is_complete(dummy_env):
    # Given
    img = Image('tralala', tag='itou', environment=dummy_env)

    # When
    default_env = img.default_environment

    # Then
    assert default_env == dummy_env


def test_image_environment_is_not_shared(dummy_env):
    """Ensure that an image default environment is copied

    Otherwise changing the value of default_environment may change
    the environment of other images
    """
    # Given
    img = Image('tralala', tag='itou', environment=dummy_env)

    # When
    default_env = img.default_environment

    # Then
    assert default_env is not dummy_env


def test_image_pullname_when_hash_given():
    """Ensures basic attributes are assigned as expected
    """
    # Given
    name = 'tralala'
    tag = 'itou'
    hash_ = 'sha256:0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef'
    image = Image(name, tag=tag, hash_=hash_)

    # When
    assert image.pullname == f"{name}@{hash_}"


def test_image_pullname_when_tag_given():
    """Ensures pullname is as expected when the image was build with a tag
    """
    # Given
    name = 'tralala'
    tag = 'itou'
    image = Image(name, tag=tag)

    # When
    assert image.pullname == f"{name}:{tag}"


def test_image_pullname_when_tag_and_hash_given():
    """Ensures pullname is as expected when the image was build with a tag & a hash
    """
    # Given
    name = 'tralala'
    tag = 'itou'
    hash_ = 'sha256:0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef'
    image = Image(name, tag=tag, hash_=hash_)

    # When
    assert image.pullname == f"{name}@{hash_}"


def test_image_pullname_when_no_tag_nor_hash_given():
    """Ensures pullname is as expected when the image was build with a tag & a hash
    """
    # Given
    name = 'tralala'
    image = Image(name, tag=None)

    # When
    assert image.pullname == f"{name}"


def test_image_pullname_when_default_tag_given():
    """Ensures pullname is as expected when the image was build with a tag & a hash
    """
    # Given
    name = 'tralala'
    image = Image(name)

    # When
    assert image.pullname == f"{name}:{DEFAULT_IMAGE_TAG}"


# vim: et:sw=4:syntax=python:ts=4:
