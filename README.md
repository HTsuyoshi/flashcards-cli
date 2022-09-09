# flashcards-cli

A simple script that reads a .csv file and presents flashcards inside the terminal.

![Sample](./assets/sample.gif)

There are a few ways to run it:

- [Docker](#run-\(docker\))
- [Host machine](#run-\(host\))

## Run (Docker)

Create the `flashcard` image:

```sh
make build
```

Run the `flashcard` image:

```sh
make start
```

Erasing the image:

```sh
make clean
```

## Run (host)

#### Requirements

- `argparse`
- `pandas`
- `wcwidth`
- `re`
- `colorama`

Install the [Decks](https://github.com/HTsuyoshi/jp-flash-decks) with the flashcards

To run the program:

```sh
python3 flascards.py
```

## TODO

- [ ] Refactor the code
- [ ] Split types of algotihms (Sets and SM2+) in other classes
- [ ] Implement [SM2+](http://www.blueraja.com/blog/477/a-better-spaced-repetition-learning-algorithm-sm2)
