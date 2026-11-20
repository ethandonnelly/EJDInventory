from DatabaseSetup import session
import datetime


class Forecast:
    def __init__(self, id_of_forecasted_item, end_month=None, end_year=None, start_month=None, start_year=None, smoothing_factor=None):
        self.id_of_forecasted_item = id_of_forecasted_item
        self.end_month = end_month
        self.end_year = end_year
        self.start_month = start_month
        self.start_year = start_year
        self.smoothing_factor = smoothing_factor

    @staticmethod
    def current_date():
        current_date = str(datetime.datetime.now())
        return current_date

    @staticmethod
    def current_year():
        # Slice into first 4 characters of current date to get current year
        current_year = Forecast.current_date()[0:4]
        return current_year

    @staticmethod
    def current_month():
        # Slice into current date between 5th and 7th character to get current month
        current_month = Forecast.current_date()[5:7]
        return current_month

    # Sets end as the previous month as need a full 30 days of data
    def set_end_year_and_month(self):

        current_year = Forecast.current_year()
        current_month = Forecast.current_month()

        # If current month is January
        if current_month == "01":
            # Go to previous year and set month as December
            self.end_year = str(int(current_year) - 1)
            self.end_month = "12"
        # If current month isn't January
        else:
            # Keep year the same and go back 1 month
            self.end_year = str(current_year)
            self.end_month = str(int(current_month) - 1).zfill(2)

    # Sets start as 1 year back from start as it's a 12-month AMA
    def set_start_year_and_month(self):
        self.start_year = str(int(self.end_year) - 1)
        if self.end_month == "12":
            self.start_month = "01"
        else:
            self.start_month = str(int(self.end_month) + 1).zfill(2)

    def query_sales_data(self):
        from UpdateCurrentLevelClasses import Sale
        # Query sales data using the id of the item being forecasted
        sales_data = session.query(Sale.date, Sale.amount).filter(Sale.sold_item_id == self.id_of_forecasted_item).all()
        return sales_data

    def sum_sales_for_individual_month(self, year, month):
        total_sales_for_month = 0
        sales_data = self.query_sales_data()

        # Iterate through all sales in sales_data
        for sale in sales_data:
            # Sales data is a list of [Sale.date, Sale.amount], so need to index into each
            date_of_sale = sale[0]
            sales_amount = sale[1]

            # Then further index into date_of_sale
            year_of_sale = date_of_sale[0:4]
            month_of_sale = date_of_sale[5:7]

            # If the sale being looked at in current iteration's date falls within the target month
            if year_of_sale == year and month_of_sale == month:
                # Add it's sales amount to the total for the target month
                total_sales_for_month += sales_amount

        return total_sales_for_month

    def list_total_sales_for_all_months_old1(self):
        # Initialising an empty list
        # Once this method has run, this list should contain 36 sales figures
        total_sales = []

        # Initialising start year and start month
        year = self.start_year
        month = self.start_month

        while True:
            # Sum the sales for current month in iteration and append it to total sales list
            sales_for_that_month = self.sum_sales_for_individual_month(year, month)
            total_sales.append(sales_for_that_month)

            # Check if end year and month have been hit
            if year == self.start_year and month == self.start_month:
                return total_sales

            # Then go back to the previous month

            # If current month is January
            if month == "01":
                # Go to previous year and set month as December
                year = str(int(year) - 1)
                month = "12"
            # If current month isn't January
            else:
                # Keep year the same and go back 1 month
                year = str(year)
                month = str(int(month) - 1).zfill(2)

    def list_total_sales_for_all_months(self):
        # Initialising an empty list
        # Once this method has run, this list should contain 36 sales figures
        total_sales = []

        # Initialising start year and end month
        year = self.start_year
        month = self.start_month

        while True:
            # Sum the sales for current month in iteration and append it to total sales list
            sales_for_that_month = self.sum_sales_for_individual_month(year, month)
            total_sales.append(sales_for_that_month)

            # Check if start year and month have been hit
            if year == self.end_year and month == self.end_month:
                print(total_sales)
                return total_sales

            # Then go back to the previous month

            # If current month is January
            if month == "12":
                # Go to previous year and set month as December
                year = str(int(year) + 1)
                month = "01"
            # If current month isn't January
            else:
                # Keep year the same and go back 1 month
                year = str(year)
                month = str(int(month) + 1).zfill(2)

    def percentage_difference_calculator(self, value1, value2):
        # Error checking for months with no sales data
        if value1 == 0 or value2 == 0:
            return None
        else:
            # Calculate the difference
            difference = value2 - value1
            # Calculate the percentage difference
            percentage_difference = (difference / value1) * 100
            return round(percentage_difference, 2)

    def get_all_percentage_differences_between_months(self, all_sales):
        differences = []
        for i in range(len(all_sales) - 1):
            difference = self.percentage_difference_calculator(all_sales[i], all_sales[i + 1])
            if difference is None:
                return None
            else:
                differences.append(difference)

        return differences

    def calculate_mean_percentage_difference(self, all_percentage_differences):
        if all_percentage_differences is None:
            return None
        else:
            total = 0

            for i in all_percentage_differences:
                total += i

            mean_percentage_difference = total / len(all_percentage_differences)
            return round(mean_percentage_difference, 3)

    def get_mean_percentage_difference_between_monthly_sales(self):
        # Get the percentages differences between the monthly sales
        percentage_differences_between_monthly_sales = self.get_all_percentage_differences_between_months(self.list_total_sales_for_all_months())
        # Calculate the mean of those percentage differences
        mean_percentage_difference_between_monthly_sales = self.calculate_mean_percentage_difference(percentage_differences_between_monthly_sales)

        return mean_percentage_difference_between_monthly_sales

    def set_smoothing_factor(self):
        # Calculate mean percentage difference
        mpd = self.get_mean_percentage_difference_between_monthly_sales()

        # Set smoothing factor based on mpd
        if mpd is None:
            self.smoothing_factor = None
        elif mpd <= 4:
            self.smoothing_factor = 0.5
        elif 4 < mpd <= 8:
            self.smoothing_factor = 0.6
        elif 8 < mpd <= 12:
            self.smoothing_factor = 0.7
        elif 12 < mpd <= 16:
            self.smoothing_factor = 0.8
        elif 16 < mpd <= 20:
            self.smoothing_factor = 0.9
        else:
            self.smoothing_factor = 1

    def calculate_initial_value(self):
        total = 0
        # Get sales for each month
        all_sales = self.list_total_sales_for_all_months()
        # Add up the sales of the first 6 months
        for i in all_sales[0:6]:
            total += i
        
        # Divide it by 6
        initial_value = total / 6
        
        return initial_value

    def calculate_individual_ema(self, sales_amount, previous_ema):
        value = (sales_amount * self.smoothing_factor) + (previous_ema * (1 - self.smoothing_factor))
        return round(value)

    def calculate_all_ema_values(self):
        # If smoothing factor is None due to previous validations, pass on None
        if self.smoothing_factor is None:
            return None
        # If sales data is valid, calculate rolling ema:
        else:
            print(self.smoothing_factor)
            # Get all sales
            all_sales = self.list_total_sales_for_all_months()
            # Calculate initial value
            initial_value = self.calculate_initial_value()
            # To begin with, set the previous ema as the initial value
            previous_ema = initial_value

            all_ema_values = []
            # Iterate through each month in all_sales
            for s in all_sales:
                # Calculate the ema value that month's sales value
                ema_value = self.calculate_individual_ema(s, previous_ema)
                # Append the sale's value to all_ema_values list
                all_ema_values.append(ema_value)
                previous_ema = ema_value

            return all_ema_values

    def get_current_month_forecast_value(self):
        all_ema_values = self.calculate_all_ema_values()
        # If rolling_ema is None due to previous validations, output error message
        if all_ema_values is None:
            return "Can't Forecast Due\nto Not Having 12\nMonths of Sales Data"
        # If valid, return value
        else:
            # The forecasted value for the current month is the last value in all ema values
            forecasted_value = all_ema_values[-1]
            return forecasted_value

    def get_remaining_current_month_forecast(self):
        # Get the amount of sales that have already happened in the current month
        existing_sales_for_current_month = self.sum_sales_for_individual_month(Forecast.current_year(), Forecast.current_month())
        # Take that value away from the forecast value
        current_month_forecast = self.get_current_month_forecast_value()
        if isinstance(current_month_forecast, str):
            return current_month_forecast
        remaining_sales_from_forecast = current_month_forecast - existing_sales_for_current_month
        # Return the forecasted sales remaining after taking away the sales that have already happened
        return remaining_sales_from_forecast

    def get_mean_percentage_difference_between_monthly_emas(self):
        # Get all the percentages differences between monthly ema values
        percentage_differences_between_monthly_emas = self.get_all_percentage_differences_between_months(self.calculate_all_ema_values())
        # Calculate the mean percentage difference between all of them
        mean_percentage_difference_between_monthly_emas = self.calculate_mean_percentage_difference(percentage_differences_between_monthly_emas)

        return mean_percentage_difference_between_monthly_emas

    def calculate_next_month_forecast_value(self):
        # Get the current month forecast_value
        current_month_forecast_value = self.get_current_month_forecast_value()

        # Check if current month forecast error message has been returned by checking string
        if type(current_month_forecast_value) is str:
            # If the current month error message has been returned, it means there is not enough data
            # So also return the error message
            return "Can't Forecast Due\nto Not Having 12\nMonths of Sales Data"

        # If the actual value has been returned, it means there is sales data, so calculation can happen
        else:
            # Get the mean percentage difference
            mean_percentage_difference = self.get_mean_percentage_difference_between_monthly_emas()
            # Turn the mean percentage difference into a percentage multiplier
            percentage_multiplier = 1 + (mean_percentage_difference / 100)
            # Multiply the current month forecast by the mean percentage difference to get the next month forecast
            next_month_forecast_value = current_month_forecast_value * percentage_multiplier

            # Return the rounded next month forecast value
            return round(next_month_forecast_value)

    # == GRAPH ==

    def list_all_month_names(self, end_month, end_year):

        # == STORE CORRESPONDING MONTH NUMBERS AND NAMES ==

        # Create the hash table
        hash_table = HashTable(13)

        # Add the keys and values to the hash table
        hash_table.add_value(1, "Jan")
        hash_table.add_value(2, "Feb")
        hash_table.add_value(3, "Mar")
        hash_table.add_value(4, "Apr")
        hash_table.add_value(5, "May")
        hash_table.add_value(6, "Jun")
        hash_table.add_value(7, "Jul")
        hash_table.add_value(8, "Aug")
        hash_table.add_value(9, "Sep")
        hash_table.add_value(10, "Oct")
        hash_table.add_value(11, "Nov")
        hash_table.add_value(12, "Dec")

        # == CREATE THE LIST OF MONTH NAMES IN TIMEFRAME ==

        # Initialise an empty list that will hold month names
        full_month_names = []

        # Start at the month and year that will be
        month = int(self.start_month)
        year = int(self.start_year)

        # Loop through from the start month and year to the current month and year
        while True:

            # === ADD CORRESPONDING MONTH NAME OF CURRENT MONTH TO LIST ===

            # Get the month name from the hash table for the month currently in iteration
            month_name = hash_table.get_value(month)
            # Get the year current month is in
            month_year = str(year)[2:4]
            # Put them together to get full month name e.g. Jan26
            full_month_name = f"{month_name}{month_year}"
            # Add that name to the full month names list
            full_month_names.append(full_month_name)

            # === CHECK IF CURRENT MONTH AND YEAR MATCH END OF GRAPH MONTH AND YEAR ===

            # If current month and year in iteration match the end of graph month and year, break the loop
            if month == int(end_month) and year == int(end_year):
                # Return the month names
                return full_month_names

            # === MOVE FORWARD TO NEXT MONTH ===

            # Handle if it's December
            if month == 12:
                year += 1
                month = 1
            # If it's not December, move forward normally
            else:
                month += 1

    # Method that goes forward two months from the end of the forecast date
    def get_graph_end_month_and_year(self):

        # === GET END OF FORECAST MONTH AND YEAR ===
        end_of_forecast_month = int(self.end_month)
        end_of_forecast_year = int(self.end_year)

        # === MOVE FORWARD 2 MONTHS ===
        # Handle if month is November
        if end_of_forecast_month == 11:
            end_of_graph_month = "01"
            end_of_graph_year = str(end_of_forecast_year + 1).zfill(2)
        elif end_of_forecast_month == 12:
            end_of_graph_month = "02"
            end_of_graph_year = str(end_of_forecast_year + 1)
        # If month isn't November, just move forward normally
        else:
            end_of_graph_month = str(end_of_forecast_month + 2).zfill(2)
            end_of_graph_year = str(end_of_forecast_year)
        # Return both the end of graph month and year
        return end_of_graph_month, end_of_graph_year

class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [None] * size

    def hash_function(self, key):
        return key

    def add_value(self, key, value):
        # Index into the hash table
        index = self.hash_function(key)
        # Check if index is empty
        if self.table[index] is None:
            # If index is empty, insert the key and value
            self.table[index] = (key, value)

    def get_value(self, key):
        index = self.hash_function(key)
        # If key matches
        if self.table[index][0] == key:
            # Return the value
            return self.table[index][1]
        else:
            return None
