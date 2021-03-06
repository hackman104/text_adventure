# Need to figure out how to track which rooms border others

class Ship(object):
    def __init__(self, status, rooms):
        """
        status is a dictionary representing the status of key systems
        rooms is a list of rooms in the ship
        """
        self.status = status
        self.rooms = rooms

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

    def __str__(self):
        return self.status

class Room(object):
    def __init__(self, name, description, level, items, borders):
        """
        name is the name of the room
        description a string describing the room if the user enters 'look'
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