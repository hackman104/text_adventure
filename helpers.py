# Need to figure out how to track which rooms border others
# Hypersleep pods sealed until ship systems back online - robot not programmed to deactivate time lock
# Figure out how to have one item inside of another

room_info = {
    'Engineering':          [['Engine Room', 'Systems Hallway'], "This is the engineering room, where the Engineering Officer works.", 0, ["Desk", "Lamp"]],
    'Engine Room':          [['Engineering', 'Systems Hallway', 'Life Support'], "This is the engine room. The internally accessible parts of the drive array are here.", 0, ["Lever", "Partially Open Panel", "Plasma Cutter"]],
    'Life Support':         [['Engine Room', 'Systems Hallway'],  "The life support systems are managed and maintained in this room.", 0, ["Computer", "Clipboard", "Breaker"]],
    'Systems Hallway':      [['Engine Room', 'Engineering', 'Life Support', 'Ramp A'], "I am in the systems hallway. This connects the rooms on the lowest level of the ship.", 0, ["Doorways"]],
    'Ramp A':               [['Systems Hallway', 'Main Hallway'], "This is the ramp that connects the lowest level and the main level of the ship.", 1, ["Screwdriver"]],
    'Main Hallway':         [['Lavatory', 'Crew Quarters', 'Hypersleep Pods', 'Mess Hall', 'Medical Bay', 'Docking Bay', 'Security'], "This is the main hallway, which connects all of the rooms on the main level of the ship.", 1, ["Flashlight"]],
    'Lavatory':             [['Main Hallway', 'Hypersleep Pods'], "I am in the crew's lavatory. It is surprisingly messy.", 1, ["Toilet Paper", "Soap", "Toilet"]],
    'Hypersleep Pods':      [['Main Hallway', 'Lavatory', 'Crew Quarters'], "The hypersleep pods are in this room. The crew are all in their pods. The readouts all display warnings.", 1, ["Computer", "Hypersleep pods", "Portable Data Drive"]],
    'Crew Quarters':        [['Hypersleep Pods', 'Main Hallway'], "These are the crew quarters. There are several bunks and some foot lockers.", 1, ["Foot locker", "Multitool"]],
    'Mess Hall':            [['Main Hallway'], "I am in the mess hall. There are two tables and several chairs, with a small kitchen and pantry in the back.", 1, ["Pantry", "Cabinet", "Scissors", "Knife"]],
    'Medical Bay':          [['Main Hallway'], "This is the medical bay, where the ship medical officer treats illnesses and injuries.", 1, ["Table", "Bed", "Hypodermic Needle", "Notepad", "Computer"]],
    'Docking Bay':          [['Main Hallway', 'Security'], "This is the docking bay. It is currently locked down.", 1, ["Computer", "Bay Door", "Bay Door Control", "Data Cable"]],
    'Security':             [['Main Hallway', 'Docking Bay'], "This is the security office. It monitors the ship and the docking bay.", 1, ["Computer", "Shock Bolt Gun", "Tazer", "Cabinet"]],
    'Ramp B':               [['Main Hallway', 'Bridge'], "This is the ramp that connects the main and upper levels of the ship.", 1, []],
    'Bridge':               [['Ramp B', 'Communications', 'Navigation', 'Bridge Hallway'], "This is the bridge, the command center of the ship.", 2, []],
    'Communications':       [['Bridge'], "", 2, []],
    'Navigation':           [['Bridge'], "", 2, []],
    'Bridge Hallway':       [['Captain\'s Quarters', 'Bridge'], "", 2, []],
    'Captain\'s Quarters':  [['Bridge Hallway'], "", 2, []]
}

item_info = {

}

item_usability = {
    "lookable":     ["look"],
    "usable":       ["look", "use"],
    "takeable":     ["look", "take"],
    "openable":     ["look", "open"],
    "combinable":   ["look", "take", "combine"],
}

class Ship(object):
    def __init__(self, status, rooms):
        """
        status is a dictionary representing the status of key systems
        rooms is a list of rooms in the ship
        """
        self.status = status
        self.rooms = []
        for room in rooms:
            self.rooms.append(Room(room, room_info[room][1], room_info[room][2], room_info[room][3], room_info[room][0]))

    def get_status(self):
        """
        Gets the status of the ship and its core systems
        """
        return self.status

    def set_status(self, system, new_status):
        """
        updates the status of a ship system
        system: a string representing a key in self.status
        new_status: a string representing the updated status
        """
        if system in self.status.keys():
            self.status[system] = new_status
        else:
            print("Error: Specified System not Found.")

    def __str__(self):
        return str(self.status)

class Room(object):
    def __init__(self, name, description, level, items, borders):
        """
        name is the name of the room
        description a string describing the room if the user enters 'look'
        level is an int representing the floor of the room
        items a list of items available for interaction in the room
        borders is a list of rooms which border the current room
        """
        self.name = name
        self.description = description
        self.items = items
        self.level = level
        self.borders = borders

    def get_name(self):
        """
        Returns the room's name
        """
        return self.name

    def get_description(self):
        """
        Returns the room's description
        """
        return self.description

    def get_items(self):
        """
        Returns a list of the room's items
        """
        return self.items

    def display_items(self):
        if len(self.items) == 0:
            print("There are no items in this room.")
        elif len(self.items) == 2:
            print(f"Items in this room: {self.items[0]} and {self.items[1]}")
        else:
            print("Items in this room:", ", ".join(self.items))

    def take_item(self, item):
        """
        Removes the selected item from the room and returns it. To be used if a user picks it up.
        """
        if item in self.items:
            if item.check_interaction('take'):
                inv_item = self.items.pop(item)
                return inv_item
            else:
                print("I can't take that item. It is either too big or bolted down")
        else:
            print("Error: item not found in room.")

    def __str__(self):
        return self.description
    
    def check_border(self, room):
        """
        returns True if the rooms border one another, False if otherwise
        """
        if room in self.borders:
            return True
        else:
            return False

class Item(object):
    def __init__(self, name, description, interactions):
        """
        name is a string with the name of the item
        description is a detailed description of the object, to be used if the user looks at it.
        interactions is a list of valid commands for the object.
        """
        self.name = name
        self.description = description
        self.interactions = interactions

    def get_name(self):
        """
        returns the name of the item
        """
        return self.name

    def get_description(self):
        """
        returns a description of the item if the user looks at it
        """
        return self.description

    def check_interaction(self, action):
        """
        Checks whether the user command is in the item's list of valid actions.
        If it is, return true. If not, return False.
        """
        if action in self.interactions:
            return True
        else:
            return False

    def __str__(self):
        return self.description

class Robot(object):
    def __init__(self, ship, position, inventory):
        """
        ship is the robot's current ship
        position is a room in the ship
        inventory is a list of items
        """
        self.ship = ship
        self.position = position
        self.inventory = []

    def get_inventory(self):
        """
        returns the robot's current inventory
        """
        return self.inventory

    def add_item(self, item):
        """
        item is of class Item
        adds item to robot's inventory
        """
        self.inventory.append(item)

    def remove_item(self, item):
        """
        item is of class Item
        removes an item from robot's inventory, for example if it has been used
        """
        if item in self.inventory:
            self.inventory.remove(item)

    def get_position(self):
        """
        returns the robot's current position
        """
        return self.position

    def change_position(self, new_room):
        """
        moves robot to a new room
        """
        if self.position.check_border(new_room):
            self.position = new_room
        else:
            print("You can't travel there from here.")

    def __str__(self):
        return f"You are in the {self.position.name} on level {self.position.level}."

    def look(self, item=None):
        if item:
            print(item)
        else:
            print(self.__str__())
            print(self.position.description)