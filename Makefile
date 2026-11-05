.PHONY: build check links stars

build:
	python3 scripts/build.py

check:
	python3 scripts/build.py --check

links:
	python3 scripts/check_links.py

stars:
	python3 scripts/refresh_stars.py && python3 scripts/build.py
