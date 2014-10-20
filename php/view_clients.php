<?php
include "settings.php";

function get_clients($API_URL, $token) {
    $url = $API_URL . 'c/items';
    $result = json_decode(get($url, $token));
    return $result->{'@items'};
}

function dump_client_info($client_obj) {
    print "------------\n";
    print "first name: " . $client_obj->first_name;
    print "\n";
    print "infix: " . $client_obj->infix;
    print "\n";
    print "last name: " . $client_obj->last_name;
    print "\n";
    print "id: " . $client_obj->id;
    print "\n";
    print "email: " . $client_obj->email;
    print "\n\n";
}

$clients = get_clients($API_URL, $token);
foreach ($clients as $client) {
    dump_client_info($client);
}
