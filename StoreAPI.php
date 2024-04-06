<?php

// Connection preferences
$servername = "db";
$dbname = "StoreManager";
$username = "username";
$password = "password";

$user = $pass = $purp = $role = "";


// create login string
if($_SERVER["REQUEST_METHOD"] == "GET"){
    $user = $_GET["user"];
    $pass = $_GET["pass"];
    $purp = $_GET["purp"];
} else if($_SERVER["REQUEST_METHOD"] == "POST"){
    $user = $_POST["user"];
    $pass = $_POST["pass"];
    $purp = $_POST["purp"];
}

$loginstring = openssl_encrypt($pass, "AES-128-CTR", $user, 0, "-%1+4@c=~~cT3LXA");
//echo $loginstring; // in case of creating new user

// Create and test connection
$conn = new mysqli($servername, $username, $password, $dbname);
if($conn -> connect_error){
    die("Could not connect: ".$conn -> connect_error);
}

// Attempt to execute SQL
$sql = "SELECT Role, LoginString FROM Users";
$result = $conn -> query($sql);

// check if any login string was valid
if($result -> num_rows > 0){
    while($row = $result -> fetch_assoc()){
        if($row["LoginString"] == $loginstring){
            $role = $row["Role"];
            break;
        }
    }
    if($role == ""){
        $conn -> close();
        die("Wrong username and / or password!");
    }
} else {
    $conn -> close();
    die("No records in users database!");
}

// ----------------- Post authentication -----------------

if($purp == "a"){ // Return user role if only authenticating
    echo $role;

} else if($purp == "g" && $role != "Pardevejs"){ // If checking for totals
    $startTime = $_GET["starttime"];
    $endTime = $_GET["endtime"];

    // get profit
    $sql = "SELECT Total FROM Purchases WHERE PurchaseTime BETWEEN '" . $startTime . "' AND '" . $endTime . "'";
    $result = $conn -> query($sql);

    $profit = $loss = 0;

    if($result -> num_rows > 0){
        while($row = $result -> fetch_assoc()){
            $profit += $row["Total"];
        }
    }
    
    // get losses
    $sql = "SELECT Price FROM Restock WHERE RestockTime BETWEEN '" . $startTime . "' AND '" . $endTime . "'";
    $result = $conn -> query($sql);

    if($result -> num_rows > 0){
        while($row = $result -> fetch_assoc()){
            $loss += $row["Price"];
        }
    }
    // return profit, loss and total seperated by commas
    echo $profit . "," . $loss . "," . $profit - $loss;


} else if($purp == "s") { // If adding a sales entry
    //$itemcodes = $_POST["items"];
    $itemcodes = $_GET["items"];

    $items = explode(",",$itemcodes);
    foreach(range(0, count($items)-1) as $i){
        $items[$i] = explode("x", $items[$i]);
    }

    $sql = "SELECT * FROM Items";
    $result = $conn -> query($sql);

    $total = 0;

    while($row = $result -> fetch_assoc()){
        foreach($items as $i){
            if($row["Barcode"] == $i[0]){
                $total += floatval($row["ItemPrice"]) * intval($i[1]);
                $sql = "UPDATE Items SET Stock = " . intval($row["Stock"]) - intval($i[1]) . " WHERE Barcode = " . $row["Barcode"];
                $conn -> query($sql);
            }
        }
    }
    $sql = "INSERT INTO Purchases (ItemCodes, Total) VALUES ('" . $itemcodes . "', '" . $total . "')";
    $conn -> query($sql);

    echo $total;
}else if($purp == "r" && $role != "Pardevejs"){
    // $item = $_POST["item"];
    $item = $_GET["item"];
    // $count = $_POST["count"];
    $count = $_GET["count"];
    // $price = $_POST["price"];
    $price = $_GET["price"];

    $sql = "SELECT Barcode, Stock FROM Items";
    $result = $conn -> query($sql);

    while($row = $result -> fetch_assoc()){
        if($row["Barcode"] == $item){
            $stock = $row["Stock"];
            break;
        }

    }

    $sql = "INSERT INTO Restock (RestockProduct, ProductCount, Price) VALUES ('" . $item . "', '" . $count . "', '" . $price . "')";
    $conn -> query($sql);

    $sql = "UPDATE Items SET Stock = " . intval($stock) + intval($count) . " WHERE Barcode = " . $item;
    echo $conn -> query($sql);
}
$conn -> close();
?>
