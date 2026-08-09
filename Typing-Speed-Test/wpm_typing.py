import curses
from curses import wrapper
import random
import time


def get_sentence():
    # ENTER THE RELATIVE PATH OF TEXT.TXT
    with open("ENTER THE RELATIVE PATH OF TEXT.TXT", "r") as file:
        sentences = file.readlines()

    return random.choice(sentences).strip()


def show_intro(screen):
    screen.clear()
    screen.addstr("⚡ Typing Speed Challenge")
    screen.addstr("\n\nPress any key to start...")
    screen.refresh()
    screen.getch()


def draw_interface(screen, sentence, typed_chars, speed):
    screen.addstr(0, 0, sentence)
    screen.addstr(2, 0, f"Words Per Minute: {speed}")

    for position, letter in enumerate(typed_chars):
        color = curses.color_pair(1)

        if letter != sentence[position]:
            color = curses.color_pair(2)

        screen.addstr(0, position, letter, color)


def typing_game(screen):
    phrase = get_sentence()
    user_input = []

    start = time.time()

    screen.nodelay(True)

    while True:
        elapsed = max(time.time() - start, 1)

        speed = round((len(user_input) / 5) / (elapsed / 60))

        screen.clear()
        draw_interface(screen, phrase, user_input, speed)
        screen.refresh()

        if "".join(user_input) == phrase:
            screen.nodelay(False)
            break

        try:
            pressed_key = screen.getkey()
        except:
            continue

        if ord(pressed_key) == 27:
            return False

        if pressed_key in ("KEY_BACKSPACE", "\b", "\x7f"):
            if user_input:
                user_input.pop()

        elif len(user_input) < len(phrase):
            user_input.append(pressed_key)

    return True


def run_program(screen):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)

    show_intro(screen)

    while True:
        finished = typing_game(screen)

        if not finished:
            break

        screen.addstr(
            4,
            0,
            "Great job! Press any key for another round or ESC to quit."
        )

        key = screen.getkey()

        if ord(key) == 27:
            break


wrapper(run_program)
