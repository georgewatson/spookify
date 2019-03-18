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


def main():
    """
    The main function
    See module docstring
    """
    # If a name is provided as an argument,
    # process it
    # and print the result.
    if sys.argv[1:]:
        name = ' '.join(sys.argv[1:])
        print(spookify(name))

    # If no name is provided,
    # act as a REPL.
    else:
        name = ""
        list_type = ''
        valid_types = ['festive', 'spooky']

        try:
            # Loop until we receive a valid input
            while list_type not in valid_types:
                list_type = (input(
                    "Select a word list (default: spooky) > ").lower()
                             or 'spooky')

            # Keep asking for names
            while name.lower() not in ['exit', 'quit']:
                name = input("Enter a name (or 'exit') > ")
                print(spookify(name, list_type=list_type))

        # Handle interrupt signals gracefully
        except (KeyboardInterrupt, EOFError):
            sys.exit(0)


if __name__ == "__main__":
    main()

# eof
