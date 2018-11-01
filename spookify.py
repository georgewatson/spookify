#!/usr/bin/env python3

"""
SPOOKIFY
Halloween name generator

Usage:
    ./spookify.py <name>

Spookifies all words over 3 characters.
To force a match for words shorter than 3 characters, append some dots or
something.
"""

# pylint: disable=consider-using-enumerate

import random
import sys
import string


def levenshtein(string1, string2):
    """
    Calculates the Levenshtein distance between two strings
    See https://en.wikipedia.org/wiki/Levenshtein_distance
    """
    # Only the last two rows of the matrix are actually necessary
    row1 = [None] * (len(string2) + 1)
    row2 = [None] * (len(string2) + 1)

    # Fill in row1 with the distance from an empty string1 (the length)
    for i in range(len(row1)):
        row1[i] = i

    # Calculate distances from previous row
    for i in range(len(string1)):
        # First element is empty string2, so use length again
        row2[0] = i + 1

        for j in range(len(string2)):
            # Calculate costs
            insertions = row2[j] + 1
            deletions = row1[j+1] + 1
            if string1[i] == string2[j]:
                substitutions = row1[j]
            else:
                substitutions = row1[j] + 1

            # Find the smallest number of modifications
            row2[j+1] = min(insertions, deletions, substitutions)

        # Move down a row and repeat
        row1 = row2.copy()

    # Result is the last element of row1
    return row1[-1]


# A list of spooky words for potential substitutions
SPOOKY_WORDS = ["halloween",
                "axe", "axeman", "axes", "axewound",
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

    # Convert all strings to lowercase
    name = name.lower()
    new_name = ""

    # Randomly shuffle the spooky words for variety, then sort by length to
    # encourage longer substitutions
    random.shuffle(SPOOKY_WORDS)
    SPOOKY_WORDS.sort(key=len, reverse=True)

    # For each word in the name...
    for word in name.split():
        if len(word) < 3 or word in ['and', 'for', 'the']:
            new_name = new_name + " " + word
            continue

        min_score = len(word) + 1
        new_word = word
        best_sub = ()

        # Get all substrings of length >= 3
        substrings = []
        for i in range(len(word)):
            for j in range(i, len(word)):
                if len(word[i:j+1]) >= 3:
                    substrings.append(word[i:j+1])
        # Sort by length, to encourage longer substitutions
        random.shuffle(substrings)
        substrings.sort(key=len, reverse=True)

        # Compare each substring to each spooky word
        for name_part in substrings:
            for spooky_word in SPOOKY_WORDS:
                # Don't make the word shorter
                if len(spooky_word) >= len(name_part):
                    # Record the best match found so far
                    this_levenshtein = levenshtein(spooky_word, name_part)
                    this_score = this_levenshtein / len(spooky_word)
                    # Strictly less-than to encourage longer subs
                    if this_score < min_score:
                        min_score = this_score
                        best_sub = (name_part, spooky_word)

        # Substitute the relevant substring, delimited by hyphens
        if new_word:
            new_word = word.replace(best_sub[0], "-"+best_sub[1]+"-")
            # But remove the hyphens at word boundaries
            if new_word[0] == '-':
                new_word = new_word[1:]
            if new_word[-1] == '-':
                new_word = new_word[:-1]

        # Add this word to the name
        new_name = new_name + " " + new_word

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
