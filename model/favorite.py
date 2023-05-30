from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configure the database connection URL based on your database system
engine = create_engine('sqlite:///favorites.db')  # SQLite example

Base = declarative_base()
Session = sessionmaker(bind=engine)

class FavoriteTeam(Base):
    __tablename__ = 'favorite_teams'
    id = Column(Integer, primary_key=True)
    team_name = Column(String)

# Create the table if it doesn't exist
Base.metadata.create_all(engine)

def add_favorite_team(team_name):
    session = Session()
    favorite_team = FavoriteTeam(team_name=team_name)
    session.add(favorite_team)
    session.commit()
    session.close()

def get_favorite_teams():
    session = Session()
    favorite_teams = session.query(FavoriteTeam).all()
    session.close()
    return favorite_teams
