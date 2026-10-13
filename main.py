#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
from PIL import Image, ImageOps, ImageEnhance
import numpy as np

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.slider import Slider
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.togglebutton import ToggleButton
from kivy.clock import Clock
from kivy.core.window import Window

# ============================================================
INPUT_DIR = "/storage/emulated/0/Download/neg"
# ============================================================


def apply_mask(img, strength, r_adj, g_adj, b_adj):
    if strength <= 0.01 or img.mode != "RGB":
        return img
    arr = np.array(img).astype(np.float32)
    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
    r_new = r + (r_adj * strength)
    g_new = g + (g_adj * strength)
    b_new = b + (b_adj * strength)
    arr[:, :, 0] = np.clip(r_new, 0, 255)
    arr[:, :, 1] = np.clip(g_new, 0, 255)
    arr[:, :, 2] = np.clip(b_new, 0, 255)
    return Image.fromarray(arr.astype(np.uint8))


def build_lut_gamma(gamma):
    inv_gamma = 1.0 / max(gamma, 0.1)
    lut = np.array([((i / 255.0) ** inv_gamma) * 255 for i in range(256)])
    return np.clip(lut, 0, 255).astype(np.uint8)


def apply_adjustments(img, gamma, contrast, brightness, warmth):
    if img.mode != "RGB":
        img = img.convert("RGB")

    if abs(gamma - 1.0) > 0.01:
        lut = build_lut_gamma(gamma)
        bands = [b.point(lut) for b in img.split()]
        img = Image.merge("RGB", bands)

    if abs(contrast) > 0.01:
        img = ImageEnhance.Contrast(img).enhance(1.0 + contrast)

    if abs(brightness) > 0.1:
        factor = 1.0 + (brightness / 50.0)
        img = ImageEnhance.Brightness(img).enhance(factor)

    if abs(warmth) > 0.01:
        arr = np.array(img).astype(np.float32)
        arr[:, :, 0] = np.clip(arr[:, :, 0] + (warmth * 25), 0, 255)
        arr[:, :, 2] = np.clip(arr[:, :, 2] - (warmth * 25), 0, 255)
        img = Image.fromarray(arr.astype(np.uint8))

    return img


class MaskTestApp(App):
    def build(self):
        self.mask_on = False
        self.mask = 1.0
        self.r_adj = -35.0
        self.g_adj = 4.0
        self.b_adj = -6.0

        self.invert_on = False
        self.gamma = 1.4
        self.contrast = 0.3
        self.brightness = 0.0
        self.warmth = 0.4

        root = BoxLayout(orientation='vertical', padding=16, spacing=14)

        root.add_widget(Label(
            text="Maska + Odwracanie kolorow",
            size_hint_y=None, height=40, font_size='18sp', halign='center'
        ))

        self.btn_mask = ToggleButton(
            text="Maska: WYLACZONA",
            size_hint_y=None, height=48, font_size='15sp',
            background_color=(0.5, 0.2, 0.2, 1)
        )
        self.btn_mask.bind(on_press=self.toggle_mask)
        root.add_widget(self.btn_mask)

        self.btn_invert = ToggleButton(
            text="Odwracanie: WYLACZONE",
            size_hint_y=None, height=48, font_size='15sp',
            background_color=(0.5, 0.2, 0.2, 1)
        )
        self.btn_invert.bind(on_press=self.toggle_invert)
        root.add_widget(self.btn_invert)

        self.labels = {}
        self.sliders = {}

        def add_slider(name, min_val, max_val, default, step=0.01):
            box = BoxLayout(orientation='vertical', size_hint_y=None, height=72, spacing=2)

            label = Label(
                text=f"{name}: {default:.1f}",
                size_hint_y=None,
                height=22,
                font_size='10sp',
                halign='left',
                valign='middle'
            )
            label.bind(size=label.setter('text_size'))

            self.labels[name] = label
            box.add_widget(label)

            slider = Slider(min=min_val, max=max_val, value=default, step=step,
                            size_hint_y=None, height=34)
            slider.bind(value=lambda inst, val: self.on_slider(name, val))
            self.sliders[name] = slider
            box.add_widget(slider)

            root.add_widget(box)

        root.add_widget(Label(text="— Maska RGB —", size_hint_y=None, height=26, font_size='10sp'))
        add_slider("Sila maski", 0.0, 2.5, self.mask)
        add_slider("Maska R", -80, 10, self.r_adj, step=0.5)
        add_slider("Maska G", -40, 40, self.g_adj, step=0.5)
        add_slider("Maska B", -40, 40, self.b_adj, step=0.5)

        root.add_widget(Label(text="— Po odwracaniu —", size_hint_y=None, height=26, font_size='13sp'))
        add_slider("Gamma", 0.5, 2.0, self.gamma)
        add_slider("Contrast", -0.5, 1.0, self.contrast)
        add_slider("Brightness", -30, 30, self.brightness, step=0.1)
        add_slider("Warmth", -1.0, 1.0, self.warmth)

        self.update_sliders_state()

        self.btn_run = Button(
            text="Przetworz zdjecia",
            size_hint_y=None, height=54, font_size='16sp',
            background_color=(0.15, 0.55, 0.3, 1)
        )
        self.btn_run.bind(on_press=self.start_process)
        root.add_widget(self.btn_run)

        self.log_label = Label(text="", size_hint_y=1, font_size='12sp',
                               halign='left', valign='top')
        self.log_label.bind(size=self.log_label.setter('text_size'))
        scroll = ScrollView()
        scroll.add_widget(self.log_label)
        root.add_widget(scroll)

        return root

    def toggle_mask(self, instance):
        self.mask_on = not self.mask_on
        if self.mask_on:
            self.btn_mask.text = "Maska: WLACZONA"
            self.btn_mask.background_color = (0.15, 0.55, 0.25, 1)
            self.log("Maska WLACZONA")
        else:
            self.btn_mask.text = "Maska: WYLACZONA"
            self.btn_mask.background_color = (0.5, 0.2, 0.2, 1)
            self.log("Maska WYLACZONA")
        self.update_sliders_state()

    def toggle_invert(self, instance):
        self.invert_on = not self.invert_on
        if self.invert_on:
            self.btn_invert.text = "Odwracanie: WLACZONE"
            self.btn_invert.background_color = (0.15, 0.55, 0.25, 1)
            self.log("Odwracanie WLACZONE")
        else:
            self.btn_invert.text = "Odwracanie: WYLACZONE"
            self.btn_invert.background_color = (0.5, 0.2, 0.2, 1)
            self.log("Odwracanie WYLACZONE")
        self.update_sliders_state()

    def update_sliders_state(self):
        for name in ["Sila maski", "Maska R", "Maska G", "Maska B"]:
            self.sliders[name].disabled = not self.mask_on
        for name in ["Gamma", "Contrast", "Brightness", "Warmth"]:
            self.sliders[name].disabled = not self.invert_on

    def on_slider(self, name, value):
        if name == "Sila maski":
            self.mask = value
        elif name == "Maska R":
            self.r_adj = value
        elif name == "Maska G":
            self.g_adj = value
        elif name == "Maska B":
            self.b_adj = value
        elif name == "Gamma":
            self.gamma = value
        elif name == "Contrast":
            self.contrast = value
        elif name == "Brightness":
            self.brightness = value
        elif name == "Warmth":
            self.warmth = value
        self.labels[name].text = f"{name}: {value:.1f}"

    def log(self, text):
        self.log_label.text += text + "\n"

    def clear_log(self):
        self.log_label.text = ""

    def start_process(self, instance):
        self.btn_run.disabled = True
        self.clear_log()                          # <-- czyszczenie tablicy wynikow
        self.log("Przetwarzam...\n")
        Clock.schedule_once(lambda dt: self.prepare_files(), 0.05)

    def prepare_files(self):
        input_path = Path(INPUT_DIR)
        if not input_path.exists():
            self.log(f"Brak katalogu:\n{INPUT_DIR}")
            self.btn_run.disabled = False
            return

        self.output_path = input_path / "pozytyw"
        self.output_path.mkdir(exist_ok=True)

        self.files = list(input_path.glob("*.jpg")) + list(input_path.glob("*.jpeg")) \
                     + list(input_path.glob("*.JPG")) + list(input_path.glob("*.JPEG"))

        if not self.files:
            self.log("Brak plikow JPG")
            self.btn_run.disabled = False
            return

        stan_mask = "WLACZONA" if self.mask_on else "WYLACZONA"
        stan_inv = "WLACZONE" if self.invert_on else "WYLACZONE"
        self.log(f"Znaleziono {len(self.files)} plikow")
        self.log(f"Maska: {stan_mask} | Odwracanie: {stan_inv}\n")

        self.current_index = 0
        self.total = len(self.files)
        Clock.schedule_once(lambda dt: self.process_next(), 0.05)

    def process_next(self):
        if self.current_index >= self.total:
            self.log(f"\nGotowe! ({self.total}/{self.total})")
            self.log("Wyniki w katalogu 'pozytyw'")
            self.btn_run.disabled = False
            return

        i = self.current_index
        file = self.files[i]
        nr = i + 1

        try:
            self.log(f"[{nr}/{self.total}] {file.name} ...")
            with Image.open(file) as img:
                if img.mode != "RGB":
                    img = img.convert("RGB")

                if self.mask_on:
                    img = apply_mask(img, self.mask, self.r_adj, self.g_adj, self.b_adj)

                if self.invert_on:
                    img = ImageOps.invert(img)
                    img = apply_adjustments(
                        img, self.gamma, self.contrast,
                        self.brightness, self.warmth
                    )

                img.save(self.output_path / file.name, quality=95)
            self.log(f"   OK  ({nr}/{self.total})")
        except Exception as e:
            self.log(f"   Blad: {e}")

        self.current_index += 1
        # nastepny plik – UI zdaza sie odswiezyc
        Clock.schedule_once(lambda dt: self.process_next(), 0.05)


if __name__ == "__main__":
    Window.clearcolor = (0.12, 0.12, 0.14, 1)
    MaskTestApp().run()