<?php
# Error settings
ini_set('display_errors', 1);
error_reporting(E_ALL);

function add_token($http_headers, $token) {
    if ($token !== NULL) {
        array_push($http_headers, 'Authorization: md-token ' . $token);
    }
    return $http_headers;
}

function post($url, $payload, $token = NULL) {
    $json_string = json_encode($payload);
    $http_headers = array(
        'Content-Type: application/json',
        'Accept: application/json',
        'Content-Length: ' . strlen($json_string)
    );

    $http_headers = add_token($http_headers, $token);

    $settings = array(
        CURLOPT_CUSTOMREQUEST => "POST",
        CURLOPT_POSTFIELDS => $json_string,
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_HTTPHEADER => $http_headers,
        CURLOPT_URL => $url
    );

    $ch = curl_init();
    curl_setopt_array($ch, $settings);
    if( ! $result = curl_exec($ch)) {
        trigger_error(curl_error($ch));
    }
    curl_close($ch);
    return $result;
}

function patch($url, $payload, $token = NULL) {
    $json_string = json_encode($payload);
    $http_headers = array(
        'Content-Type: application/json',
        'Accept: application/json',
        'Content-Length: ' . strlen($json_string)
    );

    $http_headers = add_token($http_headers, $token);

    $settings = array(
        CURLOPT_CUSTOMREQUEST => "PATCH",
        CURLOPT_POSTFIELDS => $json_string,
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_HTTPHEADER => $http_headers,
        CURLOPT_URL => $url
    );

    $ch = curl_init();
    curl_setopt_array($ch, $settings);
    $result = curl_exec($ch);
    curl_close($ch);
    return $result;
}

function get($url, $token = NULL) {
    $http_headers = array('Accept: application/json');
    $http_headers = add_token($http_headers, $token);

    $settings = array(
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_HTTPHEADER => $http_headers,
        CURLOPT_URL => $url
    );

    $ch = curl_init();
    curl_setopt_array($ch, $settings);
    if( ! $result = curl_exec($ch)) {
        trigger_error(curl_error($ch));
    }
    curl_close($ch);
    return $result;
}

function get_token($API_URL, $login, $password) {
    $url = $API_URL . 'authenticate';

    $payload = array(
        "description" => "Organization",
        "id" => "org",
        "login" => $login,
        "password" => $password
    );
    $result = json_decode(post($url, $payload));
    if (property_exists($result, 'token')) {
        return $result->token;
    } else {
        print $result->message . "\n";
        return false;
    }
}

function random_first_name() {
    $first_names = array(
        "Jack",
        "John",
        "Fred",
        "Simone",
        "Anne",
        "Eve"
    );
    return $first_names[array_rand($first_names)];
}

function random_infix() {
    $infixes = array(
        "",
        "the",
        "of",
        "von"
    );

    return $infixes[array_rand($infixes)];
}

function random_last_name() {
    $last_names = array(
        "Bauer",
        "Astaire",
        "Woo",
        "Bovarie",
        "Fredricks",
        "Gutmans"
    );
    return $last_names[array_rand($last_names)];
}

function random_id() {
    return (string) rand(1000, 10000);
}

function random_email($first_name, $infix , $last_name) {
    $domains = array(
        "example.com",
        "example.org",
        "example.foo",
        "example.bar",
        "example.qux"
    );

    $email = strtolower($first_name);
    if ($infix != '') {
        $email .= '.' . strtolower($infix);
    }
    $email .= '.' . strtolower($last_name);
    $email .= '@' . $domains[array_rand($domains)];
    return $email;
}

function random_date_of_birth() {
    $year = rand(1900, 2013);
    $month = rand(1, 12);
    $day = rand(1, 28);  # Because of February.
    return $year . '-' . $month . '-' . $day;
}

function random_gender() {
    $genders = array('m', 'f');
    return $genders[array_rand($genders)];
}

