function updateClock() {
	const now = new Date();
	const hours = now.getHours().toString().padStart(2, '0');
	const minutes = now.getMinutes().toString().padStart(2, '0');
	const timeString = `${hours}:${minutes}`;
	const clock = document.getElementById("clock");
	clock.innerHTML = timeString;
}

setInterval(updateClock, 1000);