import customtkinter
from Fonts import logo_font, title_font, heading_font, normal_font
from InventoryItemClass import InventoryItem

item_subcategory = None

class NewItemScreen(customtkinter.CTkFrame):
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

        # Button to go to dashboard screen
        self.display_dashboard_button = customtkinter.CTkButton(self.navigation_bar_frame, text="Dashboard", font=normal_font, command=lambda: root.display_screen("dashboard_screen"))
        self.display_dashboard_button.grid(row=0, column=0, sticky="nesw")

        # Heading that tells the user they are currently on adding new item screen
        self.add_new_item_heading = customtkinter.CTkLabel(self.navigation_bar_frame, text="Add New Item", font=heading_font)
        self.add_new_item_heading.grid(row=0, column=1, sticky="nesw")

        # Button to go to update item screen
        self.display_update_item_button = customtkinter.CTkButton(self.navigation_bar_frame, text="Update Existing Item", font=normal_font, command=lambda: root.display_screen("update_item_screen"))
        self.display_update_item_button.grid(row=0, column=2, sticky="nesw")

        # Button to go to inventory report screen
        self.display_inventory_report_button = customtkinter.CTkButton(self.navigation_bar_frame, text="Inventory Report", font=normal_font, command=lambda: root.display_screen("inventory_report_screen"))
        self.display_inventory_report_button.grid(row=0, column=3, sticky="nesw")

        # Button to go to settings screen
        self.display_settings_button = customtkinter.CTkButton(self.navigation_bar_frame, text="Settings", font=normal_font, command=lambda: root.display_screen("settings_screen"))
        self.display_settings_button.grid(row=0, column=4, sticky="nesw")

        # Button to exit application
        self.exit_button = customtkinter.CTkButton(self.navigation_bar_frame, text="Exit", font=normal_font, fg_color="red", command=lambda: exit())
        self.exit_button.grid(row=0, column=5, sticky="nesw")

        # = NEW ITEM SCREEN WIDGETS =

        # == ITEM NAME ENTRY ==

        # Creating the Item Name entry and placing it in the window
        self.item_name_entry = customtkinter.CTkEntry(self.main_frame, height=70, width=300, placeholder_text="Enter Item Name", font=normal_font)
        self.item_name_entry.grid(row=1, column=1)

        # == ITEM DESCRIPTION ENTRY ==

        # Creating the "Enter Item Description" heading and placing it in the window
        self.item_description_label = customtkinter.CTkLabel(self.main_frame, text="Enter Item Description:", font=normal_font)
        self.item_description_label.grid(row=3, column=1)

        # Creating the item description entry box and placing it in the window
        self.item_description_box = customtkinter.CTkTextbox(self.main_frame, height=200, width=300, font=normal_font)
        self.item_description_box.grid(row=4, column=1)

        # == ITEM COST ENTRY ==

        # Creating the "Enter Item Cost" heading and placing it in the window
        self.item_cost_heading = customtkinter.CTkLabel(self.main_frame, text="Enter Item Cost", font=normal_font)
        self.item_cost_heading.grid(row=6, column=1)

        # Creating the item cost (pounds part) entry box and placing it in the window
        self.item_cost_pounds_entry = customtkinter.CTkEntry(self.main_frame, height=70, width=70, placeholder_text="£:", font=normal_font)
        self.item_cost_pounds_entry.grid(row=6, column=2)

        # Creating the decimal point and placing it in the window
        self.item_cost_decimal_point = customtkinter.CTkLabel(self.main_frame, text=".", font=("Arial", 150))
        self.item_cost_decimal_point.grid(row=6, column=3, sticky="n")

        # Creating the item cost (pence part) entry box and placing it in the window
        self.item_cost_pence_entry = customtkinter.CTkEntry(self.main_frame, height=70, width=70, placeholder_text="p:", font=normal_font)
        self.item_cost_pence_entry.grid(row=6, column=4)

        # == ITEM PRICE ENTRY ==

        # Creating the "Enter Item Price" heading and placing it in the window
        self.item_price_heading = customtkinter.CTkLabel(self.main_frame, text="Enter Item Price", font=normal_font)
        self.item_price_heading.grid(row=8, column=1)

        # Creating the item price (pounds part) entry box and placing it in the window
        self.item_price_pounds_entry = customtkinter.CTkEntry(self.main_frame, height=70, width=70, placeholder_text="£:", font=normal_font)
        self.item_price_pounds_entry.grid(row=8, column=2)

        # Creating the decimal point and placing it in the window
        self.item_price_decimal_point = customtkinter.CTkLabel(self.main_frame, text=".", font=("Arial", 150))
        self.item_price_decimal_point.grid(row=8, column=3, sticky="n")

        # Creating the item price (pence part) entry box and placing it in the window
        self.item_price_pence_entry = customtkinter.CTkEntry(self.main_frame, height=70, width=70, placeholder_text="p:", font=normal_font)
        self.item_price_pence_entry.grid(row=8, column=4)

        # == ITEM REORDER POINT ENTRY ==

        # Creating reorder point entry box and placing it in the window using the grid
        self.item_reorder_point_entry = customtkinter.CTkEntry(self.main_frame, height=70, width=300, placeholder_text="Enter Reorder Point", font=normal_font)
        self.item_reorder_point_entry.grid(row=1, column=6)

        # == ITEM MINIMUM POINT ENTRY ==

        # Creating minimum point entry box and placing it in the window using the grid
        self.item_min_point_entry = customtkinter.CTkEntry(self.main_frame, height=70, width=300, placeholder_text="Enter Min Point", font=normal_font)
        self.item_min_point_entry.grid(row=1, column=5)

        # == ITEM MAXIMUM POINT ENTRY ==

        # Creating maximum point entry box and placing it in the window using the grid
        self.item_max_point_entry = customtkinter.CTkEntry(self.main_frame, height=70, width=300, placeholder_text="Enter Max Point", font=normal_font)
        self.item_max_point_entry.grid(row=3, column=5)

        # == ITEM CURRENT LEVEL ENTRY ==

        # Creating current level entry box and placing it in the window using the grid
        self.item_current_level_entry = customtkinter.CTkEntry(self.main_frame, height=70, width=300, placeholder_text="Enter Current Level", font=normal_font)
        self.item_current_level_entry.grid(row=3, column=6)

        # == SUPPLIER EMAIL ENTRY ==

        # Creating supplier email entry box and placing it in the window using the grid
        self.supplier_email_entry = customtkinter.CTkEntry(self.main_frame, height=70, width=300, placeholder_text="Enter Supplier Email", font=normal_font)
        self.supplier_email_entry.grid(row=4, column=6)

        # == CHOOSING INITIAL CATEGORY ==

        # The heading that lets the user know to choose a category
        self.choose_initial_category_heading = customtkinter.CTkLabel(self.main_frame, text="Choose Initial\nCategory:", font=normal_font)
        self.choose_initial_category_heading.grid(row=1, column=7)

        # List of initial categories
        self.initial_categories = ["Fashion and Apparel",
                                   "Home and Kitchen",
                                   "Leisure",
                                   "Technological",
                                   "Food and Beverage",
                                   "Books and Media",
                                   "Health and Beauty",
                                   "Construction",
                                   "Pharmaceuticals",
                                   "Automotive"]

        # The category picker widget
        self.initial_category_picker = customtkinter.CTkOptionMenu(self.main_frame,
                                                                   values=self.initial_categories,
                                                                   font=normal_font,
                                                                   dropdown_font=normal_font,
                                                                   command=self.choose_subcategory,
                                                                   width=300)
        self.initial_category_picker.grid(row=2, column=7)

        # == PROCEED BUTTON ==
        # Button that when pressed, calls the method that processes all the user's inputs and then creates the new item
        self.proceed_button = customtkinter.CTkButton(self.main_frame, text="Proceed", width=300, height=70, font=normal_font, command=self.process_inputs)
        self.proceed_button.grid(row=6, column=9)

    # Method that takes the pounds and pence part of the item cost or item price and formats it into a float
    def format_money(self, pounds, pence):
        money = f"{pounds}.{pence}"
        return float(money)

    # Method that gets all the inputs from the entry boxes and calls the checking methods from the logic file
    def process_inputs(self):

        # Setting the name_check variable as the result of the check_name method from the Inventory Item class in the logic file
        name_check = InventoryItem.check_name(self.item_name_entry.get())
        # If the item name is valid, move onto checking the item description
        if name_check is True:
            description_check = InventoryItem.check_description(self.item_description_box.get(0.0, "end"))

            if description_check is True:
                cost_check = InventoryItem.check_money_values(self.item_cost_pounds_entry.get(), self.item_cost_pence_entry.get())

                if cost_check is True:
                    # If item cost is valid, format the cost using the format_money method
                    formatted_cost = self.format_money(self.item_cost_pounds_entry.get(), self.item_cost_pence_entry.get())
                    price_check = InventoryItem.check_money_values(self.item_price_pounds_entry.get(), self.item_price_pence_entry.get())

                    if price_check is True:
                        # If item price is valid, format the price using the format_money method
                        formatted_price = self.format_money(self.item_price_pounds_entry.get(), self.item_price_pence_entry.get())
                        min_point_check = InventoryItem.check_min_point(self.item_min_point_entry.get())

                        if min_point_check is True:
                            max_point_check = InventoryItem.check_max_point(self.item_max_point_entry.get())

                            if max_point_check is True:
                                reorder_point_check = InventoryItem.check_reorder_point(self.item_reorder_point_entry.get())

                                if reorder_point_check is True:
                                    current_level_check = InventoryItem.check_current_level(self.item_current_level_entry.get())

                                    if current_level_check is True:
                                        supplier_email_check = InventoryItem.check_supplier_email(self.supplier_email_entry.get())

                                        if supplier_email_check is True:
                                            # If all inputs are valid
                                            # Get the item subcategory from the global variable
                                            global item_subcategory
                                            if item_subcategory is not None:

                                                # Call the method from the Inventory Item class in the logic file that creates a new inventory item
                                                InventoryItem.add_new_item(self.item_name_entry.get(),
                                                                           self.item_description_box.get(0.0, "end"),
                                                                           formatted_cost,
                                                                           formatted_price,
                                                                           self.item_current_level_entry.get(),
                                                                           self.item_reorder_point_entry.get(),
                                                                           self.item_min_point_entry.get(),
                                                                           self.item_max_point_entry.get(),
                                                                           item_subcategory,
                                                                           self.supplier_email_entry.get())

                                                # Then display the dashboard to the user
                                                self.root.display_screen("dashboard_screen")
                                            else:
                                                for existing_error_message in self.main_frame.grid_slaves(row=7, column=9):
                                                    existing_error_message.grid_forget()
                                                sub_category_error_message = customtkinter.CTkLabel(self.main_frame, text="Item sub-category\nneeds to\nbe present", font=normal_font)
                                                sub_category_error_message.grid(row=7, column=9)

                                        else:
                                            for existing_error_message in self.main_frame.grid_slaves(row=7, column=9):
                                                existing_error_message.grid_forget()
                                            supplier_email_error_message = customtkinter.CTkLabel(self.main_frame, text=supplier_email_check, font=normal_font)
                                            supplier_email_error_message.grid(row=7, column=9)
                                    else:
                                        for existing_error_message in self.main_frame.grid_slaves(row=7, column=9):
                                            existing_error_message.grid_forget()
                                        current_level_error_message = customtkinter.CTkLabel(self.main_frame, text=current_level_check, font=normal_font)
                                        current_level_error_message.grid(row=7, column=9)

                                else:
                                    for existing_error_message in self.main_frame.grid_slaves(row=7, column=9):
                                        existing_error_message.grid_forget()
                                    reorder_point_error_message = customtkinter.CTkLabel(self.main_frame, text=reorder_point_check, font=normal_font)
                                    reorder_point_error_message.grid(row=7, column=9)

                            else:
                                for existing_error_message in self.main_frame.grid_slaves(row=7, column=9):
                                    existing_error_message.grid_forget()
                                max_point_error_message = customtkinter.CTkLabel(self.main_frame, text=max_point_check, font=normal_font)
                                max_point_error_message.grid(row=7, column=9)

                        else:
                            for existing_error_message in self.main_frame.grid_slaves(row=7, column=9):
                                existing_error_message.grid_forget()
                            min_point_error_message = customtkinter.CTkLabel(self.main_frame, text=min_point_check, font=normal_font)
                            min_point_error_message.grid(row=7, column=9)

                    else:
                        for existing_error_message in self.main_frame.grid_slaves(row=7, column=9):
                            existing_error_message.grid_forget()
                        price_error_message = customtkinter.CTkLabel(self.main_frame, text=price_check, font=normal_font)
                        price_error_message.grid(row=7, column=9)

                else:
                    for existing_error_message in self.main_frame.grid_slaves(row=7, column=9):
                        existing_error_message.grid_forget()
                    cost_error_message = customtkinter.CTkLabel(self.main_frame, text=cost_check, font=normal_font)
                    cost_error_message.grid(row=7, column=9)

            else:
                for existing_error_message in self.main_frame.grid_slaves(row=7, column=9):
                    existing_error_message.grid_forget()
                description_error_message = customtkinter.CTkLabel(self.main_frame, text=description_check, font=normal_font)
                description_error_message.grid(row=7, column=9)

        else:
            for existing_error_message in self.main_frame.grid_slaves(row=7, column=9):
                existing_error_message.grid_forget()
            name_error_message = customtkinter.CTkLabel(self.main_frame, text=name_check, font=normal_font)
            name_error_message.grid(row=7, column=9)

    # == CHOOSING SUB-CATEGORY ==

    def choose_subcategory(self, initial_choice):
        # Heading that tells user to pick a sub-category
        choose_subcategory_heading = customtkinter.CTkLabel(self.main_frame, text="Choose\nSub-Category:", font=normal_font)
        choose_subcategory_heading.grid(row=7, column=7)

        # If the initial category choice which was passed in as a parameter is Fashion and Apparel
        if initial_choice == "Fashion and Apparel":
            # Show the sub-category picker that has the sub-category options for fashion and apparel
            fa_sub_categories = ["Clothing", "Footwear", "Jewelry"]
            fa_sub_category_picker = customtkinter.CTkOptionMenu(self.main_frame, values=fa_sub_categories, font=normal_font, dropdown_font=normal_font, width=300, command=self.set_global_item_subcategory)
            fa_sub_category_picker.grid(row=8, column=7)

        elif initial_choice == "Home and Kitchen":
            hk_sub_categories = ["Furniture/Furnishings", "Kitchenware", "Home Decor" "Appliances"]
            hk_sub_category_picker = customtkinter.CTkOptionMenu(self.main_frame, values=hk_sub_categories, font=normal_font, dropdown_font=normal_font, width=300, command=self.set_global_item_subcategory)
            hk_sub_category_picker.grid(row=8, column=7)

        elif initial_choice == "Leisure":
            l_sub_categories = ["Toys", "Games", "Sporting/Outdoor Goods"]
            l_sub_category_picker = customtkinter.CTkOptionMenu(self.main_frame, values=l_sub_categories, font=normal_font, dropdown_font=normal_font, width=300, command=self.set_global_item_subcategory)
            l_sub_category_picker.grid(row=8, column=7)

        elif initial_choice == "Technological":
            t_sub_categories = ["Computers", "Mobile Phones", "TV's", "Accessories"]
            t_sub_category_picker = customtkinter.CTkOptionMenu(self.main_frame, values=t_sub_categories, font=normal_font, dropdown_font=normal_font, width=300, command=self.set_global_item_subcategory)
            t_sub_category_picker.grid(row=8, column=7)

        elif initial_choice == "Food and Beverage":
            fb_sub_categories = ["Short-Expiry Food", "Moderate-Expiry Food", "Long-Expiry Food", "Short-Expiry Beverage", "Moderate-Expiry Beverage", "Long-Expiry Beverage"]
            fb_sub_category_picker = customtkinter.CTkOptionMenu(self.main_frame, values=fb_sub_categories, font=normal_font, dropdown_font=normal_font, width=300, command=self.set_global_item_subcategory)
            fb_sub_category_picker.grid(row=8, column=7)

        elif initial_choice == "Books and Media":
            bm_sub_categories = ["Books", "Music", "Movies"]
            bm_sub_category_picker = customtkinter.CTkOptionMenu(self.main_frame, values=bm_sub_categories, font=normal_font, dropdown_font=normal_font, width=300, command=self.set_global_item_subcategory)
            bm_sub_category_picker.grid(row=8, column=7)

        elif initial_choice == "Health and Beauty":
            hb_sub_categories = ["Skincare", "Cosmetics", "Accessories"]
            hb_sub_category_picker = customtkinter.CTkOptionMenu(self.main_frame, values=hb_sub_categories, font=normal_font, dropdown_font=normal_font, width=300, command=self.set_global_item_subcategory)
            hb_sub_category_picker.grid(row=8, column=7)

        elif initial_choice == "Construction":
            c_sub_categories = ["Construction Materials", "Construction Accessories", "Construction Tools"]
            c_sub_category_picker = customtkinter.CTkOptionMenu(self.main_frame, values=c_sub_categories, font=normal_font, dropdown_font=normal_font, width=300, command=self.set_global_item_subcategory)
            c_sub_category_picker.grid(row=8, column=7)

        elif initial_choice == "Pharmaceuticals":
            p_sub_categories = ["General Sale Medicines", "Pharmacy Medicines", "Prescription Only Medicines"]
            p_sub_category_picker = customtkinter.CTkOptionMenu(self.main_frame, values=p_sub_categories, font=normal_font, dropdown_font=normal_font, width=300, command=self.set_global_item_subcategory)
            p_sub_category_picker.grid(row=8, column=7)

        elif initial_choice == "Automotive":
            a_sub_categories = ["Vehicles", "Automotive Parts/Accessories", "Maintenance Tools"]
            a_sub_category_picker = customtkinter.CTkOptionMenu(self.main_frame, values=a_sub_categories, font=normal_font, dropdown_font=normal_font, width=300, command=self.set_global_item_subcategory)
            a_sub_category_picker.grid(row=8, column=7)

    # Method that sets the global variable item subcategory
    def set_global_item_subcategory(self, sub_category_choice):
        # Takes sub-category choice that was passed in as a parameter and sets the value of the global variable to it
        global item_subcategory
        item_subcategory = sub_category_choice
