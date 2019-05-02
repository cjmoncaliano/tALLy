function add_role() {
  var table = document.getElementById("dashboard_table").getElementsByTagName('tbody')[0];
  var row = table.insertRow(table.rows.length);

  console.log(table)
  var cell1 = row.insertCell(0);
  var newText = document.createTextNode(user_info.open_roles[1].role);
  cell1.appendChild(newText);
}

add_role()
