# Standard library imports

# Third party imports
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import inspect

# Local application imports


config = {
    'host': 'mysql_db',
    'port': 3306,
    'user': 'root',
    'password': 'password',
    'database': 'testdb'
}
db_user = config.get('user')
db_pwd = config.get('password')
db_host = config.get('host')
db_port = config.get('port')
db_name = config.get('database')

config_str = f'mysql+pymysql://{db_user}:{db_pwd}@{db_host}:{db_port}/{db_name}'

engine = create_engine(config_str, echo = True)
Base = declarative_base()
Session = sessionmaker(bind=engine)

def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}
