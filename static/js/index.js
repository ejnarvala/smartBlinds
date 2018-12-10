var lightDOM, tiltDOM, closeTimeDOM, openTimeDOM, submitButtonDOM

function init(){
	lightDOM = document.getElementById('light');
	tiltDOM = document.getElementById('tilt');
	openTimeDOM = document.getElementById('openTime');
	closeTimeDOM = document.getElementById('closeTime');
	submitButtonDOM = document.getElementById('submit');

// poll server every second for status
	setInterval(function(){
		console.log('fetching');
		fetch('/api/data')
			.then(res => res.json())
			.then(jsonData => updateVals(jsonData))
			.catch(error => console.error('Error:', error));
		}, 1000);


	// var openTime = new Date(data.openTime*1000);
	// var closeTime = new Date(data.closeTime*1000);
	// openTimeDOM.value = openTime.toTimeString().split(' ')[0].slice(0,-3);
	// closeTimeDOM.value = closeTime.toTimeString().split(' ')[0].slice(0,-3);
}


function updateVals(data){
	console.log(data);
	lightDOM.innerHTML = data.light;
	tiltDOM.value = data.tilt;
	openTimeDOM.value = data.openTime;
	closeTimeDOM.value = data.closeTime;
	if(data.busy){
		submitButtonDOM.disabled = true;
		submitButtonDOM.innerHTML = 'Busy';
	}else{
		submitButtonDOM.disabled = false;
		submitButtonDOM.innerHTML = 'Submit';
	}
}


