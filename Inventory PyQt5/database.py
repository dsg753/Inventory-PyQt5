from sqlalchemy import Column, Integer, String, Boolean, Date, Float, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define the SQLAlchemy base class
Base = declarative_base()

# Database Name
DB_NAME = "inventory_database.sqlite"

# Define the Machinery Inventory model
class МашиниИнвентар(Base):
    __tablename__ = "машини_инвентар"

    id = Column(Integer, primary_key=True, autoincrement=True)
    инвентарен_номер = Column(String(50), nullable=False, unique=True)  # Unique Inventory Number
    сериен_номер = Column(String(50), nullable=False, unique=True)  # Unique Serial Number
    име = Column(String(100), nullable=False)  # Name
    тип = Column(String(50), nullable=False)  # Type
    състояние = Column(String(50), nullable=False)  # Condition
    стойност = Column(Float, nullable=False)  # Value
    дата_на_придобиване = Column(Date, nullable=True)  # Acquisition Date

# Define the Machinery Rental model
class МашиниПодНаем(Base):
    __tablename__ = "машини_под_наем"

    id = Column(Integer, primary_key=True, autoincrement=True)
    инвентарен_номер = Column(String(50), nullable=False, unique=True)  # Unique Inventory Number
    сериен_номер = Column(String(50), nullable=False, unique=True)  # Unique Serial Number
    име = Column(String(100), nullable=False)  # Name
    дневен_наем = Column(Float, nullable=False)  # Daily Rent (should be a number)
    стойност = Column(Float, nullable=False)  # Value (should be a number)
    дата_на_последна_поддръжка = Column(Date, nullable=True)  # Last Maintenance Date

# Create the SQLite database (if it doesn't already exist)
engine = create_engine(f"sqlite:///{DB_NAME}")

def recreate_database():
    """Recreate the database with the updated schema."""
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

# Recreate the database to ensure the schema is up-to-date
recreate_database()

Session = sessionmaker(bind=engine)
session = Session()

print("Database and tables created successfully.")