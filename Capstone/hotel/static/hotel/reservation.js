document.addEventListener('DOMContentLoaded',function () {
	calcPriceR();
	calcTLeft();
})
function getYMD(ymd) {
	// ymd should have the format MonthName DD, YYYY or MonthName DD, YYYY,
	var ymd_ = ymd.split(' ')

	var months = ['Jan.','Feb.','March','Apr.','May','June','July','Aug.','Sep.','Oct.','Nov.','Dec.']
	for(var i=0; i<12; i++){
		if(ymd_[0]==months[i])
			ymd_[0]=i
	}
	ymd_[1]=ymd_[1].substring(0,ymd_[1].indexOf(','))
	if (ymd_[2][ymd_[2].length-1] == ",")
		ymd_[2]=ymd_[2].substring(0,ymd_[2].indexOf(','))

	ymd_ = [ymd_[2], ymd_[0], ymd_[1]]

	return ymd_ 
}
function getYMDHM(ymdhm) {
	// ymdhm should have the format MonthName DD, YYYY, HH:MM a(p).m.
	var ymdhm_ = ymdhm.split(' ')
	var ymd_ = getYMD(ymdhm)

	var hhmm = ymdhm_[3].split(':') //11:12 will be 11,12 
	if(ymdhm_[4]=="p.m." && hhmm[0]!=12) hhmm[0] = parseInt(hhmm[0]) + 12;

	ymdhm_ = [ymd_[0],ymd_[1],ymd_[2],hhmm[0],hhmm[1]]
	return ymdhm_

}
function calcPriceR() {
	var priceToBePaid = document.getElementById("priceToBePaid")
	var checkin = document.getElementById("check-in-disp").dataset.id
	var checkout = document.getElementById("check-out-disp").dataset.id
	var pricePerRoom = priceToBePaid.dataset.id
	var	bf = priceToBePaid.dataset.bf
	bf = bf == "True" ? 1:0
	checkin = getYMD(checkin)
	checkout = getYMD(checkout)
	var from = new Date(checkin[0], checkin[1], checkin[2])
	var to = new Date(checkout[0], checkout[1], checkout[2])
	var dur = (to.getTime() - from.getTime())/(1000*60*60*24)
	var price = dur * (parseFloat(pricePerRoom) + 20.00*bf)

	priceToBePaid.innerHTML = price
}
function calcTLeft() {
	var reservedTime = document.getElementById("reservedTime");
	var id = reservedTime.dataset.id;

	var userId = document.getElementById('user').dataset.id
	var countDown = reservedTime.innerHTML
	countDown = getYMDHM(countDown)
	date = new Date(countDown[0],countDown[1],countDown[2],countDown[3],countDown[4],0)

	const reservationDuration = 0.0004//in days
	const element = document.getElementById("timer-"+id)
	var counterInterval = setInterval(function() {
		var nownow = new Date()
		var duration = (nownow.getTime() - date.getTime())/(1000*3600*24)
		if(duration < reservationDuration){
			var tempD = reservationDuration - duration
			var daysLeft = Math.floor(tempD)
			
			var tempH = (tempD - daysLeft)*24
			var hoursLeft = Math.floor(tempH)

			var tempM = (tempH - hoursLeft)*60
			var minutesLeft = Math.floor(tempM)>9 ? Math.floor(tempM) : "0"+Math.floor(tempM)			

			var tempS = (tempM - minutesLeft)*60
			var secondsLeft = Math.floor(tempS)>9 ? Math.floor(tempS): "0"+Math.floor(tempS)			

			element.innerHTML = daysLeft + "day(s) and "+hoursLeft+":"+minutesLeft+":"+secondsLeft+" left"
		}
		else{
			clearInterval(counterInterval)
			element.innerHTML = "Reservation expired"
			// delete reservation
			fetch("/reservationFor/"+userId, {
				method: 'PUT'
			})
			document.getElementById('doesrExist').style.display = "none"
			document.getElementsByClassName('noReservation').array.forEach(element => {
				element.style.display = "block"
			});
		} 	
	},1000) 
}

function enablePaymentMethod() {
	document.getElementById('pay-form').style.display = "inline"
	document.getElementById('book-button').style.display = "none"
}