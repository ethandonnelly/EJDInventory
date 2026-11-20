import DatabaseSetup
DatabaseSetup.initialise_database()

import customtkinter
from WelcomeScreenClass import WelcomeScreen
from DashboardScreenClass import DashboardScreen
from NewItemScreenClass import NewItemScreen
from UpdateItemScreenClass import UpdateItemScreen
from InventoryReportScreenClass import InventoryReportScreen
from SettingsScreenClass import SettingsScreen


class Root(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1920x1080")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # Create a root frame to place the screens into
        self.root_frame = customtkinter.CTkFrame(self)
        self.root_frame.grid(row=0, column=0, sticky="nesw")

        self.root_frame.rowconfigure(0, weight=1)
        self.root_frame.columnconfigure(0, weight=1)

        # Dictionary to hold all screens
        self.all_screens = {}
        
        # All the pages
        self.pages = {
            "welcome_screen": WelcomeScreen,
            "dashboard_screen": DashboardScreen,
            "add_new_item_screen": NewItemScreen,
            "update_item_screen": UpdateItemScreen,
            "inventory_report_screen": InventoryReportScreen,
            "settings_screen": SettingsScreen,
        }

        # Iterate through each page and turn it into a screen
        for i in self.pages:
            self.create_screen(i)

        self.display_screen("welcome_screen")

    def create_screen(self, screen_name):
        # Get the screen name from the pages dictionary
        screen = self.pages[screen_name]
        # Create the new screen
        new_screen = screen(self.root_frame, self)
        # Add the screen to the screens dictionary
        self.all_screens[screen_name] = new_screen

    # This method is used to display the different screens
    def display_screen(self, screen_to_display):
        # Access the screen to display from the all_screens dictionary
        screen = self.all_screens[screen_to_display]
        if screen_to_display == "update_item_screen":
            # If update item screen is being displayed, update the picker options
            screen.update_picker_options()
        if screen_to_display == "dashboard_screen":
            # If dashboard is being displayed, update the picker options
            screen.update_picker_options()

            # Log all new sales and deliveries
            from UpdateCurrentLevelClasses import Sale, Delivery
            Sale.log_all_new_sales()
            Delivery.log_all_new_deliveries()

        if screen_to_display == "inventory_report_screen":
            # If inventory report is being displayed, update the picker options
            screen.update_picker_options()
        screen.grid(row=0, column=0, sticky="nesw")
        # Using the tkraise() method to display the screen
        screen.tkraise()


main = Root()
main.mainloop()
