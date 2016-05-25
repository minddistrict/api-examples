<?php
include "settings.php";

function get_professionals($base_url, $token) {
    $url = $base_url . 'p/items';
    $result = json_decode(get($url, $token));
    return $result->{'@items'};
}

function get_professional($base_url, $token, $id=False, $email=False) {
    if ((!$id and !$email) or ($id and $email)) {
        exit("Please search for id or email.");
    }
    $professionals = get_professionals($base_url, $token);
    foreach ($professionals as $professional) {
        if ($id and $professional->id == $id) {
            return $professional;
        } else if ($email and $professional->email == $email) {
            return $professional;
        }
    }
    return False;
}

function add_professional(
        $base_url, $token, $first_name, $infix, $last_name, $id, $email) {
    $url = $base_url . 'p';

    $payload = array(
        "active" => true,
        "first_name" => $first_name,
        "infix" => $infix,
        "last_name" => $last_name,
        "id" => $id,
        "email" => $email
    );
    $result = json_decode(post($url, $payload, $token));

    if (property_exists($result, 'code') && $result->code != 201) {
        print $payload['email'];
        print $payload['id'];
        print "\n";
        foreach ($result->extra as $err) {
            print $err->message;
            print "\n";
        }
    } else {
        return get_professional($base_url, $token, $id);
    }
}

function update_professional(
        $url, $token, $first_name, $infix, $last_name, $id, $email) {

    $payload = array(
        "first_name" => $first_name,
        "infix" => $infix,
        "last_name" => $last_name,
        "id" => $id,
        "email" => $email
    );
    patch($url, $payload, $token);
}

function add_random_professional($base_url, $token) {
    $first_name = random_first_name();
    $infix = random_infix();
    $last_name = random_last_name();
    return add_professional(
        $base_url,
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

function import_professionals ($base_url, $token, $filepath) {
    $file = fopen($filepath, 'r');
    $header_seen = false;
    while (($line = fgetcsv($file)) !== FALSE) {
        if (!$header_seen) {
            $header_seen = true;
            continue;
        }
        $email = strtolower($line[0]);
        $id = $line[1];
        $first_name = $line[2];
        $infix = $line[3];
        $last_name = $line[4];
        $role = $line[5];

        $professional = get_professional($base_url, $token, $id);
        if($professional) {
            update_professional(
                $professional->{'@url'},
                $token,
                $first_name,
                $infix,
                $last_name,
                $id,
                $email);
            set_role($professional->{'@url'}, $token, $role);
            echo "Updated professional $email.\n";
        } else {
            $professional = add_professional(
                $base_url,
                $token,
                $first_name,
                $infix,
                $last_name,
                $id,
                $email);
            if ($professional) {
                set_role($professional->{'@url'}, $token, $role);
                echo "Added $email.\n";
            }
        }
    }
    fclose($file);
}

import_professionals($config_url, $config_token, $config_path);
# $professional_url = add_random_professional($config_url, $config_token);
# $result = set_role($professional_url, $config_token, "therapist");
