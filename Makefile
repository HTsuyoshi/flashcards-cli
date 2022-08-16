.PHONY: 'clean start stop setup'

start:
	@docker run --rm -it -e COLUMNS -e LINES flashcard:latest

build:
	@docker build -t flashcard .

clean:
	@docker rmi flashcard
