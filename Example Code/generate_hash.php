<?php

$user = "hypervision";
$pass = "BigBrother";

$userhash = password_hash($user, PASSWORD_BCRYPT);
$passhash = password_hash($pass, PASSWORD_BCRYPT);

echo $userhash;
echo "<br>";
echo $passhash;

?>