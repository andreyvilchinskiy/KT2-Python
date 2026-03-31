import random
import os
from typing import List, Tuple, Dict

GALLOWS_FOLDER: str = "gallows"
WORDS_FILE: str = "words.txt"
MAX_MISTAKES: int = 5

words_list: List[str] = []
descriptions_list: List[str] = []
current_word: str = ""
current_description: str = ""
guessed_letters: List[str] = []
mistakes_count: int = 0
status_message: str = ""


def initialize_game() -> None:
    load_words_from_file()
    select_random_word()
    reset_game_state()


def load_words_from_file() -> None:
    global words_list, descriptions_list
    words_list = []
    descriptions_list = []

    try:
        with open(WORDS_FILE, 'r', encoding='utf-8') as file:
            for line in file:
                if ';' in line:
                    word, description = line.strip().split(';', 1)
                    words_list.append(word.upper())
                    descriptions_list.append(description)
    except FileNotFoundError:
        words_list = ["ПИТОН", "ПРОГРАММА"]
        descriptions_list = ["язык программирования", "компьютерная программа"]


def select_random_word() -> None:
    global current_word, current_description
    if words_list:
        index = random.randint(0, len(words_list) - 1)
        current_word = words_list[index]
        current_description = descriptions_list[index]
    else:
        current_word = "ПИТОН"
        current_description = "язык программирования"


def reset_game_state() -> None:
    global guessed_letters, mistakes_count, status_message
    guessed_letters = []
    mistakes_count = 0
    status_message = ""


def get_display_word() -> str:
    display = []
    for letter in current_word:
        if letter in guessed_letters:
            display.append(letter)
        else:
            display.append('_')
    return ' '.join(display)


def check_letter(letter: str) -> Tuple[bool, str]:
    letter = letter.upper()

    if len(letter) != 1 or not letter.isalpha():
        return False, "Ошибка: введите одну букву"

    if letter in guessed_letters:
        return False, "Эта буква уже была"

    if letter not in current_word:
        return False, "Такой буквы нет"
    else:
        return True, "Есть такая буква!"


def check_win() -> bool:
    for letter in current_word:
        if letter not in guessed_letters:
            return False
    return True


def check_loss() -> bool:
    return mistakes_count >= MAX_MISTAKES


def get_gallows_stage() -> str:
    stage_file = os.path.join(GALLOWS_FOLDER, f"stage_{mistakes_count}.txt")
    try:
        with open(stage_file, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return f"Стадия {mistakes_count} виселицы (файл не найден)"


def get_game_info() -> Dict:
    guessed_str = ', '.join(sorted(guessed_letters)) if guessed_letters else 'пока нет'

    info = {
        'display_word': get_display_word(),
        'description': current_description,
        'guessed_letters': guessed_str,
        'mistakes': mistakes_count,
        'max_mistakes': MAX_MISTAKES,
        'gallows': get_gallows_stage(),
        'status_message': status_message,
        'is_won': check_win(),
        'is_lost': check_loss()
    }
    return info


def make_move(letter: str) -> Dict:
    global mistakes_count, status_message, guessed_letters
    letter = letter.upper()
    is_correct, message = check_letter(letter)
    status_message = message
    
    if is_correct or (not is_correct and message != "Ошибка: введите одну букву"):
        if letter not in guessed_letters and letter.isalpha() and len(letter)==1:
            guessed_letters.append(letter)
            if not is_correct:
                mistakes_count += 1
    return get_game_info()


def restart_game() -> Dict:
    select_random_word()
    reset_game_state()
    return get_game_info()


def display_output(game_info: Dict) -> None:
    print("\n" + "=" * 50)
    print(f"Тема: {game_info['description']}")
    print(f"Слово: {game_info['display_word']}")
    print(f"Использованные буквы: {game_info['guessed_letters']}")
    print(f"Ошибок: {game_info['mistakes']}/{game_info['max_mistakes']}")
    print("\n" + game_info['gallows'])
    print(game_info['status_message'])


def display_goodbye() -> None:
    print("\n" + "=" * 50)
    print("Спасибо за игру!")
    print("=" * 50)


def get_user_input(prompt: str) -> str:
    return input(prompt)