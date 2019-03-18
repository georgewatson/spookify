[![PyPI version](https://badge.fury.io/py/spookify.svg)](https://badge.fury.io/py/spookify)

# spookify
Spooky Halloween name generator

Also supports a limited festive dictionary

## Installation
This project is available [on PyPI](https://pypi.org/project/spookify/);
install using
* `pip3 install spookify`

Or clone [this repo](https://github.com/georgewatson/spookify) and build it
yourself, if you prefer.

Non-standard dependencies:
* [jellyfish](https://github.com/jamesturk/jellyfish)
  `pip3 install jellyfish`
* [regex](https://bitbucket.org/mrabarnett/mrab-regex)
  `pip3 install regex`

## Usage
Once installed through pip, run using
* `spookify`, or
* `python3 -m spookify [name]`

If no name is provided on the command line, the script will run in interactive
mode, allowing many names to be generated in a single session.
This also allows the selection of alternative dictionaries (see "Available
dictionaries", below).

If you don't wish to install the package through pip, spookify can be run
directly by cloning this repo and running `spookify/__main__.py`.

Spookify can also be imported for use in other Python scripts, in the typical
fashion:
* `import spookify [as ...]`
* `from spookify import [...]`

This exposes the following functions:
* `spookify.spookify(name[, list_type][, shuffle])`  
  Returns a punned-upon version of the string `name`.  
  Possible values of `list_type` are listed under "Available dictionaries"
  below.
* `spookify.best_substitution(word, possible_subs[, shuffle])`  
  Performs the best substitution of a member of the list `possible_subs` into
  `word`.
* `spookify.score_substitution(word_part, possible_sub[, vowels])`  
  Scores the desirability of replacing the string `word_part` with
  `possible_sub` (lower is better).

Functions with pseudo-random elements all support a `shuffle` argument.
By setting this to `False`, this can be disabled, resulting in a consistent
return value.

See the function docstrings for more details.

### Available dictionaries
* `spooky` (default)
* `festive`

## Examples

| Name             | `spooky`              | `festive`         |
|------------------|-----------------------|-------------------|
| George Watson    | Ge-ogre Bats-on       | Geo-tree Hats-on  |
| Richard Stallman | Witch-ard Skull-man   | Ri-card Star-lman |
| Linus Torvalds   | Li-guts To-graveyards | Pine-us Toy-valds |
| Donald Trump     | Demon-ald T-pumpkin   | Coal-d T-jumper   |
| Theresa May      | T-eerie-sa Candy      | Cheers-a Mary     |
| Ubuntu           | U-haunt-u             | U-fun-tu          |

## Licensing
This software is made available under an MIT License.
See the `LICENSE` file for more information.

This allows you to do whatever you want with the software,
free of charge,
including making modifications and distributing it commercially,
provided you retain the contents of the (very short) `LICENSE` file
in an appropriate place in all copies you distribute.
This file includes an attribution to the authors of this repository.

All potential contributors are expected to license their contributions under
the same licence,
and *may* add their names to the copyright notice in a pull request.

Although no patents are, at present, claimed on this software,
for the avoidance of doubt,
the "without limitation" line in the license text is considered by the authors
to be an explicit licence of any relevant patents.
