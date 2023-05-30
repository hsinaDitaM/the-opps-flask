from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create the database engine
engine = create_engine('sqlite:///nfl_players.db', echo=True)

# Create a base class for declarative models
Base = declarative_base()

# Define the NFL player model
class NFLPlayer(Base):
    __tablename__ = 'nfl_players'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    dob = Column(Date)

    def __repr__(self):
        return f"NFLPlayer(name='{self.name}', age={self.age}, dob='{self.dob}')"

# Create the table in the database
Base.metadata.create_all(engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

# Add NFL player records to the table
players_data = [
    {'name': 'Tom Brady', 'age': 44, 'dob': '1977-08-03'},
    {'name': 'Aaron Rodgers', 'age': 37, 'dob': '1983-12-02'},
    {'name': 'Patrick Mahomes', 'age': 25, 'dob': '1995-09-17'},
    {'name': 'Russell Wilson', 'age': 32, 'dob': '1988-11-29'},
    {'name': 'J.J. Watt', 'age': 32, 'dob': '1989-03-22'},
    {'name': 'Davante Adams', 'age': 28, 'dob': '1992-12-24'},
    {'name': 'DeAndre Hopkins', 'age': 29, 'dob': '1992-06-06'},
    {'name': 'Derrick Henry', 'age': 27, 'dob': '1994-01-04'},
    {'name': 'Travis Kelce', 'age': 31, 'dob': '1989-10-05'},
    {'name': 'T.J. Watt', 'age': 26, 'dob': '1994-10-11'},
    {'name': 'Josh Allen', 'age': 25, 'dob': '1996-05-21'},
    {'name': 'Lamar Jackson', 'age': 24, 'dob': '1997-01-07'},
    {'name': 'Stephon Gilmore', 'age': 30, 'dob': '1990-09-19'},
    {'name': 'Christian McCaffrey', 'age': 25, 'dob': '1996-06-07'},
    {'name': 'Alvin Kamara', 'age': 25, 'dob': '1995-07-25'},
    {'name': 'Aaron Donald', 'age': 30, 'dob': '1991-05-23'},
    {'name': 'Khalil Mack', 'age': 30, 'dob': '1991-02-22'},
    {'name': 'Stefon Diggs', 'age': 27, 'dob': '1993-11-29'},
    {'name': 'Tyreek Hill', 'age': 27, 'dob': '1994-03-01'},
    {'name': 'Deshaun Watson', 'age': 25, 'dob': '1995-09-14'},
    {'name': 'George Kittle', 'age': 27, 'dob': '1993-10-09'},
    {'name': 'DeVante Adams', 'age': 28, 'dob': '1992-12-24'},
    {'name': 'Michael Thomas', 'age': 28, 'dob': '1993-03-03'},
    {'name': 'Ezekiel Elliott', 'age': 26, 'dob': '1995-07-22'},
    {'name': 'Dalvin Cook', 'age': 25, 'dob': '1995-08-10'},
    {'name': 'Saquon Barkley', 'age': 24, 'dob': '1997-02-09'},
    {'name': 'Nick Bosa', 'age': 23, 'dob': '1997-10-23'},
    {'name': 'Myles Garrett', 'age': 25, 'dob': '1995-12-29'}
]

for player_data in players_data:
    player = NFLPlayer(**player_data)
    session.add(player)

# Commit the changes to the database
session.commit()

# Close the session
session.close()
