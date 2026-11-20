from sqlalchemy.orm import mapped_column, Mapped, relationship
from DatabaseSetup import session, AbstractBase
import os

current_user_id = None


# = USER CLASS =
class User(AbstractBase):
    # Setting Database table name
    __tablename__ = "users"

    # == SETTING DATABASE FIELDS ==

    # Initialises username, email and password fields
    username: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column()
    password: Mapped[str] = mapped_column()
    sales_confirmation_email_address: Mapped[str] = mapped_column()
    gmail_code: Mapped[str] = mapped_column()
    delivery_request_csv_directory: Mapped[str] = mapped_column()

    # == RELATIONSHIP WITH INVENTORY ITEMS ==
    # Creating the relationship between user and inventory item
    users_inventory_items: Mapped[list["InventoryItem"]] = relationship(back_populates="user")

    # == SETTING OBJECT ATTRIBUTES ==

    def __init__(self, username, email, password, sales_confirmation_email_address, gmail_code, delivery_request_csv_directory):
        # Uses super() to inherit id attribute from AbstractBase
        super().__init__()
        # Initialises username, email and password attributes
        self.username = username
        self.email = email
        self.password = password
        self.sales_confirmation_email_address = sales_confirmation_email_address
        self.gmail_code = gmail_code
        self.delivery_request_csv_directory = delivery_request_csv_directory


    # Method that encrypts password
    @staticmethod
    def encrypt_password(password):
        # Initialising the variable that will hold password once it has been encrypted
        encrypted_password = ""

        # Iterate through each character in password
        for character in password:
            # Get the ord of the character
            ord_of_character = ord(character)
            # Shift it by 5
            shifted_character = ord_of_character + 5
            # Add it to the encrypted password string
            encrypted_password += chr(shifted_character)

        return encrypted_password

    # Method that decrypts password
    @staticmethod
    def decrypt_password(encrypted_password):
        # Initialising the variable that will hold password once it has been decrypted
        decrypted_password = ""

        # Iterate through each character in password
        for character in encrypted_password:
            # Get the ord of the character
            ord_of_character = ord(character)
            # Shift it back 5
            shifted_character = ord_of_character - 5
            # Add it to the decrypted password string
            decrypted_password += chr(shifted_character)

        return decrypted_password


    # == METHODS FOR CREATING ACCOUNT ==

    # Static method that checks the username input when creating a new account
    @staticmethod
    def check_new_username(username):
        # Presence check
        if username != "":
            # Length check
            if 5 <= len(username) <= 30:
                # Only letters or numbers check
                if username.isalnum() is True:
                    # Unique check (checks if the username inputted doesn't already exist)
                    if not session.query(User).filter(User.username == username).count() > 0:
                        # If all conditions are met, return True
                        return True
                    else:
                        return "Username\nalready exists"
                else:
                    return "Username can only\ncontains letters or numbers"
            else:
                return "Username needs to be\nbetween 5 and 30 characters"
        else:
            return "Username needs to be\npresent"

    # Static method that checks the email input when creating an account
    @staticmethod
    def check_new_email(email):
        # Presence check
        if email != "":
            # Email format check
            if "@" in email:
                # Unique check
                if 4<= len(email) <= 254:
                    if not session.query(User).filter(User.email == email).count() > 0:
                        # If all conditions are met, return True
                        return True
                    else:
                        return "Email already\nexists"
                else:
                    return "Email needs to be between\n 4 and 254 characters"
            else:
                return "Email needs to\ncontain @"
        else:
            return "Email needs to\nbe present"

    @staticmethod
    def check_new_password(password):
        # Presence check
        if password != "":
            # Length check
            if 8 <= len(password) <= 30:
                # If all conditions are met, return True
                return True
            else:
                return "Password needs to be\nbetween 8 and 30 characters"
        else:
            return "Password needs to\nbe present"

    # This static method is the main method that controls the checking of the logging in details
    @staticmethod
    def check_new_details(username, email, password):
        # Setting the username_status variable as whatever the result of the check_new_username method will be
        username_status = User.check_new_username(username)
        # Setting the email_status variable as whatever the result of the check_new_email method will be
        email_status = User.check_new_email(email)
        # Setting the password variable as whatever the result of the check_new_password method will be
        password_status = User.check_new_password(password)

        # If username is valid
        if username_status is True:
            # If email is valid
            if email_status is True:
                # If password is valid
                if password_status is True:

                    encrypted_password = User.encrypt_password(password)
                    # Create a new instance of the User class using username, email and the encrypted password
                    new_user = User(username, email, encrypted_password, "not_set", "not_set", "not_set")

                    # Add the new user to the database
                    session.add(new_user)
                    session.commit()

                    # Query the user id of the user just added
                    user_id = session.query(User.id).filter(User.username == username, User.email == email, User.password == encrypted_password).scalar()
                    global current_user_id
                    # Set the global variable that holds current user id to the id of the user that has just been added
                    current_user_id = user_id

                    return True

                else:
                    # If password is not valid, return the specific reason why
                    return password_status
            else:
                return email_status
        else:
            return username_status

    # Methods that checks details for logging in
    @staticmethod
    def check_existing_details(username, email, password):
        encrypted_password = User.encrypt_password(password)
        # If the user's inputs match details already in the system
        if session.query(User).filter(User.username == username, User.email == email, User.password == encrypted_password).count() > 0:
            # If it does match

            # Query the user id of the user that just logged in
            user_id = session.query(User.id).filter(User.username == username, User.email == email, User.password == encrypted_password).scalar()
            global current_user_id
            # Set the global variable that holds current user id to the id of the user that has just logged in
            current_user_id = user_id

            return True
        else:
            # If it doesn't match, return False
            return False

    # == SETTINGS SCREEN LOGIC ==

    # === SETTING UP AUTOMATIC REORDERING PART 1 ===

    # Method that adds new sales confirmation email address or updates existing
    @staticmethod
    def add_new_sales_confirmation_email(sales_confirmation_email):
        # Queries the user
        user = session.query(User).filter(User.id == current_user_id).first()
        # Sets the sales confirmation email in database to the one passed in as parameter
        user.sales_confirmation_email = sales_confirmation_email
        # Commits the change
        session.commit()

    # Method that gets sales confirmation email address
    @staticmethod
    def get_sales_confirmation_email_address():
        sales_confirmation_email_address = session.query(User.sales_confirmation_email_address).filter(User.id == current_user_id).scalar()
        return sales_confirmation_email_address

    # == SETTING UP AUTOMATIC REORDERING PART 2 ==

    # Method that validates user input for gmail code
    @staticmethod
    def check_gmail_code(gmail_code):
        # Presence Check
        if gmail_code != "":
            # Length check
            if gmail_code.isalnum():
                if len(gmail_code) == 16:
                    return True
                else:
                    return "Gmail code needs to be\n16 characters long"
            else:
                return "Gmail code can't\ncontain any spaces"
        else:
            return "Gmail code needs to\n be present"

    # Method that adds new gmail app password or update existing
    @staticmethod
    def add_new_gmail_code(gmail_code):
        # Encrypts the gmail code using the existing encrypt_password method
        encrypted_gmail_code = User.encrypt_password(gmail_code)
        # Queries the user
        user = session.query(User).filter(User.id == current_user_id).first()
        # Sets the gmail code in database to the encrypted version of what was passed in as parameter
        user.gmail_code = encrypted_gmail_code
        # Commit the change
        session.commit()

    # Method that queries the gmail code from the database
    @staticmethod
    def get_gmail_code():
        # Query the gmail code
        gmail_code = session.query(User.gmail_code).filter(User.id == current_user_id).scalar()
        # Check if gmail code is not set:
        if gmail_code == "not_set":
            return None
        else:
            # Decrypt the gmail code
            decrypted_gmail_code = User.decrypt_password(gmail_code)
            # Return decrypted gmail code
            return decrypted_gmail_code

    @staticmethod
    def get_email_address():
        email_address = session.query(User.email).filter(User.id == current_user_id).scalar()
        return email_address

    # === UPDATING USER DETAILS ===

    # Method that updates username
    @staticmethod
    def update_username(new_username):
        global current_user_id
        # Query the current user by filtering id by current user id
        user = session.query(User).filter(User.id == current_user_id).first()
        # Set the username of the current user that has just been queried as the username that has been passed in as parameter
        user.username = new_username
        # Commit the change
        session.commit()

    # Method that updates email
    # Same functionality as update_username
    @staticmethod
    def update_email(new_email):
        global current_user_id
        user = session.query(User).filter(User.id == current_user_id).first()
        user.email = new_email
        session.commit()

    # Method that updates password
    # Same functionality as update_username
    @staticmethod
    def update_password(new_password):
        global current_user_id
        user = session.query(User).filter(User.id == current_user_id).first()
        # Encrypts the password before updating it
        encrypted_new_password = User.encrypt_password(new_password)
        user.password = encrypted_new_password
        session.commit()

    # === DELETING USER ===

    @staticmethod
    def delete_user():
        from InventoryItemClass import InventoryItem
        global current_user_id
        # Query all the inventory items owned by the user by filtering the query by current user id
        ids_of_all_user_inventory_items = session.query(InventoryItem.id).filter(InventoryItem.user_id == current_user_id).all()
        # Remove the brackets around each id
        all_ids = [i[0] for i in ids_of_all_user_inventory_items]
        # Iterate through all the id's of all the inventory items that user has
        for item_id in all_ids:
            # Call the method that will delete the item, and all its sales and deliveries
            InventoryItem.delete_item(item_id)

        # Now all inventory items have been deleted, the user can be deleted
        user = session.query(User).filter(User.id == current_user_id).first()
        # Delete that user
        session.delete(user)
        session.commit()

    # === CSV DIRECTORY ===

    @staticmethod
    def add_delivery_csv_directory(csv_directory):
        # Queries the user
        user = session.query(User).filter(User.id == current_user_id).first()
        # Sets the delivery request csv directory in database to what the user has just inputted
        user.delivery_request_csv_directory = csv_directory
        # Commit the change
        session.commit()

    @staticmethod
    def check_delivery_csv_directory(csv_directory):
        # If the directory exists, return True
        if os.path.isdir(csv_directory):
            return True
        else:
            # If the directory doesn't exist, output the error message
            return "Directory Doesn't Exist"

    @staticmethod
    def get_delivery_request_csv_directory():
        directory = session.query(User.delivery_request_csv_directory).filter(User.id == current_user_id).scalar()
        return directory
