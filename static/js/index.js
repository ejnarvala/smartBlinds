var lightDOM, tiltDOM, closeTimeDOM, openTimeDOM

function init(){
	lightDOM = document.getElementById('light');
	tiltDOM = document.getElementById('tilt');
	openTimeDOM = document.getElementById('openTime');
	closeTimeDOM = document.getElementById('closeTime');
	lightDOM.innerHTML = data.light;
	tiltDOM.value = data.tilt;
	openTimeDOM.value = data.openTime;
	closeTimeDOM.value = data.closeTime;
	// var openTime = new Date(data.openTime*1000);
	// var closeTime = new Date(data.closeTime*1000);
	// openTimeDOM.value = openTime.toTimeString().split(' ')[0].slice(0,-3);
	// closeTimeDOM.value = closeTime.toTimeString().split(' ')[0].slice(0,-3);
}

