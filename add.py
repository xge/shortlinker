#!/usr/bin/env python3
__author__ = 'hagen'
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from slugify import slugify

from Redirect import Redirect
import argparse
from connection import connection
from go import Go


class Add:
    def __init__(self, conn, slug, target, exp):
        slug = slugify(slug)

        url = target

        redirect = Redirect(slug=slug, target=url, expiration_date=exp)

        engine = create_engine(conn)

        Session = sessionmaker(bind=engine)
        session = Session()
        session.merge(redirect)
        session.commit()

        print('Successfully added {}'.format(redirect))

        session.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-conn", help="Optional MySQL Connection String, default is specified in connection.py",
                        default=connection)
    parser.add_argument("-exp", help="Optional expiration date")
    parser.add_argument("slug", help="The URL slug")
    parser.add_argument("target", help="The target URL")
    parser.add_argument("out", help="Output directory")
    args = parser.parse_args()

    # handle cli input
    Add(args.conn, args.slug, args.target, args.exp)

    # update php file
    Go(args.conn, args.out)
    print('Successfully updated php file.')
