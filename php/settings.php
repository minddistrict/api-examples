<?php
# API specific settings
ini_set('display_errors', 1);
error_reporting(E_ALL);

include "util.php";

$config = parse_ini_file('config.ini');
$config_token = $config['token'];
$config_path = $config['path'];
$config_url = $config['url'];


if (strpos($config_url, 'api' == False)) {
    exit('The API url is incorrect; it does not contain "api".');
}

# Double parentheses to prevent the "passed by reference warning".
if (end((str_split($config_url))) != '/') {
    exit('The API url needs to end with a "/" character.');
}
