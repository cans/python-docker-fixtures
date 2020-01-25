#!/bin/bash

select_python_version() {
    printf "Enabling python version %s ..." "${1}"
    eval "$(pyenv init -)"
    pyenv shell "$(pyenv versions | sed -nEe 's/^([^0-9]+)('"${1//./\\.}"'\.[0-9]+)(.*)/\2/p')"
    echo " done."
}


ensure_venv_exists() {
    select_python_version "${1}"
    python -m venv ~/.venv
    # shellcheck source=/dev/null
    . ~/.venv/bin/activate
    if [ "3.6" = "${1}" ]
    then
        pip install -U pip
    fi
}
