"""Alphabet data and speech text for ABC Kids (no Kivy imports, so it is easy to test)."""

# letter, picture word, how the letter NAME is said aloud
_DATA = [
    ("A", "Apple", "Ay"), ("B", "Ball", "Bee"), ("C", "Cat", "See"),
    ("D", "Dog", "Dee"), ("E", "Elephant", "Ee"), ("F", "Fish", "Eff"),
    ("G", "Giraffe", "Jee"), ("H", "House", "Aitch"), ("I", "Ice cream", "Eye"),
    ("J", "Juice", "Jay"), ("K", "Kite", "Kay"), ("L", "Lion", "Ell"),
    ("M", "Moon", "Em"), ("N", "Nest", "En"), ("O", "Orange", "Oh"),
    ("P", "Penguin", "Pee"), ("Q", "Queen", "Cue"), ("R", "Rainbow", "Ar"),
    ("S", "Sun", "Ess"), ("T", "Tiger", "Tee"), ("U", "Umbrella", "You"),
    ("V", "Violin", "Vee"), ("W", "Whale", "Double you"), ("X", "Xylophone", "Ex"),
    ("Y", "Yo-yo", "Why"), ("Z", "Zebra", "Zee"),
]

LETTERS = [
    {
        "letter": letter,
        "lower": letter.lower(),
        "word": word,
        "say": say,
        "pic": "%s.png" % letter.lower(),
    }
    for letter, word, say in _DATA
]


def speech_text(item):
    """What the voice says for one letter, e.g. 'Ay. Ay is for Apple.'"""
    return "%s. %s is for %s." % (item["say"], item["say"], item["word"])
