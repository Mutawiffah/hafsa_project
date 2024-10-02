import random
# mansion rooms
#khadija
rooms = { 
    "Entrance hall": {
        "description": "Welcome! You have entered in the Entrance hall of the Game  . The flickering light casts shadow on the walls and you feel a sudden chill. To inform you that on the north side is Grand dining hall and to the south is our Library.",
        "exits": {"north": "Grand dining hall"},
        "items": ["candle"],
        "puzzle": {"find_hidden_passage": False},  
    },
    "Grand dining hall": {
        "description": "The Grand dining hall is dimly lit, with a long table set for a feast that never happened.The air is thick with silence and a locked door to the west to increase your curiosity.",
        "exits": {"south": "Entrance hall", "east": "library"},
        "items": ["strange_key"],
        "puzzle": {"door_locked": True, "find_key": False},
    },
    "library": {
        "description": "As you enter your foot in  the libraray you see Books are filled with dust, The library is dusty filled with old books,It feels like a hidden message lies here.",
        "exits": {"west": "Grand dining hall", "north": "attic","south":"basement"},
        "items": ["old_box","scroll"],
        "puzzle": {"find_hidden_passage": False,"open_scroll": False, "solve_riddle":False},
    },
    "basement": {
        "description": "You see! Basement  has deep silence. It feels very dark and a chill of fear everywhere as someone is watching you.Papers scattered on the floor.",
        "exits": {"east": "attic","north": "library"},
        "items": ["lock_picker"],
        "puzzle": {"picked_door_lock": False },
    },
    "attic": {
        "description": "The attic is a messy area filled with spiders and cobwebs The wooden floor creaks with every step and silenced is filled i the room and a strange glow from a sealed box.",
        "exits": {"south": "library", "west": "basement"},
        "items": ["silver_amulet"],
        "puzzle": {"find_amulet": False,"activate_seal":False},
    },
}
# hafsa
# Variables 
current_room = "Entrance hall"
inventory = []
time_left = 300  

# A flag for protection
protected = False
puzzle_solved = False

# Displays the current room and its items
def look():
    """ Displaying the current room's description and items. """
    room = rooms[current_room]
    print(f"{room['description']}")
    if room["items"]:
        print(f"You see: {', '.join(room['items'])}")
    else:
        print("There is nothing to show. Try again!!")

#khadija
# Moving between rooms
def move(direction):
    global current_room, time_left
    if direction in rooms[current_room]["exits"]:
        current_room = rooms[current_room]["exits"][direction]
        look()
        time_left -= 1  
        ghost_encounter()
        check_time()
    else:
        print("Sorry ! You are not allowed to go that way yet.")

# Pick up an item
def take(item):
    if item in rooms[current_room]["items"]:
        inventory.append(item)
        rooms[current_room]["items"].remove(item)
        print(f"The item you picked is :  {item}.") 
    else:
        print(f"The {item} you picked could not be found.")
#hafsa
# Drop an item
def drop(item):
    if item in inventory:
        inventory.remove(item)
        rooms[current_room]["items"].append(item)
        print(f"oh! You dropped the {item}.")      

    else:
        print(f"Sorry!You don't have the {item}.")

# Using an item in the current room
def use_item(item):
    global puzzle_solved
    global protected

    if item not in inventory:
        print(f"You don't have the {item}. You need to take it before using it.")
        return

    if item == "candle" and current_room == "Entrance hall":
        rooms[current_room]["puzzle"]["find_hidden_passage"] = True
        print("You lit the candle, and the walls in the halls begin to shift and reveal a hidden passage covered in spider webs!")
    
    elif item == "silver_amulet" and current_room== "attic":
        if rooms["attic"]["puzzle"]["find_amulet"]:
           protected = True
           rooms["attic"]["puzzle"]["activate_seal"] = True
           print("You feel protected with the silver amulet.")
           
        

    elif item == "strange_key" and current_room == "Grand dining hall":
       if rooms["Grand dining hall"]["puzzle"]["door_locked"]:
          rooms[current_room]["puzzle"]["find_key"] = True
          rooms["Grand dining hall"]["puzzle"]["door_locked"] = False
          print("You unlocked the door with the strange key! You see the library in front of you. Large shelf filled with dust covered books")
       else:
        print("The door is already unlocked.")

    
    elif item == "lock_picker" and current_room == "basement":
        if rooms["basement"]["puzzle"]["picked_door_lock"]:
            rooms["basement"]["puzzle"]["picked_door_lock"] = True
            print("You unlocked the door with the lock picker!. You can escape the mysterious castle alive now")
            puzzle_solved= True
               

    elif item == "old_box" and current_room == "library":
        rooms[current_room]["puzzle"]["open_box"] = True
        print("you open the old box to reveal a mystical scroll and you wonder what secrets it may contain!")
    
    elif item== "scroll" and current_room == "library":
        rooms[current_room]["puzzle"]["open_scroll"] = True
        solve_riddle()
    else:
        print(f"You can't use the {item} here.")

def solve_riddle():
        puzzle_message = "I am a place where secrets lie, above the rooms where shadows spy. What am I?"

    
        border_char = "-*-"
        message_length = len(puzzle_message) + 4  
        print(border_char * message_length)
        print(f"{border_char} {puzzle_message} {border_char}")
        print(border_char * message_length)
        answer = input("Your answer :   ").lower()
        if answer == "attic":
           rooms["library"]["puzzle"]["solve_riddle"] = True
           print("Your answer is correct. You have unlocked the basement door")
        else:
           print("Wrong answer! Please try again")
#khadija
# Ghost encounter check
def ghost_encounter():
    global protected, time_left
    if random.randint(1, 5) == 3:  
        if protected:
            print("The silver amulet glows, wrapping  U in protective Aura")
            protected = False  
        else:
            time_left -= 10  
            print("A ghost appears and saps your energy! You feel weaker...")
            check_time()


def check_time():
    if time_left <= 0:
        print("Midnight has come ! The haunted spirits have claimed you for  eternity...")
        quit()
    else:
        print(f"Time left until midnight: {time_left} minutes")


def save_game():
    with open("haunted_mansion_save.txt", "w") as save_file:
        save_file.write(f"{current_room}\n")
        save_file.write(",".join(inventory) + "\n")
        save_file.write(f"{time_left}\n")
    print("Game saved!")

# Loading the game
def load_game():
    global current_room, inventory, time_left
    try:
        
        load_file = open("haunted_mansion_save.txt", "r")
        
  
        current_room = load_file.readline().strip()  
        inventory = load_file.readline().strip().split(",")  
        time_left = int(load_file.readline().strip()) 
        
      
        load_file.close()

      
        print("Game loaded!")
        look()

    except FileNotFoundError:
        print("No saved game found.")

#hafsa
# Help/Instructions
def display_help():
    print("""
Available commands:
- go [direction] : Move in a direction (north, south, east, west)
- look : Redisplay the current room's description
- take [item] : Pick up an item from the room
- drop [item] : Drop an item from your inventory
- use [item] : Use an item in the room
- inventory : View your current items
- save : Save the game
- load : Load a saved game
- quit : Exit the game
- help : Display available commands
-check time : displays time left          
""")

# Main game loop
def main():
    print("Welcome to the Haunted Mansion Escape!")
    look()

    while True:
        command = input("What would you like to do? ").lower().split()

        if len(command) == 0:
            print("Invalid command.")
            continue

        action = command[0]

        if action == "quit":
            print("Thanks for playing!")
            break
        elif action == "go":
            if len(command) > 1:
                move(command[1])
            else:
                print("Go where?")
        elif action == "take":
            if len(command) > 1:
                take(command[1])
            else:
                print("Take what?")
        elif action == "drop":
            if len(command) > 1:
                drop(command[1])
            else:
                print("Drop what?")
        elif action == "use":
            if len(command) > 1:
                use_item(command[1])
            else:
                print("Use what?")
        elif action == "look":
            look()
        elif action == "inventory":
            print(f"You are carrying: {', '.join(inventory) if inventory else 'nothing'}")
        elif action == "save":
            save_game()
        elif action == "load":
            load_game()
        elif action == "help":
            display_help()
        elif action == "check" and len(command) > 1 and command[1] == "time":
            check_time()     
        else:
            print("Invalid command. Type 'help' for a list of commands.")

if __name__ == "__main__":
    main()
