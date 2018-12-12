var lightDOM, tiltDOM, closeTimeDOM, openTimeDOM, submitButtonDOM

function init(){
	lightDOM = document.getElementById('light');
	tiltDOM = document.getElementById('tilt');
	statusDOM = document.getElementById('status');
	openTimeDOM = document.getElementById('openTime');
	closeTimeDOM = document.getElementById('closeTime');
	submitButtonDOM = document.getElementById('submit');
	// tiltTarget = document.getElementById('tiltTarget');
	openTimeTarget = document.getElementById('openTimeTarget');
	closeTimeTarget = document.getElementById('closeTimeTarget');
	openBlindsButtonDOM = document.getElementById('openBlindsButton')
	closeBlindsButtonDOM = document.getElementById('openBlindsButton')



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


function buttonClick(){
	var payload = {
		openTimeTarget: openTimeTarget.value,
		closeTimeTarget: closeTimeTarget.value
		}
	fetch('/api/target', {method: 'POST', body: JSON.stringify(payload)})
		.then(res => res.json())
		.then(response => console.log('Success:', JSON.stringify(response)))
		.catch(error => console.log('Error:', error));
}

function openBlinds(){
	freezeButtons()
	fetch('/api/openBlind')
		.then(res =>res.json())
		.then(response => {
			if(response.success){
				console.log('Successfully Opened Blinds');
				unfreezeButtons();
			}else{
				console.log('Server Error:', response.error);
				unfreezeButtons();
			}
		})
		.catch(error => {
			console.log("Error:", error);	
			unfreezeButtons();
		})
}

function closeBlinds(){
	freezeButtons()
	fetch('/api/closeBlind')
		.then(res =>res.json())
		.then(response => {
			if(response.success){
				console.log('Successfully Closed Blinds');
				unfreezeButtons();
			}else{
				console.log('Server Error:', response.error);
				unfreezeButtons();
			}
		})
		.catch(error => {
			console.log("Error:", error);
			unfreezeButtons();
		})
}


function freezeButtons(){
	submitButtonDOM.disabled = true;
	openBlindsButtonDOM.disabled = true;
	closeBlindsButtonDOM.disabled = true;

	submitButtonDOM.innerHTML = 'Busy';
	closeBlindsButtonDOM.innerHTML = 'Busy';
	openBlindsButtonDOM.innerHTML = 'Busy';

}

function unfreezeButtons(){
	submitButtonDOM.disabled = false;
	openBlindsButtonDOM.disabled = false;
	closeBlindsButtonDOM.disabled = false;

	submitButtonDOM.innerHTML = 'Submit';
	closeBlindsButtonDOM.innerHTML = 'Close Blinds';
	openBlindsButtonDOM.innerHTML = 'Open Blinds';

}

function updateVals(data){
	console.log(data);
	lightDOM.innerHTML = data.light;
	tiltDOM.innerHTML = data.tilt;
	openTimeDOM.innerHTML = data.openTime;
	closeTimeDOM.innerHTML = data.closeTime;
	if(data.isOpen){
		statusDOM.innerHTML = 'Blinds Opened';
	}else{
		statusDOM.innerHTML = 'Blinds Closed';
	}

}


