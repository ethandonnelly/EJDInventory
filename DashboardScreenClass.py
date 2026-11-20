import customtkinter
from Fonts import heading_font, normal_font, title_font
from InventoryItemClass import InventoryItem
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class DashboardScreen(customtkinter.CTkFrame):
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

        # Title that tells the user they are currently on dashboard screen
        self.dashboard_title = customtkinter.CTkLabel(self.navigation_bar_frame, text="Dashboard", font=title_font)
        self.dashboard_title.grid(row=0, column=0, sticky="nesw")

        # Button to go to new item screen
        self.display_add_new_item_button = customtkinter.CTkButton(self.navigation_bar_frame, text="Add New Item", font=normal_font, command=lambda: root.display_screen("add_new_item_screen"))
        self.display_add_new_item_button.grid(row=0, column=1, sticky="nesw")

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

        # = DASHBOARD CONTENTS =

        # == INVENTORY ITEM PICKER ==

        # This is where the user can choose what inventory item they want to see dashboard stats for

        # Heading that tells user to choose an inventory item
        self.choose_inventory_item_heading = customtkinter.CTkLabel(self.main_frame, text="Choose\nInventory Item", font=heading_font)
        self.choose_inventory_item_heading.grid(row=1, column=0)

        # Create an item picker that holds an empty list
        self.inventory_item_picker = customtkinter.CTkOptionMenu(self.main_frame, values=[""], font=normal_font, dropdown_font=normal_font, width=300, command=self.display_dashboard_content)
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
            self.no_items_label = customtkinter.CTkLabel(self.main_frame, text="No Items To View,\nAdd a New Item First", font=normal_font)
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




    def display_dashboard_content(self, chosen_item):

        # == GET ITEM ID ==
        # This gets the item id of the item name that was chosen in the picker
        item_id = InventoryItem.query_item_id(chosen_item)

        # = DASHBOARD CONTENTS =

        # == ITEM CURRENT LEVEL ==

        # Item current level heading
        item_current_level_heading = customtkinter.CTkLabel(self.main_frame, text="Item\nCurrent Level:", font=heading_font)
        item_current_level_heading.grid(row=3, column=0)


        # Item current level value
        item_current_level = InventoryItem.query_current_level(item_id)
        item_current_level_value_label = customtkinter.CTkLabel(self.main_frame, text=f"  {item_current_level}  ", font=normal_font)
        item_current_level_value_label.grid(row=4, column=0)

        # == ITEM FORECAST ==

        # Import Forecast class
        from ForecastClass import Forecast

        # == ITEM FORECAST ==

        # Create instance
        forecast = Forecast(item_id)

        # === SETTING METHODS ===
        forecast.set_end_year_and_month()
        forecast.set_start_year_and_month()
        forecast.set_smoothing_factor()

        # === CURRENT MONTH FORECAST VALUE ===

        current_month_forecast_heading = customtkinter.CTkLabel(self.main_frame, text="Sales Forecast\n(Current Month):", font=heading_font)
        current_month_forecast_heading.grid(row=1, column=2)

        # Get the value that will be displayed
        remaining_current_month_forecast = forecast.get_remaining_current_month_forecast()

        # Put the value into the text
        forecast_text = f"Total Discounting Sales\nThat Have Already\nOccurred This Month: {remaining_current_month_forecast}  "
        # Put the text into a label
        current_month_forecast_value_label = customtkinter.CTkLabel(self.main_frame, text=forecast_text, font=normal_font)
        # Place the label into the GUI
        current_month_forecast_value_label.grid(row=2, column=2)

        # === NEXT MONTH FORECAST VALUE ===

        next_month_forecast_heading = customtkinter.CTkLabel(self.main_frame, text="Sales Forecast\n(Next Month):", font=heading_font)
        next_month_forecast_heading.grid(row=3, column=2)

        # Get the value that will be displayed
        next_month_forecast_value = forecast.calculate_next_month_forecast_value()

        # Put the value into a label
        next_month_forecast_value_label = customtkinter.CTkLabel(self.main_frame, text=next_month_forecast_value, font=normal_font)
        # Place the label onto the screen
        next_month_forecast_value_label.grid(row=4, column=2)

        # === INVENTORY LEVEL RECOMMENDATION ===

        if isinstance(remaining_current_month_forecast, str):
            current_month_recommendation = remaining_current_month_forecast
            next_month_recommendation = next_month_forecast_value
        else:
            current_month_recommendation = InventoryItem.create_inventory_recommendation_for_current_month(item_current_level, remaining_current_month_forecast)
            next_month_recommendation = InventoryItem.create_inventory_recommendation_for_next_month(item_current_level, next_month_forecast_value)

        current_month_recommendation_heading = customtkinter.CTkLabel(self.main_frame, text="Inventory\nRecommendation\n(This Month):", font=heading_font)
        current_month_recommendation_heading.grid(row=1, column=3)

        current_month_recommendation_label = customtkinter.CTkLabel(self.main_frame, text=current_month_recommendation, font=normal_font)
        current_month_recommendation_label.grid(row=2, column=3)

        next_month_recommendation_heading = customtkinter.CTkLabel(self.main_frame, text="Inventory\nRecommendation\n(Next Month):", font=heading_font)
        next_month_recommendation_heading.grid(row=3, column=3)

        next_month_recommendation_label = customtkinter.CTkLabel(self.main_frame, text=next_month_recommendation, font=normal_font)
        next_month_recommendation_label.grid(row=4, column=3)

        # == SALES GRAPH ==
        from GraphClass import Graph

        # === GRAPH HEADING ===
        sales_graph_heading = customtkinter.CTkLabel(self.main_frame, text="Sales Graph (Past Year):", font=heading_font)
        sales_graph_heading.grid(row=4, column=7)

        # === GETTING THE VALUES TO PUT INTO GRAPH ===

        # Get the corresponding month names for the past 12 months including the forecasted value for current month
        if isinstance(remaining_current_month_forecast, str):
            end_month_and_year_of_graph = (forecast.end_month, forecast.end_year)
        else:
            end_month_and_year_of_graph = forecast.get_graph_end_month_and_year()
        each_month_names = forecast.list_all_month_names(end_month_and_year_of_graph[0], end_month_and_year_of_graph[1])
        # Get the corresponding sales for the past 12 months from month previous to current month
        each_month_sales = forecast.list_total_sales_for_all_months()

        total_current_month_forecast = forecast.get_current_month_forecast_value()
        # Add the two forecasted values to the sales values for graph
        if not isinstance(total_current_month_forecast, str):
            each_month_sales.append(total_current_month_forecast)
            each_month_sales.append(next_month_forecast_value)

        # === PLOTTING THE GRAPH ===

        # Create the instance of Graph class using the month names and month sales
        sales_graph = Graph(each_month_names, each_month_sales)
        sales_graph.plot()

        # === PUTTING GRAPH INTO GUI ===

        # Creating a canvas to hold the graph
        canvas = FigureCanvasTkAgg(sales_graph.figure, master=self.main_frame)
        canvas.draw()
        # Placing the canvas in the grid
        canvas.get_tk_widget().grid(row=5, column=7)
