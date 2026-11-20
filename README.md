# EJD Inventory

An inventory management system I designed for small businesses to be able to better manage their stock. I built this project for my A-level Computer Science programming coursework.

I developed this project before I started using Git, hence why this has only been recently uploaded for ease of viewing. If you want to the process of me coding this project, including my research, development, testing and evaluation - you can view it in my original write up document (https://docs.google.com/document/d/1tdmw7goFLMwDU5F-V9zf1jJBxIzyMiOJNLPm-iYSvvo/edit?usp=sharing)

You can also view my full video demonstration here https://www.youtube.com/watch?si=sqLb3oWqss1_OAB-&v=WqIE5xLGILQ&feature=youtu.be
## Features
- **Inventory management** - creating and updating inventory items, including descriptions, costs, prices, existing inventory levels, supplier details and alert levels
- **Automated inventory tracking** - processed emailed sales receipts and delivery invoices, extracted data from the PDF attachments and used that data to update inventory levels
- **Sales forecasting** - used an custom exponential moving average algorithm, with a smoothing factor that changed based how volatile the data was
- **Stock buying recommendations** - compared current inventory levels against forecasted sales to give a recommendation on how many units to order
- **Sales graphs** - displayed historical sales along with forecasted values using Matplotlib
- **Financial reporting** - calculated and visualised revenue, cost of goods sold and gross profit
- **Relational database** - one to many relationship between user and inventory items, one to many relationship between inventory item and sales and one to many relationship between inventory item and deliveries

## Technologies Used
- **Python** - used object-oriented principles for application logic
- **CustomTkinter** - interface
- **SQLite** - relational database for users, inventory items, sales and deliveries
- **SQLAlchemy ORM** - setting up, managing and querying the database
- **Matplotlib** - graphing sales as well as the financial metrics
- **Email related tools (imap-tools, SMTP, MIME)** - retrieving and processing emails
- **Pdfplumber** - extracting text and tables from PDFs