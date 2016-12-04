<?php

error_log("-------- buildnamefile------");

// writes out long file of wikipedia pages
$term = $_REQUEST['term'];
$json = $_REQUEST['names'];
//var_dump($json);
//$decodedjson = html_entity_decode($json);
//$names = json_decode($json);
$names = $json;
$uterm = strtoupper($term);

// build string
$s="";
for ($i=0; $i < count($names); $i++){
	$s .=  $names[$i] . PHP_EOL;
	error_log($s);
}

$filename = "wikipedia_subcats_of_" . $uterm . ".txt";
//$fp = file_put_contents($filename, "\r\n-----" . $names[0] . "\r\n", FILE_APPEND | LOCK_EX);
$fp = file_put_contents($filename, $s , FILE_APPEND | LOCK_EX);

// $fp = fopen($fname, 'w');
// fwrite($fp,$j);
//fclose($fp);

//print "<p>File written: $fname";

?>