from data.db_session import create_session, global_init
from data.users import User
from data.stocks import Stock
from data.companies import Company

import os


global_init(os.path.join("db", "database.db"))


def main():
    session = create_session()
    print(session.query(Stock.id).all())
    print(session.query(Stock.id).get(Stock.id == 1))


if __name__ == '__main__':
    main()