from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
import os
import time


class Sqlite(object):
    _session_class = None
    _engine = None

    @staticmethod
    def get_db_path(project_name, db_dir_path):
        if not os.path.exists(db_dir_path):
            os.makedirs(db_dir_path)
        return os.path.join(db_dir_path, project_name) + ".db"

    @classmethod
    def rename_old_database(cls, project_name, db_dir_path=None):
        db_dir_path = db_dir_path or './data'
        db_path = cls.get_db_path(project_name, db_dir_path)
        if os.path.exists(db_path):
            old_name = db_path + "_" + str(int(time.time()))
            os.rename(db_path, old_name)

    @classmethod
    def get_sqlite_engine(cls, project_name, db_dir_path=None):
        if cls._engine:
            return cls._engine
        db_path = cls.get_db_path(project_name, db_dir_path)
        engine = create_engine(f"sqlite:///{db_path}", echo=False, poolclass=StaticPool,
                               connect_args={'check_same_thread': False})
        cls._engine = engine
        return engine

    @classmethod
    def set_session_class(cls, db_engine):
        session_class = sessionmaker(bind=db_engine)
        cls._session_class = session_class
        return cls._session_class

    @classmethod
    def get_session(cls):
        return cls._session_class()
