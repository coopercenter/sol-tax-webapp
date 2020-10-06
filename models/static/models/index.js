var add_commas = document.querySelectorAll(".comma_value")

for(var i = 0; i < add_commas.length; i++){
    add_commas[i].innerHTML = (parseInt(add_commas[i].innerText).toLocaleString())
}