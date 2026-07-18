# Mastermind (CLI)

A terminal implementation of the classic **Mastermind** code-breaking game. The computer generates a secret 4-color code, and you have a limited number of tries to guess it — with feedback after each guess telling you how close you are.

## How to play

- The computer picks a secret code of 4 colors (repeats allowed) from: `R`, `G`, `B`, `Y`, `W`, `O` (Red, Green, Blue, Yellow, White, Orange)
- You have 10 tries to guess the exact code
- After each guess, you're told:
  - **Correct Positions** — how many colors are the right color _and_ in the right spot
  - **Incorrect Positions** — how many colors are in your guess and in the code, but in the wrong spot
- Guess all 4 correctly to win. Run out of tries and the code is revealed.

## Requirements

- Python 3.6+ (no external dependencies)

## Usage

Run the script:

```bash
python mastermind.py
```

Enter your guess as 4 space-separated colors, for example:

```
Guess: R G B Y
```

The game will validate your input (correct length, valid colors) before scoring it.

## How it works

- `generate_code()` builds a random 4-color secret code from `COLORS`.
- `guess_code()` reads and validates player input, looping until a valid guess (right length, valid colors) is entered.
- `check_code()` scores a guess against the code:
  1. Counts how many of each color exist in the code.
  2. First pass: counts exact matches (right color, right position), decrementing the color count as each is used.
  3. Second pass: counts color matches in the wrong position, using only colors not already claimed by an exact match — this prevents double-counting a color that only appears once in the code.
- `game()` runs the main loop: generate a code, take guesses up to `TRIES` times, and report the result.

## Limitations & ideas for contribution

- No support for changing code length, color set, or number of tries without editing constants directly in the source
- No hint system beyond correct/incorrect position counts
- No replay prompt — the game ends after one round
- Could be extended with:
  - Command-line arguments or a config option for difficulty (code length, number of colors, tries)
  - A "play again?" loop
  - Colored terminal output (e.g. using `colorama`) instead of letter codes
  - A guess history/board showing all previous guesses and their scores
  - Unit tests for `check_code()`, especially around duplicate-color edge cases
