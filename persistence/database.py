from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///database.db", future=True)
Base = declarative_base()
Base.metadata.create_all(engine)
SessionFactory = sessionmaker(bind=engine)
session = SessionFactory()


def add_metadata(base):
    base.metadata.create_all(engine)


def save(obj) -> None:
    if obj is None:
        return
    session.add(obj)
    session.commit()
    session.close()


def init() -> None:
    from models.scrapedproduct import ScrapedProduct
    Base.metadata.drop_all(engine)
    add_metadata(ScrapedProduct)


if __name__ == "__main__":
    pass
