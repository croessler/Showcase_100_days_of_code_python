""" 
=== 100 Days of Code (Python): Coffee Machine (Day 15) ===

This module is to emulate a Coffee Machine as a coding exercise.
It has two special features, appart from the basic requirements:
1.) The "UI" updates according to the current situation instead of 
    just having a rolling output.
2.) The code is flexible so that a new entry in the recipe-dictionary 
    (recipes.py) makes the new option directly available and the 
    programm can deal with the change without code changes.
"""

from sys import exit as sysexit
from time import sleep
from os import system
from art import LOGO
from recipes import beverages as BEVERAGES

### Functions

def clear():
    """ Clear Terminal Output """
    system('clear')

def get_screen(l_situation="start",l_choice=None):
    """Provides UI for the respective situation"""
    clear()
    print(LOGO)

    if l_situation == "start":
        l_choice = 0
        print("What would you like?")
        for i,beverage in enumerate(BEVERAGES):
            print(f"{i+1}) {beverage['Name']} (${beverage['Price']})")
        l_choice = input("Please enter the number of your choice: ")
        return evaluate_input(l_situation,l_choice)
    elif l_situation == "report":
        generate_report()
        input("Press any key to return to the main menue.")
        return "start",None
    elif l_situation == "beverage":
        # to maintain the input information in l_choice, i use a separate variable, beverage_nr,
        # to access the respective information in the data. They are always one appart.
        beverage_nr = int(l_choice)-1
        print(f"{BEVERAGES[beverage_nr]['Name']} selected")
        if check_ressources(beverage_nr):
            return "payment", l_choice
        else:
            return "start", None
    elif l_situation == "payment":
        drink = BEVERAGES[int(l_choice)-1]
        print(f"That would be ${drink['Price']}, please.")
        inserted_quarters = int(input("Please insert quaters: "))
        inserted_dimes = int(input("Please insert dimes: "))
        inserted_nickles = int(input("Please insert nickles: "))
        inserted_pennies = int(input("Please insert pennies: "))
        if process_coins(inserted_quarters, inserted_dimes, inserted_nickles,
                          inserted_pennies, drink['Price']):
            return "prepare_drink", l_choice
        else:
            print("Sorry, that is not enough money. Please try again!")
            return "start", None
    elif l_situation == "prepare_drink":
        brew_beverage(l_choice)
        return "start", None


def evaluate_input(l_situation, l_choice):
    """Evaluate input in the UI"""
    if l_situation == "start":
        if l_choice == "off":
            print("Shutting down...")
            sysexit()
        elif l_choice == "report":
            l_situation = "report"
            return l_situation,None
        elif l_choice in BEVERAGE_NR_LIST:
            return "beverage", l_choice
        else:
            print(f"Error during evaluation of situation {l_situation} and choice {l_choice}!")
            exit()

def generate_report():
    """Generates report of ressorces"""
    print("Report of ressources:")
    print(f"Water: {AVAILABLE_WATER}ml")
    print(f"Milk: {AVAILABLE_MILK}ml")
    print(f"Coffee: {AVAILABLE_COFFEE}g")
    print(f"Money: ${CASHREGISTER}")

def check_ressources(selection):
    """Checks for required  ressources"""
    drink = BEVERAGES[selection]
    if drink['Water'] > AVAILABLE_WATER:
        print(f"Not enough water for {drink['Name']}!")
        input("Press any key to return to the main menue.")
        return False
    elif drink['Coffee'] > AVAILABLE_COFFEE:
        print(f"Not enough coffee for {drink['Name']}!")
        input("Press any key to return to the main menue.")
        return False
    elif drink['Milk'] > AVAILABLE_MILK:
        print(f"Not enough milk for {drink['Name']}!")
        input("Press any key to return to the main menue.")
        return False
    else:
        return True


def process_coins(inserted_quarters, inserted_dimes, inserted_nickles,
                   inserted_pennies, drink_price):
    """Processes different amount of coins and sums them up"""
    l_total = ((inserted_quarters *0.25)
               + (inserted_dimes * 0.10)
               + (inserted_nickles * 0.05)
               + (inserted_pennies * 0.01))
    global CASHREGISTER
    if l_total >= drink_price:
        if l_total != drink_price:
            print(f"\nHere is your change: ${round(l_total-drink_price,2)}.")
            input("Press any key to start brewing.")
        CASHREGISTER += drink_price
        return True
    else:
        return False


def brew_beverage(l_choice):
    """Emulates brewing and consuming ressources"""
    drink = BEVERAGES[int(l_choice)-1]
    print(f"Preparing your {drink['Name']}. Please wait ...")
    sleep(3)
    # reduce ressources
    global AVAILABLE_WATER
    global AVAILABLE_MILK
    global AVAILABLE_COFFEE
    AVAILABLE_WATER -= drink['Water']
    AVAILABLE_MILK -= drink['Milk']
    AVAILABLE_COFFEE -= drink['Coffee']
    print()
    print(f"Here is your {drink['Name']} ☕. Enjoy!")
    input("Press any key to return to the main menue.")


### Variables and Parameters
AVAILABLE_WATER = 300
AVAILABLE_MILK = 200
AVAILABLE_COFFEE = 100
CASHREGISTER = 0

BEVERAGE_NR_LIST = [] # make a list of strings that are allowed input options for beverages
for i,beverage in enumerate(BEVERAGES):
    BEVERAGE_NR_LIST.append(str(i+1))

SITUATION = "start"
CHOICE = None

### Body
while True:
    SITUATION, CHOICE = get_screen(SITUATION,CHOICE)
