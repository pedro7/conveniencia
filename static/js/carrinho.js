var finalizar_btn = document.getElementById('finalizar_btn');
var consultar_btn = document.getElementById('consultar_btn');

var finalizar_modal = document.getElementById('finalizar_modal');
var consultar_modal = document.getElementById('consultar_modal');

var fechar_modal_1 = document.getElementById('fechar_modal1');
var fechar_modal_2 = document.getElementById('fechar_modal2');

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

window.onclick = function(event) {
    if (event.target == finalizar_modal) {
      finalizar_modal.style.display = "none";
    }
    else if (event.target == consultar_modal) {
        consultar_modal.style.display = 'none'
    }
  };
