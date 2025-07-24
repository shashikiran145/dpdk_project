#!/bin/bash

cd -- "$( dirname -- "${BASH_SOURCE[0]}" )"

if [[ ! -x ./env/bin/ptf ]]; then
	echo "Install ptf"
	python3 -m venv env
	./env/bin/pip install --upgrade pip
	./env/bin/pip install ptf==0.9.1
fi

sudo ./env/bin/ptf -i 0@veth0 -i 1@veth2 -i 2@veth4 --test-dir tests/ --qlen 2000 "$@"
