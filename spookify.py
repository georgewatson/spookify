#!/usr/bin/env python3

"""
SPOOKIFY
Halloween name generator
<https://github.com/georgewatson/spookify>

George Watson, 2018
Available under an MIT licence (see LICENSE)

Usage:
    ./spookify.py <name>

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

Provides the following functions:
    spookify(name)*
        The main function
        Returns a spookified Halloween version of the string 'name'
    best_substitution(word, possible_subs)*
        Performs the best substitution of a member of possible_subs into word
    score_substitution(word_part, possible_sub)
        Scores the desirability of replacing word_part with possible_sub

    (Functions marked * include random elements)

Global variables:
    SPOOKY_WORDS
        A list of spooky words

The above components are available for use in other code if imported correctly,
and should have no side effects.
However, Spookify is not at present packaged as a formal module and is provided
as-is without any guarantee of safety or fitness for purpose.
"""

# pylint: disable=c-extension-no-member

import json
import os
import random
import string
import sys
import regex as re
import jellyfish


def best_substitution(word, possible_subs):
    """
    Finds the best possible substitution in a given word,
    and returns the modified word
    In the case of a tie, modifications are chosen at random

    Note: This function has a random element
    """
    # Skip short words
    ignored_words = ['and', 'for', 'the']
    if len(word) < 3 or word in ignored_words:
        return word

    # Get all substrings of length >= 3
    substrings = [word[i:j+1]
                  for i in range(len(word) - 2)
                  for j in range(i+2, len(word))]

    # Sort by length to encourage longer substitutions
    # Technically impure, but who cares?
    random.shuffle(substrings)
    substrings.sort(key=len, reverse=True)

    # Find the best spooky substitution
    best_sub = min([(name_part,
                     substitution,
                     score_substitution(name_part, substitution))
                    for name_part in substrings
                    for substitution in possible_subs],
                   key=lambda t: t[2])

    # Substitute the relevant substring, delimited by hyphens
    word = word.replace(best_sub[0], "-"+best_sub[1]+"-")
    # But remove the hyphens at word boundaries
    word = re.sub(r'^-|-$', "", word)

    # Return the result
    return word


def score_substitution(word_part, possible_sub):
    """
    Determines the score of a substitution (lower is better)
    Criteria:
        Identical words score 0
        Substitutions are given a score equal to their normalized
            Damerau-Levenshtein distance
            (the number of insertions, deletions, substitutions &
            transpositions, divided by the length of the substitution)
    """
    # TODO: Consider integrating a phonetic element
    # (jellyfish provides several)

    # If the words are the same, no substitution is needed
    # Avoid expensive operations
    if possible_sub == word_part:
        return 0

    # Otherwise, check the normalised Damerau-Levenshtein distance
    return jellyfish.damerau_levenshtein_distance(
        possible_sub, word_part) / len(possible_sub)


def spookify(name, list_type='spooky'):
    """
    Spookify
    Generates a spooky version of a provided string, intended for names.
    This acts as the main function for the 'spookify' module.
    See 'spookify' module docstring for more info.

    This function takes input from a json file in the 'wordlists' directory,
    and has random elements.
    """

    # Convert strings to lowercase
    name = name.lower()

    # Import the word list from a JSON-formatted file
    # If no file with that name exists, default to spooky
    # IO makes this technically impure, but really how is this any different
    # from just declaring the lists inside the function?
    filename = os.path.join(
        sys.path[0], 'wordlists', '.'.join([list_type, 'json']))
    if os.path.isfile(filename):
        word_file = open(filename, 'r')
    else:
        word_file = open(os.path.join(
            sys.path[0], 'wordlists', 'spooky.json'), 'r')
    word_list = json.load(word_file)
    word_file.close()

    # Randomly shuffle the spooky words for variety,
    # then sort by length to encourage longer substitutions
    # Technically impure, but who cares?
    random.shuffle(word_list)
    word_list.sort(key=len, reverse=True)

    # Construct a new name by applying the best substitution to each word
    new_name = " ".join([best_substitution(name_word, word_list)
                         for name_word in name.split()])

    return string.capwords(new_name)


# Don't run automatically if imported as a module
if __name__ == '__main__':

    # TODO: Make wordlist selection a flag

    # Get a name from the command line
    if sys.argv[1:]:
        NAME = ' '.join(sys.argv[1:])
        print(spookify(NAME))
    else:
        NAME = ""
        # If no name is provided, act as a repl
        LIST_TYPE = input("Select a word list (default: spooky) > ")
        while NAME.lower() not in ['exit', 'quit']:
            # try/except to elegantly handle ^C and ^D
            try:
                NAME = input("Enter a name (or 'exit') > ")
                print(spookify(NAME, list_type=LIST_TYPE))
            except (KeyboardInterrupt, EOFError):
                break

# eof
