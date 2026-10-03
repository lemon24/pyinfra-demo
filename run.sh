#!/bin/bash
#
# usage: ./run.sh command [argument ...]
#
# Executable documentation for the development workflow.
#
# See https://death.andgravity.com/run-sh for how this works.


# preamble

set -o nounset
set -o pipefail
set -o errexit

PROJECT_ROOT=${0%/*}
if [[ $0 != $PROJECT_ROOT && $PROJECT_ROOT != "" ]]; then
    cd "$PROJECT_ROOT"
fi
readonly PROJECT_ROOT=$( pwd )
readonly SCRIPT="$PROJECT_ROOT/$( basename "$0" )"


# main development workflow

function install {
    pip install --group dev
    pip install -e app
    pre-commit install --install-hooks
}

function clean {
    pushd infra; vagrant destroy -f; popd
    ssh-keygen -R '[pyinfra.local]:2022'
    ssh-keygen -R pyinfra.andgravity.com
    ssh-keygen -R app.pyinfra.andgravity.com
    rm -f hello.txt
}

function reset {
    clean
    pushd infra
    vagrant up
    pyinfra inventories/beta.py apt.update -y
    popd
}


# utilities

function watch {
    entr-project-files -cdr "$SCRIPT" "$@"
}

function entr-project-files {
    set +o errexit
    while true; do
        ls-project-files | entr "$@"
        if [[ $? -eq 0 ]]; then
            break
        fi
    done
}

function ls-project-files {
    git ls-files "$@"
    git ls-files --exclude-standard --others "$@"
}

function checkout {
    local commit
    if [[ -n "${1:-}" ]]; then
        commit=$( git log --all --grep="$1" -i -F --format='%H' -n 1 )
    fi
    git checkout ${commit:-main} && clear && git --no-pager log -n1 --oneline
}


"$@"
