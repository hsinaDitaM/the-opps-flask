from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Configure the database connection URL based on your database system
engine = create_engine('sqlite:///favorites.db')  # SQLite example

# Create a session factory
Session = sessionmaker(bind=engine)
session = Session()
