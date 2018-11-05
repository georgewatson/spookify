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
    random
    regex
    string
    sys

Provides the following functions:
    spookify(name)*
        The main function
        Returns a spookified Halloween version of the string 'name'

    best_substitution(word, possible_subs)*
        Performs the best substitution of a member of possible_subs into word
    is_anagram(string1, string2)
        Determines whether two strings contain the exact same characters
    levenshtein(string1, string2)
        Calculates the Levenshtein distance between two strings
    score_substitution(word_part, possible_sub)
        Scores the desirability of replacing word_part with possible_sub

    (Functions marked * include randomness)

Global variables:
    SPOOKY_WORDS
        A list of spooky words

The above components are available for use in other code if imported correctly,
and should have no side effects.
However, Spookify is not at present packaged as a formal module and is provided
as-is without any guarantee of safety or fitness for purpose.
"""

import json
import random
import string
import sys
import regex as re


def best_substitution(word, possible_subs):
    """
    Finds the best possible substitution in a given word,
    and returns the modified word
    In the case of a tie, modifications are chosen at random
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


def is_anagram(string1, string2):
    """
    Checks whether two strings contain the same characters
    Returns True if so, else False
    """
    # Strings of different lengths can't be anagrams
    # so we might as well avoid sorting them
    if len(string1) != len(string2):
        return False

    return sorted(string1) == sorted(string2)


def levenshtein(string1, string2):
    """
    Calculates the Levenshtein distance between two strings
    This is the minimum number of single-character changes (insertions,
    deletions, and substitutions) required to transform one string into the
    other.
    See <https://en.wikipedia.org/wiki/Levenshtein_distance>
    """
    # Only two rows of the matrix are actually necessary
    # Fill in prev_row with the distance from an empty string1 (the length)
    prev_row = range(len(string2) + 1)
    # Pad this_row to the correct length with Nones
    this_row = [None] * (len(string2) + 1)

    # Calculate distances from previous row
    for i, char1 in enumerate(string1):
        # First element is empty string2, so use length again
        this_row[0] = i + 1

        # Calculate the minimum cost
        for j, char2 in enumerate(string2):
            this_row[j+1] = min(this_row[j] + 1,
                                prev_row[j+1] + 1,
                                prev_row[j] + (0 if char1 == char2 else 1))

        # Move down a row and repeat
        prev_row = this_row.copy()

    # Result is the last element of the matrix
    return this_row[-1]


def score_substitution(word_part, possible_sub):
    """
    Determines the score of a substitution (lower is better)
    Criteria:
        Identical words score 0
        Substitutions are given a score equal to their Levenshtein
            distance divided by the length of the substitution
        Anagrams score half, so character swaps are sort-of treated as 1 edit
    """
    # TODO: Consider Damerau-Levenshtein
    # This counts transposition of adjacent characters as 1 edit,
    # capturing the "best" anagrams and also giving near-anagrams a boost

    # If the words are the same, no substitution is needed
    if possible_sub == word_part:
        return 0

    # Favour anagrams by halving their score
    # Effectively treats a character swap as a single edit
    if is_anagram(word_part, possible_sub):
        return levenshtein(possible_sub, word_part) / (2 * len(possible_sub))

    # Otherwise, check the Levenshtein distance
    # Divide by length to encourage longer subs
    return levenshtein(possible_sub, word_part) / len(possible_sub)


def spookify(name):
    """
    Spookify
    Generates a spooky version of a provided string, intended for names.
    This acts as the main function for the 'spookify' module.
    See 'spookify' module docstring for more info.
    """

    # Convert strings to lowercase
    name = name.lower()

    # Copy the word list to avoid side effects
    word_list = WORD_LIST.copy()

    # Randomly shuffle the spooky words for variety,
    # then sort by length to encourage longer substitutions
    # Technically impure, but who cares?
    random.shuffle(word_list)
    word_list.sort(key=len, reverse=True)

    # Construct a new name by applying the best substitution to each word
    new_name = " ".join([best_substitution(name_word, word_list)
                         for name_word in name.split()])

    return string.capwords(new_name)


# Import the word list from a JSON-formatted file
WORD_FILE = open("spooky_words.json", 'r')
WORD_LIST = json.load(WORD_FILE)

# Don't run automatically if imported as a module
if __name__ == '__main__':

    NAME = ""

    # Get a name from the command line
    if sys.argv[1:]:
        NAME = ' '.join(sys.argv[1:])
        print(spookify(NAME))
    else:
        # If no name is provided, act as a repl
        while NAME.lower() not in ['exit', 'quit']:
            # try/except to elegantly handle ^C
            try:
                NAME = input("Enter a name (or 'exit') > ")
                print(spookify(NAME))
            except KeyboardInterrupt:
                break

# eof
