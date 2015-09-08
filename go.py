#!/usr/bin/env python3
__author__ = 'Hagen <hagen@xgerdax.de>'
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Redirect import Redirect
import argparse
from connection import connection
from datetime import datetime


class Go:
    def __init__(self, conn, out):
        engine = create_engine(conn)
        Session = sessionmaker(bind=engine)
        session = Session()

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
    parser = argparse.ArgumentParser()
    parser.add_argument("-conn", help="Optional MySQL Connection String, default is specified in connection.py",
                        default=connection)
    parser.add_argument("out", help="Output directory")
    args = parser.parse_args()
    go = Go(args.conn, args.out)
