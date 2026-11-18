from .parser import Parser
from .user_input import UserInput
from .printer import Printer


class MenuManager:
    def __init__(self, menu:dict, display_title, enter_to_continue = True):
        self.menu = menu
        self.display_title = display_title
        self.enter_to_continue = enter_to_continue

    def get_tltle(self, menu_key):
        return self.menu[menu_key][0]

    def get_action(self, menu_key):
        return self.menu[menu_key][1]

    def display_menu(self):
        self.display_title()
        for index, option in self.menu.items():
            print(f"{index}. {option[0]}")

    def display_enter_to_continue(self):
        input("\n\nPress Enter to continue... ")

    def run(self):
        while True:
            self.display_menu()
            menu_parser = Parser.parse_from_range(1, len(self.menu))
            choice = UserInput.ask(menu_parser, f"\nChoose an option [1-{len(self.menu)}]: ")
            title = self.get_tltle(choice)
            action = self.get_action(choice)
            if action is None:
                break

            try:
                Printer.display_function_title(title)
                action()
            except ValueError as e:
                print("Error:", e)
            finally:
                if self.enter_to_continue:
                    self.display_enter_to_continue()
