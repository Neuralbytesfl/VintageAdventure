# main.py
import json
from gui import GameGUI
from game import GameState

def load_data():
    with open('data/rooms.json') as f:
        rooms = json.load(f)['rooms']
    with open('data/items.json') as f:
        items = json.load(f)['items']
    with open('data/puzzles.json') as f:
        puzzles = json.load(f)['puzzles']
    return rooms, items, puzzles

def main():
    # Load game data
    rooms, items, puzzles = load_data()

    # Initialize game state
    game_state = GameState(rooms, items, puzzles)

    # Start the GUI
    gui = GameGUI(game_state)
    gui.run()

if __name__ == '__main__':
    main()
