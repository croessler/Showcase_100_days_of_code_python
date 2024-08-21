"""
This is a "flash card" implementation in Python.
Flash card is a system to learn vocabulary with (virtual) learning
cards which are shown in succession. For each card, the "foreign" 
language side is shown and after some seconds, the card is flipped
to its backside, showing the same word in the "familiar" language. 
Additionally, there is a ❌ and ✅ button to indicate whether the 
word was known or not. Known words are removed from the deck, 
unknown words are put back and will reappear again.

This is part of Angela Yu's Udemy course "100 Days of Code" (Day 31)
Since working it out is a challenge, the code differs from the
solution presented in the course. The main feature is probably, that
this is a VIETNAMESE version (vietnamese-english). Like the original
French vocabulary list, this list is based on the lists compiled by 
hermitdave, who extracted the words from Open Subtitles for various
languages, counted the word frequency and listed them accordingly. 
The english translation was done with Google Translate in August 2024
(while the word list was compiled in 2018).
"""

# =========================== Imports ====================================
from tkinter import Tk,Canvas, PhotoImage, Button, messagebox
from random import choice
from os import path, chdir, remove
import csv
import pandas

# =========================== Set the PWD ================================
path_to_dir = path.dirname(__file__)
chdir(path_to_dir)

# =========================== Constants ==================================
BACKGROUND_COLOR = "#B1DDC6"
TEXT_LANGUAGE_POS_X = 400
TEXT_LANGUAGE_POS_Y = 150
TEXT_LANGUAGE_FONT = ("Ariel", 40, "italic")
TEXT_WORD_POS_X = 400
TEXT_WORD_POS_Y = 263
TEXT_WORD_FONT = ("Ariel", 60, "bold")
LANGUAGE_1 = "Vietnamese"
LANGUAGE_2 = "English"
LANGUAGE_SOURCE_FILE = "./data/vietnamese_words.csv"
FLIP_TIMER = None
ITEM = None

# =========================== Read in the vocabulary stack ===============

## if there is a "words_to_learn.csv", use it as data source. If not,
## use the complete stack in "french_words.csv".
DATA=pandas.DataFrame()
if path.exists("./data/words_to_learn.csv"):
    try:
        DATA=pandas.read_csv("./data/words_to_learn.csv")
    except pandas.errors.EmptyDataError:
        pass

if DATA.empty:
    DATA=pandas.read_csv(LANGUAGE_SOURCE_FILE)

DATA_DICT_LIST = DATA.to_dict(orient="records")

# =========================== Logic ======================================

def prepare_card():
    #print("prepare_card() called")
    if DATA_DICT_LIST:
        global ITEM
        ITEM = choice(DATA_DICT_LIST)
        CANVAS_1.itemconfigure(TEXT_WORD_1,text=ITEM[LANGUAGE_1])
        CANVAS_2.itemconfigure(TEXT_WORD_2,text=ITEM[LANGUAGE_2])
    else:
        messagebox.showinfo(title="List empty", message="There are no more vocabulary in the list.")
        remove("./data/words_to_learn.csv")
        exit()

def show_front():
    #print("show_front() called")
    CANVAS_2.grid_remove()
    CANVAS_1.grid(row=0, column=0, columnspan=2)

def show_back():
    #print("show_back() called")
    CANVAS_2.grid(row=0, column=0, columnspan=2)

def button_right_click():
    #print("button_right_click() called")
    WINDOW.after_cancel(FLIP_TIMER)
    ## Remove the word and update "words_to_learn.csv"
    global DATA_DICT_LIST
    DATA_DICT_LIST.remove(ITEM)
    with open("./data/words_to_learn.csv","w") as file:
        writer = csv.DictWriter(file, fieldnames=[LANGUAGE_1, LANGUAGE_2])
        writer.writeheader()
        for entry in DATA_DICT_LIST:
            writer.writerow(entry)
    ## Call run() for the next card
    run()

def button_wrong_click():
    #print("button_wrong_click() called")
    WINDOW.after_cancel(FLIP_TIMER)
    run()

def run():
    #print("run() called")
    prepare_card()
    show_front()
    global FLIP_TIMER
    FLIP_TIMER = WINDOW.after(3000,show_back)

# =========================== UI Setup ===================================
WINDOW = Tk()
WINDOW.title(f"Flash Card {LANGUAGE_1}-{LANGUAGE_2}")
WINDOW.config(padx=50, pady=50,bg=BACKGROUND_COLOR)

## Canvas for the front of the card (Language 1)
CANVAS_1 = Canvas(width=800,height=526, highlightthickness=0,
                bg=BACKGROUND_COLOR)
CARD_FRONT = PhotoImage(file="./images/card_front.png")
CANVAS_1.create_image(400,263, image=CARD_FRONT)
TEXT_LANGUAGE_1 = CANVAS_1.create_text(TEXT_LANGUAGE_POS_X, TEXT_LANGUAGE_POS_Y,
                                   text=LANGUAGE_1, font=TEXT_LANGUAGE_FONT, fill="black",
                                   justify="center")
TEXT_WORD_1 = CANVAS_1.create_text(TEXT_WORD_POS_X, TEXT_WORD_POS_Y, text="Word",
                   font=TEXT_WORD_FONT, fill="black", justify="center")

## Canvas for the back of the card (Language 2)
CANVAS_2 = Canvas(width=800,height=526, highlightthickness=0,
                bg=BACKGROUND_COLOR)
CARD_BACK = PhotoImage(file="./images/card_back.png")
CANVAS_2.create_image(400,263, image=CARD_BACK)
TEXT_LANGUAGE_2 = CANVAS_2.create_text(TEXT_LANGUAGE_POS_X, TEXT_LANGUAGE_POS_Y,
                                   text=LANGUAGE_2, font=TEXT_LANGUAGE_FONT, fill="white",
                                   justify="center")
TEXT_WORD_2 = CANVAS_2.create_text(TEXT_WORD_POS_X, TEXT_WORD_POS_Y, text="Word",
                   font=TEXT_WORD_FONT, fill="white", justify="center")

## Buttons
BUTIMG_RIGHT = PhotoImage(file="./images/right.png")
BUTTON_RIGHT = Button(image=BUTIMG_RIGHT, borderwidth=0, highlightthickness=0,
                      command=button_right_click)
BUTTON_RIGHT.grid(row=1, column=0)
BUTIMG_WRONG = PhotoImage(file="./images/wrong.png")
BUTTON_WRONG = Button(image=BUTIMG_WRONG, borderwidth=0, highlightthickness=0,
                      command=button_wrong_click)
BUTTON_WRONG.grid(row=1, column=1)

# =========================== Control ====================================
run()
WINDOW.mainloop()
