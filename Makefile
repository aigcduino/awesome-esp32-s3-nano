.PHONY: build check links stars dataset

build:
	python3 scripts/build.py

check:
	python3 scripts/build.py --check

links:
	python3 scripts/check_links.py

stars:
	python3 scripts/refresh_stars.py && python3 scripts/build.py

dataset:
	python3 scripts/export_dataset.py
