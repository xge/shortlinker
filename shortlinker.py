#!/usr/bin/env python3
__author__ = 'Hagen <spam@xgerdax.de>'
from datetime import datetime

import argparse

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from slugify import slugify

from Redirect import Redirect
from connection import connection

parser = argparse.ArgumentParser()
parser.add_argument('-conn', help='Optional MySQL Connection String, default is specified in connection.py',
                    default=connection)
parser.add_argument('-exp', help='Optional expiration date')
parser.add_argument('-slug', help='The URL slug')
parser.add_argument('-target', help='The target URL')
parser.add_argument('-out', help='Output directory')
parser.add_argument('-write', help='Write the current database to `out`', action='store_true')
parser.add_argument('-l', '--list', help='List all stored redirects.', action='store_true')
args = parser.parse_args()


class Shortlinker:
    def __init__(self, conn):
        self.conn = conn
        self.engine = create_engine(conn)

    def add(self, slug, target, exp):
        redirect = Redirect(slug=slug, target=target, expiration_date=exp)

        session = sessionmaker(bind=self.engine)()
        session.merge(redirect)
        session.commit()

        print('Successfully added {}'.format(redirect))

        session.close()

    def list(self):
        session = sessionmaker(bind=self.engine)()
        for redirect in session.query(Redirect).order_by(Redirect.slug):
            print(redirect)
        session.close()

    def write(self, out):
        session = sessionmaker(bind=self.engine)()

        today = datetime.now()

        with open('{}/.htaccess'.format(out), "wt") as fout:
            seq = []
            seq.append('RewriteEngine on\n')
            seq.append('RewriteRule (.*)$ index.php?slug=$1 [QSA]\n')
            fout.writelines(seq)

        with open('{}/index.php'.format(out), "wt") as fout:
            with open("index.bare.php", "rt") as fin:
                for line in fin:
                    if "// INSERT" in line:
                        seq = []
                        for redirect in session.query(Redirect).order_by(Redirect.slug):
                            if redirect.expiration_date is None or redirect.expiration_date > today:
                                seq.append('\tcase "{}":\n'.format(redirect.slug))
                                seq.append('\t\theader("Location: {}", true, 301);\n'.format(redirect.target))
                                seq.append('\t\texit();\n')
                        fout.writelines(seq)
                    else:
                        fout.write(line)

        session.close()


if __name__ == '__main__':
    shortlinker = Shortlinker(args.conn)

    if args.list is True:
        shortlinker.list()
    elif args.write is True and args.out is not None:
        shortlinker.write(args.out)
        shortlinker.list()
    else:
        if args.slug is not None and args.target is not None and args.out is not None:
            shortlinker.add(slugify(args.slug), args.target, args.exp)
            shortlinker.write(args.out)
            print('Successfully updated php file.')
        else:
            print(parser.print_help())
