from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
from config import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=False)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class SermonEntry(Base):
    __tablename__ = "sermons"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    youtube_url = Column(String, nullable=False)
    date = Column(String, nullable=False)

def init_db():
    """Creates the database tables if they do not exist."""
    Base.metadata.create_all(bind=engine)

def save_to_database(sermon_title, youtube_url, date_value):
    """Inserts a new sermon record into the SQLite database."""
    session = SessionLocal()
    try:
        new_entry = SermonEntry(
            title=sermon_title,
            youtube_url=youtube_url,
            date=date_value
        )
        session.add(new_entry)
        session.commit()
        print("Successfully saved to database!")
    except Exception as e:
        session.rollback()
        print(f"An error occurred while saving: {e}")
    finally:
        session.close()


def get_all_sermons():
    """Fetches all sermon entries from the database."""
    session = SessionLocal()
    try:
        # Fetch all rows from the sermons table
        sermons = session.query(SermonEntry).all()
        return sermons
    except Exception as e:
        print(f"An error occurred while fetching data: {e}")
        return []
    finally:
        session.close()