from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = 'postgres://<username>:<password>@<ip-address/
# hostname>/<database_name'
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:password@localhost/fastapi'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()
