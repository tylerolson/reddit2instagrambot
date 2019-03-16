all: help

help:
	@echo "make run - runs the program"
	@echo "make cleanall - cleans everything"
	@echo "make cleanpy - cleans the Python temp files"
	@echo "make cleanmedia - cleans the media folder"
	@echo "make cleanlog - cleans the debug log"

run:
	python3 main.py

cleanall: cleanpy cleanmedia cleanlog

cleanpy:
	@find . -name '*.pyc' -exec rm -v --force {} +

cleanmedia:
	@rm -v --force media/*

cleanlog:
	@rm -v --force debug.log
