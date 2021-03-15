# -*- coding: utf-8; -*-
import os


CONTAINERIZED_CI_VENDOR_VARS = ('GITHUB_ACTION', 'CIRCLECI')


def is_containerized_ci():
    if 'VIRTUAL_MACHINE' in os.environ:
        return False
    if 'CI' not in os.environ:
        return False
    if any(var in os.environ for var in CONTAINERIZED_CI_VENDOR_VARS):
        return True
    return False


# vim: et:sw=4:syntax=python:ts=4:
