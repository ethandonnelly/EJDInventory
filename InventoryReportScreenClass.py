import customtkinter
from Fonts import logo_font, title_font, heading_font, normal_font
from InventoryItemClass import InventoryItem
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class InventoryReportScreen(customtkinter.CTkFrame):
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

        # Button to go to add new item screen
        self.display_new_item_screen_button = customtkinter.CTkButton(self.navigation_bar_frame, text="Add New Item", font=normal_font, command=lambda: root.display_screen("add_new_item_screen"))
        self.display_new_item_screen_button.grid(row=0, column=1, sticky="nesw")

        # Button to go to update item screen
        self.display_update_item_button = customtkinter.CTkButton(self.navigation_bar_frame, text="Update Existing Item", font=normal_font, command=lambda: root.display_screen("update_item_screen"))
        self.display_update_item_button.grid(row=0, column=2, sticky="nesw")

        # Heading that tells the user they are currently on inventory report screen
        self.add_new_item_heading = customtkinter.CTkLabel(self.navigation_bar_frame, text="Inventory Report", font=title_font)
        self.add_new_item_heading.grid(row=0, column=3, sticky="nesw")

        # Button to go to settings screen
        self.display_settings_button = customtkinter.CTkButton(self.navigation_bar_frame, text="Settings", font=normal_font, command=lambda: root.display_screen("settings_screen"))
        self.display_settings_button.grid(row=0, column=4, sticky="nesw")

        # Button to exit application
        self.exit_button = customtkinter.CTkButton(self.navigation_bar_frame, text="Exit", font=normal_font, fg_color="red", command=lambda: exit())
        self.exit_button.grid(row=0, column=5, sticky="nesw")


        # == INVENTORY ITEM PICKER ==

        # Heading that tells user to choose an inventory item
        self.choose_inventory_item_heading = customtkinter.CTkLabel(self.main_frame, text="Choose\nInventory\nItem", font=heading_font)
        self.choose_inventory_item_heading.grid(row=0, column=0)

        # Create an item picker that holds an empty list
        self.inventory_item_picker = customtkinter.CTkOptionMenu(self.main_frame, values=[""], font=normal_font, dropdown_font=normal_font, width=300, command=self.display_inventory_report_content)
        self.inventory_item_picker.grid(row=1, column=0)


    # Method that updates picker options when screen is opened
    def update_picker_options(self):
        all_item_names = InventoryItem.query_all_inventory_item_names()
        # If the user has no items
        if all_item_names == []:
            # Get rid of the inventory item picker and choose inventory item label
            self.inventory_item_picker.grid_forget()
            self.choose_inventory_item_heading.grid_forget()
            # Output a message that says no items to update
            self.no_items_label = customtkinter.CTkLabel(self.main_frame, text="No Items To Update\nAdd a New Item\nBefore Trying to\nUpdate", font=normal_font)
            self.no_items_label.grid(row=1, column=0)
        else:

            # If no items label exists
            if hasattr(self, "no_items_label"):
                # Remove the no_items_label
                self.no_items_label.grid_forget()

            # Re-grid heading
            self.choose_inventory_item_heading.grid(row=0, column=0)

            # Update the values in item picker from being an empty list to being the names just queried
            self.inventory_item_picker.configure(values=all_item_names)
            # Re-grid inventory item picker
            self.inventory_item_picker.grid(row=1, column=0)


    def display_inventory_report_content(self, item):
        from InventoryItemClass import InventoryItem
        from ForecastClass import Forecast
        from GraphClass import Graph

        # === GET ITEM ID ===
        # Query item id using the method
        item_id = InventoryItem.query_item_id(item)

        # === GETTING EACH MONTH NAME AND EACH MONTH SALES ===

        # Creating an instance of the forecast class so that I can use the list_total_sales
        forecast = Forecast(item_id)
        # Setting methods
        forecast.set_end_year_and_month()
        forecast.set_start_year_and_month()

        # Get all sales that have happened in timeframe
        each_month_sales = forecast.list_total_sales_for_all_months()
        # Get all names of months within timeframe
        each_month_names = forecast.list_all_month_names(forecast.end_month, forecast.end_year)


        # == REVENUE VALUE ==

        revenue_value_heading = customtkinter.CTkLabel(self.main_frame, text="Total Revenue\n(Past Year):", font=heading_font)
        revenue_value_heading.grid(row=1, column=3)

        # Calculate a revenue value for each month in timeframe
        each_month_revenue_values = InventoryItem.list_all_months_revenue(item_id, each_month_sales)

        # Calculating the total revenue using the monthly revenue figures
        total_revenue_value = InventoryItem.calculate_total_revenue(each_month_revenue_values)

        # Placing the total revenue value into the GUI
        revenue_value_label = customtkinter.CTkLabel(self.main_frame, text=f"  {total_revenue_value}  ", font=normal_font)
        revenue_value_label.grid(row=2, column=3)

        # == REVENUE GRAPH ==

        revenue_graph_heading = customtkinter.CTkLabel(self.main_frame, text="Revenue Graph\n(Past Year):", font=heading_font)
        revenue_graph_heading.grid(row=3, column=3)

        # Create an instance of Graph class for revenue graph
        revenue_graph = Graph(each_month_names, each_month_revenue_values)
        # Plot the graph
        revenue_graph.plot()

        # Create a canvas to place the revenue graph into
        canvas = FigureCanvasTkAgg(revenue_graph.figure, master=self.main_frame)
        canvas.draw()
        # Place the canvas into the screen grid
        canvas.get_tk_widget().grid(row=4, column=3)


        # == COST OF GOODS SOLD VALUE ==

        cogs_value_heading = customtkinter.CTkLabel(self.main_frame, text="Total Cost of Goods Sold\n(Past Year):", font=heading_font)
        cogs_value_heading.grid(row=1, column=5)

        # Calculate a cost of goods sold value for each month in timeframe
        each_month_cogs_values = InventoryItem.list_all_months_cogs(item_id, each_month_sales)

        # Calculating the total cost of goods sold using the monthly cogs figures
        total_cogs_value = InventoryItem.calculate_total_cogs(each_month_cogs_values)

        # Placing the total cogs value into the GUI
        cogs_value_label = customtkinter.CTkLabel(self.main_frame, text=f"  {total_cogs_value}  ", font=normal_font)
        cogs_value_label.grid(row=2, column=5)

        # == COST OF GOODS SOLD GRAPH ==

        cogs_graph_heading = customtkinter.CTkLabel(self.main_frame, text="Cost of Goods Sold Graph\n(Past Year):", font=heading_font)
        cogs_graph_heading.grid(row=3, column=5)

        # Create an instance of Graph class for cost of goods sold graph
        cogs_graph = Graph(each_month_names, each_month_cogs_values)
        # Plot the graph
        cogs_graph.plot()

        # Create canvas to be able to place the graph into the GUI
        canvas = FigureCanvasTkAgg(cogs_graph.figure, master=self.main_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=4, column=5)


        # == GROSS PROFIT VALUE ==

        gross_profit_value_heading = customtkinter.CTkLabel(self.main_frame, text="Total Gross Profit\n(Past Year):", font=heading_font)
        gross_profit_value_heading.grid(row=1, column=7)

        # Calculate a gross profit value for each month in timeframe
        each_month_gross_profit_values = InventoryItem.list_all_months_gross_profit(each_month_revenue_values, each_month_cogs_values)

        # Calculate total gross profit using the monthly gross profit figures
        total_gross_profit_value = InventoryItem.calculate_total_gross_profit(each_month_gross_profit_values)

        # Place the total gross profit value into the GUI
        gross_profit_value_label = customtkinter.CTkLabel(self.main_frame, text=f"  {total_gross_profit_value}  ", font=normal_font)
        gross_profit_value_label.grid(row=2, column=7)

        # == GROSS PROFIT GRAPH ==

        gross_profit_graph_heading = customtkinter.CTkLabel(self.main_frame, text="Gross Profit Graph\n(Past Year):", font=heading_font)
        gross_profit_graph_heading.grid(row=3, column=7)

        gross_profit_graph = Graph(each_month_names, each_month_gross_profit_values)
        gross_profit_graph.plot()

        canvas = FigureCanvasTkAgg(gross_profit_graph.figure, master=self.main_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=4, column=7)
