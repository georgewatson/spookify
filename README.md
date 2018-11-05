# spookify
Spooky Halloween name generator

Also supports a limited festive dictionary

## Installation

This project is available [on PyPI](https://pypi.org/project/spookify/);
install using
* `pip install spookify`

Or clone this repo and build it yourself, if you prefer.

Non-standard dependencies:
* [jellyfish](https://github.com/jamesturk/jellyfish)
  `pip install jellyfish`

## Usage

Once installed through pip, run using
* `python3 -m spookify [name]`

If no name is provided on the command line, the script will run in REPL mode,
allowing many names to be generated in a single session.
This also allows the selection of alternative dictionaries.

## Examples:
* George Watson ⇒ Ge-ogre Bats-on
* Dave Jones ⇒ Grave Bones
* Richard Stallman ⇒ Witch-ard Skull-man
* Donald Trump ⇒ Demon-ald Grim-p
* Theresa May ⇒ T-hearse Mummy
* Albus Dumbledore ⇒ Al-bats Dum-bleed-ore
* Engineering and Physical Sciences Research Council ⇒ Engin-eerie-g And
  Phy-spectral Scare-nces Re-fear-ch Wound-il

It's not very good.
