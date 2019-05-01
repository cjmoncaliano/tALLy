function add_role() {
  var table = document.getElementById("dashboard_table").getElementsByTagName('tbody')[0];
  var row = table.insertRow(table.rows.length);
    
  var cell1 = row.insertCell(0);
  var newText = document.createTextNode(user_info.open_roles[1].role);
  cell1.appendChild(newText);
    
  //var cell2 = row.insertCell(1);
  //cell1.innerHTML = user_info.open_roles[1].role};
  //cell2.innerHTML = "NEW CELL2";
}

add_role()