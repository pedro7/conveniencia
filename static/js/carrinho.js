var finalizar_btn = document.getElementById('finalizar_btn');
var consultar_btn = document.getElementById('consultar_btn');

var finalizar_modal = document.getElementById('finalizar_modal');
var consultar_modal = document.getElementById('consultar_modal');
var total_gasto_modal = document.getElementById('total_gasto_modal');

var fechar_modal_1 = document.getElementById('fechar_modal1');
var fechar_modal_2 = document.getElementById('fechar_modal2');
var fechar_modal_3 = document.getElementById('fechar_modal3');

finalizar_btn.addEventListener('click', function() {
    finalizar_modal.style.display = 'block';
});

consultar_btn.addEventListener('click', function() {
    consultar_modal.style.display = 'block';
});

fechar_modal_1.onclick = function() {
    finalizar_modal.style.display = "none";
};

fechar_modal_2.onclick = function() {
    consultar_modal.style.display = "none";
};

if (fechar_modal_3 != null) {
    fechar_modal_3.onclick = function() {
        total_gasto_modal.style.display = "none";
    };
}

window.onclick = function(event) {
    if (event.target == finalizar_modal) {
      finalizar_modal.style.display = "none";
    }
    else if (event.target == consultar_modal) {
        consultar_modal.style.display = 'none'
    }
    else if (event.target == total_gasto_modal) {
        total_gasto_modal.style.display = 'none'
    }
  };
