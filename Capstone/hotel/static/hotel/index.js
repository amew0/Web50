function disableFnT() {
	btn = document.getElementById("btn-FT")
	if(btn.style.display == "block") {
		document.getElementById('fromB').disabled = true
	}
		
}
function updateFromB() {
	document.getElementById('toB').removeAttribute("disabled");
	document.getElementById('btn-FT').removeAttribute("disabled");
}
function updateToB() {
	var valueFromB = document.getElementById("fromB").value
	valueFromB = new Date(valueFromB)
	minTo = valueFromB.getTime()
	minTo = new Date(minTo + 1000*60*60*24) // added one day

	year =  minTo.getFullYear()
	month = Math.floor(minTo.getMonth() + 1) > 9 ? minTo.getMonth() + 1 : "0"+(minTo.getMonth() + 1)
	date = Math.floor(minTo.getDate()) > 9 ? minTo.getDate() : "0"+(minTo.getDate())
	
	minTo_format = year+"-"+month+"-"+date
	document.getElementById('toB').min = minTo_format
}
function verifyFnT() {
	var from = document.getElementById("fromB").value
	var to = document.getElementById("toB").value
	if (from > to){
		alert("Check if the intended check-in is before check-out.")
		location.reload()
	}
}
function calculatePrice() {
	let select = document.getElementById('select-typeRoom')
	let selected = select.options[select.selectedIndex].value
	var checked = document.getElementById("checkbox-1").checked
	var from = document.getElementById("from-saved").value
	var to = document.getElementById("to-saved").value
	from = new Date(from)
	to = new Date (to)
	
	var num_of_days = (to.getTime() - from.getTime())/(1000*60*60*24)
	var price = 0.00
	fetch('/roomprices')
	.then(response => response.json())
	.then(data=>{
		for(let datum in data)
			if(datum == selected)
				price = data[datum]
		price = parseFloat(price)
		if(checked) {
			price+=20.00
		}
		document.getElementById('total-price').innerHTML=(price*num_of_days).toFixed(2)
	})
	

	
}
function enablePaymentMethod(){
	payM = document.getElementById('payment-method')
	payM.style.display = "inline"
	payM.required = true

	document.getElementById('pay-submit').style.display = "inline"
	document.getElementById('book-button').style.display = "none"
}
