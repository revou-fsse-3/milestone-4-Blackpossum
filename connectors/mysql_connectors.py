from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

username = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
database_name=os.getenv("DB_NAME")


try:
    ConnectionString = f'mysql+mysqlconnector://{username}:{password}@{host}/{database_name}'
    engine = create_engine(ConnectionString)
    connection = engine.connect()
    Session = sessionmaker(connection)
    print('database connect succesfully'),200
except Exception as e:
    print('failed to connect to database'),500
