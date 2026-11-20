

from sqlalchemy.orm import mapped_column, Mapped, relationship
from DatabaseSetup import session, AbstractBase
from sqlalchemy import ForeignKey
import imap_tools, io, pdfplumber, datetime, csv, smtplib
from imap_tools import MailBox, AND
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


class Order(AbstractBase):
    # Making it an abstract class
    __abstract__ = True

    # == INITIALISING DATABASE FIELDS ==

    date: Mapped[int] = mapped_column()
    amount: Mapped[int] = mapped_column()

    # == INITIALISING ATTRIBUTES  ==

    def __init__(self, date, amount):
        self.date = date
        self.amount = amount

    # Method that iterates through all the user's unseen emails from desired sender and returns the pdfs
    @staticmethod
    def get_pdfs_in_unseen_emails(sender_email_address):
        # Import User class
        from UserClass import User

        # List that holds all pdfs
        all_pdfs = []

        # Get the user's email address
        current_user_email_address = User.get_email_address()
        # Get the user's gmail code
        current_user_gmail_code = User.get_gmail_code()
        # Set the server
        server = "imap.gmail.com"

        if current_user_gmail_code is None:
            return None

        try:
            # Open the user's inbox
            with MailBox(server).login(current_user_email_address, current_user_gmail_code) as inbox:
                # Iterate through each email that is from the desired sender and hasn't been read
                for email in inbox.fetch(AND(from_=sender_email_address, seen=False)):
                    # Iterate through each attachment in each email
                    for attachment in email.attachments:
                        # Get the filename
                        filename = attachment.filename
                        # If the file is a pdf
                        if ".pdf" in filename:
                            # Get the pdf using .payload method
                            pdf = attachment.payload
                            # Append the pdf to all_pdfs list
                            all_pdfs.append(io.BytesIO(pdf))
            # Return list of all_pdfs
            return all_pdfs
        # If no details have been set yet, don't do anything
        except imap_tools.errors.MailboxLoginError:
            pass

    # Method to read the pdf document
    @staticmethod
    def read_pdf_document(pdf):
        # Open the document
        with pdfplumber.open(pdf) as doc:
            # Index into the first page
            page = doc.pages[0]
            # Extract the text
            text = page.extract_text()
            return text

    # Method that reads the pdf document table contents
    @staticmethod
    def read_table_in_pdf(document):
        # Open the document
        with pdfplumber.open(document) as doc:
            # Index into first page
            page = doc.pages[0]
            # Use the extract table method
            table = page.extract_table()
            # Return the table
            return table[1:]

    # Method that finds the date in the delivery or sales receipt
    @staticmethod
    def find_date_in_pdf(pdf_text):
        # Iterate through each character in the pdf text
        for i in range(len(pdf_text)):
            # If "Date" heading is found
            if pdf_text[i] == "D" and pdf_text[i + 1] == "a" and pdf_text[i + 2] == "t" and pdf_text[i + 3] == "e":
                # Move 6 characters forward as actual date starts 6 places after "D" in "Date:"
                start_of_date_index = i + 6
                # Set end of date as 10 characters after start as date is 10 characters long
                end_of_date_index = start_of_date_index + 10
                # Slice into doc text between the start of date index and end of date character
                date = pdf_text[start_of_date_index:end_of_date_index]
                # Return the date
                return date

    @staticmethod
    def get_current_date():
        date = datetime.datetime.now()
        # Slice into the date
        return str(date)[0:11]

    # == REQUESTING A NEW DELIVERY IN RESPONSE TO CURRENT LEVEL BEING BELOW REORDER POINT ==

    # Method that checks if new current level is less than or equal to reorder point
    @staticmethod
    def check_reorder_point(item_id, new_current_level):
        from InventoryItemClass import InventoryItem

        # Query the database for the max point of the item whose id has been passed in as parameter
        max_point = session.query(InventoryItem.max_point).filter(InventoryItem.id == item_id).scalar()
        # Query the database for the reorder point of the item whose id has been passed in as parameter
        reorder_point = session.query(InventoryItem.reorder_point).filter(InventoryItem.id == item_id).scalar()

        # If the updated current level which was passed in as a parameter is less than or equal to reorder point
        if new_current_level <= reorder_point:
            # Set the target inventory number as the max point
            target_inventory_number = max_point
            # Take away how much inventory the user already has from the target inventory number to get amount needed
            amount_needed = target_inventory_number - new_current_level
            # Return the amount needed
            return amount_needed
        # If the updated current level is not less than or equal to reorder point, return False
        else:
            return False

    @staticmethod
    def request_new_delivery(id_of_requested_item, amount_requested):
        # Import InventoryItem class
        from InventoryItemClass import InventoryItem

        # Query the name of the item that is being requested so it can be added to csv file
        item_name = InventoryItem.get_item_name(id_of_requested_item)

        # Create the delivery request csv by calling the method and passing in item id, item name, and amount requested
        delivery_request_csv = Order.create_new_delivery_request_csv(id_of_requested_item, item_name, amount_requested)

        # Call the method that sends the delivery request
        Order.send_delivery_request_email(delivery_request_csv, id_of_requested_item)


    @staticmethod
    def create_new_delivery_request_csv(id_of_item_requested, name_of_item_requested, item_amount_requested):
        # Import User class
        from UserClass import User

        # Use the item id passed in as parameter in order to complete delivery request csv name
        delivery_request_csv_name = f"DeliveryRequestOfItemId{id_of_item_requested}.csv"

        # By opening the file name with "w" it creates the csv
        with open(delivery_request_csv_name, "w", newline="") as delivery_request_csv:
            writer = csv.writer(delivery_request_csv)

            # Add the headings
            headings = ["Item ID Requested", "Item Name Requested", "Item Amount Requested"]
            writer.writerow(headings)

            # Add the item
            new_line = [id_of_item_requested, name_of_item_requested, item_amount_requested]
            writer.writerow(new_line)

        # Query the directory
        directory = User.get_delivery_request_csv_directory()
        # Add together the directory and the csv name
        return rf"{directory}\{delivery_request_csv_name}"


    @staticmethod
    def send_delivery_request_email(delivery_request_csv, id_of_requested_item):
        # Import User class
        from UserClass import User
        # Import InventoryItem class
        from InventoryItemClass import InventoryItem

        # Set the required details to be able to send the email
        current_users_email_address = User.get_email()
        current_users_gmail_code = User.get_gmail_code()
        suppliers_email_address = InventoryItem.get_suppliers_email(id_of_requested_item)
        server = "smtp.gmail.com"
        port = 587

        # Create the email
        email = MIMEMultipart()

        # Set the different aspects of the email
        email["Subject"] = "Delivery Request"
        email["From"] = current_users_email_address
        email["To"] = suppliers_email_address

        # Open the delivery request form and attach it to the email
        with open(delivery_request_csv, "r", newline="") as csv_file:
            email.attach(MIMEApplication(csv_file.read(), Name=f"DeliveryRequestOfItemId{id_of_requested_item}.csv"))

        # Start the connection to the smtp server
        smtp_connection = smtplib.SMTP(server, port)
        smtp_connection.starttls()

        # Login using previously set details
        smtp_connection.login(current_users_email_address, current_users_gmail_code)

        # Send the email
        smtp_connection.sendmail(email["From"], email["To"], email.as_string())
        smtp_connection.quit()

class Sale(Order):
    __tablename__ = "sales"

    # == SETTING UP RELATIONSHIP BETWEEN SALE AND INVENTORY ITEM ==

    # Creating the many-to-one relationship by passing InventoryItem in without list
    inventory_item: Mapped["InventoryItem"] = relationship(back_populates="sale")
    # Setting item id as the foreign key
    sold_item_id: Mapped[int] = mapped_column(ForeignKey("inventory_items.id"))

    def __init__(self, date, amount, sold_item_id):
        # Inherit date and amount from Order
        super().__init__(date, amount)
        # Initialise sold item id
        self.sold_item_id = sold_item_id

    # Method that gets all the sales info pdfs
    @staticmethod
    def get_all_new_sales_pdfs():
        # Import from User class
        from UserClass import User

        # Call the method in User class that gets the email address where sales information comes from
        sales_confirmation_email_address = User.get_sales_confirmation_email_address()
        # Call the method in Order class that gets all the unseen sales receipt pdfs that are sent by the email address just found
        all_sales_pdfs = Order.get_pdfs_in_unseen_emails(sales_confirmation_email_address)
        # Return a list of pdfs
        return all_sales_pdfs

    # Methods that logs all new sales
    @staticmethod
    def log_all_new_sales():
        # Call the method that gets all the sales pdfs
        all_sales_pdfs = Sale.get_all_new_sales_pdfs()
        # If there are no sales pdfs, don't do anything
        if all_sales_pdfs is None:
            pass
        # If there is sales pdfs:
        else:
            # As all_sales_pdfs variable holds a list of pdfs, iterate through each pdf
            for pdf in all_sales_pdfs:
                # For each in the list, call the method that reads all the contents
                pdf_text = Order.read_pdf_document(pdf)
                # Call the method that finds the date of the document using pdf_text as parameter
                date_in_doc = Order.find_date_in_pdf(pdf_text)

                # Then also for each pdf in list, get the table content
                pdf_table_content = Order.read_table_in_pdf(pdf)

                # Iterate through each row in the table in pdf
                for row in pdf_table_content:
                    # Each row in pdf table is in form sold_item_id, sold_item_name, amount_sold
                    # Index into sold_item_id and amount_sold
                    sold_item_id = int(row[0])
                    amount_sold = int(row[2])

                    # Call the method that logs an individual sale
                    Sale.log_individual_sale(date_in_doc, amount_sold, sold_item_id)

    # Method for logging a single sale
    @staticmethod
    def log_individual_sale(date_of_sale, amount_sold, sold_item_id):
        # Create a new instance of sales class
        new_sale = Sale(date_of_sale, amount_sold, sold_item_id)
        # Add the new sale to database
        session.add(new_sale)
        # Commit the change
        session.commit()

        # Call the update current level method
        Sale.update_current_level_from_sale(amount_sold, sold_item_id)

    # Method that updates current inventory level in response to sales
    @staticmethod
    def update_current_level_from_sale(amount_sold, sold_item_id):
        # Import InventoryItem class
        from InventoryItemClass import InventoryItem

        # Query the current level of that item before any sales have occurred
        current_level_before_sales = session.query(InventoryItem.current_level).filter(InventoryItem.id == sold_item_id).scalar()
        # Minus the sales amount
        current_level_after_sales = current_level_before_sales - amount_sold

        # Update the current level to the new amount
        item_sold = session.query(InventoryItem).filter(InventoryItem.id == sold_item_id).first()
        item_sold.current_level = current_level_after_sales
        session.commit()

        # Call the method in Order class the checks reorder point
        reorder_point_check = Order.check_reorder_point(sold_item_id, current_level_after_sales)
        # If reorder_point_check is False, don't do anything
        if reorder_point_check is False:
            pass
        else:
            # If check_reorder_point method is not False, it returns the amount needed
            amount_needed = reorder_point_check
            # So call the request new delivery method using the amount needed
            Order.request_new_delivery(sold_item_id, amount_needed)


class Delivery(Order):
    __tablename__ = "deliveries"

    # == SETTING UP RELATIONSHIP BETWEEN DELIVERY AND INVENTORY ITEM ==

    # Creating the many-to-one relationship by passing InventoryItem in without list
    inventory_item: Mapped["InventoryItem"] = relationship(back_populates="delivery")
    # Setting item id as the foreign key
    delivered_item_id: Mapped[int] = mapped_column(ForeignKey("inventory_items.id"))

    def __init__(self, date, amount, delivered_item_id):
        # Inherit date and amount from Order
        super().__init__(date, amount)
        # Initialise sold item id
        self.delivered_item_id = delivered_item_id

    # Method that gets all the delivery receipt pdfs
    @staticmethod
    def get_all_new_delivery_pdfs():
        # Import InventoryItem class
        from InventoryItemClass import InventoryItem

        # Initialise list to hold all delivery receipt pdfs
        all_delivery_pdfs = []
        # Call method in InventoryItem class that gets all supplier email addresses
        all_supplier_email_addresses = InventoryItem.get_all_supplier_email_addresses()

        # Iterate through each supplier email address
        for email_address in all_supplier_email_addresses:
            # # Call the method in Order class that gets all the unseen delivery receipt pdfs that are sent by the email address in current iteration
            pdfs = Order.get_pdfs_in_unseen_emails(email_address)
            if pdfs:
                # Append all the pdfs returned from get_pdfs_in_unseen_emails method to the all_delivery_pdfs list
                all_delivery_pdfs.append(pdfs)

        # Return list of all delivery receipt pdfs
        return all_delivery_pdfs

    # Methods that logs all new deliveries
    # Haven't commented as it has the exact same logic as log_all_new_sales
    @staticmethod
    def log_all_new_deliveries():
        all_delivery_pdfs = Delivery.get_all_new_delivery_pdfs()
        # If there is no delivery pdfs, do nothing
        if all_delivery_pdfs == [None] or all_delivery_pdfs == [[]] or all_delivery_pdfs == [[], [], []] or all_delivery_pdfs == [[], []]:
            pass
        # If there is delivery pdfs
        else:
            for pdf in all_delivery_pdfs:
                # Index into pdf
                pdf = pdf[0]
                pdf_text = Order.read_pdf_document(pdf)
                date_in_doc = Order.find_date_in_pdf(pdf_text)

                pdf_table_content = Order.read_table_in_pdf(pdf)

                for row in pdf_table_content:
                    delivered_item_id = int(row[0])
                    amount_delivered = int(row[2])

                    Delivery.log_individual_delivery(date_in_doc, amount_delivered, delivered_item_id)

    # Method for logging a single sale
    # Haven't commented as it has the exact same logic as log_individual_sale
    @staticmethod
    def log_individual_delivery(date_of_delivered, amount_delivered, delivered_item_id):
        new_sale = Delivery(date_of_delivered, amount_delivered, delivered_item_id)
        session.add(new_sale)
        session.commit()

        Delivery.update_current_level_from_delivery(amount_delivered, delivered_item_id)

    # Method that updates current inventory level in response to sales
    # Haven't commented as it has the exact same logic as update_current_level_from_sale
    @staticmethod
    def update_current_level_from_delivery(amount_delivered, delivered_item_id):
        from InventoryItemClass import InventoryItem

        item_sold = session.query(InventoryItem).filter(InventoryItem.id == delivered_item_id).first()

        current_level_before_deliveries = item_sold.current_level
        current_level_after_deliveries = current_level_before_deliveries + amount_delivered

        item_sold.current_level = current_level_after_deliveries
        session.commit()
