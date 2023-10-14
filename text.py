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
    """Prompt the user to make a choice from a list of valid choices.
    Display an error message and reprompt until a valid choice is made.

    Arguments
    ---------
    options: list[str]
    - A list of choices for the user to choose from.
      Each choice is enumerated starting from 1.
      A choice is made by inputting its number.
    
    inline: bool (default: False)
    - Whether to display options inline with the prompt.
      If False, options will be displayed as an enumerated list.

    cancel: bool (default: False)
    - Whether to allow the user to cancel their choice.
      If True, prompt informs users thry can cancel their choice with 'b'.
      None is returned if user cancels their choice.

    prompt: str
    - text to display as the prompt
    
    errmsg: str
    - text to display for invalid choice, before reprompt
    
    prelude: str
    - text to display before enumeration of choices
    """
    # Prompt preparation
    if inline and cancel:
        prompt += f" ({'/'.join(options)} or 'b' to go back): "
    elif not inline and cancel:
        prompt += " (or 'b' to go back): "

    # Display enumerated choices
    if prelude:
        print(prelude)
    if not inline:
        for i, option in enumerate(options, start=1):
            print(f"{i}. {option}")
    print('')

    # User prompt and choice validation
    choice = input(prompt)
    while not (choice.isdecimal() and 1 <= int(choice) <= len(options)):
        print(errmsg)
        choice = input(prompt)
        if cancel and choice.lower() == 'b':
            return None
    print('')
    return choice

