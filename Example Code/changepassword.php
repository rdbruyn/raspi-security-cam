<!DOCTYPE html>
<html>
<title>Pi Security Camera Web Interface</title>
<body>

<?php

$db = new SQLite3('/home/pi/Desktop/Security_Cam_Project/credentials.sqlite');
$results = $db->query("SELECT * FROM info");
$entry = $results->fetchArray();

$username = $entry['username'];
$currentpass = $entry['password'];

$user = (isset($_POST['user'])) ? $_POST['user'] : "";
$originalpass = (isset($_POST['originalpass'])) ? $_POST['originalpass'] : "";
$pass1 = (isset($_POST['pass1'])) ? $_POST['pass1'] : "";
$pass2 = (isset($_POST['pass2'])) ? $_POST['pass2'] : "";

$fail = true;

if (password_verify($originalpass, $currentpass))
{
	if($pass1 === $pass2)
	{
		if(strlen($pass1) > 7)
		{
			$fail = false;
			$hashedpass = password_hash($pass1, PASSWORD_BCRYPT);
			$del = $db->exec("DELETE FROM info");
			if(!$del) echo $db->lastErrorMsg();
			
			$add = $db->exec("INSERT INTO info (username,password) VALUES('$username', '$hashedpass')");
			if(!$add) echo $db->lastErrorMsg();
			$db->close();
			header('Location:index.php');
		}
		else echo "New password must be 8 characters in length";
	}
	else echo "New passwords don't match.";
}

if(fail)
{
	echo "<form method='POST' action='changepassword.php'>";
	echo "Username: <input type='text' name='user'></input><br>";
	echo "Original Password: <input type='password' name='originalpass'></input><br>";
	echo "New Password: <input type='password' name='pass1'></input><br>";
	echo "Confirm New Password: <input type='password' name='pass2'></input><br>";
	echo "<input type='submit' name='submit' value='Ok'></input>";
	echo "</form>";
}


?>

<br><br>
<a href='index.php'>Back to login page</a>

</body>
</html>