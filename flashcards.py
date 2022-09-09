from random import shuffle
from re import escape, sub
from wcwidth import wcswidth
from argparse import ArgumentParser
from enum import Enum
from colorama import Fore
import pandas as pd
import os

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


def ansi_mag(text: str) -> str:
    return sub(escape(']'), f'{Fore.RESET}]',sub(escape('['), f'[{Fore.MAGENTA}', text))


class State(Enum):
    menu = 'm'
    set_deck = 's'
    playing = 'e'
    config = 'c'
    quit = 'q'


class Mode(Enum):
    bySets = 0
    sm2plus = 1


class Icon(Enum):
    WRONG = f'{Fore.RED}{Fore.RESET}'
    CORRECT = f'{Fore.GREEN}{Fore.RESET}'
    INPUT = '> '
    BOX_V = '│'
    BOX_H = '─'
    BOX_UL = '┌'
    BOX_UR = '┐'
    BOX_BR = '┘'
    BOX_BL = '└'


class Algorithm(Enum):
    SETS = 0
    SM2P = 1


class GameLogic:
    set_size: int = 10
    set_index: int = 0
    correct_answers: int = 0
    wrong_answers: int = 0
    Mode: Mode = Mode.bySets
    current_set: pd.DataFrame

    @classmethod
    def play(cls):
        list_order = [
            *range(GameLogic.set_index,
                GameLogic.set_index
                + min(GameLogic.set_size,
                      len(Game.deck_df) - GameLogic.set_index)
            )]
        already_answered = []

        GameLogic.correct_answers, GameLogic.wrong_answers = 0, 0
        shuffle(list_order)

        while len(list_order) > 0:
            next_word = list_order[0]
            GameScreen.print_round(len(list_order),
                                   GameLogic.current_set['Category'][next_word],
                                   GameLogic.current_set['Question'][next_word])

            action = input(Icon.INPUT.value).lower()
            if action == 's':
                right = GameScreen.print_round_answer(
                        GameLogic.current_set['Category'][next_word],
                        GameLogic.current_set['Question'][next_word],
                        GameLogic.current_set['Answer'][next_word]
                        )
                if right:
                    if next_word not in already_answered:
                        GameLogic.correct_answers += 1
                        already_answered.append(next_word)
                    Game.deck_df['Correct'][next_word] = 1
                    Game.deck_df.to_csv(Game.deck_path, index=False)
                    list_order.pop(0)
                    continue

                if next_word not in already_answered:
                    GameLogic.wrong_answers += 1
                    already_answered.append(next_word)
                shuffle(list_order)
            if action == 'c':
                break


class GameScreen:
    two_wide_font: bool = True

    INVALID_INPUT: str = 'Invalid input'
    DECK_ERROR: str = 'Deck does\'nt exist'

    EFFECTS: list = [
            escape(Fore.GREEN),
            escape(Fore.RED),
            escape(Fore.MAGENTA),
            escape(Fore.RESET)
            ]

    @classmethod
    def get_window_size(cls) -> tuple[int, int]:
        return (int(os.get_terminal_size().columns), int(os.get_terminal_size().lines))

    @classmethod
    def ansi_len(cls, text: str) -> int:
        ansi_char = 0
        for effect in GameScreen.EFFECTS:
            from re import findall
            all = findall(effect, text)
            if all != []:
                ansi_char += sum([len(e) for e in all])
        return ansi_char

    @classmethod
    def ansi_exist(cls, text: str) -> bool:
        for effect in GameScreen.EFFECTS:
            from re import match
            if match(effect, text):
                return True
        return False

    @classmethod
    def ansi_remove(cls, text: str) -> str:
        for effect in GameScreen.EFFECTS:
            from re import sub
            text = sub(effect, '', text)
        return text

    @classmethod
    def print_rows(cls, options: list[str]) -> None:
        options_quantity = len(options)
        width, height = GameScreen.get_window_size()

        screen = ''
        width_ratio = 0.9
        border_ratio = 0.15
        padding_ratio = 0.5 - border_ratio

        border = int(height * border_ratio)
        padding_up = int(height*padding_ratio) - (options_quantity // 2)
        padding_down = padding_up - (options_quantity % 2)

        text_width = int(width * width_ratio)

        # │ text │ function
        def center_text(text: str, border: tuple[str, str]) -> str:
            asian_char = 0
            no_ansi_text = GameScreen.ansi_remove(text)
            asian_char = 0
            if GameScreen.two_wide_font and \
                wcswidth(no_ansi_text) > len(no_ansi_text):
                asian_char = wcswidth(no_ansi_text) - len(no_ansi_text) # 2-wide characters
            ansi_char = GameScreen.ansi_len(text)
            final_text_width = text_width - asian_char + ansi_char
            screen_width = width - asian_char + ansi_char
            return f'{border[0]}{text.center(final_text_width)}{border[1]}' \
                .center(screen_width)

        # border
        # ┌──────┐ 1 row
        # │      │ padding
        # │ text │ options
        # │      │ padding
        # └──────┘ 1 row
        # border

        screen += '\n' * (border)
        screen += center_text(Icon.BOX_H.value * text_width, (Icon.BOX_UL.value, Icon.BOX_UR.value)) + '\n'
        screen += (center_text('', (Icon.BOX_V.value, Icon.BOX_V.value)) + '\n') * (padding_up - 1)
        screen += ''.join(center_text(option, (Icon.BOX_V.value, Icon.BOX_V.value)) + '\n' for option in options)
        screen += (center_text('', (Icon.BOX_V.value, Icon.BOX_V.value)) + '\n') * (padding_down - 1)
        screen += center_text(Icon.BOX_H.value * text_width, (Icon.BOX_BL.value, Icon.BOX_BR.value)) + '\n'
        screen += '\n' * (border - 1)

        print(screen)


    @classmethod
    def print_menu(cls) -> None:
        options = [
            'SUPER FLASHCARDS CARALHO',
            '',
            f'Current deck: {Game.deck_path}',
            '',
            ]
        options.extend(
            ansi_mag(i) for i in [
            '[E]nter the game',
            '[S]elect deck',
            '[C]onfig',
            '[Q]uit'
            ])

        if Game.invalid:
            options.extend(['', GameScreen.INVALID_INPUT])
            Game.invalid = False

        if Game.deck_error:
            options.extend(['', GameScreen.DECK_ERROR])
            Game.deck_error = False

        GameScreen.print_rows(options)


    @classmethod
    def print_game_menu(cls) -> None:
        last: int = min(GameLogic.set_index
                        + GameLogic.set_size, len(Game.deck_df)) - 1
        GameLogic.current_set = Game.deck_df.loc[GameLogic.set_index: last]

        set_indexcons = []
        for word, right in zip(GameLogic.current_set['Question'],
                               GameLogic.current_set['Correct']):

            if right:
                set_indexcons.append(Icon.CORRECT.value.center(wcswidth(word)
                    + GameScreen.ansi_len(Icon.CORRECT.value)))
            else:
                set_indexcons.append(Icon.WRONG.value.center(wcswidth(word)
                    + GameScreen.ansi_len(Icon.CORRECT.value)))

        options = [
            f'Current set {GameLogic.set_index}/{len(Game.deck_df)}',
            '',
            '  '.join(GameLogic.current_set['Question']),
            '  '.join(set_indexcons),
            '',
            ]

        options.extend(
            ansi_mag(i) for i in [
            '[N]ext [B]ack '
            '[G]o [C]hange Deck',
            ])
        options.extend([
            f'{GameLogic.correct_answers}/{GameLogic.set_size}'
            ])

        GameScreen.print_rows(options)


    @classmethod
    def print_round(cls, words_left: int, category: str, word: str) -> None:
        options = [
            f'Category {category}',
            '',
            word,
            '',
            ]
        options.extend(
            ansi_mag(i) for i in [
            '[S]how Answer '
            '[C]hange Set',
            '',
            ])
        options.extend([
            f'Correct: {GameLogic.correct_answers} '
            f'Wrong: {GameLogic.wrong_answers}',
            f'Left: {words_left}'
            ])
        GameScreen.print_rows(options)


    @classmethod
    def print_round_answer(cls, category: str, word: str, answer: str) -> bool:
        options = [
            f'Category {category}',
            '',
            word,
            '',
            answer,
            ''
            ]
        options.extend(
            ansi_mag(i) for i in [
            '[D]idn\'t know'
            '[K]new'
            ])
        GameScreen.print_rows(options)

        while 1:
            action = input(Icon.INPUT.value).lower()
            if action == 'k':
                return True
            elif action == 'd':
                return False
            else:
                GameScreen.print_rows(options)

        return True


    @classmethod
    def print_set_deck(cls, deck_list: list[str]) -> None:
        options = ['The following decks are avaliable:', '']
        options.extend([*(ansi_mag(f'[{str(k)}] {v}')
                          for k, v in enumerate(deck_list))])
        if Game.invalid:
            options.extend(['', GameScreen.INVALID_INPUT])
            Game.invalid = False

        GameScreen.print_rows(options)


    @classmethod
    def print_learning_algorithms(cls) -> None:
        options = [
            'Avaliable Algorithms',
            '',
            ]
        options.extend(
            ansi_mag(i) for i in [
            '[S]ets',
            'S[M]2+'
            ])

        if Game.invalid:
            options.extend(['', GameScreen.INVALID_INPUT])
            Game.invalid = False

        GameScreen.print_rows(options)

    @classmethod
    def print_config(cls) -> None:
        options = [
            'Configuration',
            '',
            f'Algorithm: {GameLogic.Mode}',
            f'Set size: {GameLogic.set_size}',
            ''
            ]
        options.extend(
            ansi_mag(i) for i in [
            '[S]et new size',
            '[L]earning algorithm (!)',
            '[M]enu'
            ])

        if Game.invalid:
            options.extend(['', GameScreen.INVALID_INPUT])
            Game.invalid = False

        GameScreen.print_rows(options)


class Game:
    state: State = State.menu
    two_wide_font: bool

    invalid: bool = False
    deck_error: bool = False

    deck_path: str = ''
    deck_folder: str = ''
    deck_df: pd.DataFrame

    def __init__(self, two_wide_font: bool, deck_folder: str) -> None:
        GameScreen.two_wide_font = two_wide_font
        Game.deck_folder = deck_folder
        while 1:
            self.loop()

    def loop(self) -> None:
        if Game.state == State.menu:
            self.menu()
        elif Game.state == State.set_deck:
            self.set_deck()
        elif Game.state == State.playing:
            self.game()
        elif Game.state == State.config:
            self.config()
        elif Game.state == State.quit:
            exit(0)

    # Main menu
    def menu(self) -> None:
        GameScreen.print_menu()
        action = input(Icon.INPUT.value).lower()
        try:
            Game.state = State(action)
        except Exception:
            Game.invalid = True

    # Set deck
    def set_deck(self) -> None:
        if not os.path.isdir(Game.deck_folder):
            os.mkdir(Game.deck_folder)

        deck_list = os.listdir(Game.deck_folder)
        GameScreen.print_set_deck(deck_list)

        chosen_deck = input(Icon.INPUT.value)
        if not chosen_deck.isnumeric():
            Game.invalid = True
            return

        if int(chosen_deck) >= len(deck_list) or int(chosen_deck) < 0:
            Game.invalid = True
            return

        Game.deck_path = os.path.join(Game.deck_folder,
                                      deck_list[int(chosen_deck)])
        self.open_deck()
        Game.state = State.menu

    def open_deck(self) -> bool:
        try:
            Game.deck_df = pd.read_csv(Game.deck_path)
        except (FileNotFoundError, IsADirectoryError):
            Game.deck_error = True
            return False
        return True

    # Game
    def game(self) -> None:
        if not self.open_deck():
            Game.state = State.menu
            return

        GameScreen.print_game_menu()
        action = input(Icon.INPUT.value).lower()
        if action == 'n':
            if GameLogic.set_index < len(Game.deck_df):
                GameLogic.set_index += GameLogic.set_size
        elif action == 'b':
            if GameLogic.set_index - GameLogic.set_size >= 0:
                GameLogic.set_index -= GameLogic.set_size
        elif action == 'g':
            GameLogic.play()
        elif action == 'c':
            Game.state = State.menu
        else:
            Game.invalid = True

    # Config
    def config(self) -> None:
        GameScreen.print_config()
        action = input(Icon.INPUT.value).lower()
        if action == 's':
            self.set_set_size()
        elif action == 'l':
            self.learning_algorithms()
        elif action == 'm':
            Game.state = State('m')
        else:
            Game.invalid = True

    def learning_algorithms(self):
        GameScreen.print_learning_algorithms()
        action = input(Icon.INPUT.value).lower()
        try:
            Game.Mode = Mode(action)
        except Exception:
            Game.invalid = True

    def set_set_size(self) -> None:
        options = ['New size:']
        GameScreen.print_rows(options)

        set_size = input(Icon.INPUT.value)
        if not set_size.isnumeric():
            Game.invalid = True
            return

        if int(set_size) < 0:
            Game.invalid = True
            return

        GameLogic.set_size = int(set_size)


if __name__ == '__main__':
    args = parser.parse_args()
    Game(args.font, args.deck)
