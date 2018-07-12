import time
import sys
from pathlib import Path

def main():
    skip_intro = check_if_played()
    print()
    display_text("texts/intro.txt", skip_intro)
    time.sleep(1)
    display_text("texts/start.txt")
    time.sleep(1)
    robot_intro()

def check_if_played():
    """
    Checks to see if key file resources/played.txt exists. If it does, returns True to indicate game has been played before.
    Otherwise it creates the file and returns False.
    """
    skip = False
    
    try:
        with open("resources/played.txt", "r") as check:
            while True:
                ans = input("It appears you've played the game before. Would you like to skip the intro? (y/n) ")
                if ans.lower() in ['y', 'n', 'yes', 'no']:
                    break
                else:
                    print("Please provide a valid answer.")
                    print()
            if ans == 'y' or ans == 'yes':
                skip = True
    except FileNotFoundError:
        with open("resources/played.txt", "w") as check:
            check.write('played\n')

    return skip

def slow_print(text):
    """
    Takes one paramater - text - which should be a string. Prints the strong one character at a time.
    """
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.02)

def display_text(file_name, skip=False):
    """
    file_name: required parameter representing the file to be read and displayed
    skip: optional parameter that defaults to False. If true, the file will not be displayed
    """
    if not skip:
        try:
            with open(file_name, "r") as f:
                text = f.read()
                slow_print(text)
        except FileNotFoundError:
            exit(1)

def robot_intro():
    """
    Provides the introduction to the robot the player will be using to explore the ship
    """
    print('\x1b[6;30;42m' + 'Welcome to the service interface for the Rapid Deploymenet Mobile Assistance Robot' + '\x1b[0m')
    print()
    time.sleep(0.5)
    print('\x1b[0;30;41m' + 'WARNING' + '\x1b[0m', end="")
    time.sleep(0.5)
    slow_print(' Deployment incomplete. Functionality and command interface limited. Please contact Engineering Officer for assistance')
    print()
    print()
    slow_print('Entering safe mode...')
    time.sleep(1)
    print()
    slow_print('Only basic commands will be understood. Type "help" for a list of commands.')
    print()
    print()

if __name__ == "__main__":
    main()