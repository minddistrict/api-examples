<?php
# API specific settings
ini_set('display_errors', 1);
error_reporting(E_ALL);

include "util.php";

$config = parse_ini_file('config.ini');
$config_url = $config['url'];
$config_token = $config['token'];
$config_path = $config['path'];
