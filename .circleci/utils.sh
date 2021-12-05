#!/bin/bash

select_python_version() {
    if [ -z "${VIRTUAL_MACHINE}" ]
    then
        echo "Not running on a virtual machine, skipping Python version selection !"
        return 0
    fi
    printf "Enabling python version %s ..." "${1}"
    eval "$(pyenv init -)"
    actual_py_version="$(pyenv install --list | grep "^  ${1}" | grep -v '-' |sort -bt . --key 3,3rn | sed 's/ //g' | head -n 1)"
    [ -z "${actual_py_version}" ] && { echo "No Python ${1} version available !" >&2 ;  return 1 ; }
    if pyenv install --skip-existing "${actual_py_version}"
    then
        pyenv rehash
        pyenv shell "${actual_py_version}"
        echo " done."
    else
        echo "failed !"
        return 1
    fi
    return 0
}


ensure_venv_exists() {
    if ! select_python_version "${1}"
    then
        return 1
    fi
    python3 -m venv --copies --prompt "${CIRCLE_JOB}" ~/.venv
    # shellcheck source=/dev/null
    . ~/.venv/bin/activate
    echo "Upgrading pip ..."
    if pip install --progress-bar="off" -U pip
    then
        echo "done"
    else
        echo 'failed !'
    fi
}
