import time
import sys
import random
from helpers import Ship, Room, Item
from colorama import init

commands = ['look', 'open', 'close', 'take', 'use', 'combine', 'exit', 'quit']
inventory = []
error_responses = ['Does not compute', 'Error parsing command, please try again', 'Command not understood, please try again']
intro_status = {'Drive System': 'Inactive', 'Life Support': 'Failing', 'Navigation': 'Offline', 'Security Status': 'Lockdown'}
ship_rooms = ['Bridge', 'Crew Quarters', 'Medical Bay', 'Main Hallway', 'Engine Room', 'Engineering', 'Security', 'Lavatory', "Captain's Quarters", "Mess Hall"]

def main():
    playing = True
    atalanta = Ship(intro_status, ship_rooms)
    skip_intro = check_if_played()
    print()
    display_text("texts/intro.txt", skip_intro)
    time.sleep(1)
    display_text("texts/start.txt")
    time.sleep(1)
    robot_intro()
    time.sleep(1)
    while playing:
        playing = get_user_input()

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
        time.sleep(0.03)

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

def get_user_input():
    """
    Prompt the user for input, split it into its elements, and check to see if the command is valid.
    If the user asks for help, provide a list of valid commands.
    If the user enters an ostensibly valid command, pass it to the try_command function.
    If the user input begins with an invalid command, return an error.
    Returns True unless the user enters 'quit' or 'exit.'
    """
    status = True
    user_input = input("Please enter your command: ")
    user_input = user_input.lower()

    args = user_input.split()

    if args[0] == 'help':
        print('My available commands are: ', end='')
        comm_str = ", ".join(commands)
        print(comm_str)
    elif args[0] in commands:
        status = try_command(args)
    else:
        print(error_responses[random.randrange(len(error_responses))])

    return status

def try_command(command):
    """
    Parses the user command to see if the action is valid. For example, 'open cabinet' would be valid,
    But 'open chair' would not be.
    If the user enters 'exit' or 'quit,' prompts them to confirm. If so, returns False, otherwise, returns True.
    """
    status = True
    if command[0] == 'exit' or command[0] == 'quit':
        while True:
            ans = input('Are you sure you want to exit the game? (y/n) ').lower()
            if ans in ['y', 'yes', 'n', 'no']:
                break
            else:
                print('Please provide a valid yes or no response.')
        if ans == 'y' or ans == 'yes':
            status = False
    
    return status
        

if __name__ == "__main__":
    main()