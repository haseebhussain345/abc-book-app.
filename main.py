"""ABC Kids: a gentle alphabet book for young children.

* Big, clear letters with a picture and a word for every letter
* A friendly voice (the phone's own text-to-speech) says each letter
* Day and night colours, no flashing, no ads, no accounts
* Colour-blind friendly: meaning is shown with words and shapes, not colour alone
"""

import os

from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import Color, Ellipse, RoundedRectangle
from kivy.metrics import dp, sp
from kivy.storage.jsonstore import JsonStore
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.widget import Widget

from letters import LETTERS, speech_text
from theme import get_theme, hex_to_rgba

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(BASE_DIR, "assets", "fonts", "ComicRelief-Bold.ttf")
PICS_DIR = os.path.join(BASE_DIR, "assets", "pics")

try:
    from jnius import PythonJavaClass, autoclass, java_method

    class _InitListener(PythonJavaClass):
        __javainterfaces__ = ["android/speech/tts/TextToSpeech$OnInitListener"]
        __javacontext__ = "app"

        def __init__(self, callback):
            super().__init__()
            self.callback = callback

        @java_method("(I)V")
        def onInit(self, status):
            self.callback(status)

    ON_ANDROID = True
except Exception:  # running on a computer, not on Android
    ON_ANDROID = False


class VoiceBox:
    """Speaks with Android's built-in text-to-speech. Never crashes the app."""

    def __init__(self):
        self.ready = False
        self.failed = not ON_ANDROID
        self.tts = None
        self._listener = None
        if not ON_ANDROID:
            return
        try:
            activity = autoclass("org.kivy.android.PythonActivity").mActivity
            tts_class = autoclass("android.speech.tts.TextToSpeech")
            self._listener = _InitListener(self._on_init)
            self.tts = tts_class(activity, self._listener)
        except Exception:
            self.failed = True

    def _on_init(self, status):
        try:
            tts_class = autoclass("android.speech.tts.TextToSpeech")
            if status != tts_class.SUCCESS:
                self.failed = True
                return
            locale = autoclass("java.util.Locale")
            self.tts.setLanguage(locale.US)
            self.tts.setSpeechRate(0.8)
            self.ready = True
        except Exception:
            self.failed = True

    def speak(self, text):
        """Returns 'ok', 'loading' or 'unavailable'."""
        if self.failed:
            return "unavailable"
        if not self.ready:
            return "loading"
        try:
            tts_class = autoclass("android.speech.tts.TextToSpeech")
            self.tts.speak(text, tts_class.QUEUE_FLUSH, None, "abc-kids")
            return "ok"
        except Exception:
            self.failed = True
            return "unavailable"


class Card(BoxLayout):
    """A rounded, coloured panel."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            self._bg_color = Color(1, 1, 1, 1)
            self._bg = RoundedRectangle(
                pos=self.pos, size=self.size,
                radius=[dp(28), dp(28), dp(28), dp(28)],
            )
        self.bind(pos=self._sync, size=self._sync)

    def set_bg(self, hex_value):
        self._bg_color.rgba = hex_to_rgba(hex_value)

    def _sync(self, *_):
        self._bg.pos = self.pos
        self._bg.size = self.size


class ProgressDots(Widget):
    """One dot per letter. The current letter is a larger dot, so progress
    is shown by shape and size, not by colour alone."""

    def __init__(self, total, **kwargs):
        self.total = total
        self.current = 0
        self.fill_hex = "#000000"
        self.dim_hex = "#000000"
        super().__init__(**kwargs)
        self.bind(pos=self.redraw, size=self.redraw)

    def set_state(self, current, fill_hex, dim_hex):
        self.current = current
        self.fill_hex = fill_hex
        self.dim_hex = dim_hex
        self.redraw()

    def redraw(self, *_):
        self.canvas.clear()
        if not self.total or self.width <= 0:
            return
        step = min(dp(14), self.width / self.total)
        x0 = self.center_x - step * self.total / 2 + step / 2
        y = self.center_y
        with self.canvas:
            for i in range(self.total):
                cx = x0 + i * step
                if i == self.current:
                    Color(*hex_to_rgba(self.fill_hex))
                    r = dp(7)
                else:
                    Color(*hex_to_rgba(self.dim_hex))
                    r = dp(3.5)
                Ellipse(pos=(cx - r, y - r), size=(2 * r, 2 * r))


def make_button(text, font_size):
    btn = Button(
        text=text,
        font_name=FONT,
        font_size=sp(font_size),
        background_normal="",
        background_down="",
        background_color=(1, 1, 1, 1),
        color=(0, 0, 0, 1),
    )
    # Gentle press feedback: the button dims a little while touched.
    btn.bind(state=lambda b, s: setattr(b, "opacity", 0.75 if s == "down" else 1.0))
    return btn


def style_button(btn, bg_hex, fg_hex):
    btn.background_color = hex_to_rgba(bg_hex)
    btn.color = hex_to_rgba(fg_hex)


def wrap_text(label, size):
    label.text_size = size


class ABCKidsRoot(BoxLayout):
    def __init__(self, voice, store, **kwargs):
        super().__init__(orientation="vertical", padding=dp(14), spacing=dp(10), **kwargs)
        self.voice = voice
        self.store = store
        self.index = 0
        self.theme_name = self._load_theme()
        self.t = get_theme(self.theme_name)

        # Top bar: title and day/night switch
        top = BoxLayout(size_hint_y=None, height=dp(56), spacing=dp(10))
        self.title = Label(
            text="ABC Kids", font_name=FONT, font_size=sp(28),
            halign="left", valign="middle", size_hint_x=0.5,
        )
        self.title.bind(size=wrap_text)
        self.theme_btn = make_button("", 18)
        self.theme_btn.size_hint_x = 0.5
        self.theme_btn.bind(on_release=self.toggle_theme)
        top.add_widget(self.title)
        top.add_widget(self.theme_btn)
        self.add_widget(top)

        # Progress: dots plus "3 of 26"
        progress = BoxLayout(size_hint_y=None, height=dp(30), spacing=dp(6))
        self.dots = ProgressDots(len(LETTERS), size_hint_x=0.74)
        self.count = Label(font_name=FONT, font_size=sp(16), size_hint_x=0.26)
        progress.add_widget(self.dots)
        progress.add_widget(self.count)
        self.add_widget(progress)

        # The big card: upper and lower case letter, then the picture
        self.card = Card(orientation="vertical", padding=dp(12), spacing=dp(6))
        letters_row = BoxLayout(size_hint_y=0.55, spacing=dp(4))
        self.upper = Label(font_name=FONT, font_size=sp(150))
        self.lower = Label(font_name=FONT, font_size=sp(120))
        letters_row.add_widget(self.upper)
        letters_row.add_widget(self.lower)
        self.picture = Image(allow_stretch=True, keep_ratio=True, size_hint_y=0.45)
        self.card.add_widget(letters_row)
        self.card.add_widget(self.picture)
        self.add_widget(self.card)

        # "A is for Apple"
        self.word = Label(
            font_name=FONT, font_size=sp(28), halign="center", valign="middle",
            size_hint_y=None, height=dp(52),
        )
        self.word.bind(size=wrap_text)
        self.add_widget(self.word)

        # Big Listen button, then Back and Next
        self.listen_btn = make_button("Listen", 30)
        self.listen_btn.size_hint_y = None
        self.listen_btn.height = dp(72)
        self.listen_btn.bind(on_release=self.listen)
        self.add_widget(self.listen_btn)

        nav = BoxLayout(size_hint_y=None, height=dp(72), spacing=dp(10))
        self.prev_btn = make_button("Back", 26)
        self.next_btn = make_button("Next", 26)
        self.prev_btn.bind(on_release=lambda *_: self.go(-1))
        self.next_btn.bind(on_release=lambda *_: self.go(1))
        nav.add_widget(self.prev_btn)
        nav.add_widget(self.next_btn)
        self.add_widget(nav)

        # Small status line (voice messages)
        self.status = Label(font_name=FONT, font_size=sp(16), size_hint_y=None, height=dp(26))
        self.add_widget(self.status)

        self.refresh()

    # ----- settings -------------------------------------------------
    def _load_theme(self):
        try:
            if self.store is not None and self.store.exists("settings"):
                name = self.store.get("settings").get("theme", "day")
                if name in ("day", "night"):
                    return name
        except Exception:
            pass
        return "day"

    def _save_theme(self):
        try:
            if self.store is not None:
                self.store.put("settings", theme=self.theme_name)
        except Exception:
            pass

    def toggle_theme(self, *_):
        self.theme_name = "night" if self.theme_name == "day" else "day"
        self.t = get_theme(self.theme_name)
        self._save_theme()
        self.refresh()

    # ----- letters --------------------------------------------------
    def go(self, step):
        self.index = (self.index + step) % len(LETTERS)
        self.refresh()

    def listen(self, *_):
        item = LETTERS[self.index]
        result = self.voice.speak(speech_text(item))
        if result == "unavailable":
            self.status.text = "Voice is not available on this device."
        elif result == "loading":
            self.status.text = "Getting the voice ready. Tap Listen again."
        else:
            self.status.text = ""

    def on_touch_down(self, touch):
        if self.card.collide_point(*touch.pos):
            touch.ud["swipe_from"] = touch.x
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        start = touch.ud.get("swipe_from")
        if start is not None:
            dx = touch.x - start
            if abs(dx) > dp(80):
                self.go(-1 if dx > 0 else 1)  # swipe right = back, left = next
                return True
        return super().on_touch_up(touch)

    def refresh(self):
        t = self.t
        item = LETTERS[self.index]
        text_hex = t["text"]

        Window.clearcolor = hex_to_rgba(t["bg"])
        for label in (self.title, self.count, self.word):
            label.color = hex_to_rgba(text_hex)
        self.upper.color = hex_to_rgba(text_hex)
        self.lower.color = hex_to_rgba(text_hex)
        self.status.color = hex_to_rgba(t["subtext"])

        self.upper.text = item["letter"]
        self.lower.text = item["lower"]
        self.word.text = "%s is for %s" % (item["letter"], item["word"])
        self.count.text = "%d of %d" % (self.index + 1, len(LETTERS))
        self.picture.source = os.path.join(PICS_DIR, item["pic"])
        self.card.set_bg(t["tints"][self.index % len(t["tints"])])
        self.dots.set_state(self.index, t["accent"], t["track"])

        style_button(self.theme_btn, t["soft_bg"], t["soft_text"])
        style_button(self.listen_btn, t["primary_bg"], t["primary_text"])
        style_button(self.prev_btn, t["soft_bg"], t["soft_text"])
        style_button(self.next_btn, t["soft_bg"], t["soft_text"])
        self.theme_btn.text = "Night mode" if self.theme_name == "day" else "Day mode"


class ABCKidsApp(App):
    title = "ABC Kids"

    def build(self):
        try:
            store = JsonStore(os.path.join(self.user_data_dir, "settings.json"))
        except Exception:
            store = None
        self.voice = VoiceBox()
        return ABCKidsRoot(self.voice, store)


if __name__ == "__main__":
    ABCKidsApp().run()
