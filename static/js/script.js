function redirectToUrl(url) {
    window.location.href = url;
}


$(document).ready(function() {
    // Initialize Inputmask for the "preco" input field
    $('#id_preco').inputmask("currency", {
      radixPoint: ".",
      groupSeparator: ",",
      digits: 2,
      autoGroup: true,
      prefix: 'R$ ',
      rightAlign: false,
      removeMaskOnSubmit: true
    });
  });

$(document).ready(function() {
    $("#id_codigo_barras").inputmask({
        mask: "9 999999 999999",
        removeMaskOnSubmit: true
    });
});


$(document).ready(function() {
    $('#id_cpf').inputmask({
      mask: '999.999.999-99',
      removeMaskOnSubmit: true
    });
});

$(document).ready(function() {
    $('#id_data_de_nascimento').inputmask("99/99/9999");
});

function filterTable() {
  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementById("searchInput");
  filter = input.value.toUpperCase();
  table = document.querySelector("table");
  tr = table.getElementsByTagName("tr");

  for (i = 0; i < tr.length; i++) {
      td = tr[i].getElementsByTagName("td")[0]; // Assuming the first column is the name column
      if (td) {
          txtValue = td.textContent || td.innerText;
          if (txtValue.toUpperCase().indexOf(filter) > -1) {
              tr[i].style.display = "";
          } else {
              tr[i].style.display = "none";
          }
      }
  }
}

// Attach an event listener to the search input field
document.getElementById("searchInput").addEventListener("keyup", filterTable);