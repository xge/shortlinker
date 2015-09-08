# DB powered Shortlinker

This program uses a database to generate a static php file for 301-Redirects. Basically it's your own shortlinker.

## Installation

1. Create a database. MySQL Schema for example:

        -- Adminer 4.2.1 MySQL dump

        SET NAMES utf8;
        SET time_zone = '+00:00';

        CREATE TABLE `redirects` (
          `slug` varchar(255) NOT NULL,
          `target` varchar(512) NOT NULL,
          `expiration_date` datetime DEFAULT NULL,
          PRIMARY KEY (`slug`),
          UNIQUE KEY `slug` (`slug`)
        ) ENGINE=InnoDB DEFAULT CHARSET=latin1;


        -- 2015-09-08 15:48:25

2. Save your database credentials as a SQLAlchemy connection string in `connection.py`

## Usage

Use `add.py` to add your first shortlink:

    ./add.py "Handling Exceptions" https://wiki.python.org/moin/HandlingExceptions /path/to/DocumentRoot

## Protip

Use `add.py -h` to display a short help text.
