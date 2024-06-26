from sqlalchemy import create_engine
from sqlalchemy import URL
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
load_dotenv()


class ConnectDb(object):

    def __init__(self):
        self.host = os.getenv('DB_HOST')
        self.user_name = os.getenv('DB_USER')
        self.password = os.getenv('DB_PASSWORD')

    # https://docs.sqlalchemy.org/en/20/core/engines.html#mysql
    def get_engine(self):
        engine = None
        try:
            url_object = URL.create(
                "mysql+pymysql",
                username=self.user_name,
                password=self.password,
                host=self.host,
                database=os.getenv('DB_DATABASE'),
            )
            # url = "mysql://root:root@localhost/live_now"
            # engine = create_engine(url, pool_size=20)
            engine = create_engine(url_object, pool_size=30)
            # engine = create_engine(url_object, pool_size=50, echo=True)
        except Exception as e:
            print(msg=str(e))
        return engine

    def get_session(self):
        engine = self.get_engine()
        # 把 DB engine 與 session 綁在一起
        Session = sessionmaker(bind=engine)
        session = Session()
        return session
