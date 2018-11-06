#!/usr/bin/env python3

"""
SPOOKIFY
Halloween name generator
<https://github.com/georgewatson/spookify>

George Watson, 2018
Available under an MIT licence (see LICENSE)

Spookifies all words of 3 or more characters.
To force a match for words shorter than 3 characters, append some dots or
something.

Dependencies:
- Standard:
    json
    os
    random
    regex
    string
    sys
- Third-party:
    jellyfish <https://pypi.org/project/jellyfish/>
        Available through pip (pip install jellyfish)
    pkg_resources

Provides the following functions:
    spookify(name)*
        The main function
        Returns a spookified Halloween version of the string 'name'
    best_substitution(word, possible_subs)*
        Performs the best substitution of a member of possible_subs into word
    score_substitution(word_part, possible_sub)
        Scores the desirability of replacing word_part with possible_sub
    (Functions marked * include random elements)

The above components are available for use in other code if imported correctly,
and should have no side effects.
However, Spookify is not at present packaged as a formal module and is provided
as-is without any guarantee of safety or fitness for purpose.
"""

import sys
from . import spookify

# Get a name from the command line
if sys.argv[1:]:
    NAME = ' '.join(sys.argv[1:])
    print(spookify(NAME))
else:
    # If no name is provided, act as a repl
    NAME = ""
    LIST_TYPE = ''
    VALID_TYPES = ['festive', 'spooky']
    while LIST_TYPE not in VALID_TYPES:
        LIST_TYPE = input("Select a word list (default: spooky) > ")
    while NAME.lower() not in ['exit', 'quit']:
        # try/except to elegantly handle ^C and ^D
        try:
            NAME = input("Enter a name (or 'exit') > ")
            print(spookify(NAME, list_type=LIST_TYPE))
        except (KeyboardInterrupt, EOFError):
            break

# eof
