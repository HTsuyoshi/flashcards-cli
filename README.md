# flashcards-cli

A simple script that reads a .csv file and presents flashcards inside the terminal.

![Sample](./assets/sample.gif)

There are a few ways to run it:

- [Docker](#run-\(docker\))
- [Local machine](#run)

## Run (Docker)

Export the `COLUMNS` and `LINES` variables:

```sh
source export.sh
```

Create the `flascard` image:

```sh
make build
```

Run the `flascard` image:

```sh
make
```

## Run

#### Requirements

- `argparse`
- `pandas`
- `wcwidth`
- `re`

Run the following command to export the `COLUMNS` and `LINES` variables

```sh
source export.sh
```

Install the [Decks](https://github.com/HTsuyoshi/jp-flash-decks) with the flashcards

To run the program:

```sh
python3 flascards.py
```

## TODO

- Get realtime `COLUMNS` and `LINES`
- Split types of algotihms in other classes
- Possibility to change sets size
- Dockerfile with `COLUMNS` and `LINES` variables shared
- [SM2+](http://www.blueraja.com/blog/477/a-better-spaced-repetition-learning-algorithm-sm2)
