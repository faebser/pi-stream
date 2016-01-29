
.PHONY: run
run: update pistream.py
	python pistream.py


.PHONY: clean
update:
	-@git fetch --all
	-@git reset --hard origin/master

install: env/lib/python2.7/site-packages/enum env/lib/python2.7/site-packages/configparser.py
	

env/lib/python2.7/site-packages/enum:
	pip install enum34==1.0.4

env/lib/python2.7/site-packages/configparser.py:
	pip install configparser==3.3.0r2

env/lib/python2.7/site-packages/RPi:
	pip install RPi.GPIO

env:
	virtualenv env