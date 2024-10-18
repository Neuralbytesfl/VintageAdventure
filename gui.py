# gui.py

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import random

class GameGUI:
    def __init__(self, game_state):
        self.game_state = game_state
        self.root = tk.Tk()
        self.root.title("Adventure Game")
        self.root.resizable(False, False)  # Disable window resizing

        # Apply modern theme
        style = ttk.Style()
        style.theme_use('clam')  # Use 'clam' theme for a modern look

        self.in_puzzle = False
        self.canvas_items = {}
        self.player = None
        self.create_widgets()
        self.create_menu()
        self.setup_bindings()
        self.display_message(self.game_state.look())

    def create_widgets(self):
        # Create Text Area for Messages
        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=60, height=10, state='disabled')
        self.text_area.pack(pady=5)

        # Create Canvas for Player Movement
        self.canvas = tk.Canvas(self.root, width=600, height=400, bg='lightgrey')
        self.canvas.pack()

        # Initialize Player Position
        self.player_size = 20
        self.player_pos = [300, 200]  # Starting at the center
        self.player = self.canvas.create_text(self.player_pos[0], self.player_pos[1], text='X', font=('Arial', 16), tags='player')

        # Items on the Canvas
        self.load_canvas_items()

        # Movement Buttons
        self.create_movement_buttons()

        # Action Buttons
        self.create_action_buttons()

    def create_menu(self):
        # Create Menu Bar
        menubar = tk.Menu(self.root)

        # File Menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New Game", command=self.new_game)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        # Help Menu
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)

        # Display the Menu
        self.root.config(menu=menubar)

    def setup_bindings(self):
        # Bind Keys for Movement
        self.root.bind('<Up>', lambda e: self.move_player('up'))
        self.root.bind('<Down>', lambda e: self.move_player('down'))
        self.root.bind('<Left>', lambda e: self.move_player('left'))
        self.root.bind('<Right>', lambda e: self.move_player('right'))

    def create_movement_buttons(self):
        movement_frame = ttk.Frame(self.root)
        movement_frame.pack(pady=5)
        directions = [('North', 'up'), ('South', 'down'), ('East', 'right'), ('West', 'left')]
        for text, dir in directions:
            btn = ttk.Button(movement_frame, text=text, command=lambda d=dir: self.move_player(d))
            btn.pack(side='left', padx=5)

    def create_action_buttons(self):
        action_frame = ttk.Frame(self.root)
        action_frame.pack(pady=5)
        actions = [('Inventory', self.show_inventory), ('Look', self.look_around), ('Help', self.show_help)]
        for (text, func) in actions:
            btn = ttk.Button(action_frame, text=text, command=func)
            btn.pack(side='left', padx=5)

    def load_canvas_items(self):
        # Clear existing items
        for item in self.canvas_items.values():
            self.canvas.delete(item)
        self.canvas_items.clear()

        # Use the canvas's set dimensions
        canvas_width = int(self.canvas['width'])
        canvas_height = int(self.canvas['height'])

        # Place items on the canvas based on the current room
        room = self.game_state.rooms[self.game_state.current_room]
        for item_id in room['items']:
            item_data = self.game_state.items[item_id]
            # Randomly place item on canvas
            x = random.randint(50, canvas_width - 50)
            y = random.randint(50, canvas_height - 50)
            item = self.canvas.create_text(x, y, text=item_data['name'][0], font=('Arial', 14), fill='blue', tags=('item', item_id))
            self.canvas_items[item_id] = item

    def move_player(self, direction):
        dx, dy = 0, 0
        step = 20
        if direction == 'up':
            dy = -step
        elif direction == 'down':
            dy = step
        elif direction == 'left':
            dx = -step
        elif direction == 'right':
            dx = step

        # Calculate new position
        new_x = self.player_pos[0] + dx
        new_y = self.player_pos[1] + dy

        # Check boundaries
        canvas_width = int(self.canvas['width'])
        canvas_height = int(self.canvas['height'])
        if 0 < new_x < canvas_width and 0 < new_y < canvas_height:
            # Update position
            self.canvas.move(self.player, dx, dy)
            self.player_pos = [new_x, new_y]
            self.check_for_item_collision()
        else:
            self.display_message("You can't go that way.")

    def check_for_item_collision(self):
        # Check if player collides with any items
        overlapping = self.canvas.find_overlapping(self.player_pos[0]-10, self.player_pos[1]-10, self.player_pos[0]+10, self.player_pos[1]+10)
        for item in overlapping:
            tags = self.canvas.gettags(item)
            if 'item' in tags:
                item_id = tags[1]
                self.take_item_by_id(item_id)
                # Remove item from canvas
                self.canvas.delete(item)
                del self.canvas_items[item_id]
                break

    def take_item_by_id(self, item_id):
        item_name = self.game_state.items[item_id]['name']
        success, message = self.game_state.take_item(item_name)
        self.display_message(message)

    def new_game(self):
        # Reset the game state
        self.game_state.reset()
        self.canvas.delete('all')
        self.player_pos = [300, 200]
        self.player = self.canvas.create_text(self.player_pos[0], self.player_pos[1], text='X', font=('Arial', 16), tags='player')
        self.load_canvas_items()
        self.display_message("New game started!")

    def show_about(self):
        messagebox.showinfo("About", "Adventure Game\nCreated by Your Name")

    def run(self):
        self.root.mainloop()

    def display_message(self, message):
        self.text_area.config(state='normal')
        self.text_area.insert(tk.END, message + '\n\n')
        self.text_area.config(state='disabled')
        self.text_area.see(tk.END)

    def look_around(self):
        description = self.game_state.look()
        self.display_message(description)

    def show_inventory(self):
        inventory = self.game_state.get_inventory()
        if inventory:
            item_list = ', '.join(inventory)
            self.display_message(f"You are carrying: {item_list}")
        else:
            self.display_message("Your inventory is empty.")

    def show_help(self):
        commands = [
            "Use the movement buttons to move around.",
            "Collect items by moving over them.",
            "Click 'Inventory' to see your items.",
            "Click 'Look' to examine your surroundings.",
            "Use the menu to start a new game or exit."
        ]
        help_message = "Game Instructions:\n" + '\n'.join(commands)
        self.display_message(help_message)
