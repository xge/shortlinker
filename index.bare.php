<?php

$slug = $_GET["slug"];

switch($slug) {
// INSERT
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