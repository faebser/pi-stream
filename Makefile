
.PHONY: run
run: update pistream.py
	python pistream.py


.PHONY: clean
update:
	-@git fetch --all
	-@git reset --hard origin/master

env:
	virtualenv env
	
install: env
	env/bin/pip install configparser==3.3.0r2
	env/bin/pip install enum34==1.0.4