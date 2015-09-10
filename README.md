# DB powered Shortlinker

This program uses a database to generate a static php file for 301-Redirects. Basically it's your own shortlinker.

## Installation

Create a database. MySQL Schema for example:
```sql
SET NAMES utf8;
SET time_zone = '+00:00';

CREATE TABLE `redirects` (
  `slug` varchar(255) NOT NULL,
  `target` varchar(512) NOT NULL,
  `expiration_date` datetime DEFAULT NULL,
  PRIMARY KEY (`slug`),
  UNIQUE KEY `slug` (`slug`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
```

Save your database credentials as an SQLAlchemy connection string in `connection.py`

## Usage

### Inline help text

    shortlinker.py -h

### Add a new shortlink

    shortlinker.py --slug "Handling exceptions" --target https://wiki.python.org/moin/HandlingExceptions --out /path/to/output

### List current shortlinks

    shortlinker.py -l

or

    shortlinker.py --list

## Result

This would be the generated output for above execution:

```php
<?php

$slug = $_GET["slug"];

switch($slug) {
	case "handling-exceptions":
		header("Location: https://wiki.python.org/moin/HandlingExceptions", true, 301);
		exit();
    default:
        http_response_code(404);
?>

<html>
    <head>
        <title>404: Seite nicht gefunden!</title>
    </head>
    <body>
        <h1>404: Seite nicht gefunden!</h1>
        <p>Zu dem angegebenen Kurzlink konnte keine Weiterleitung gefunden werden.</p>
        <p><strong>Alles richtig geschrieben?</strong></p>
    </body>
</html>

<?php
}
?>
```

