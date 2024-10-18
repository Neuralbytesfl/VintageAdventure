# parser.py

def parse_command(command, gui):
    command = command.lower()
    if command in ['quit', 'exit']:
        gui.display_message("Thank you for playing!")
        gui.root.quit()
    elif command in ['look', 'examine']:
        gui.look_around()
    elif command == 'inventory':
        gui.show_inventory()
    else:
        gui.display_message("I don't understand that command.")
