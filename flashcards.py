from __future__ import annotations
from argparse import ArgumentParser
from game import Game

parser = ArgumentParser(
        description='Simple script to study using Flashcards\nThe '
        )

parser.add_argument(
        '-d',
        '--deck',
        help='To use the flashcards you will need a .csv file with the'
             ' flashcards. The .csv have the following columns:'
             ' Category, Question, Answer, Correct',
        default='/usr/src/app/decks',
        type=str)

parser.add_argument(
        '-f', '--font', help='If asian characters of the font you are using are 2-wide'
             ' length, set this variable to True. You can check here: 漢字',
        default=True,
        type=bool
        )

if __name__ == '__main__':
    args = parser.parse_args()
    Game(args.font, args.deck)
