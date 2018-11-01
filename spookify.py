#!/usr/bin/env python3

"""
SPOOKIFY
Halloween name generator

Usage:
    ./spookify.py <name>

Spookifies all words over 3 characters.
To force a match for words shorter than 3 characters, append some dots or
something.

Provides the following components:
    main(name)
        Returns a spookified Halloween version of the string 'name'
    levenshtein(string1, string2)
        Calculates the Levenshtein distance between two strings
    SPOOKY_WORDS
        A list of spooky words

The above components are available for use in other code if imported correctly,
and should have no side effects.
However, Spookify is not at present packaged as a formal module and is provided
as-is without any guarantee of safety or fitness for purpose.
"""

# pylint: disable=consider-using-enumerate

import random
import sys
import string


def levenshtein(string1, string2):
    """
    Calculates the Levenshtein distance between two strings
    This is the minimum number of single-character changes (insertions,
    deletions, and substitutions) required to transform one string into the
    other.
    See <https://en.wikipedia.org/wiki/Levenshtein_distance>
    """
    # Only two rows of the matrix are actually necessary
    row1 = [None] * (len(string2) + 1)
    row2 = [None] * (len(string2) + 1)

    # Fill in row1 with the distance from an empty string1 (the length)
    row1 = range(len(row1))

    # Calculate distances from previous row
    for i in range(len(string1)):
        # First element is empty string2, so use length again
        row2[0] = i + 1

        # Calculate the minimum cost
        for j in range(len(string2)):
            row2[j+1] = min(row2[j] + 1,
                            row1[j+1] + 1,
                            row1[j] + (0 if string1[i] == string2[j] else 1))

        # Move down a row and repeat
        row1 = row2.copy()

    # Result is the last element of row1
    return row1[-1]


def is_anagram(string1, string2):
    """
    Checks whether two strings contain the same characters
    Returns True if so, else False
    """
    # Strings of different lengths can't be anagrams
    if len(string1) != len(string2):
        return False

    characters1 = list(string1)
    characters2 = list(string2)
    characters1.sort()
    characters2.sort()

    return characters1 == characters2


def score_substitution(word_part, possible_sub):
    """
    Determines the score of a substitution (lower is better)
    Criteria:
        Identical words score -1
        Anagrams score         0
        Substitutions that make the word shorter are never accepted
            (they score word_length + 1, worse than any other substitution)
        Other substitutions are given a score equal to their Levenshtein
            distance divided by the length of the word
    """
    # If the words are the same, no substitution is needed
    if possible_sub == word_part:
        return -1

    # Don't make the word shorter
    if len(possible_sub) < len(word_part):
        return len(word_part) + 1

    # Accept anagrams immediately
    if is_anagram(word_part, possible_sub):
        return 0

    # Otherwise, check the Levenshtein distance
    # Divide by length to encourage longer subs
    return levenshtein(possible_sub, word_part) / len(possible_sub)


def best_substitution(word, possible_subs):
    """
    Finds the best possible substitution in a given word,
    and returns the modified word
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
    new_word = word.replace(best_sub[0], "-"+best_sub[1]+"-")
    # But remove the hyphens at word boundaries
    if new_word[0] == '-':
        new_word = new_word[1:]
    if new_word[-1] == '-':
        new_word = new_word[:-1]

    # Return the result
    return new_word


# A list of spooky words for potential substitutions
SPOOKY_WORDS = ["halloween",
                "axe", "axes", "axewound",
                "banshee", "banshees",
                "bat", "bats",
                "beast", "beastly", "beasts",
                "bite", "bites", "bitten",
                "blackcat", "blackcats",
                "bleed", "bleeding",
                "blood", "bloody", "blooded", "bloodcurdling",
                "bogeyman", "boogeyman",
                "bone", "bones", "bonechilling", "bony",
                # "boo",
                "brains",
                "broom", "broomstick", "brooms", "broomsticks",
                "cackle", "cackling",
                "cadaver", "cadavers",
                "candle", "candles",
                "candy", "chocolate",
                "cauldron", "cauldrons",
                "cemetery", "cemeteries",
                "chill", "chills", "chilling",
                "chocolate",
                "clown",
                "cobweb", "cobwebs",
                "coffin", "coffins",
                "corpse", "corpses", "corpselike",
                "costume", "costumed", "costumes",
                "creature", "creatures",
                "creep", "creepy", "creeps", "creeping", "creeper",
                "crow", "crows",
                "crypt",
                "dark", "darkness",
                "dead", "death", "deathly", "deadly",
                "demon", "demons", "demonic", "dementor", "dementors",
                "demented",
                "devil", "devils", "devilish",
                "disguise", "disguised", "disguises",
                "doom", "doomed",
                "dracula",
                "dread", "dreadful", "dreaded",
                "dying",  # "die",
                "eerie",
                "evil",
                "eyeball", "eyeballs",
                "fang", "fangs",
                "fear", "fearful",
                "frankenstein",
                "fright", "frighten", "frightening", "frightened", "frightful",
                "fullmoon",
                "ghast", "ghasts", "ghastly",
                "ghost", "ghosts", "ghostly",
                "ghoul", "ghouls", "ghoulish",
                "gore", "gory", "gored",
                "grave", "gravestone", "graves", "gravestones", "graveyard",
                "graveyards",
                "grim", "grimreaper",
                "grisly",
                "gruesome",
                "guts",
                "hairraising",
                "hallow", "hallows",
                "haunt", "haunted", "haunting", "hauntedhouse",
                "headless",
                "headstone", "headstones",
                "hearse", "hearses",
                "hell", "hellish", "hellhound", "hellcat",
                "hide", "hiding",
                "horror", "horrific", "horrify", "horrifying", "horrible",
                "howl", "howling",
                "intestines",
                "jackolantern",
                "lantern",
                "lightning",
                "livingdead",
                "macabre",
                "mausoleum", "mausoleums",
                "midnight",
                "monster", "monsters", "monstrous",
                "moonlight", "moonlit",  # "moon",
                "morbid",
                "mummy",
                "night", "nightmare", "nighttime",
                "noose",
                "occult",
                "october",
                "ogre", "ogres",
                "ominous",
                "owl",
                "petrify", "petrified", "petrifying",
                "phantom", "phantoms", "phantasm", "phantasms",
                "pitchfork",
                "poltergeist", "poltergeists",
                "possessed",
                "potion", "potions",
                "pumpkin", "pumpkins",
                "raven", "ravens",
                "reaper",
                "repulsive", "repulsed",
                "revolting", "revolted",
                "risen",
                "scare", "scary", "scared", "scarecrow",
                "scream", "screams", "screaming",
                "sever", "severed",
                "shadow", "shadows", "shadowy",
                "shock", "shocked", "shocking",
                "skeleton", "skeletons", "skeletal",
                "skull", "skulls",
                "sneak", "sneaky",
                "sorceror", "sorceress", "sorcerors", "sorceresses",
                "specter", "spectre", "specters", "spectres", "spectral",
                "spider", "spiderweb", "spiders", "spiderwebs",
                "spinechilling",
                "spirit", "spirits",
                "spook", "spooky", "spooks", "spooked",
                "startling", "startled", "startle",
                "supernatural",
                "sweets",
                "thirteen",
                "terror", "terrible", "terrifying", "terrified",
                "thrill", "thrilling",
                "thunder",
                "tomb", "tombstone", "tombs", "tombstones",
                "trembling", "tremble",
                "trick", "treat", "trickortreat", "tricks", "treats",
                "troll", "trolls",
                "undead", "undying",
                "unearthly",
                "unnerving", "unnerved",
                "vampire", "vampires", "vampiric",
                "warlock", "warlocks",
                "web", "webs",
                "weird",
                "werewolf", "werewolves", "wolf", "wolves", "wolfman",
                "wicked",
                "witch", "witches", "witchcraft", "witchy",
                "wizard", "wizards", "wizardry",
                "wound", "wounds", "wounded",
                "wraith", "wraiths",
                "zombie", "zombies"]


def main(name):
    """
    Spookify
    Generates a spooky version of a provided string, intended for names.
    See 'spookify' module docstring for more info.
    """

    # Convert strings to lowercase
    name = name.lower()

    # Randomly shuffle the spooky words for variety,
    # then sort by length to encourage longer substitutions
    random.shuffle(SPOOKY_WORDS)
    SPOOKY_WORDS.sort(key=len, reverse=True)

    # Construct a new name by applying the best substitution to each word
    new_name = " ".join([best_substitution(word, SPOOKY_WORDS)
                         for word in name.split()])

    return string.capwords(new_name)


# Don't run automatically if imported as a module
if __name__ == '__main__':
    # Get a name from the command line, or ask for one
    if sys.argv[1:]:
        NAME = ' '.join(sys.argv[1:])
    else:
        NAME = input("Enter your name: ")

    print(main(NAME))

# eof
