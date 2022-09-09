.PHONY: 'clean start stop setup'

start:
	@echo 'Trying to run the docker image'
	@docker run --rm -it -e COLUMNS -e LINES -v "${PWD}/decks:/usr/src/app/decks" flashcard:latest

build:
	@echo 'Building the docker image'
	@docker build -t flashcard .

clean:
	@echo 'Removing the docker image'
	@docker rmi flashcard
