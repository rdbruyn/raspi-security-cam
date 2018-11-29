<!DOCTYPE html>
<html>
<title>Pi Security Cam Web Interface</title>
<body>
<?php

session_start();
$_SESSION['logged_in'] = false;
if (isset($_SESSION['logged_in']) && $_SESSION['logged_in'] == true) 
{
	header("Location:display.php");
}

$db = new SQLite3('/home/pi/Desktop/Security_Cam_Project/credentials.sqlite');
if (!$db) echo $db->lastErrorMsg();
$results = $db->query("SELECT * FROM info;");
$entry = $results->fetchArray();

$user = isset($_POST['user']) ? $_POST['user'] : $user;
$pass = isset($_POST['pass']) ? $_POST['pass'] : $pass;

$userhash = password_hash($user, PASSWORD_BCRYPT);
$passhash = password_hash($pass, PASSWORD_BCRYPT);
$hasheduser = $entry['username'];
$hashedpass = $entry['password'];

if (password_verify($user, $hasheduser) && password_verify($pass, $hashedpass))
{
	session_start();
	$_SESSION['logged_in'] = true;
	header("Location:display.php");
}
else
{
	echo "<form method='POST' action='index.php'>";
	echo "User <input type='text' name='user'></input><br>";
	echo "Password <input type='password' name='pass'></input><br>";
	echo "<input type='submit' name='submit' value='Ok'></input><br><br>";
	echo "</form>";
}

?>

<br><br>
<a href='changepassword.php'>Change password</a>

</body>
</html>