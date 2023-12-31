#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 24 10:43:48 2023

@author: dcr

Code constructed from a dialog with ChatGPT 4.

Requirements:
    1. Python 3.x for running the script.
    2. Python packages tkinter and PIL installed.

Usage notes:
    1. Prepare a folder with PNG photos. Each photo should have a unique name.
    2. Currently the photo name is assumed to be of the form Last,First.png.
    3. Invoke the script either in the folder or by specifying the folder path
       as the first argument.
    4. Choose from 2 modes: flashcard (default) or 4-choice quiz (-q option).

Known issues:
    1. Sometimes the windows buttons don't work. Just restart to fix.
"""

import tkinter as tk
from PIL import Image, ImageTk
import os
import random
import sys


class FlashcardAppUpdated:
    def __init__(self, photo_folder, quiz_mode=False):
        self.photo_folder = photo_folder
        self.current_photo = None
        self.quiz_mode = quiz_mode
        self.correct_name = ""

        self.photo_paths = self.load_photo_paths()

        self.window = tk.Tk()
        self.window.title(
            "Student Name Learning App - Quiz Mode" if quiz_mode
            else "Student Name Learning App"
        )

        self.image_label = tk.Label(self.window)
        self.image_label.pack()

        self.buttons = []
        if self.quiz_mode:
            for _ in range(4):
                button = tk.Button(self.window, text="")
                button.pack()
                self.buttons.append(button)
            self.message_label = tk.Label(
                self.window, text="", font=("Helvetica", 16), fg="blue"
                )
            self.message_label.pack()
        else:
            self.name_label = tk.Label(
                self.window, text="", font=("Helvetica", 16)
                )
            self.name_label.pack()
            self.show_button = tk.Button(
                self.window, text="Show Name", command=self.show_name
                )
            self.show_button.pack()

        self.next_button = tk.Button(
            self.window, text="Next Photo", command=self.load_random_photo,
            state=tk.DISABLED
            )
        self.next_button.pack()

        self.load_random_photo()

    def load_photo_paths(self):
        if not os.path.isdir(self.photo_folder):
            print(f"Error: The specified folder '{self.photo_folder}' "
                  "does not exist.")
            sys.exit(1)
        photo_paths = [
            os.path.join(self.photo_folder, f)
            for f in os.listdir(self.photo_folder)
            if f.endswith('.png')
            ]
        if self.quiz_mode and len(photo_paths) < 4:
            print("Error: There are not enough PNG files in the folder "
                  "for quiz mode.")
            sys.exit(1)
        return photo_paths

    def load_random_photo(self):
        self.current_photo = random.choice(self.photo_paths)
        image = Image.open(self.current_photo)
        image.thumbnail((500, 500))
        photo = ImageTk.PhotoImage(image)

        self.image_label.config(image=photo)
        self.image_label.image = photo

        if self.quiz_mode:
            self.prepare_quiz_options()
            self.message_label.config(text="")
            for button in self.buttons:
                button.config(state=tk.NORMAL, fg="black")
        else:
            self.name_label.config(text="")
            self.next_button.config(state=tk.DISABLED)
            self.show_button.config(state=tk.NORMAL)

    def prepare_quiz_options(self):
        correct_name_parts = \
            os.path.basename(self.current_photo).split('.')[0].split(",")
        self.correct_name = f"{correct_name_parts[1]} {correct_name_parts[0]}"
        other_names = self.get_unique_names(3, self.correct_name)

        options = other_names + [self.correct_name]
        random.shuffle(options)

        for button, option in zip(self.buttons, options):
            button.config(
                text=option, state=tk.NORMAL,
                command=lambda opt=option: self.check_answer(opt)
                )

    def get_unique_names(self, count, exclude_name):
        unique_names = set()
        while len(unique_names) < count:
            random_photo = random.choice(self.photo_paths)
            name_parts = \
                os.path.basename(random_photo).split('.')[0].split(",")
            name = f"{name_parts[1]} {name_parts[0]}"
            if name != exclude_name:
                unique_names.add(name)
        return list(unique_names)

    def check_answer(self, selected_option):
        if selected_option == self.correct_name:
            self.message_label.config(text="Well done!", fg="green")
            for button in self.buttons:
                if button.cget("text") == selected_option:
                    button.config(fg="green")
                else:
                    button.config(state=tk.DISABLED)
            self.next_button.config(state=tk.NORMAL)
        else:
            self.message_label.config(text="Try again!", fg="red")
            for button in self.buttons:
                if button.cget("text") == selected_option:
                    button.config(state=tk.DISABLED, fg="gray")

    def show_name(self):
        name_parts = \
            os.path.basename(self.current_photo).split('.')[0].split(",")
        name = f"{name_parts[1]} {name_parts[0]}"
        self.name_label.config(text=name)
        self.next_button.config(state=tk.NORMAL)
        self.show_button.config(state=tk.DISABLED)

    def run(self):
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
        self.window.mainloop()

    def on_close(self):
        self.window.destroy()


def print_help():
    help_message = """
    Usage: python script_name.py [options]

    Options:
      -h, --help          Show this help message and exit.
      -q, --quiz          Enable quiz mode. Requires 4 photos minimum.
      [photo_folder_path] Specify the path to the photo folder. 
                          If not specified, defaults to the current directory.
    """
    print(help_message)


if __name__ == "__main__":
    help_flag = '-h' in sys.argv or '--help' in sys.argv
    quiz_mode = '-q' in sys.argv or '--quiz' in sys.argv

    args = [arg for arg in sys.argv[1:] if not arg.startswith('-')]

    if help_flag:
        print_help()
        sys.exit(0)

    photo_folder = args[0] if args else os.getcwd()

    app_updated = FlashcardAppUpdated(photo_folder, quiz_mode=quiz_mode)
    app_updated.run()
