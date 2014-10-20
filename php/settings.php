<?php
# API specific settings
ini_set('display_errors', 1);
error_reporting(E_ALL);

include "util.php";

if (!isset($argv[1])){
    exit("Supply the base url of the application as the first argument.\n");
}
$base_url = $argv[1];
if (substr($base_url, -1) != '/') {
    $base_url .= '/';
}


if (!isset($argv[2])){
    exit("Supply a username known in the application as the second argument.\n");
}
$username = $argv[2];


if (!isset($argv[3])){
    exit("Supply the corresponding password as the third argument.\n");
}
$password = $argv[3];

$API_VERSION = 1;
$API_URL = $base_url . 'api/' . $API_VERSION . '/';

$token = get_token($API_URL, $username, $password);
if ($token == false){
    exit("Could not get token.\n");
}
