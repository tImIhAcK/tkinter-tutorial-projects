from tkinter import *
import tkinter as tk
import tkinter.font as font


class RoundedButton(tk.Canvas):
    def __init__(self, parent, border_radius, padding,
                 color="", text="", font_weight="bold", font_family="Helvetica", font_size=16, command=None):

        tk.Canvas.__init__(self, parent, borderwidth=0, relief="flat",
                           highlightthickness=0, bg=parent["bg"])

        self.color = color
        self.command = command
        self.id = None
        self.font_size = font_size
        self.font_family = font_family
        self.font_weight = font_weight
        self.font = font.Font(
            size=self.font_size, family=self.font_family, weight=self.font_weight)
        self.height = font_size+(2*padding)
        width = self.font.measure(text)+(4*padding)
        self.width = width if width >= 80 else 80

        if (
            border_radius > 0.5 * self.width
            or border_radius > 0.5 * self.height
        ):
            raise ValueError("Error: total border_radius must not "
                             "exceed width or height.")

        self.id = self._shape(border_radius)

        x0, y0, x1, y1 = self.bbox("all")
        self.width = (x1 - x0)
        self.height = (y1 - y0)

        self.configure(width=self.width, height=self.height)
        self.create_text(self.width / 2, self.height / 2, text=text,
                         fill='white', font=self.font)

        self.bind("<ButtonPress-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)

    def _on_press(self, event):
        self.configure(relief="sunken")

    def _on_release(self, event):
        self.configure(relief="raised")
        if self.command is not None:
            self.command()

    def _shape(self, border_radius):
        radius = 2 * border_radius
        self.create_arc((0, radius, radius, 0),
                        start=90, extent=90,
                        fill=self.color, outline=self.color)

        self.create_arc((self.width - radius, 0, self.width,
                         radius), start=0, extent=90,
                        fill=self.color, outline=self.color)

        self.create_arc((self.width, self.height - radius,
                         self.width - radius, self.height),
                        start=270, extent=90, fill=self.color,
                        outline=self.color)

        self.create_arc((0, self.height - radius, radius, self.height),
                        start=180, extent=90, fill=self.color,
                        outline=self.color)

        return self.create_polygon(
            (
                0, self.height - border_radius,
                0, border_radius, border_radius,
                0, self.width - border_radius, 0,
                self.width, border_radius, self.width,
                self.height - border_radius,
                self.width - border_radius,
                self.height, border_radius,
                self.height
            ),
            fill=self.color,
            outline=self.color)
