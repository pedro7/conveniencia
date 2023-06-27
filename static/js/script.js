var modals = document.getElementsByClassName("modal")
var tbody = document.querySelector("tbody");
var rows = tbody.querySelectorAll("tr");

rows.forEach(function(row, index) {
    row.onclick = function() {
        modals[index].style.display = "block";
    };
});

window.onclick = function(event) {
    for (var i = 0; i < modals.length; i++) {
        if (event.target == modals[i]) {
            modals[i].style.display = "none";
        break;
        }
    }
};
