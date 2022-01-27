from models.scrapedproduct import ScrapedProduct
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///test.db", future=True)
Base = declarative_base()
Base.metadata.create_all(engine)
SessionFactory = sessionmaker(bind=engine)
session = SessionFactory()


def add_metadata(base):
    base.metadata.create_all(engine)


def save(obj) -> None:
    print(type(obj))
    session.add(obj)
    session.commit()
    session.close()


def init() -> None:
    add_metadata(ScrapedProduct)


if __name__ == "__main__":
    pass
