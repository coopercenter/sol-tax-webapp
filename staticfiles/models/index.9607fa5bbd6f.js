var add_commas = document.querySelectorAll(".comma_value")
var dollar_sign = document.querySelectorAll(".dollar_value")
var differnce_values = document.querySelectorAll(".difference")
var percentages = document.querySelectorAll(".percentage")

console.log(dollar_sign)
for(var i = 0; i < differnce_values.length; i++){
    console.log(differnce_values[i])
    if(parseInt(differnce_values[i].innerText) < 0){
        differnce_values[i].style.color = "red";
    }
}
var formatter = new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
  
    // These options are needed to round to whole numbers if that's what you want.
    //minimumFractionDigits: 0,
    maximumSignificantDigits: 6,
});

console.log(percentages)
for(var i = 0; i < percentages.length; i++){
    percentages[i].innerText = parseFloat(percentages[i].innerText) * 100
}
// console.log(formatter.format("-123456"))

for(var i = 0; i < dollar_sign.length; i++){
    // console.log(dollar_sign[i].innerText)
    dollar_sign[i].innerText = formatter.format(parseInt(dollar_sign[i].innerText))
}

for(var i = 0; i < add_commas.length; i++){
    // var value = (add_commas[i].innerText.split("$"))
    // console.log(value)
    add_commas[i].innerText = (parseInt(add_commas[i].innerText).toLocaleString())
}

var localityName = document.querySelectorAll(".locality_name")
// console.log(localityName)
for(var i = 0; i < localityName.length; i++){
    localityName[i].innerText = localityName[i].innerText.replace(/_/g, " ")
}

// for(var i = 0; i < difference.length; i++){
//     localityName[i].style.color = localityName[i].innerText.replace(/_/g, " ")
// }