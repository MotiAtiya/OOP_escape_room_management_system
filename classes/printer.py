import os

class Printer:

    @staticmethod
    def display_rooms(rooms):
        print("ID".ljust(10),
              "Name".ljust(20),
              "Difficulty".ljust(15),
              "Duration".ljust(10),
              "Players".ljust(10),
              "Price".ljust(10), 
              "Status".ljust(10))
        print()
        for r in rooms:
            print(r.room_id.ljust(10),
                  r.name.ljust(20),
                  r.difficulty.ljust(15),
                  str(r.duration).ljust(10),
                  str(r.min_players - r.max_players).ljust(10), 
                  str(r.price_per_player).ljust(10),
                  "Active" if r.is_active else "Inactive")

    @staticmethod
    def display_room_details(room):
        print()
        print("Room ID:".ljust(20), room.room_id)
        print("Name:".ljust(20), room.name)
        print("Difficulty:".ljust(20), room.difficulty)
        print("Duration:".ljust(20), room.duration, "min")
        print("Min Players:".ljust(20), room.min_players)
        print("Max Players:".ljust(20), room.max_players)
        print("Price Per Player:".ljust(20), room.price_per_player)
        print("Is Active:".ljust(20), "True" if room.is_active else "False")

    @staticmethod
    def display_bookings(bookings):
        print("ID".ljust(5),
              "Customer Name".ljust(20),
              "Room ID".ljust(8),
              "Date".ljust(11),
              "Time".ljust(7),
              "Players".ljust(8),
              "Price".ljust(8),
              "Status".ljust(10),
              "Fee")
        print()
        for b in bookings:
            booking_date = b.booking_date.strftime("%Y-%m-%d")
            booking_time = b.start_time.strftime("%H:%M")
            print(b.booking_id.ljust(5),
                  b.customer_name.ljust(20),
                  b.room_id.ljust(8),
                  booking_date.ljust(11),
                  booking_time.ljust(7),
                  str(b.players).ljust(8),
                  str(b.total_price).ljust(8),
                  b.status.ljust(10),
                  str(b.cancellation_fee))


    @staticmethod
    def display_booking_details(booking):
        print()
        print("Booking ID:".ljust(20), booking.booking_id)
        print("Customer Name:".ljust(20), booking.customer_name)
        print("Room ID:".ljust(20), booking.room_id)
        print("Date:".ljust(20), booking.booking_date)
        print("Start Time:".ljust(20), booking.start_time)
        print("Players:".ljust(20), booking.players)
        print("Total Price:".ljust(20), booking.total_price)
        print("Status:".ljust(20), booking.status)
        print("Cancellation Fee:".ljust(20), booking.cancellation_fee)


    @staticmethod
    def clear_screen():
        # Clear the terminal screen based on OS
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def display_system_title(title):
        Printer.clear_screen()
        print()
        print('=' * (len(title) + 14))
        print(' ' * 7 + title.upper())
        print('=' * (len(title) + 14))
        print()

    @staticmethod
    def display_option_title(option_title):
        Printer.clear_screen()
        print(f"\n--------- {option_title.upper()} ---------\n")


    @staticmethod
    def display_function_title(function_title):
        Printer.clear_screen()
        print(function_title)
        print("-" * len(function_title))
        print()

