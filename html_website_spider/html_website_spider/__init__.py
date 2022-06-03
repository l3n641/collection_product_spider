from .items import ProductUrlItem
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
import os, time
from .models import Base


def get_sqlite_engine(database_file_name=None):
    if not os.path.exists("./data"):
        os.makedirs("./data")

    if not database_file_name:
        suffix = str(int(time.time()))
        database_file_name = f"database_{suffix}"

    engine = create_engine(f"sqlite:///data/{database_file_name}.db", echo=False, poolclass=StaticPool,
                           connect_args={'check_same_thread': False})
    return engine


db_engine = get_sqlite_engine()
Session = sessionmaker(bind=db_engine)
Base.metadata.create_all(db_engine)
