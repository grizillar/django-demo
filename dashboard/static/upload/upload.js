var stepper;
var selectedPlatform;
var file;

document.addEventListener("DOMContentLoaded", function () {
	stepper = new Stepper(document.querySelector(".bs-stepper"), {
		animation: true,
		linear: true,
	});
});

function nextP2() {
	try {
		selectedPlatform = document.querySelector('input[name="type"]:checked').value;
		document.getElementById("noselectedalert").innerHTML = "";
		console.log(selectedPlatform);
		stepper.next();
	} catch (error) {
		document.getElementById("noselectedalert").innerHTML = '<div class="alert alert-danger" role="alert">เกิดข้อผิดพลาด ไม่พบแพลตฟอร์มที่เลือก</div>';
	}
}

function nextP3() {
	var input = document.getElementById("fileinput");
	file = input.files[0];
	if (file) {
		console.log(file);
		if (selectedPlatform == "GC") {
			stepper.next();
		} else {
			stepper.to(5);
		}
	} else {
		document.getElementById("nofilealert").innerHTML = '<div class="alert alert-danger" role="alert">เกิดข้อผิดพลาด ไม่พบไฟล์</div>';
	}
}

function prevP5() {
	if (selectedPlatform == "GC") {
		stepper.previous();
	} else {
		stepper.to(3);
	}
}

// Drag and drop file upload
let dropArea = document.getElementById("drop-box");

["dragenter", "dragover", "dragleave", "drop"].forEach((eventName) => {
	dropArea.addEventListener(eventName, preventDefaults, false);
});

function preventDefaults(e) {
	e.preventDefault();
	e.stopPropagation();
}

["dragenter", "dragover"].forEach((eventName) => {
	dropArea.addEventListener(eventName, highlight, false);
});
["dragleave", "drop"].forEach((eventName) => {
	dropArea.addEventListener(eventName, unhighlight, false);
});

function highlight(e) {
	dropArea.classList.add("highlight");
}

function unhighlight(e) {
	dropArea.classList.remove("highlight");
}

dropArea.addEventListener("drop", handleDrop, false);

function handleDrop(e) {
	let dt = e.dataTransfer;
	var input = document.getElementById("fileinput");
	input.files = dt.files;
}
