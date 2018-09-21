<?php

$filePath = $argv[1];
$result = [];

$fp = fopen($filePath, 'r');
while (!feof($fp)) {
    $buffer = fgets($fp);

    $data = explode(',', $buffer);
    $result[] = [
        'id' => $data[0]
    ];

}

var_dump(json_encode($result));