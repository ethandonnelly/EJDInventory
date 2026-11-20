

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from DatabaseSetup import session, AbstractBase


# = INVENTORY ITEM CLASS =

# Creating the Inventory Item class, it inherits from Base class
class InventoryItem(AbstractBase):
    # Setting name of table to "inventory items"
    __tablename__ = "inventory_items"

    # == INITIALISING ALL FIELDS ==

    name: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    cost: Mapped[float] = mapped_column()
    price: Mapped[float] = mapped_column()
    current_level: Mapped[int] = mapped_column()
    reorder_point: Mapped[int] = mapped_column()
    min_point: Mapped[int] = mapped_column()
    max_point: Mapped[int] = mapped_column()
    category: Mapped[str] = mapped_column()
    supplier_email: Mapped[str] = mapped_column()

    # == CREATING RELATIONSHIP WITH USER ==

    # Setting up relationship
    user: Mapped["User"] = relationship(back_populates="users_inventory_items")
    # Setting user id as the foreign key
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    # == SETTING UP RELATIONSHIP BETWEEN INVENTORY ITEM AND SALE ==
    # Setting up one-to-many relationship by passing in list
    sale: Mapped[list["Sale"]] = relationship(back_populates="inventory_item")

    # == SETTING UP RELATIONSHIP BETWEEN INVENTORY ITEM AND DELIVERY ==
    # Setting up one-to-many relationship by passing in list
    delivery: Mapped[list["Delivery"]] = relationship(back_populates="inventory_item")

    # == INITIALISING ALL ATTRIBUTES ==

    def __init__(self, name, description, cost, price, current_level, reorder_point, min_point, max_point, category, supplier_email, user_id):
        self.name = name
        self.description = description
        self.cost = cost
        self.price = price
        self.current_level = current_level
        self.reorder_point = reorder_point
        self.min_point = min_point
        self.max_point = max_point
        self.category = category
        self.supplier_email = supplier_email
        self.user_id = user_id

    # == CHECKING METHODS ==

    # Static method that checks the input for item name
    @staticmethod
    def check_name(item_name):
        # Presence Check
        if item_name != "":
            # Alphanumeric Check
            if item_name.isalnum() is True:
                # Length Check
                if 3 <= len(item_name) <= 40:
                    return True
                else:
                    return "Item name needs\nto be between\n3 and 40 characters"
            else:
                return "Item name needs\nto be only letters\nor numbers"
        else:
            return "Item name\nneeds to\nbe present"

    # Static method that checks the input for item description
    @staticmethod
    def check_description(item_description):
        # Presence Check
        if item_description != "":
            # Length Check
            if 1 < len(item_description) < 2000:
                return True
            else:
                return "Item description\nhas to be between 1\nand 2000 characters"
        else:
            return "Item description\ncan't be\nleft blank"

    # Static method that checks the input for item price and item cost
    @staticmethod
    def check_money_values(pounds, pence):
        # Presence check for pounds
        if pounds != "":
            # Number check for pounds
            if pounds.isnumeric():
                # Length check for pounds
                if len(pounds) <= 7:
                    # Presence check for pence
                    if pence != "":
                        # Number check for pence
                        if pence.isnumeric():
                            # Length check for pence
                            if len(pence) == 2:
                                return True
                            else:
                                return "Please enter two\nvalues for pence\ne.g. PP.25"
                        else:
                            return "Please enter\na number(s)\n for pence"
                    else:
                        return "Please enter\na number(s)\nfor pence"
                else:
                    return "Please enter\na pound value\nless than 8 0's"
            else:
                return "Please enter\na number(s)\nfor pounds"
        else:
            return "Please enter\na number(s)\nfor pounds"

    # Static method that checks the input for current level
    @staticmethod
    def check_current_level(current_level):
        # Presence check
        if current_level != "":
            # Only number check
            if current_level.isnumeric():
                return True
            else:
                return "Please enter an\ninteger value for\nCurrent Level"
        else:
            return "Please enter a\nvalue for\nCurrent Level"

    # Static method that checks the input for reorder point
    @staticmethod
    def check_reorder_point(reorder_point):
        # Presence check
        if reorder_point != "":
            # Only number check
            if reorder_point.isnumeric():
                return True
            else:
                return "Please enter an\ninteger value for\nReorder Point"
        else:
            return "Please enter a\nvalue for\nReorder Point"

    # Static method that checks the input for min point
    @staticmethod
    def check_min_point(min_point):
        # Presence check
        if min_point != "":
            # Only number check
            if min_point.isnumeric():
                return True
            else:
                return "Please enter an\ninteger value\nfor Min Point"
        else:
            return "Please enter a\nvalue for\nMin Point"

    # Static method that checks the input for max point
    @staticmethod
    def check_max_point(max_point):
        # Presence check
        if max_point != "":
            # Only number check
            if max_point.isnumeric():
                return True
            else:
                return "Please enter an\ninteger value for\nMax Point"
        else:
            return "Please enter a\nvalue for\nMax Point"

    # Static method that checks the input for supplier email
    @staticmethod
    def check_supplier_email(supplier_email):
        # Presence check
        if supplier_email != "":
            # Length check
            if 4 <= len(supplier_email) <= 254:
                # Email format check
                if "@" in supplier_email:
                    return True
                else:
                    return "Supplier Email\nneeds @"
            else:
                return "Supplier Email needs\nto be between 4\nand 254 characters"
        else:
            return "Supplier Email\nneeds to be\npresent"

    # Method for adding new item
    @staticmethod
    def add_new_item(name, description, cost, price, current_level, reorder_point, min_point, max_point, category, supplier_email):
        # Import current_user_id global from UserClass.py
        from UserClass import current_user_id
        # Create new instance of Inventory Item class
        new_item = InventoryItem(name, description, cost, price, current_level, reorder_point, min_point, max_point, category, supplier_email, current_user_id)
        # Add the new item to the database
        session.add(new_item)
        # Commit the change
        session.commit()

    @staticmethod
    def query_item_id(item_name):
        from UserClass import current_user_id
        item_id = session.query(InventoryItem.id).filter(InventoryItem.name == item_name, InventoryItem.user_id == current_user_id).scalar()
        return item_id

    @staticmethod
    def get_item_name(item_id):
        item_name = session.query(InventoryItem.name).filter(InventoryItem.id == item_id).scalar()
        return item_name

    @staticmethod
    def get_suppliers_email(item_id):
        suppliers_email = session.query(InventoryItem.supplier_email).filter(InventoryItem.id == item_id).scalar()
        return suppliers_email

    # == UPDATE ITEM LOGIC ==

    # Method that queries all the inventory items a user has
    @staticmethod
    def query_all_inventory_item_names_old1():
        from UserClass import current_user_id

        all_items = session.query(InventoryItem.name).filter(InventoryItem.user_id == current_user_id).all()
        return all_items

    # Method that queries all the inventory items a user has
    @staticmethod
    def query_all_inventory_item_names():
        from UserClass import current_user_id
        all_items = session.query(InventoryItem.name).filter(InventoryItem.user_id == current_user_id).all()
        # Index into each item and add each item to a list
        items = [i[0] for i in all_items]
        return items

    @staticmethod
    def get_reorder_point(item_id):
        return session.query(InventoryItem.reorder_point).filter(InventoryItem.id == item_id).scalar()

    @staticmethod
    def get_min_point(item_id):
        return session.query(InventoryItem.min_point).filter(InventoryItem.id == item_id).scalar()

    @staticmethod
    def get_max_point(item_id):
        return session.query(InventoryItem.max_point).filter(InventoryItem.id == item_id).scalar()

    @staticmethod
    def update_item_name(item_id, new_item_name):
        # Query item
        item = session.query(InventoryItem).filter(InventoryItem.id == item_id).first()
        # Change item name to the item name just inputted
        item.name = new_item_name
        # Commit the change
        session.commit()

    @staticmethod
    def update_item_description(item_id, new_item_description):
        item = session.query(InventoryItem).filter(InventoryItem.id == item_id).first()
        item.description = new_item_description
        session.commit()

    @staticmethod
    def update_item_cost(item_id, new_item_cost):
        item = session.query(InventoryItem).filter(InventoryItem.id == item_id).first()
        item.cost = new_item_cost
        session.commit()

    @staticmethod
    def update_item_price(item_id, new_item_price):
        item = session.query(InventoryItem).filter(InventoryItem.id == item_id).first()
        item.price = new_item_price
        session.commit()

    @staticmethod
    def update_item_reorder_point(item_id, new_reorder_point):
        item = session.query(InventoryItem).filter(InventoryItem.id == item_id).first()
        item.reorder_point = new_reorder_point
        session.commit()

    @staticmethod
    def update_item_min_point(item_id, new_min_point):
        item = session.query(InventoryItem).filter(InventoryItem.id == item_id).first()
        item.min_point = new_min_point
        session.commit()

    @staticmethod
    def update_item_max_point(item_id, new_item_max_point):
        item = session.query(InventoryItem).filter(InventoryItem.id == item_id).first()
        item.max_point = new_item_max_point
        session.commit()

    @staticmethod
    def update_supplier_email(item_id, new_supplier_email):
        item = session.query(InventoryItem).filter(InventoryItem.id == item_id).first()
        item.supplier_email = new_supplier_email
        session.commit()

    @staticmethod
    def delete_item(item_id):

        # Delete all the sales associated with that item
        from UpdateCurrentLevelClasses import Sale
        Sale.delete_all_sales_for_an_item(item_id)

        # Delete all the deliveries associated with that item
        from UpdateCurrentLevelClasses import Delivery
        Delivery.delete_all_deliveries_for_an_item(item_id)

        # Now all sales and deliveries have been deleted, the inventory item can be deleted
        item = session.query(InventoryItem).filter(InventoryItem.id == item_id).first()
        session.delete(item)
        return True

    # == UPDATING CURRENT LEVEL ==

    @staticmethod
    def get_all_supplier_email_addresses():
        all_supplier_email_addresses = []

        from UserClass import current_user_id
        all_inventory_item_ids = session.query(InventoryItem.id).filter(InventoryItem.user_id == current_user_id).all()
        item_ids = [i[0] for i in all_inventory_item_ids]
        for item_id in item_ids:
            supplier_email_address = session.query(InventoryItem.supplier_email).filter(InventoryItem.id == item_id).scalar()
            all_supplier_email_addresses.append(supplier_email_address)

        return all_supplier_email_addresses

    # == DASHBOARD ==

    @staticmethod
    def query_current_level(item_id):
        current_level = session.query(InventoryItem.current_level).filter(InventoryItem.id == item_id).scalar()
        return current_level

    @staticmethod
    def create_inventory_recommendation_for_current_month(current_level, current_month_forecast):
        # If current level is more than or equal to the current month forecast, user will not run out of inventory
        if current_level >= current_month_forecast:
            # So no action is needed
            return "No Action Needed"
        # If current level is less than current month forecast, they will need to order inventory
        else:
            # Calculate the difference between the forecast and the current level
            suggested_order_amount = current_month_forecast - current_level
            # Return the suggestion
            return f"Order {suggested_order_amount} Units"

    @staticmethod
    def create_inventory_recommendation_for_next_month(current_level, next_month_forecast):
        if current_level >= next_month_forecast:
            return "No Action Needed"
        else:
            suggested_order_amount = next_month_forecast - current_level
            return f"Order {suggested_order_amount} Units"

    # == INVENTORY REPORT ==

    @staticmethod
    def get_item_price(item_id):
        return session.query(InventoryItem.price).filter(InventoryItem.id == item_id).scalar()

    @staticmethod
    def get_item_cost(item_id):
        return session.query(InventoryItem.cost).filter(InventoryItem.id == item_id).scalar()

    @staticmethod
    def list_all_months_revenue(item_id, each_month_sales):
        # Empty list to hold revenues
        each_month_revenue = []
        # Query item price
        item_price = InventoryItem.get_item_price(item_id)
        # Iterate through each individual month's sales in the each_month_sales list
        for month_sales in each_month_sales:
            # Calculate revenue by multiplying sales and price
            month_revenue = month_sales * item_price
            # Append that value to each month revenue list
            each_month_revenue.append(month_revenue)

        return each_month_revenue

    @staticmethod
    def calculate_total_revenue(each_month_revenue_values):
        total_revenue = 0
        # Iterate through each month's revenue value
        for month_revenue_value in each_month_revenue_values:
            # Add the value to total revenue
            total_revenue += month_revenue_value

        # Returned the revenue value rounded to 2dp
        return f"{total_revenue:.2f}"

    @staticmethod
    def list_all_months_cogs(item_id, each_month_sales):
        each_month_cogs = []
        # Get item cost
        item_cost = InventoryItem.get_item_cost(item_id)
        # Iterate through each individual month's sales
        for month_sales in each_month_sales:
            # Multiply sales by item cost
            month_cogs = month_sales * item_cost
            # Append it to item cogs list
            each_month_cogs.append(month_cogs)

        return each_month_cogs

    @staticmethod
    def calculate_total_cogs(each_month_cogs_values):
        total_cogs = 0
        # Iterate through each month's cogs value
        for month_cogs_value in each_month_cogs_values:
            # Add the value to total cost of goods sold
            total_cogs += month_cogs_value

        return f"{total_cogs:.2f}"

    # Method that goes through each month in timeframe and takes away its cogs value from its revenue value
    @staticmethod
    def list_all_months_gross_profit(each_month_revenue, each_month_cogs):
        each_month_gross_profit = []

        # Set index so it starts at 0 so that it will index into first revenue and cogs value
        index = 0
        # As there are 12 revenue and cogs values, loop through while index is not equal to 12
        while index != 12:
            # Get the month revenue value at the index
            month_revenue = each_month_revenue[index]
            # Get the month cogs value at the index
            month_cogs = each_month_cogs[index]
            # Calculate gross profit by taking away the cogs from revenue
            month_gross_profit = month_revenue - month_cogs
            # Append that value to each month gross profit list
            each_month_gross_profit.append(month_gross_profit)
            # Increment the index
            index += 1

        return each_month_gross_profit

    @staticmethod
    def calculate_total_gross_profit(each_month_gross_profit_values):
        total_gross_profit = 0
        # Iterate through each month and add it's gross profit value to total_gross_profit
        for month_gross_profit_value in each_month_gross_profit_values:
            total_gross_profit += month_gross_profit_value

        return f"{total_gross_profit:.2f}"
