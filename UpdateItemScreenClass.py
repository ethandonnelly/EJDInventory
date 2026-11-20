import customtkinter
from Fonts import heading_font, normal_font, title_font
from InventoryItemClass import InventoryItem


class UpdateItemScreen(customtkinter.CTkFrame):
    # I am passing in root_frame so that it is placed into the root frame
    def __init__(self, root_frame, root):
        super().__init__(root_frame)
        self.root = root

        # == SCREEN GRID SETUP ==

        # Setting up the dimensions of the screen grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=20)
        self.grid_columnconfigure(0, weight=1)

        # == NAVIGATION BAR FRAME ==

        # Creating a frame that will hold the navigation bar
        self.navigation_bar_frame = customtkinter.CTkFrame(self)
        # Placing the navigation bar frame into the main grid
        self.navigation_bar_frame.grid(row=0, column=0, sticky="nesw")

        # Configuring the grid of the navigation bar so that it can hold the navigation buttons
        self.navigation_bar_frame.rowconfigure(0, weight=1)
        # 6 columns for the 6 different navigation buttons, so each get equal space
        self.navigation_bar_frame.columnconfigure((0, 1, 2, 3, 4, 5), weight=1)

        # == MAIN FRAME ==

        # Creating the main frame, this will hold everything else but the navigation buttons
        self.main_frame = customtkinter.CTkFrame(self)
        # Place the main frame into the main grid
        self.main_frame.grid(row=1, column=0, sticky="nesw")

        # Setting up the grid for the main frame like how the new item screen grid was normally
        self.main_frame.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12), weight=1)
        self.main_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10), weight=1)

        # = NAVIGATION BUTTONS =

        # Button to go to dashboard
        self.display_dashboard_button = customtkinter.CTkButton(self.navigation_bar_frame, text="Dashboard", font=normal_font, command=lambda: root.display_screen("dashboard_screen"))
        self.display_dashboard_button.grid(row=0, column=0, sticky="nesw")

        # Button to go to new item screen
        self.display_add_new_item_button = customtkinter.CTkButton(self.navigation_bar_frame, text="Add New Item", font=normal_font, command=lambda: root.display_screen("add_new_item_screen"))
        self.display_add_new_item_button.grid(row=0, column=1, sticky="nesw")

        # Title that tells the user they are currently on update item screen
        self.display_update_item_title = customtkinter.CTkLabel(self.navigation_bar_frame, text="Update Item Screen", font=title_font)
        self.display_update_item_title.grid(row=0, column=2, sticky="nesw")

        # Button to go to inventory report screen
        self.display_inventory_report_button = customtkinter.CTkButton(self.navigation_bar_frame, text="Inventory Report", font=normal_font, command=lambda: root.display_screen("inventory_report_screen"))
        self.display_inventory_report_button.grid(row=0, column=3, sticky="nesw")

        # Button to go to settings screen
        self.display_settings_button = customtkinter.CTkButton(self.navigation_bar_frame, text="Settings", font=normal_font, command=lambda: root.display_screen("settings_screen"))
        self.display_settings_button.grid(row=0, column=4, sticky="nesw")

        # Button to exit application
        self.exit_button = customtkinter.CTkButton(self.navigation_bar_frame, text="Exit", font=normal_font, fg_color="red", command=lambda: exit())
        self.exit_button.grid(row=0, column=5, sticky="nesw")

        # = UPDATE ITEM SCREEN CONTENTS =

        # == INVENTORY ITEM PICKER ==

        # This is where the user can choose what inventory item they want to see dashboard stats for

        # Heading that tells user to choose an inventory item
        self.choose_inventory_item_heading = customtkinter.CTkLabel(self.main_frame, text="Choose Inventory Item", font=heading_font)
        self.choose_inventory_item_heading.grid(row=1, column=0)

        # Create an item picker that holds an empty list
        self.inventory_item_picker = customtkinter.CTkOptionMenu(self.main_frame, values=[""], font=normal_font, dropdown_font=normal_font, width=300, command=self.display_content)
        self.inventory_item_picker.grid(row=2, column=0)


    # Method that updates picker options
    def update_picker_options(self):
        all_item_names = InventoryItem.query_all_inventory_item_names()
        # If the user has no items
        if all_item_names == []:
            # Get rid of the inventory item picker and choose inventory item label
            self.inventory_item_picker.grid_forget()
            self.choose_inventory_item_heading.grid_forget()
            # Output a message that says no items to update
            self.no_items_label = customtkinter.CTkLabel(self.main_frame, text="No Items To Update,\nAdd a New Item\nBefore Trying to\nUpdate", font=normal_font)
            self.no_items_label.grid(row=2, column=0)
        else:

            # If no items label exists
            if hasattr(self, "no_items_label"):
                # Remove the no_items_label
                self.no_items_label.grid_forget()

            # Re-grid heading
            self.choose_inventory_item_heading.grid(row=1, column=0)

            # Update the values in item picker from being an empty list to being the names just queried
            self.inventory_item_picker.configure(values=all_item_names)
            # Re-grid inventory item picker
            self.inventory_item_picker.grid(row=2, column=0)



    def display_content(self, item_name):

        item_id = InventoryItem.query_item_id(item_name)

        # == ITEM NAME ENTRY ==
        # Creating the Item Name entry and placing it in the window
        self.item_name_entry = customtkinter.CTkEntry(self.main_frame, height=70, width=300, placeholder_text="Enter Item Name", font=normal_font)
        self.item_name_entry.grid(row=1, column=2)

        # == ITEM DESCRIPTION ENTRY ==

        # Creating the "Enter Item Description" heading and placing it in the window
        self.item_description_label = customtkinter.CTkLabel(self.main_frame, text="Enter Item Description:", font=normal_font)
        self.item_description_label.grid(row=3, column=2)

        # Creating the item description entry box and placing it in the window
        self.item_description_box = customtkinter.CTkTextbox(self.main_frame, height=200, width=300, font=normal_font)
        self.item_description_box.grid(row=4, column=2)

        # == ITEM COST ENTRY ==

        # Creating the "Enter Item Cost" heading and placing it in the window
        self.item_cost_heading = customtkinter.CTkLabel(self.main_frame, text="Enter Item Cost", font=normal_font)
        self.item_cost_heading.grid(row=6, column=2)

        # Creating the item cost (pounds part) entry box and placing it in the window
        self.item_cost_pounds_entry = customtkinter.CTkEntry(self.main_frame, height=70, width=70, placeholder_text="£:", font=normal_font)
        self.item_cost_pounds_entry.grid(row=6, column=3)

        # Creating the decimal point and placing it in the window
        self.item_cost_decimal_point = customtkinter.CTkLabel(self.main_frame, text=".", font=("Arial", 150))
        self.item_cost_decimal_point.grid(row=6, column=4, sticky="n")

        # Creating the item cost (pence part) entry box and placing it in the window
        self.item_cost_pence_entry = customtkinter.CTkEntry(self.main_frame, height=70, width=70, placeholder_text="p:", font=normal_font)
        self.item_cost_pence_entry.grid(row=6, column=5)

        # == ITEM PRICE ENTRY ==

        # Creating the "Enter Item Price" heading and placing it in the window
        self.item_price_heading = customtkinter.CTkLabel(self.main_frame, text="Enter Item Price", font=normal_font)
        self.item_price_heading.grid(row=8, column=2)

        # Creating the item price (pounds part) entry box and placing it in the window
        self.item_price_pounds_entry = customtkinter.CTkEntry(self.main_frame, height=70, width=70, placeholder_text="£:", font=normal_font)
        self.item_price_pounds_entry.grid(row=8, column=3)

        # Creating the decimal point and placing it in the window
        self.item_price_decimal_point = customtkinter.CTkLabel(self.main_frame, text=".", font=("Arial", 150))
        self.item_price_decimal_point.grid(row=8, column=4, sticky="n")

        # Creating the item price (pence part) entry box and placing it in the window
        self.item_price_pence_entry = customtkinter.CTkEntry(self.main_frame, height=70, width=70, placeholder_text="p:", font=normal_font)
        self.item_price_pence_entry.grid(row=8, column=5)

        # == ITEM REORDER POINT ENTRY ==

        # Creating reorder point entry box and placing it in the window using the grid
        self.item_reorder_point_entry = customtkinter.CTkEntry(self.main_frame, height=70, width=300, placeholder_text="Enter Reorder Point", font=normal_font)
        self.item_reorder_point_entry.grid(row=1, column=7)

        # == ITEM MINIMUM POINT ENTRY ==

        # Creating minimum point entry box and placing it in the window using the grid
        self.item_min_point_entry = customtkinter.CTkEntry(self.main_frame, height=70, width=300, placeholder_text="Enter Min Level", font=normal_font)
        self.item_min_point_entry.grid(row=1, column=6)

        # == ITEM MAXIMUM POINT ENTRY ==

        # Creating maximum point entry box and placing it in the window using the grid
        self.item_max_point_entry = customtkinter.CTkEntry(self.main_frame, height=70, width=300, placeholder_text="Enter Max Level", font=normal_font)
        self.item_max_point_entry.grid(row=3, column=6)

        # == SUPPLIER EMAIL ENTRY ==

        # Creating supplier email entry box and placing it in the window using the grid
        self.supplier_email_entry = customtkinter.CTkEntry(self.main_frame, height=70, width=300, placeholder_text="Enter Supplier Email", font=normal_font)
        self.supplier_email_entry.grid(row=4, column=7)

        # == SAVE CHANGES BUTTON ==

        # Button that when pressed, calls the method that processes inputs and updates attributes
        self.save_changes_button = customtkinter.CTkButton(self.main_frame, text="Save Changes", font=normal_font, command=lambda: self.save_changes(item_id))
        self.save_changes_button.grid(row=5, column=8)

        # == DELETE ITEM ==
        # Button that when pressed, brings up another button that asks "Are You Sure?"
        self.delete_item_button = customtkinter.CTkButton(self.main_frame, text="Delete Item", font=normal_font, fg_color="red", hover_color="dark red", command=lambda: self.show_are_you_sure_button(item_name))
        self.delete_item_button.grid(row=5, column=10)


    def show_are_you_sure_button(self, item):
        # Heading that asks the user "Are You Sure?"
        are_you_sure_heading = customtkinter.CTkLabel(self.main_frame, text="Are You\nSure?", font=heading_font)
        are_you_sure_heading.grid(row=6, column=10)

        # Import InventoryItem class
        from InventoryItemClass import InventoryItem

        item_id = InventoryItem.query_item_id(item)
        # Button that when pressed, calls the delete item method from InventoryItem class
        yes_button = customtkinter.CTkButton(self.main_frame, text="Yes", font=normal_font, fg_color="red", hover_color="dark red", command=lambda: InventoryItem.delete_item(item_id))
        yes_button.grid(row=7, column=10)


    # Method that is called when "Save Changes" button is pressed
    def save_changes(self, item_id):
        # Clear any previous error messages from the grid
        for existing_error_message in self.main_frame.grid_slaves(row=8, column=8):
            existing_error_message.grid_forget()

        items_updated_message = "Updated: "


        # == ITEM NAME CHECK ==

        # If item name input exists
        if self.item_name_entry.get() != "":
            check = InventoryItem.check_name(self.item_name_entry.get())
            if check is True:
                InventoryItem.update_item_name(item_id, self.item_name_entry.get())
                # Append item name to the item updated message which will be displayed at the end
                items_updated_message += "\nItem Name"
            else:
                error_message = customtkinter.CTkLabel(self.main_frame, text=f"{check}", font=normal_font)
                error_message.grid(row=8, column=8)


        # == ITEM DESCRIPTION CHECK ==

        if self.item_description_box.get(0.0, "end-1c") != "":
            print(self.item_description_box.get(0.0, "end"))
            check = InventoryItem.check_description(self.item_description_box.get(0.0, "end"))
            if check is True:
                InventoryItem.update_item_description(item_id, self.item_description_box.get(0.0, "end"))
                items_updated_message += "\nItem Description"
            else:
                error_message = customtkinter.CTkLabel(self.main_frame, text=f"{check}", font=normal_font)
                error_message.grid(row=8, column=8)


        # == ITEM PRICE CHECK ==

        # If item price input exists
        if self.item_price_pounds_entry.get() != "":
            check = InventoryItem.check_money_values(self.item_price_pounds_entry.get(), self.item_price_pence_entry.get())
            if check is True:
                formatted_price = self.format_money(self.item_price_pounds_entry.get(), self.item_price_pence_entry.get())
                InventoryItem.update_item_price(item_id, formatted_price)
                items_updated_message += "\nItem Price"
            else:
                error_message = customtkinter.CTkLabel(self.main_frame, text=f"{check}", font=normal_font)
                error_message.grid(row=8, column=8)


        # == ITEM COST CHECK ==

        # If item cost input exists
        if self.item_cost_pounds_entry.get() != "":
            check = InventoryItem.check_money_values(self.item_cost_pounds_entry.get(), self.item_cost_pence_entry.get())
            if check is True:
                formatted_cost = self.format_money(self.item_cost_pounds_entry.get(), self.item_cost_pence_entry.get())
                InventoryItem.update_item_cost(item_id, formatted_cost)
                items_updated_message += "\nItem Cost"
            else:
                error_message = customtkinter.CTkLabel(self.main_frame, text=f"{check}", font=normal_font)
                error_message.grid(row=8, column=8)


        # == ITEM REORDER POINT CHECK ==

        # If item reorder point input exists
        if self.item_reorder_point_entry.get() != "":
            # Call the checking method
            check = InventoryItem.check_reorder_point(self.item_reorder_point_entry.get())
            # If check is valid, update the reorder point to be the input
            if check is True:
                InventoryItem.update_item_reorder_point(item_id, self.item_reorder_point_entry.get())
                items_updated_message += "\nItem Reorder Point"
            # If check isn't valid, output the error message
            else:
                error_message = customtkinter.CTkLabel(self.main_frame, text=f"{check}", font=normal_font)
                error_message.grid(row=8, column=8)


        # == ITEM MIN POINT CHECK ==

        # If item min point input exists
        if self.item_min_point_entry.get() != "":
            # Call the checking method
            check = InventoryItem.check_min_point(self.item_min_point_entry.get())
            # If check is valid, update the reorder point to be the input
            if check is True:
                InventoryItem.update_item_min_point(item_id, self.item_min_point_entry.get())
                items_updated_message += "\nItem Min Point"
            else:
                error_message = customtkinter.CTkLabel(self.main_frame, text=f"{check}", font=normal_font)
                error_message.grid(row=8, column=8)


        # == ITEM MAX POINT CHECK ==

        # If item max point input exists
        if self.item_max_point_entry.get() != "":
            # Call the checking method
            check = InventoryItem.check_max_point(self.item_max_point_entry.get())
            # If check is valid, update the reorder point to be the input
            if check is True:
                InventoryItem.update_item_max_point(item_id, self.item_max_point_entry.get())
                items_updated_message += "\nItem Max Point"
            # If check isn't valid, output the error message
            else:
                error_message = customtkinter.CTkLabel(self.main_frame, text=f"{check}", font=normal_font)
                error_message.grid(row=8, column=8)


        # == SUPPLIER EMAIL CHECK ==

        # If supplier email input exists
        if self.supplier_email_entry.get() != "":
            # Call the checking method
            check = InventoryItem.check_supplier_email(self.supplier_email_entry.get())
            # If check is valid, update the supplier email to be the input
            if check is True:
                InventoryItem.update_supplier_email(item_id, self.supplier_email_entry.get())
                items_updated_message += "\nSupplier Email"
            # If check isn't valid, output the error message
            else:
                error_message = customtkinter.CTkLabel(self.main_frame, text=f"{check}", font=normal_font)
                error_message.grid(row=8, column=8)


        self.items_updated_success_message = customtkinter.CTkLabel(self.main_frame, text=items_updated_message, font=normal_font)
        self.items_updated_success_message.grid(row=6, column=8)


    # Method that takes the pounds and pence part of the item cost or item price and formats it into a float
    def format_money(self, pounds, pence):
        money = f"{pounds}.{pence}"
        return float(money)
