var modal = document.getElementsByClassName("modal")[0]
var table = document.querySelector("table");
var rows = table.querySelectorAll("tr");

var filteredRows = Array.from(rows).filter(function(rows, index) {
  return index !== 0 && index !== rows.length - 1;
});

filteredRows.forEach(function(row) {
  row.onclick = function() {
    modal.style.display = "block";
  };
});

var span = document.getElementsByClassName("close")[0];

span.onclick = function() {
  modal.style.display = "none";
};

window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
};
