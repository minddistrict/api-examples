<?php
include "settings.php";

function add_professional(
        $API_URL, $token, $first_name, $infix, $last_name, $id, $email) {
    $url = $API_URL . 'p';

    $payload = array(
        "active" => true,
        "first_name" => $first_name,
        "infix" => $infix,
        "last_name" => $last_name,
        "id" => $id,
        "email" => $email
    );
    $result = json_decode(post($url, $payload, $token));
    return $result->{"@url"};
}

function add_random_professional($API_URL, $token) {
    $first_name = random_first_name();
    $infix = random_infix();
    $last_name = random_last_name();
    return add_professional(
        $API_URL,
        $token,
        $first_name,
        $infix,
        $last_name,
        random_id(),
        random_email($first_name, $infix, $last_name)
    );
}

$ROLES = array(
    'secretary' => 'ith.Secretary',
    'therapist' => 'ith.Therapist',
    'supervisor' => 'ith.Supervisor',
    'application manager' => 'ith.ApplicationManager',
    'analyst' => 'ith.Analyst'
);

function set_role($url, $token, $role) {
    global $ROLES;
    $url = $url . "/roles";
    $role = trim(strtolower($role));
    $payload = array(
        "roles" => array($ROLES[strtolower($role)])
    );

    return json_decode(patch($url, $payload, $token));
}

function import_professionals ($url, $token, $filepath) {
    $file = fopen($filepath, 'r');
    $header_seen = false;
    while (($line = fgetcsv($file)) !== FALSE) {
        if (!$header_seen) {
            $header_seen = true;
            continue;
        }
        $email = $line[0];
        $id = $line[1];
        $first_name = $line[2];
        $infix = $line[3];
        $last_name = $line[4];
        $role = $line[5];
        $professional_url = add_professional(
            $url, $token, $first_name, $infix, $last_name, $id, $email);
        set_role($professional_url, $token, $role);
    }
    fclose($file);
}

import_professionals($config_url, $config_token, $config_path);
# $professional_url = add_random_professional($config_url, $config_token);
# $result = set_role($professional_url, $config_token, "therapist");
