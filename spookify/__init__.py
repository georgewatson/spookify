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
    spookify(name, [list_type], [seed])*
        The main function
        Returns a punned-upon version of the string 'name', using the selected
        wordlist; by default, spooky Halloween substitutions are used
    best_substitution(word, possible_subs, [seed])*
        Performs the best substitution of a member of possible_subs into word
    score_substitution(word_part, possible_sub)
        Scores the desirability of replacing word_part with possible_sub
(Functions marked * include pseudo-random elements; a seed may be defined if
this is undesirable)
"""

# pylint: disable=c-extension-no-member

import json
import os
import random
import string
import regex as re
import jellyfish
import pkg_resources


def best_substitution(word, possible_subs, seed=None):
    """
    Finds the best possible substitution in a given word,
    and returns the modified word
    In the case of a tie, modifications are chosen at random

    Arguments:
        word            A word upon which to pun
        possible_subs   A list of words that may be inserted into 'word'
        seed            (optional) A seed for the random number generator

    Note: The return value of this function may not be fixed if no seed is
    defined
    """
    # Skip short words
    ignored_words = ['and', 'for', 'the']
    if len(word) < 3 or word in ignored_words:
        return word

    # Get all substrings of length >= 3
    substrings = [word[i:j+1]
                  for i in range(len(word) - 2)
                  for j in range(i+2, len(word))]

    # Shuffle elements, then sort by length to encourage longer substitutions
    # By defining a seed, the order of the shuffled elements can be fixed
    if seed:
        random.seed(seed)
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

    Arguments:
        word_part       Substring to maybe be replaced with 'possible_sub'
        possible_sub    The string with which 'word_part' may be replaced
    """
    # If the words are the same, no substitution is needed
    # Avoid expensive operations
    if possible_sub == word_part:
        return 0

    # Otherwise, check the normalised Damerau-Levenshtein distance
    return jellyfish.damerau_levenshtein_distance(
        possible_sub, word_part) / len(possible_sub)


def spookify(name, list_type='spooky', seed=None):
    """
    Spookify
    Generates a spooky version of a provided string, intended for names.
    This acts as the main function for the 'spookify' module.
    See 'spookify' module docstring for more info.

    Arguments:
        name        A name (or other string) on which to pun
        list_type   (optional) The wordlist to use (default: spooky)
                    <list_type>.json must exist in spookify/wordlists
        seed        (optional) A seed for the random number generator

    Note: The return value of this function may not be fixed if no seed is
    defined.
    This function takes input from a json file stored in the package directory.
    """

    # Convert strings to lowercase
    name = name.lower()

    # Import the word list from a JSON-formatted file
    # If no file with that name exists, default to spooky
    filename = pkg_resources.resource_filename(
        'spookify', ''.join(['wordlists/', list_type.lower(), '.json']))
    if not os.path.isfile(filename):
        filename = pkg_resources.resource_filename('spookify',
                                                   'wordlists/spooky.json')
    with open(filename, 'r') as word_file:
        word_list = json.load(word_file)

    # Randomly shuffle the spooky words for variety,
    # then sort by length to encourage longer substitutions
    if seed:
        random.seed(seed)
    random.shuffle(word_list)
    word_list.sort(key=len, reverse=True)

    # Construct a new name by applying the best substitution to each word
    new_name = " ".join([best_substitution(name_word, word_list, seed)
                         for name_word in name.split()])

    return string.capwords(new_name)

# eof
