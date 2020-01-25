#!/bin/bash
set -eo pipefail
# shellcheck source=/dev/null
. ~/.venv/bin/activate

package="$(echo /tmp/workspace/dockerfixtures*.whl)"
if [ -f "${package}" ]
then
    mkdir ./dist
    cp /tmp/workspace/dockerfixtures*.whl ./dist
else
    python setup.py sdist bdist_wheel
    cp dist/*.whl /tmp/workspace/
    python -m setuptools_scm | sed -Ene 's/^(Guessed Version +)(.*)/\2/ip' > /tmp/workspace/version
fi

printf '\033[1;32m****************************************************\033[0m\n'
printf "Package version: "
cat /tmp/workspace/version
printf '\033[1;32m****************************************************\033[0m\n'
