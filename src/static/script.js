var modalaceitar = document.getElementById("aceitar");
var modalrejeitar = document.getElementById("rejeitar");
var btnaceitar = document.getElementById("btnaceitar");

var btnrejeitar = document.getElementById("btnrejeitar");

var span = document.getElementsByClassName("icon-fechar")[0];

btnaceitar.onclick = function() {
    modalaceitar.style.display = "block";
}

btnrejeitar.onclick = function() {
    modalrejeitar.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
    modalaceitar.style.display = "none";
}

span.onclick = function() {
    modalrejeitar.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modalaceitar) {
    modalaceitar.style.display = "none";
    }

    if (event.target == modalrejeitar) {
    modalrejeitar.style.display = "none";
    }
}
