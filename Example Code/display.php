<!DOCTYPE html>
<html>
<title>Pi Security Cam Web Interface</title>
<body>

<?php
	session_start();
	if(!isset($_SESSION['logged_in']) || $_SESSION['logged_in'] == false) header('Location:index.php');

	$db = new SQLite3('/home/pi/Desktop/Security_Cam_Project/footage.sqlite');
	$months = array('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December');
?>

<a href='logout.php'>Log Out</a><br><br><br>

<?php
	ini_set('display_errors', 'On');
	error_reporting(E_ALL);

	echo "<TABLE BORDER='3' CELLSPACING='1' CELLPADDING='10'>";
	echo "<CAPTION>Video Footage</CAPTION>";
	$results = $db->query("SELECT * FROM recordings ORDER BY id DESC");
	while ($row = $results->fetchArray())
	{
		$directory = 'Video_Footage/'.$row['Filename'].'.mp4';
		$m = $months[$row['Month'] - 1];
		$d = $row['Day'];
		$name = $row['Filename'];
		$h = substr($name, 9, 8);
		//echo "<a href=$directory>$name</a><br>";
		echo "<TR>";
		echo "<TD>$m</TD><TD>$d</TD><TD>$h</TD><TD><a href=$directory>View</a></TD>";
		echo "</TR>";	
	}
	echo "</TABLE>";
?>

</body>
</html>