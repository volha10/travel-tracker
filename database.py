from sqlmodel import SQLModel, create_engine

db_url = "sqlite:///trips.db"
engine = create_engine(db_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
