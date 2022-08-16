import argparse

parser = argparse.ArgumentParser(
        description='Simple script to study using Flashcards\nThe '
        )

parser.add_argument(
        '-d',
        '--deck',
        help='To use the flashcards you will need a .csv file with the flascards. The .csv have the following columns: Category, Question, Answer, Correct',
        default='~/.local/share/decks',
        type=str
        )

parser.add_argument(
        '-f',
        '--font',
        help='If asian characters of the font you are using are 2-wide length, set this variable to True. You can check here: 漢字',
        default=True,
        type=bool
        )

import pandas as pd
import enum
import os

class State(enum.Enum):
    menu      = 'm'
    set_deck  = 's'
    playing   = 'e'
    config    = 'c'
    quit      = 'q'

class Game_mode(enum.Enum):
    bySets  = 0
    sm2plus = 1

    def config(self):
        pass

class Ansi_escape(enum.Enum):
    UNDERLINE = '\u001b[4m'
    BOLD      = '\u001b[1m'
    GREEN     = '\u001b[32m'
    RED       = '\u001b[31m'
    MAGENTA   = '\u001b[35m'
    RESET     = '\u001b[0m'
    CLEAR     = '\u001b[H\u001b[2J'

class Ansi_escape_regex(enum.Enum):
    UNDERLINE = '\u001b\[4m'
    BOLD      = '\u001b\[1m'
    GREEN     = '\u001b\[32m'
    RED       = '\u001b\[31m'
    MAGENTA   = '\u001b\[35m'
    RESET     = '\u001b\[0m'
    CLEAR     = '\u001b\[H\u001b\[2J'

def apply_underline(text: str) -> str:
    return f'{Ansi_escape.UNDERLINE.value}{text}{Ansi_escape.RESET.value}'

def apply_bold(text: str) -> str:
    return f'{Ansi_escape.BOLD.value}{text}{Ansi_escape.RESET.value}'

def apply_magenta(text: str) -> str:
    return f'{Ansi_escape.MAGENTA.value}{text}{Ansi_escape.RESET.value}'

def apply_green(text: str) -> str:
    return f'{Ansi_escape.GREEN.value}{text}{Ansi_escape.RESET.value}'

def apply_red(text: str) -> str:
    return f'{Ansi_escape.RED.value}{text}{Ansi_escape.RESET.value}'

class Icons(enum.Enum):
    WRONG_ICON   = ''
    CORRECT_ICON = ''
    INPUT        = '> '
    BOX_V        = '│'
    BOX_H        = '─'
    BOX_UL       = '┌'
    BOX_UR       = '┐'
    BOX_BR       = '┘'
    BOX_BL       = '└'

class Game:
    state:State         = State.menu
    game_mode:Game_mode = Game_mode.bySets
    two_wide_font:bool

    invalid:bool        = False
    deck_error:bool     = False

    width:int  = int(os.environ['COLUMNS'])
    height:int = int(os.environ['LINES'])

    deck_path:str        = ''
    deck_df:pd.DataFrame

    set_size:int           = 10
    current_set:int        = 0
    correct_answers:int    = 0
    wrong_answers:int      = 0
    current_set_words:list
    current_set_words_category:list
    current_set_words_answer:list
    current_set_words_right:list

    DECK_FOLDER_PATH:str = '/home/azz/.local/share/decks'

    INVALID_INPUT:str = 'Invalid input'
    DECK_ERROR:str    = 'Deck does\'nt exist'

    def __init__(self, deck_path: str, two_wide_font: bool) -> None:
        self.deck_path = deck_path
        self.two_wide_font = two_wide_font
        while 1:
            self.loop()

    def loop(self) -> None:
        print(Ansi_escape.CLEAR.value)
        if self.state == State.menu:
            self.menu()
        elif self.state == State.set_deck:
            self.set_deck()
        elif self.state == State.playing:
            self.game()
        elif self.state == State.config:
            self.config()
        elif self.state == State.quit:
            exit(0)

    # TODO: Realtime env variables
    def get_window_size(self) -> tuple[int, int]:
        return (int(os.environ['COLUMNS']), int(os.environ['LINES']))

    ### Main menu ###
    def menu(self) -> None:
        self.print_menu()
        action = input(Icons.INPUT.value).lower()
        try:
            self.state = State(action)
        except:
            self.invalid = True

    def print_menu(self) -> None:
        options = [f'{apply_bold(apply_red(apply_underline("SUPER FLASHCARDS CARALHO")))}',
                '',
                f'Current deck: {apply_green(self.deck_path)}',
                '',
                f'[{apply_magenta("E")}]nter the game',
                f'[{apply_magenta("S")}]elect deck',
                f'[{apply_magenta("C")}]onfig',
                f'[{apply_magenta("Q")}]uit']

        if self.invalid == True:
            options.extend(['', self.INVALID_INPUT])
            self.invalid = False

        if self.deck_error == True:
            options.extend(['', self.DECK_ERROR])
            self.deck_error = False

        self.print_rows(len(options), options)

    ### Set deck ###
    def set_deck(self) -> None:
        if not os.path.isdir(self.DECK_FOLDER_PATH):
            os.mkdir(self.DECK_FOLDER_PATH)

        deck_list = os.listdir(self.DECK_FOLDER_PATH)
        self.print_set_deck(deck_list)

        chosen_deck = input(Icons.INPUT.value)
        if chosen_deck.isnumeric():
            if int(chosen_deck) >= len(deck_list) or int(chosen_deck) < 0:
                self.invalid = True
            else:
                self.deck_path = os.path.join(self.DECK_FOLDER_PATH, deck_list[int(chosen_deck)])
                try:
                    self.deck_df = pd.read_csv(self.deck_path)
                except:
                    self.invalid = True
                self.state = State.menu
        else:
            self.invalid = True

    def print_set_deck(self, deck_list: list[str]) -> None:
        options = ['The following decks are avaliable:', '']
        options.extend([*(f'{apply_magenta(str(k))} - {v}' for k, v in enumerate(deck_list))])
        if self.invalid == True:
            options.extend(['', self.INVALID_INPUT])
            self.invalid = False

        self.print_rows(len(options), options)

    ### Game ###
    def game(self) -> None:
        try:
            self.deck_df = pd.read_csv(self.deck_path)
        except:
            self.deck_error = True
            self.state = State.menu
            return
        self.print_game()
        action = input(Icons.INPUT.value).lower()
        if action == 'n':
            if self.current_set < len(self.deck_df):
                self.current_set += self.set_size
        elif action == 'b':
            if self.current_set - self.set_size >= 0:
                self.current_set -= self.set_size
        elif action == 'g':
            self.play()
        elif action == 'c':
            self.state = State.menu
        else:
            self.invalid = True

    def print_game(self) -> None:
        from wcwidth import wcswidth
        last:int = min(self.current_set + self.set_size, len(self.deck_df)) - 1
        self.current_set_words          = self.deck_df['Question'].loc[self.current_set:last]
        self.current_set_words_right    = self.deck_df['Correct'].loc[self.current_set:last]
        self.current_set_words_category = self.deck_df['Category'].loc[self.current_set:last]
        self.current_set_words_answer   = self.deck_df['Answer'].loc[self.current_set:last]

        current_set_icons = []
        for word, right in zip(self.current_set_words, self.current_set_words_right):
            from wcwidth import wcswidth
            correct = apply_green(Icons.CORRECT_ICON.value)
            wrong = apply_red(Icons.WRONG_ICON.value)

            if right:
                current_set_icons.append(correct.center(wcswidth(word) + self.ansi_len(correct)))
            else:
                current_set_icons.append(wrong.center(wcswidth(word) + self.ansi_len(wrong)))

        options = [f'Current set {self.current_set}/{len(self.deck_df)}',
                '',
                '  '.join(self.current_set_words),
                '  '.join(current_set_icons),
                '',
                f'[{apply_magenta("N")}]ext [{apply_magenta("B")}]ack [{apply_magenta("G")}]o [{apply_magenta("C")}]hange Deck',
                f'{self.correct_answers}/{self.set_size}']

        self.print_rows(len(options), options)

    def play(self):
        from random import shuffle
        list_order       = [*range(self.current_set, self.current_set + min(self.set_size, len(self.deck_df) - self.current_set))]
        already_answered = []
        self.correct_answers, self.wrong_answers = 0, 0
        shuffle(list_order)

        while len(list_order) > 0:
            next_word = list_order[0]
            self.print_round(len(list_order), self.current_set_words_category[next_word], self.current_set_words[next_word])
            action = input(Icons.INPUT.value).lower()
            if action == 's':
                right = self.print_round_answer(self.current_set_words_category[next_word], self.current_set_words[next_word], self.current_set_words_answer[next_word])
                if right:
                    if not next_word in already_answered:
                        self.correct_answers += 1
                        already_answered.append(next_word)
                    self.deck_df['Correct'][next_word] = 1
                    self.deck_df.to_csv(self.deck_path, index = False)
                    list_order.pop(0)
                else:
                    if not next_word in already_answered:
                        self.wrong_answers += 1
                        already_answered.append(next_word)
                    shuffle(list_order)
            if action == 'c':
                break

    def print_round(self, words_left: int, category: str, word: str) -> None:
        options = [f'Category {category}',
                '',
                word,
                '',
                f'[{apply_magenta("S")}]how Answer [{apply_magenta("C")}]hange Set',
                '',
                f'Correct: {self.correct_answers} Wrong: {self.wrong_answers}',
                f'Left: {words_left}']
        self.print_rows(len(options), options)

    def print_round_answer(self, category: str, word: str, answer: str) -> bool:
        options = [f'Category {category}',
                '',
                word,
                '',
                answer,
                '',
                f'[{apply_magenta("D")}]idn\'t know [{apply_magenta("K")}]new']
        self.print_rows(len(options), options)

        while 1:
            action = input(Icons.INPUT.value).lower()
            if action == 'k':
                return True
            elif action == 'd':
                return False
            else:
                self.print_rows(len(options), options)

        return True

    ### Config ###
    def config(self) -> None:
        self.print_config()
        action = input(Icons.INPUT.value).lower()
        if action == 's':
            self.set_set_size()
        elif action == 'l':
            self.learning_algorithms()
        elif action == 'm':
            self.state = State('m');
        else:
            self.invalid = True

    def print_config(self) -> None:
        options = ['Configuration',
                '',
                f'Algorithm: {self.game_mode}',
                f'Set size: {self.set_size}',
                '',
                f'[{apply_magenta("S")}]et new size',
                f'[{apply_magenta("L")}]earning algorithm (!)',
                f'[{apply_magenta("M")}]enu']

        if self.invalid == True:
            options.extend(['', self.INVALID_INPUT])
            self.invalid = False

        self.print_rows(len(options), options)

    def learning_algorithms(self):
        self.print_learning_algorithms()
        action = input(Icons.INPUT.value).lower()
        try:
            self.game_mode = Game_mode(action)
        except:
            self.invalid = True

    def print_learning_algorithms(self) -> None:
        options = ['Avaliable Algorithms',
                '',
                f'[{apply_magenta("S")}]ets',
                f'S[{apply_magenta("M")}]2+']

        if self.invalid == True:
            options.extend(['', self.INVALID_INPUT])
            self.invalid = False

        self.print_rows(len(options), options)

    def set_set_size(self) -> None:
        options = ['Write the new size:']

        self.print_rows(len(options), options)

        set_size = input(Icons.INPUT.value)

        if set_size.isnumeric():
            if int(set_size) < 0:
                self.invalid = True
            else:
                self.set_size = int(set_size)
        else:
            self.invalid = True

    def print_rows(self, options_quantity: int, options: list[str]) -> None:
        screen = ''

        width_ratio = 0.9

        border_ratio = 0.15
        border_up = int(self.height * border_ratio) + int(self.height % (border_ratio ** -1))
        border_down = int(self.height * border_ratio)

        padding_ratio = 0.5 - border_ratio
        padding_rows_up = int(self.height*padding_ratio) - (options_quantity // 2 + options_quantity % 2) - 1
        padding_rows_down = int(self.height*padding_ratio) - options_quantity // 2 - 1

        text_width = int(self.width * width_ratio)

        #│ text │ function
        def center_text(text: str, border: tuple[str, str]):
            from wcwidth import wcswidth
            asian_char = 0
            no_ansi_text = self.ansi_remove(text)
            if self.two_wide_font and wcswidth(no_ansi_text) > len(no_ansi_text):
                asian_char = wcswidth(no_ansi_text) - len(no_ansi_text) # 2-wide characters
            ansi_char = self.ansi_len(text)
            final_text_width =  text_width - asian_char + ansi_char
            screen_width = self.width - asian_char + ansi_char
            return f'{border[0]}{text.center(final_text_width)}{border[1]}'.center(screen_width)

        screen += '\n' * (border_up)                                                                           # border
        screen += center_text(Icons.BOX_H.value * text_width, (Icons.BOX_UL.value, Icons.BOX_UR.value)) + '\n'        # ┌──────┐ 1 row
        screen += (center_text('', (Icons.BOX_V.value, Icons.BOX_V.value)) + '\n') * (padding_rows_up)                  # │      │ padding
        screen += ''.join(center_text(option, (Icons.BOX_V.value, Icons.BOX_V.value)) + '\n' for option in options)   # │ text │ options
        screen += (center_text('', (Icons.BOX_V.value, Icons.BOX_V.value)) + '\n') * (padding_rows_down)                # │      │ padding
        screen += center_text(Icons.BOX_H.value * text_width, (Icons.BOX_BL.value, Icons.BOX_BR.value)) + '\n'        # └──────┘ 1 row
        screen += '\n' * (border_down - 1)                                                                     # border

        print(screen)

    ### ANSI ###
    def ansi_len(self, text: str) -> int:
        ansi_char = 0
        for effect in [i.value for i in Ansi_escape_regex]:
            from re import findall
            all = findall(effect, text)
            if all != []:
                ansi_char += sum([len(e) for e in all])
        return ansi_char

    def ansi_exist(self, text: str) -> bool:
        for effect in [i.value for i in Ansi_escape_regex]:
            from re import match
            if match(effect, text):
                return True
        return False

    def ansi_remove(self, text: str) -> str:
        for effect in [i.value for i in Ansi_escape_regex]:
            from re import sub
            text = sub(effect, '', text)
        return text

if __name__ == '__main__':
    args = parser.parse_args()
    Game(args.deck, args.font)
