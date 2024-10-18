# game.py

class GameState:
    def __init__(self, rooms, items, puzzles):
        self.rooms = rooms
        self.items = items
        self.puzzles = puzzles
        self.current_room = 'entrance'
        self.inventory = []
        self.visited_rooms = set()
        self.game_flags = {}
        self.initial_rooms = {k: v.copy() for k, v in rooms.items()}
        self.initial_items = {k: v.copy() for k, v in items.items()}
        self.initial_puzzles = {k: v.copy() for k, v in puzzles.items()}

    def reset(self):
        # Reset the game state to the initial state
        self.rooms = {k: v.copy() for k, v in self.initial_rooms.items()}
        self.items = {k: v.copy() for k, v in self.initial_items.items()}
        self.puzzles = {k: v.copy() for k, v in self.initial_puzzles.items()}
        self.current_room = 'entrance'
        self.inventory = []
        self.visited_rooms = set()
        self.game_flags = {}

    def move(self, direction):
        room = self.rooms[self.current_room]
        if direction in room['exits']:
            next_room = room['exits'][direction]
            self.current_room = next_room
            self.visited_rooms.add(next_room)
            return True, self.look()
        else:
            return False, "You can't go that way."

    def take_item(self, item_name):
        room = self.rooms[self.current_room]
        item_id = self.get_item_id_by_name(item_name, room['items'])
        if item_id:
            self.inventory.append(item_id)
            room['items'].remove(item_id)
            return True, f"You have taken the {item_name}."
        else:
            return False, f"There is no {item_name} here."

    def take_item_by_id(self, item_id):
        item_name = self.items[item_id]['name']
        return self.take_item(item_name)

    def use_item(self, item_name):
        item_id = self.get_item_id_by_name(item_name, self.inventory)
        if item_id:
            # Implement item usage logic here
            return True, f"You used the {item_name}."
        else:
            return False, f"You don't have a {item_name}."

    def get_item_id_by_name(self, item_name, item_list):
        # Helper method to get item ID by name from a list of item IDs
        for item_id in item_list:
            if self.items[item_id]['name'].lower() == item_name.lower():
                return item_id
        return None

    def look(self):
        room = self.rooms[self.current_room]
        description = room['description']
        if room['items']:
            item_names = [self.items[item]['name'] for item in room['items']]
            description += "\nYou see: " + ', '.join(item_names)
        return description

    def get_inventory(self):
        if self.inventory:
            item_descriptions = [self.items[item]['name'] for item in self.inventory]
            return item_descriptions
        else:
            return []

    def examine_item(self, item_name):
        item_id = self.get_item_id_by_name(item_name, self.inventory)
        if item_id:
            item = self.items[item_id]
            return True, f"{item['name']}: {item['description']}"
        else:
            return False, f"You don't have a {item_name}."
