var add_commas = document.querySelectorAll(".comma_value")
console.log(add_commas)
for(var i = 0; i < add_commas.length; i++){
    add_commas[i].innerHTML = (parseInt(add_commas[i].innerText).toLocaleString())
}

var localityName = document.querySelectorAll(".locality_name")
console.log(localityName)
for(var i = 0; i < localityName.length; i++){
    localityName[i].innerText = localityName[i].innerText.replace(/_/g, " ")
}