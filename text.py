"""text.py

Module to help with formatting and displaying text, and prompting for text input
"""
from typing import Any


def prompt_valid_choice(
    options: list[str],
    *,  # parameters below are keyword-only
    inline: bool = False,
    cancel: bool = False,
    prompt: str = "Pick an option",
    errmsg: str = "Invalid option, try again.",
    prelude: str = "",
) -> "str | None":
    # Prompt preparation
    if inline and cancel:
        prompt += f" ({'/'.join(options)} or 'b' to go back): "
    elif not inline and cancel:
        prompt += " (or 'b' to go back): "

    if prelude:
        print(prelude)
    if not inline:
        for i, option in enumerate(options, start=1):
            print(f"{i}. {option}")
    print('')
    choice = input(prompt)
    while not (choice.isdecimal() and 1 <= int(choice) <= len(options)):
        print(errmsg)
        choice = input(prompt)
        if cancel and choice.lower() == 'b':
            return None
    print('')
    return choice

