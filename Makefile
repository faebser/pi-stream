
.PHONY: run
run: update install pistream.py
	env/bin/python pistream.py


.PHONY: clean
update:
	-@git fetch --all
	-@git reset --hard origin/master

install: env/lib/python2.7/site-packages/enum env/lib/python2.7/site-packages/configparser.py
	

env/lib/python2.7/site-packages/enum: env
	env/bin/pip install enum34==1.0.4

env/lib/python2.7/site-packages/configparser.py: env
	env/bin/pip install configparser==3.3.0r2

env:
	virtualenv env