from .parser import Parser
from .user_input import UserInput

class MenuManager:
    def __init__(self, menu:dict):
        self.menu = menu

    def get_tltle(self, menu_key):
        return self.menu[menu_key][0]

    def get_action(self, menu_key):
        return self.menu[menu_key][1]


    def display_menu(self):
        for index, option in self.menu.items():
            print(f"{index}. {option[0]}")

    def enter_to_continue(self):
        input("\n\nPress Enter to continue... ")

    def run(self):
        while True:
            # display_system_title()
            self.display_menu()
            menu_parser = Parser.parse_from_range(1, len(self.menu))
            choice = UserInput.ask(menu_parser, f"\nChoose an option [1-{len(self.menu)}]: ")
            title = self.get_tltle(choice)
            action = self.get_action(choice)
            if action is None:
                break

            try:
                # display_function_title(title)
                print(title)
                action()
            except ValueError as e:
                print("Error:", e)
            finally:
                self.enter_to_continue()

