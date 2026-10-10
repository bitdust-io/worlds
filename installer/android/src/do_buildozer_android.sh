#!/bin/sh

set -eu

missing_system_dependency=0
for command in git zip unzip java javac pip3 virtualenv autoconf libtoolize pkg-config cmake automake autopoint gettext; do
    if ! command -v "$command" >/dev/null 2>&1; then
        missing_system_dependency=1
    fi
done

if [ "$missing_system_dependency" -eq 1 ]; then
    sudo apt update
    sudo apt install -y git zip unzip openjdk-17-jdk python3-pip python3-virtualenv autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo6 cmake libffi-dev libssl-dev automake autopoint gettext
fi

curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- --default-toolchain none -y

rustup toolchain install nightly --allow-downgrade --profile minimal --component clippy

. "$HOME/.cargo/env"

VENV="venv"

rm -rf "${VENV}"

python3.14 -m venv "${VENV}"

. "${VENV}/bin/activate"

pip install git+https://github.com/kivy/buildozer

pip install legacy-cgi setuptools 'cython>=3.1,<3.4'

buildozer android "$@"
