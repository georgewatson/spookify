#!/usr/bin/env python3

"""
SPOOKIFY
Halloween name generator
<https://github.com/georgewatson/spookify>

George Watson, 2018
Available under an MIT licence
(see LICENSE file, or https://opensource.org/licenses/MIT)

Spookifies all words of 3 or more characters.
To force a match for words shorter than 3 characters, append some dots or
something.

Dependencies (specific to this file):
- Standard:
    sys
- The remainder of the 'spookify' module (spookify/__init__.py)
For additional dependencies, see __init__.py

This file is used to run spookify from the command line.
To do this, type:
    python3 -m spookify [name]
If no name is provided, spookify will run in interactive mode.

For information on using spookify functions in your own code, see __init__.py

See README.md for more details.
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
        LIST_TYPE = input(
            "Select a word list (default: spooky) > ").lower() or 'spooky'
    while NAME.lower() not in ['exit', 'quit']:
        # try/except to elegantly handle ^C and ^D
        try:
            NAME = input("Enter a name (or 'exit') > ")
            print(spookify(NAME, list_type=LIST_TYPE))
        except (KeyboardInterrupt, EOFError):
            break

# eof
