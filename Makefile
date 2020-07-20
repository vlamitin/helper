SHELL := /bin/bash

init:
	python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt

install:
	echo "#!/bin/bash" > /home/${USER}/bin/helper && echo "${PWD}/venv/bin/python ${PWD}/helper.py \$$@" >> /home/${USER}/bin/helper && chmod +x /home/${USER}/bin/helper && ln -s ${PWD}/login.sh /home/${USER}/bin/helper_login
