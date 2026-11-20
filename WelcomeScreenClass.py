import customtkinter
from UserClass import User
from Fonts import logo_font, heading_font, normal_font


class WelcomeScreen(customtkinter.CTkFrame):
    # I am passing in root_frame so that it is placed into the root frame
    def __init__(self, root_frame, root):
        super().__init__(root_frame)
        self.root = root

        # Setting up the grid to be able to place items into the Welcome Screen
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10), weight=1)
        self.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10), weight=1)

        # = WELCOME SCREEN WIDGETS =

        self.ejd_inventory_title = customtkinter.CTkLabel(self, text="EJD\nINVENTORY", font=logo_font)
        self.ejd_inventory_title.grid(row=0, column=5, sticky="nwe")

        # Heading that tells the user that the below boxes are used for creating an account
        self.create_account_title = customtkinter.CTkLabel(self, text="Create Account", font=heading_font)
        self.create_account_title.grid(row=3, column=4, sticky="nwe")

        # == ENTRY BOXES FOR CREATING AN ACCOUNT ==

        self.new_username_entry = customtkinter.CTkEntry(self, height=70, width=250, placeholder_text="Enter Username", font=normal_font)
        self.new_username_entry.grid(row=4, column=4, sticky="nwe")

        self.new_email_entry = customtkinter.CTkEntry(self, height=70, width=250, placeholder_text="Enter Email", font=normal_font)
        self.new_email_entry.grid(row=5, column=4, sticky="nwe")

        self.new_password_entry = customtkinter.CTkEntry(self, height=70, width=250, placeholder_text="Enter Password", font=normal_font)
        self.new_password_entry.grid(row=6, column=4, sticky="nwe")

        # Heading that tells user the below boxes are used for logging in
        self.login_title = customtkinter.CTkLabel(self, text="Login", font=heading_font)
        self.login_title.grid(row=3, column=6, sticky="nwe")

        # == ENTRY BOXES FOR LOGGING IN ==

        self.existing_username_entry = customtkinter.CTkEntry(self, height=70, width=250, placeholder_text="Enter Username", font=normal_font)
        self.existing_username_entry.grid(row=4, column=6, sticky="nwe")

        self.existing_email_entry = customtkinter.CTkEntry(self, height=70, width=250, placeholder_text="Enter Email", font=normal_font)
        self.existing_email_entry.grid(row=5, column=6, sticky="nwe")

        self.existing_password_entry = customtkinter.CTkEntry(self, height=70, width=250, placeholder_text="Enter Password", font=normal_font)
        self.existing_password_entry.grid(row=6, column=6, sticky="nwe")

        # == BUTTONS FOR PROCESSING INPUTS ==

        # Button that when pressed checks the users input for the creating account boxes
        self.create_account_button = customtkinter.CTkButton(self, height=70, width=250, text="Create Account", font=normal_font, command=self.check_create_account_inputs)
        self.create_account_button.grid(row=7, column=4, sticky="nwe")

        # Button that when pressed checks the users input for the logging in boxes
        self.login_button = customtkinter.CTkButton(self, height=70, width=250, text="Login", font=normal_font, command=self.check_login_inputs)
        self.login_button.grid(row=7, column=6, sticky="nwe")

    # Method for checking the inputs when creating an account
    def check_create_account_inputs(self):

        # Retrieves the values from the username, email and password inputs and set them as variables
        new_username = self.new_username_entry.get()
        new_email = self.new_email_entry.get()
        new_password = self.new_password_entry.get()

        # Calls the check method for creating an account from the User class in the Logic File
        check = User.check_new_details(new_username, new_email, new_password)

        # If that check returns True
        if check is True:
            # Let the user proceed to the next screen
            self.root.display_screen("dashboard_screen")
        # If that check returns False, output the reason for the failed check to the user
        else:
            error_message = customtkinter.CTkLabel(self, text=check, font=normal_font)
            error_message.grid(row=8, column=4, sticky="nwe")

    # Method for checking the inputs when logging in
    def check_login_inputs(self):

        # Retrieves the values from the username, email and password inputs and set them as variables
        existing_username = self.existing_username_entry.get()
        existing_email = self.existing_email_entry.get()
        existing_password = self.existing_password_entry.get()

        # Calls the check method for logging in from the User class in the Logic File
        check = User.check_existing_details(existing_username, existing_email, existing_password)

        # If that check returns True
        if check is True:
            # Let the user proceed to the next screen
            self.root.display_screen("dashboard_screen")
        # If that check returns False, output the reason for the failed check to the user
        else:
            error_message = customtkinter.CTkLabel(self, text="Incorrect details\ncombination", font=normal_font)
            error_message.grid(row=8, column=6, sticky="nwe")
