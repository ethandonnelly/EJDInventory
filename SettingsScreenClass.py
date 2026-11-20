

import customtkinter, webbrowser
from Fonts import title_font, heading_font, normal_font
from UserClass import User


class SettingsScreen(customtkinter.CTkFrame):
    # I am passing in root_frame so that it is placed into the root frame
    def __init__(self, root_frame, root):
        super().__init__(root_frame)
        self.root = root

        # == SCREEN GRID SETUP ==

        # Organised the grid so there is two rows, a top row and a bottom row
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=20)
        self.grid_columnconfigure(0, weight=1)

        # == NAVIGATION BAR FRAME ==

        # Created a frame that will hold the navigation bar
        self.navigation_bar_frame = customtkinter.CTkFrame(self)
        # Placed it in the top row
        self.navigation_bar_frame.grid(row=0, column=0, sticky="nesw")

        # Now I have configured the grid of the navigation bar so that it can hold the navigation buttons
        self.navigation_bar_frame.rowconfigure(0, weight=1)
        # 6 columns for the 6 different navigation buttons, so each get equal space
        self.navigation_bar_frame.columnconfigure((0, 1, 2, 3, 4, 5), weight=1)

        # == MAIN FRAME ==

        # Creating the main frame, this will hold everything else but the navigation buttons
        self.main_frame = customtkinter.CTkFrame(self)
        self.main_frame.grid(row=1, column=0, sticky="nesw")

        # Set up the grid for the main frame like how I would normally set up a screen grid
        self.main_frame.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10), weight=1)
        self.main_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10), weight=1)

        # == NAVIGATION BUTTONS ==

        # Button to go to dashboard screen
        self.display_dashboard_button = customtkinter.CTkButton(self.navigation_bar_frame, text="Dashboard", font=normal_font, command=lambda: self.root.display_screen("dashboard_screen"))
        self.display_dashboard_button.grid(row=0, column=0, sticky="nesw")

        # Button to go to add new item
        self.new_item_button = customtkinter.CTkButton(self.navigation_bar_frame, text="Add New Item", font=normal_font, command=lambda: self.root.display_screen("new_item_screen"))
        self.new_item_button.grid(row=0, column=1, sticky="nesw")

        # Button to go to update item screen
        self.display_update_item_button = customtkinter.CTkButton(self.navigation_bar_frame, text="Update Existing Item", font=normal_font, command=lambda: self.root.display_screen("update_item_screen"))
        self.display_update_item_button.grid(row=0, column=2, sticky="nesw")

        # Button to go to inventory report screen
        self.display_inventory_report_button = customtkinter.CTkButton(self.navigation_bar_frame, text="Inventory Report", font=normal_font, command=lambda: self.root.display_screen("inventory_report_screen"))
        self.display_inventory_report_button.grid(row=0, column=3, sticky="nesw")

        # Heading that tells user they are on settings screen
        self.settings_title = customtkinter.CTkLabel(self.navigation_bar_frame, text="Settings", font=title_font)
        self.settings_title.grid(row=0, column=4, sticky="nesw")

        # Button to exit the application
        self.exit_button = customtkinter.CTkButton(self.navigation_bar_frame, text="Exit", font=normal_font, fg_color="red", command=lambda: exit())
        self.exit_button.grid(row=0, column=5, sticky="nesw")

        # == CHOOSING COLOUR SCHEME ==

        # Heading that tells user to choose main colour
        self.choose_main_colour_heading = customtkinter.CTkLabel(self.main_frame, text="Choose Main Colour:", font=heading_font)
        self.choose_main_colour_heading.grid(row=0, column=0)

        # Colour choices
        main_colours = ["Dark", "Light"]
        # Creating the colour option menu
        self.main_colour_option_menu = customtkinter.CTkOptionMenu(self.main_frame, values=main_colours, width=300, font=normal_font, dropdown_font=normal_font, command=self.set_main_colour)
        self.main_colour_option_menu.grid(row=1, column=0)

        # == SETTING UP AUTOMATIC REORDERING PART 1 ==

        self.setting_up_reordering_part1_title = customtkinter.CTkLabel(self.main_frame, text="Setting Up Auto\nReordering Part 1:", font=heading_font)
        self.setting_up_reordering_part1_title.grid(row=2, column=0)

        self.reordering_part1_step1_text = customtkinter.CTkLabel(self.main_frame, text="Step 1: Enter/Update the email\naddress that you receive\n sale confirmations from:", font=normal_font)
        self.reordering_part1_step1_text.grid(row=3, column=0)

        # Entry box for sales confirmation email address
        self.sale_confirmation_email_entry = customtkinter.CTkEntry(self.main_frame, height=70, width=330, placeholder_text="E.g. sales@shopify.com", font=normal_font)
        self.sale_confirmation_email_entry.grid(row=4, column=0)

        # Buttons that saves sales confirmation email
        self.save_confirmation_email_button = customtkinter.CTkButton(self.main_frame, text="Save Email", height=70, font=normal_font, command=self.save_sales_confirmation_email_address)
        self.save_confirmation_email_button.grid(row=5, column=0, sticky="nwe")

        self.reordering_part1_step2_text = customtkinter.CTkLabel(self.main_frame, text="Step 2: Enter/Update the directory\nwhere you store delivery CSVs:", font=normal_font)
        self.reordering_part1_step2_text.grid(row=7, column=0)

        # Entry box for csv directory
        self.delivery_csv_directory_entry = customtkinter.CTkEntry(self.main_frame, height=70, width=330, placeholder_text="Directory:", font=normal_font)
        self.delivery_csv_directory_entry.grid(row=8, column=0)

        # Buttons that csv directory
        self.save_delivery_csv_directory_button = customtkinter.CTkButton(self.main_frame, text="Save Directory", height=70, font=normal_font, command=self.save_delivery_csv_directory)
        self.save_delivery_csv_directory_button.grid(row=9, column=0, sticky="nwe")

        # == SETTING UP AUTOMATIC REORDERING PART 2 ==

        self.setting_up_reordering_part2_title = customtkinter.CTkLabel(self.main_frame, text="Setting Up Auto\nReordering Part 2:", font=heading_font)
        self.setting_up_reordering_part2_title.grid(row=1, column=2)

        self.instruction_part2_step1_text = customtkinter.CTkLabel(self.main_frame, text="Step 1: Follow the link\n below and make sure that\n 2FA is enabled", font=normal_font)
        self.instruction_part2_step1_text.grid(row=2, column=2)

        # Button that when clicked, opens the link to set up 2FA
        self.google_account_link = customtkinter.CTkButton(self.main_frame, text="Link: Setup Google 2FA", height=70, font=normal_font, command=lambda: self.open_link("https://myaccount.google.com/security"))
        self.google_account_link.grid(row=3, column=2, sticky="nwe")

        self.instruction_part2_step2_text = customtkinter.CTkLabel(self.main_frame, text="Step 2: Follow the link\n below and create a new\n app password for 'Gmail'", font=normal_font)
        self.instruction_part2_step2_text.grid(row=4, column=2)

        # Button that when clicked, opens the link to set up gmail code
        self.setup_gmail_code_link = customtkinter.CTkButton(self.main_frame, text="Link: Setup Gmail Code", height=70, font=normal_font, command=lambda: self.open_link("https://myaccount.google.com/u/5/apppasswords"))
        self.setup_gmail_code_link.grid(row=5, column=2, sticky="nwe")

        self.instruction_step_3_text = customtkinter.CTkLabel(self.main_frame, text="Step 3: Paste the code in\nthe box below (with spaces removed)", font=normal_font)
        self.instruction_step_3_text.grid(row=6, column=2)

        # Entry box for gmail code
        self.gmail_code_entry = customtkinter.CTkEntry(self.main_frame, height=70, width=300, placeholder_text="Gmail Code:", font=normal_font)
        self.gmail_code_entry.grid(row=7, column=2)

        # Buttons that saves gmail code
        self.save_code_button = customtkinter.CTkButton(self.main_frame, text="Save Gmail Code", height=70, font=normal_font, command=self.save_gmail_code)
        self.save_code_button.grid(row=8, column=2, sticky="nwe")

        # == UPDATE USER DETAILS ==

        # === HEADING ===

        self.update_details_heading = customtkinter.CTkLabel(self.main_frame, text="Update Details:", font=heading_font)
        self.update_details_heading.grid(row=1, column=4, sticky="nesw")

        # === UPDATE USERNAME ===

        # Entry box where the new username the user wishes to use is inputted
        self.update_username_entry = customtkinter.CTkEntry(self.main_frame, height=70, width=300, placeholder_text="Update Username:", font=normal_font)
        self.update_username_entry.grid(row=2, column=4)

        # Button that when clicked calls the update username method
        self.update_username_button = customtkinter.CTkButton(self.main_frame, text="Update Username", height=70, font=normal_font, command=self.get_new_username)
        self.update_username_button.grid(row=3, column=4, sticky="nwe")

        # === UPDATE EMAIL ===

        # Entry box where the new email the user wishes to use is inputted
        self.update_email_entry = customtkinter.CTkEntry(self.main_frame, height=70, width=300, placeholder_text="Update Email:", font=normal_font)
        self.update_email_entry.grid(row=5, column=4)

        # Button that when clicked calls the update email method
        self.update_email_button = customtkinter.CTkButton(self.main_frame, text="Update Email", height=70, font=normal_font, command=self.get_new_email)
        self.update_email_button.grid(row=6, column=4, sticky="nwe")

        # === UPDATE PASSWORD ===

        # Entry box where the new password the user wishes to use is inputted
        self.update_password_entry = customtkinter.CTkEntry(self.main_frame, height=70, width=300, placeholder_text="Update Password:", font=normal_font)
        self.update_password_entry.grid(row=8, column=4)

        # Button that when clicked calls the update password method
        self.update_password_button = customtkinter.CTkButton(self.main_frame, text="Update Password", height=70, font=normal_font, command=self.get_new_password)
        self.update_password_button.grid(row=9, column=4, sticky="nwe")

        # == DELETE ACCOUNT ==

        # Button that when pressed, brings up another button that asks "Are You Sure?"
        self.delete_account_button = customtkinter.CTkButton(self.main_frame, text="Delete Account", font=normal_font, fg_color="red", hover_color="dark red", command=self.show_are_you_sure_button)
        self.delete_account_button.grid(row=6, column=8, sticky="nesw")

    # Method that saves csv directory
    def save_delivery_csv_directory(self):
        # Get the value from the directory input box
        directory = self.delivery_csv_directory_entry.get()
        check = User.check_delivery_csv_directory(directory)
        if check is True:
            # If input is valid, call the method that adds the delivery csv to database
            User.add_delivery_csv_directory(directory)
            # Then output a message to tell the user the delivery csv has been updated
            for existing_error_message in self.main_frame.grid_slaves(row=10, column=0):
                existing_error_message.grid_forget()
            directory_added_message = customtkinter.CTkLabel(self.main_frame, text="Directory Added", font=normal_font)
            directory_added_message.grid(row=10, column=0, sticky="nwe")
        else:
            # If the csv directory is not valid, output the reason why it failed the check
            error_message = customtkinter.CTkLabel(self.main_frame, text=check, font=normal_font)
            error_message.grid(row=10, column=0, sticky="nwe")

    # Method that shows are you sure button when delete account button is pressed
    def show_are_you_sure_button(self):
        # Heading that asks the user "Are You Sure?"
        are_you_sure_heading = customtkinter.CTkLabel(self.main_frame, text="Are You\nSure?", font=heading_font)
        are_you_sure_heading.grid(row=7, column=8)

        # Button that when pressed, calls the delete user method from User class in logic file and also exits the application
        yes_button = customtkinter.CTkButton(self.main_frame, text="Yes", font=normal_font, fg_color="red", hover_color="dark red", command=lambda: [User.delete_user(), exit()])
        yes_button.grid(row=8, column=8, sticky="nesw")

    # Method for updating username
    def get_new_username(self):
        # Gets the value from the username input box
        new_username_input = self.update_username_entry.get()
        # Passes that value into the checking method from the User class in the logic file
        check = User.check_new_username(new_username_input)
        if check is True:
            # If the new username is valid, call the method inside User class that updates the username inside the database
            User.update_username(new_username_input)
            # Then output a message to tell the user their username has been updated
            for existing_error_message in self.main_frame.grid_slaves(row=4, column=4):
                existing_error_message.grid_forget()

            username_updated_message = customtkinter.CTkLabel(self.main_frame, text="Username Updated", font=normal_font)
            username_updated_message.grid(row=4, column=4, sticky="nwe")
        else:
            # If the new username is not valid, output the reason why it failed the check
            error_message = customtkinter.CTkLabel(self.main_frame, text=check, font=normal_font)
            error_message.grid(row=4, column=4, sticky="nwe")

    # Method for updating email
    # Same functionality as update_username but just for email
    def get_new_email(self):
        new_email_input = self.update_email_entry.get()
        check = User.check_new_email(new_email_input)
        if check is True:
            User.update_email(new_email_input)
            for existing_error_message in self.main_frame.grid_slaves(row=7, column=4):
                existing_error_message.grid_forget()

            email_updated_message = customtkinter.CTkLabel(self.main_frame, text="Email Updated", font=normal_font)
            email_updated_message.grid(row=7, column=4, sticky="nwe")
        else:
            error_message = customtkinter.CTkLabel(self.main_frame, text=check, font=normal_font)
            error_message.grid(row=7, column=4, sticky="nwe")

    # Method for updating password
    # Same functionality as update_username but just for password
    def get_new_password(self):
        new_password_input = self.update_password_entry.get()
        check = User.check_new_password(new_password_input)
        if check is True:
            User.update_password(new_password_input)
            for existing_error_message in self.main_frame.grid_slaves(row=10, column=4):
                existing_error_message.grid_forget()

            password_updated_message = customtkinter.CTkLabel(self.main_frame, text="Password Updated", font=normal_font)
            password_updated_message.grid(row=10, column=4, sticky="nwe")
        else:
            error_message = customtkinter.CTkLabel(self.main_frame, text=check, font=normal_font)
            error_message.grid(row=10, column=4, sticky="nwe")


    # Method that saves the sales confirmation email address
    def save_sales_confirmation_email_address(self):
        sales_confirmation_email = self.sale_confirmation_email_entry.get()
        # Use existing email check from UserClass.py as it has the same functionality as what I want here
        check = User.check_new_email(sales_confirmation_email)
        # If that check returns True
        if check is True:
            # Add the sales confirmation email address to database
            User.add_new_sales_confirmation_email(sales_confirmation_email)
            # Output the success message
            for existing_error_message in self.main_frame.grid_slaves(row=6, column=0):
                existing_error_message.grid_forget()

            success_message = customtkinter.CTkLabel(self.main_frame, text="Email Address\nAdded", font=normal_font)
            success_message.grid(row=6, column=0, sticky="nwe")
        # If that check returns False, output the reason for the failed check to the user
        else:
            error_message = customtkinter.CTkLabel(self.main_frame, text=check, font=normal_font)
            error_message.grid(row=6, column=0, sticky="nwe")

    # Method that opens the link which is passed in as a parameter
    def open_link(self, link):
        webbrowser.open(link)

    # Method that saves the user's gmail code
    def save_gmail_code(self):
        gmail_code = self.gmail_code_entry.get()
        check = User.check_gmail_code(gmail_code)

        # If that check returns True
        if check is True:
            # Calls the method from UserClass.py that adds the gmail code
            User.add_new_gmail_code(gmail_code)
            # Output the success message
            for existing_error_message in self.main_frame.grid_slaves(row=9, column=2):
                existing_error_message.grid_forget()

            success_message = customtkinter.CTkLabel(self.main_frame, text="Code Saved", font=normal_font)
            success_message.grid(row=9, column=2, sticky="nwe")
        # If that check returns False, output the reason for the failed check to the user
        else:
            error_message = customtkinter.CTkLabel(self.main_frame, text=check, font=normal_font)
            error_message.grid(row=9, column=2, sticky="nwe")

    # Method that sets colour mode
    def set_main_colour(self, colour_choice):
        # Sets colour mode to whatever user chose in picker
        customtkinter.set_appearance_mode(colour_choice)
