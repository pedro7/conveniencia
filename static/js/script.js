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

