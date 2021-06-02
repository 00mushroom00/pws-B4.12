
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime as dt

DB_PATH = "sqlite:///sochi_athletes.sqlite3"

Base = declarative_base()

class User(Base):
    __tablename__ = "user"
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    first_name = sa.Column(sa.Text)
    last_name = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    email = sa.Column(sa.Text)
    birthdate = sa.Column(sa.Text)
    height = sa.Column(sa.Float)

class Athelete(Base):
    __tablename__ = "athelete"
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    age = sa.Column(sa.Integer)
    birthdate = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    height = sa.Column(sa.Float)
    name = sa.Column(sa.Text)
    weight = sa.Column(sa.Integer)
    gold_medals = sa.Column(sa.Integer)
    silver_medals = sa.Column(sa.Integer)
    bronze_medals = sa.Column(sa.Integer)
    total_medals = sa.Column(sa.Integer)
    sport = sa.Column(sa.Text)
    country = sa.Column(sa.Text)

def connect_db():
        engine = sa.create_engine(DB_PATH)
        Base.metadata.create_all(engine)
        Sessions = sessionmaker(engine)
        session = Sessions()
    return session

def print_user(user):
    output = (
        f" Id: {user.id}\n"
        f" Name: {user.first_name} {user.last_name}\n"
        f" Gender: {user.gender}\n"
        f" Email: {user.email}\n" 
        f" Birthdate: {user.birthdate}\n"
        f" Height: {user.height}\n"
    )
    print(output)
    
def print_athlete(athlete):
    output = (
        f" Id: {athlete.id}\n"
        f" Name: {athlete.name}\n"
        f" Age: {athlete.age}\n"
        f" Birthdate: {athlete.birthdate}\n"
        f" Gender: {athlete.gender}\n"
        f" Height: {athlete.height}\n"
        f" Weight: {athlete.weight}\n"
        f" Gold_medals: {athlete.gold_medals}\n"
        f" Silver_medals: {athlete.silver_medals}\n"
        f" Bronze_medals: {athlete.bronze_medals}\n"
        f" Total_medals: {athlete.total_medals}\n"
        f" Sport: {athlete.sport}\n"
        f" Country: {athlete.country}\n"
    ) 
    print(output)
    
def find_nearby_athletes(session, user):
        athlete_nearby_height_is_found = False
    athlete_nearby_birthdate_is_found = False

            min_dif_heights = 0

            min_dif_birthdates = 0

        athlete_nearby_height = session.query(Athelete).filter(Athelete.height == user.height).first()
        if not athlete_nearby_height is None:
            athlete_nearby_height_is_found = True
        
        athlete_nearby_birthdate = session.query(Athelete).filter(Athelete.birthdate == user.birthdate).first()
        if not athlete_nearby_birthdate is None:
            athlete_nearby_birthdate_is_found = True
        
                if not athlete_nearby_height_is_found or not athlete_nearby_birthdate_is_found:
        athletes = session.query(Athelete).all()

                                            
            if not athlete_nearby_birthdate_is_found:
                        
                user_birthdate = dt.datetime.strptime(user.birthdate, "%Y-%m-%d")
            
        for athlete in athletes:
            if not athlete_nearby_height_is_found:
                    if not athlete.height is None:
                        dif_heights = abs(user.height - athlete.height)
                                if (min_dif_heights == 0) or (dif_heights < min_dif_heights):
                        min_dif_heights = dif_heights
                        athlete_nearby_height = athlete

            if not athlete_nearby_birthdate_is_found:
                    if not athlete.birthdate is None:
                        athlete_birthdate = dt.datetime.strptime(athlete.birthdate, "%Y-%m-%d")
                            dif_birthdates = abs(user_birthdate - athlete_birthdate)
                    if (min_dif_birthdates == 0) or (dif_birthdates < min_dif_birthdates):
                        min_dif_birthdates = dif_birthdates
                        athlete_nearby_birthdate = athlete

    result = {
        "athlete_nearby_height": athlete_nearby_height,
        "dif_heights": min_dif_heights,
        "athlete_nearby_birthdate": athlete_nearby_birthdate,
        "dif_birthdates": min_dif_birthdates
    }
    return result

def main():
    session = connect_db()

        user_id = input("Enter user id: ")
    user = session.query(User).filter(User.id == user_id).first()
        if user is None:
        print("No user with id:", user_id)
        return
    
        print("\nSelected user:")
    print_user(user)
    
        result = find_nearby_athletes(session, user)
        if not result["athlete_nearby_height"] is None:
        print("Nearest athlete by height:")
        print_athlete(result["athlete_nearby_height"])
        print(f"Heights difference: {result['dif_heights']}\n")
    else:
        print("No nearest athlete by height\n")
        if not result["athlete_nearby_birthdate"] is None:
        print("Nearest athlete by birthdate:")
        print_athlete(result["athlete_nearby_birthdate"])
        print(f"Birthdates difference: {result['dif_birthdates']}\n")
    else:
        print("No nearest athlete by birthdate\n")

if __name__ == "__main__":
    main()
