from .database import engine, Base
from .models import BitcoinPrice

def init_db():
    # Create all tables in the database
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
