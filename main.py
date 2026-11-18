from classes.escape_room_system import EscapeRoomSystem

def main():
    try:
        escape_room_system = EscapeRoomSystem()
        escape_room_system.run()
    except KeyboardInterrupt:
            print("\nBye!")


if __name__ == "__main__":
    main()
    

