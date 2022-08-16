.PHONY: 'clean start stop setup'

start:
	@docker run --rm -it -e COLUMNS -e LINES -v "${PWD}/decks:/usr/src/app/decks" flashcard:latest

build:
	@docker build -t flashcard .

clean:
	@docker rmi flashcard
