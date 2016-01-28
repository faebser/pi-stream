
.PHONY: run
run: activate update pistream.py
	python pistream.py


.PHONY: clean
update:
	-@git fetch --all
	-@git reset --hard origin/master

env:
	virtualenv env
	pip install configparser==3.3.0r2
	pip install enum34==1.0.4

.PHONE: activate
activate: env
	source env/bin/activate