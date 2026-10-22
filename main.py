import os

from kivy.app import App
from kivy.core.audio import SoundLoader
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.utils import get_color_from_hex

WORDS = {
    "A": "Apple", "B": "Ball", "C": "Cat", "D": "Dog", "E": "Elephant",
    "F": "Fish", "G": "Giraffe", "H": "House", "I": "Ice cream", "J": "Juice",
    "K": "Kite", "L": "Lion", "M": "Moon", "N": "Nest", "O": "Orange",
    "P": "Penguin", "Q": "Queen", "R": "Rainbow", "S": "Sun", "T": "Tiger",
    "U": "Umbrella", "V": "Violin", "W": "Whale", "X": "Xylophone",
    "Y": "Yo-yo", "Z": "Zebra",
}

LETTERS = list(WORDS.keys())

BG_COLORS = [
    "#FF6B6B", "#FFA94D", "#FFD43B", "#69DB7C", "#4DABF7", "#9775FA",
    "#F783AC", "#38D9A9", "#FF8787", "#74C0FC", "#B197FC", "#63E6BE",
    "#FFC078",
]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIO_DIR = os.path.join(BASE_DIR, "assets", "audio")


class ABCBook(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=20, spacing=15, **kwargs)
        self.index = 0
        self.sound = None

        with self.canvas.before:
            self.bg_color = Color(*get_color_from_hex(BG_COLORS[0]))
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_bg, size=self._update_bg)

        self.title_label = Label(
            text="My ABC Book", font_size="28sp", bold=True,
            size_hint_y=0.1, color=(1, 1, 1, 1),
        )
        self.letter_label = Label(
            font_size="190sp", bold=True, size_hint_y=0.45, color=(1, 1, 1, 1),
        )
        self.word_label = Label(
            font_size="40sp", size_hint_y=0.12, color=(1, 1, 1, 1),
        )
        self.status_label = Label(
            text="", font_size="16sp", size_hint_y=0.06, color=(1, 1, 1, 0.9),
        )

        self.add_widget(self.title_label)
        self.add_widget(self.letter_label)
        self.add_widget(self.word_label)
        self.add_widget(self.status_label)

        buttons = BoxLayout(size_hint_y=0.17, spacing=12)
        self.prev_btn = self._make_button("Previous", "#364FC7", self.previous_letter)
        self.hear_btn = self._make_button("Hear it!", "#2B8A3E", self.play_sound)
        self.next_btn = self._make_button("Next", "#C2255C", self.next_letter)
        for b in (self.prev_btn, self.hear_btn, self.next_btn):
            buttons.add_widget(b)
        self.add_widget(buttons)

        self.show_letter()

    @staticmethod
    def _make_button(text, hex_color, callback):
        btn = Button(
            text=text, font_size="22sp", bold=True,
            background_normal="", background_color=get_color_from_hex(hex_color),
            color=(1, 1, 1, 1),
        )
        btn.bind(on_release=callback)
        return btn

    def _update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def show_letter(self):
        letter = LETTERS[self.index]
        self.letter_label.text = f"{letter}{letter.lower()}"
        self.word_label.text = f"{letter} is for {WORDS[letter]}"
        self.bg_color.rgba = get_color_from_hex(BG_COLORS[self.index % len(BG_COLORS)])
        self.status_label.text = ""
        if self.sound:
            self.sound.stop()

    def next_letter(self, *args):
        self.index = (self.index + 1) % len(LETTERS)
        self.show_letter()

    def previous_letter(self, *args):
        self.index = (self.index - 1) % len(LETTERS)
        self.show_letter()

    def play_sound(self, *args):
        """Plays assets/audio/<letter>.wav (e.g. a.wav) if it exists.
        Otherwise shows a placeholder message so the app never crashes."""
        letter = LETTERS[self.index].lower()
        for ext in ("wav", "ogg", "mp3"):
            path = os.path.join(AUDIO_DIR, f"{letter}.{ext}")
            if os.path.exists(path):
                self.sound = SoundLoader.load(path)
                if self.sound:
                    self.sound.play()
                    self.status_label.text = ""
                    return
        self.status_label.text = f"(Audio placeholder: add assets/audio/{letter}.wav)"


class ABCBookApp(App):
    title = "ABC Book"

    def build(self):
        return ABCBook()


if __name__ == "__main__":
    ABCBookApp().run()
