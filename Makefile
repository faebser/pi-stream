
.PHONY: run
run: update pistream.py
	python pistream.py


.PHONY: clean
update:
	-@git fetch --all
	-@git reset --hard origin/master
