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

# Only upload non-developement packages (which name does not contain a '+' sign)
if grep -vl '+' /tmp/workspace/version > /dev/null
then
    cat > ~/.pypirc <<HERE
[distutils]
index-servers =
    pypi

[pypi]
repository = ${1}
username = __token__
password = ${2}
HERE

    twine upload -r pypi dist/*.whl
    rm ~/.pypirc
else
    printf '\033[0;31mNot uploading the package, it appears to be a development one.\033[0m\n'
fi
