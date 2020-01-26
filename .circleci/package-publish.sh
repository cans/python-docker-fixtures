#!/bin/bash
set -eo pipefail
# shellcheck source=/dev/null
. ~/.venv/bin/activate

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

    twine upload -r pypi /tmp/workspace/*.whl
    rm ~/.pypirc
else
    printf '\033[0;31mNot uploading the package, it appears to be a development one.\033[0m\n'
fi
