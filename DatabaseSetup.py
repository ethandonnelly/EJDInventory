from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, mapped_column, Mapped, sessionmaker

# = SETTING UP DATABASE CONNECTION =

# Creating a connection to the database
connection = create_engine("sqlite:///EJDInventoryDatabase.db")

# Creating a session which allows me to interact with the database I have just connected to
Session = sessionmaker(bind=connection)
session = Session()

# = SETTING UP BASE CLASS =

# Initialising Main
# This is what allows a class to correspond to a database table
Main = declarative_base()

# Creating the base class
class AbstractBase(Main):
    # Set abstract to True
    __abstract__ = True
    # Initialising the id field
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)



def initialise_database():
    # Import all tables
    import UserClass
    import InventoryItemClass
    import UpdateCurrentLevelClasses

    # Create all tables
    Main.metadata.create_all(bind=connection)
