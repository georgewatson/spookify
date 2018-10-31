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


def levenshtein(string_1, string_2):
    """
    Calculate the Levenshtein distance between two strings
    From
    https://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Levenshtein_distance#Python
    (CC-BY-SA)
    """
    if string_1 == string_2:
        return 0
    elif not string_1:
        return len(string_2)
    elif not string_2:
        return len(string_1)
    v_0 = [None] * (len(string_2) + 1)
    v_1 = [None] * (len(string_2) + 1)
    for i in range(len(v_0)):
        v_0[i] = i
    for i in range(len(string_1)):
        v_1[0] = i + 1
        for j in range(len(string_2)):
            cost = 0 if string_1[i] == string_2[j] else 1
            v_1[j + 1] = min(v_1[j] + 1, v_0[j + 1] + 1, v_0[j] + cost)
        for j in range(len(v_0)):
            v_0[j] = v_1[j]

    return v_1[len(string_2)]


SPOOKY_WORDS = ["halloween",
                "bat", "bats",
                "banshee", "banshees",
                "beast", "beastly", "beasts",
                "blackcat", "blackcats",
                "blood", "bloody", "blooded", "bloodcurdling",
                "bite", "bites", "bitten",
                "bogeyman", "boogeyman",
                "bone", "bones", "bonechilling",
                # "boo",
                "brains",
                "broom", "broomstick", "brooms", "broomsticks",
                "cackle", "cackling",
                "cadaver", "cadavers",
                "candle", "candles",
                "candy", "chocolate",
                # "cat", "cats",
                "cauldron", "cauldrons",
                "cemetery", "cemeteries",
                "chill", "chills", "chilling",
                "corpse", "corpses", "corpselike",
                "costume", "costumed", "costumes",
                "clown",
                "cobweb", "cobwebs",
                "coffin", "coffins",
                "creature", "creatures",
                "crow", "crows",
                "crypt",
                "creep", "creepy", "creeps", "creeping", "creeper",
                "darkness",  # "dark",
                "dead", "death", "deathly", "deadly",
                "dying",  # "die",
                "disguise", "disguised", "discuises",
                "demon", "demons", "demonic",
                "devil", "devils", "devilish",
                "dracula",
                "dread", "dreadful", "dreaded",
                "doom", "doomed",
                "eerie",
                "evil",
                "eyeball", "eyeballs",
                "fang", "fangs",
                "fear", "fearful",
                "fullmoon",
                "fright", "frighten", "frightening", "frightened", "frightful",
                "ghast", "ghastly",
                "ghost", "ghosts", "ghostly",
                "ghoul", "ghouls", "ghoulish",
                "gore", "gory", "gored",
                "guts",
                "gruesome",
                "grave", "gravestone", "graves", "gravestones", "graveyard",
                "graveyards",
                "grim", "grimreaper",
                "grisly",
                "gruesome",
                "hair-raising",
                "hallow", "hallows",
                "haunt", "haunted", "haunting", "haunted-house",
                "headless",
                "headstone", "headstones",
                "hearse", "hearses",
                "hell", "hellish", "hellhound", "hellcat",
                "horror", "horrific", "horrify", "horrifying", "horrible",
                # "hide",
                "howl", "howling",
                "intestines",
                "jackolantern",
                "lantern",
                "living-dead",
                "lightning",
                "macabre",
                "mausoleum", "mausoleums",
                "monster", "monsters", "monstrous",
                "midnight",
                "moonlight", "moonlit",  # "moon",
                "morbid",
                "mummy",
                "night", "nightmare", "nighttime",
                "noose",
                "occult",
                "owl",
                "october",
                "ominous",
                "ogre", "ogres",
                "petrify", "petrified", "petrifying",
                "phantom", "phantoms", "phantasm", "phantasms",
                "possessed",
                "pitchfork",
                "poltergeist", "poltergeists",
                "potion", "potions",
                "pumpkin", "pumpkins",
                "raven", "ravens",
                "reaper",
                "revolting", "revolted",
                "repulsive", "repulsed",
                "risen",
                "scare", "scary", "scared", "scarecrow",
                "scream", "screams", "screaming",
                "shadow", "shadows", "shadowy",
                "shock", "shocked", "shocking",
                "skeleton", "skeletons", "skeletal",
                "skull", "skulls",
                "sneak", "sneaky",
                "sorceror", "sorceress",
                "specter", "spectre", "specters", "spectres", "spectral",
                "spider", "spiderweb", "spiders", "spiderwebs",
                "spine-chilling",
                "spirit", "spirits",
                "spook", "spooky", "spooks", "spooked",
                "startling", "startled", "startle",
                "supernatural",
                "terror", "terrible", "terrifying", "terrified",
                "trembling", "tremble",
                "thrill", "thrilling",
                "thunder",
                "tomb", "tombstone", "tombs", "tombstones",
                "trick", "treat", "trickortreat", "tricks", "treats",
                "troll", "trolls",
                "undead", "undying",
                "unearthly",
                "unnerving", "unnerved",
                "vampire", "vampires", "vampiric",
                "warlock", "warlocks",
                # "web", "webs",
                "weird",
                "werewolf", "werewolves", "wolf", "wolves", "wolfman",
                "wicked",
                "witch", "witches", "witchcraft", "witchy",
                "wizard", "wizards", "wizardry",
                "wraith", "wraiths",
                "zombie", "zombies"]


def main():
    """
    The main function
    """
    # Get a name from the command line, or ask for one
    if sys.argv:
        name = ' '.join(sys.argv[1:])
    else:
        name = input("Enter your name: ")

    # Convert all strings to lowercase
    name = name.lower()
    new_name = ""

    # For each word in the name...
    for word in name.split():
        if len(word) < 3:
            new_name = new_name + " " + word
            continue

        min_levenshtein = len(word) + 1
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
            random.shuffle(SPOOKY_WORDS)
            for spooky_word in SPOOKY_WORDS:
                # Record the best match found so far
                this_levenshtein = levenshtein(spooky_word, name_part)
                # Strictly less-than to encourage longer subs
                if this_levenshtein < min_levenshtein:
                    min_levenshtein = this_levenshtein
                    best_sub = (name_part, spooky_word)

        # Substitute the relevant substring, delimited by hyphens
        if min_levenshtein < len(word) + 1:
            new_word = word.replace(best_sub[0], "-"+best_sub[1]+"-")
        # But remove the hyphens at word boundaries
        if new_word[0] == '-':
            new_word = new_word[1:]
        if new_word[-1] == '-':
            new_word = new_word[:-1]

        # Add this word to the name
        new_name = new_name + " " + new_word

    print(string.capwords(new_name))


if __name__ == '__main__':
    main()
